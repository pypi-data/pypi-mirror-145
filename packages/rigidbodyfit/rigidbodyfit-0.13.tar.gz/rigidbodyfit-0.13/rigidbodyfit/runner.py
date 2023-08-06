""" Run the command line interface """
import json
import logging
import sys

import biopandas.pdb

import importlib.metadata
import numpy as np

import scipy.interpolate
import scipy.optimize
import scipy.spatial.transform

import rich.console
import rich.logging
import rich.progress

import mrcfile

import rigidbodyfit.arguments
import rigidbodyfit.structure


def create_rich_logger():
    FORMAT = "%(message)s"
    logging.basicConfig(level="INFO",
                        format=FORMAT,
                        datefmt="[%X]",
                        handlers=[rich.logging.RichHandler()])
    return logging.getLogger("rich")


class ShiftAndOrientation:
    def __init__(self, combined_vector):
        self.shift = combined_vector[:3]
        self.orientation = combined_vector[3:]


def three_d_vector_to_rotation(vector):
    return scipy.spatial.transform.Rotation.from_quat(
        cube_to_quaternion(vector))


def cube_to_quaternion(vector):
    # https://www.ri.cmu.edu/pub_files/pub4/kuffner_james_2004_1/kuffner_james_2004_1.pdf
    # defines the mapping that is used here as:
    #
    # s = rand();
    # σ1 = √1−s;
    # σ2 = √s;
    # θ1 = 2π ∗ rand();
    # θ2 = 2π ∗ rand();
    # x = sin(θ1) ∗σ1;
    # y = cos(θ1) ∗σ1;
    # z = sin(θ2) ∗σ2;
    # w = cos(θ2) ∗σ2;
    # return (w, x, y,z)
    #
    # Note that they use a different quaternion convention,
    # so we return (x, y, z, w) instead

    def shift_into_cube(x):
        if x % 2 == 0:
            return x - np.floor(x)
        return 1 - x + np.floor(x)

    vector_in_cube = np.array(list(map(shift_into_cube, vector)))
    sigma_1 = np.sqrt(1 - vector_in_cube[0])
    sigma_2 = np.sqrt(vector_in_cube[0])
    theta_1 = 2 * np.pi * vector_in_cube[1]
    theta_2 = 2 * np.pi * vector_in_cube[2]
    return np.array([
        np.sin(theta_1) * sigma_1,
        np.cos(theta_1) * sigma_1,
        np.sin(theta_2) * sigma_2,
        np.cos(theta_2) * sigma_2
    ])


class AffineProjection:
    def __init__(self, shift, rotation):
        self.shift = shift
        self.rotation = rotation

    def toJSON(self):
        AA_to_nm = 0.1

        asDict = {
            "shift_in_nm": (AA_to_nm * self.shift).tolist(),
            "orientation_quaternion": self.rotation.as_quat().tolist(),
            "orientation_matrix": self.rotation.as_matrix().tolist()
        }
        return json.dumps(asDict,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)


class Transformator:
    def __init__(self, coordinates, density_origin, density_extent):
        self.coordinates = coordinates
        self.coordinates_center = np.average(self.coordinates, axis=0)
        self.density_origin = density_origin
        self.density_extent = density_extent

    def apply(self, shift, mrp):
        # move structure to coordinate center, rotate there, then move to density origin and extra shift
        rotation = three_d_vector_to_rotation(mrp)

        return rotation.apply(
            self.coordinates - self.coordinates_center
        ) + self.density_origin + shift * self.density_extent

    def apply_to_other(self, shift, mrp, other_coordinates):

        rotation = three_d_vector_to_rotation(mrp)

        return rotation.apply(
            other_coordinates - self.coordinates_center
        ) + self.density_origin + shift * self.density_extent

    def as_affine_projection(self, shift, mrp):
        """As the transformator rotates around the center of geometry of the
           given coordinates, the corresponding affine transformation that
           rotates around the coordinate system origin needs to take this
           difference in center of rotation into account.

        Args:
            shift : shift vector
            quaternion : rotation around center of geometry

        Returns:
            AffineProjection : a transformation that corresponds to the given
                               shift and quaternion
        """

        rotation = three_d_vector_to_rotation(mrp)
        rotation_shift = -rotation.apply(self.coordinates_center)
        return AffineProjection(rotation=rotation,
                                shift=self.density_origin +
                                shift * self.density_extent + rotation_shift)


def gridpoints(voxel_size, extend, density_origin):
    return


class OverlapOptimiser:
    def __init__(self, gridpoints, voxels, coordinate_transformator):
        self.coordinate_transformator = coordinate_transformator
        self.interpolator = scipy.interpolate.RegularGridInterpolator(
            gridpoints, voxels, bounds_error=False, fill_value=0.)

    # def calculate_with_shift(self, shift):

    #     return -np.log(np.average(self.interpolator(self.mobile + shift)))

    def calculate_with_shift_and_rotation(self, shift_rotation):

        shift_and_orientation = ShiftAndOrientation(shift_rotation)

        mobile_rotated_shifted = self.coordinate_transformator.apply(
            shift_and_orientation.shift, shift_and_orientation.orientation)

        return -np.average(self.interpolator(mobile_rotated_shifted))

def origin_vector(density):

    origin = np.array(density.header.origin.tolist())

    if np.all(origin == 0):
        origin[0] = density.header.nxstart * density.voxel_size['x']
        origin[1] = density.header.nystart * density.voxel_size['y']
        origin[2] = density.header.nzstart * density.voxel_size['z']

    return origin

def run():
    """ run the command line interface """

    # set up the console for printing
    console = rich.console.Console()

    # derive the program version via git
    try:
        version = importlib.metadata.version("rigidbodyfit")
    except importlib.metadata.PackageNotFoundError:
        version = "Unknown"

    command_line_arguments = (
        rigidbodyfit.arguments.get_command_line_arguments(version))

    log = create_rich_logger()

    # read density data and determine voxel size and shift vector from it
    log.info("Reading density ...")

    density = mrcfile.open(command_line_arguments.density)
    voxels = density.data.T

    density_origin_vector = origin_vector(density)
    density_grid = tuple([
        density.voxel_size.tolist()[i] * np.arange(voxels.shape[i]) +
        density_origin_vector[i] for i in range(3)
    ])
    density_extend = np.array(density.voxel_size.tolist()) * voxels.shape

    log.info("done")

    log.info("Reading structure file ...")
    structure = rigidbodyfit.structure.Structure(
        command_line_arguments.structure, command_line_arguments.exclude)
    log.info(
        f"selected {structure.coordinates.size // 3} atoms for fitting, ignoring atom names containing {command_line_arguments.exclude}"
    )

    log.info("Optimising shift and rotatation ...")

    mobile_coordinates = Transformator(structure.coordinates,
                                       density_origin=density_origin_vector,
                                       density_extent=density_extend)

    overlap = OverlapOptimiser(voxels=voxels,
                               coordinate_transformator=mobile_coordinates,
                               gridpoints=density_grid)

    number_iterations = pow(2, command_line_arguments.sampling_depth)
    if command_line_arguments.sampling_depth < 0:
        log.info(
            "Did you just set the sampling-depth to a negative value just to see what happens then?"
        )
        number_iterations = int(1)

    with rich.progress.Progress() as progress:

        optimizer_task = progress.add_task(
            f"optimizing using {number_iterations} iterations",
            total=number_iterations)

        def print_fun(x, f, accepted):
            progress.advance(optimizer_task, advance=1)

        result = scipy.optimize.basinhopping(
            overlap.calculate_with_shift_and_rotation, [0.5] * 6,
            stepsize=0.01,
            niter=number_iterations,
            minimizer_kwargs={'method': 'L-BFGS-B'},
            callback=print_fun)

    log.info(
        f"Best average voxel value at structure coordintates : {-result.fun:.4f} ."
    )

    bestFit = ShiftAndOrientation(result.x)

    all_coordinates = structure.all_coordinates()

    structure.set_coordinates(
        mobile_coordinates.apply_to_other(bestFit.shift, bestFit.orientation,
                                          all_coordinates))

    # use input structure as template for output
    structure.full_structure.to_pdb(command_line_arguments.output_structure)

    bestFitAsAffine = mobile_coordinates.as_affine_projection(
        bestFit.shift, bestFit.orientation)
    command_line_arguments.output_transform.write(bestFitAsAffine.toJSON())
