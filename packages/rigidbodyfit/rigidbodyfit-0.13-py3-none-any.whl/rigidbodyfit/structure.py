import biopandas.pdb


class Structure:
    def __init__(self, filename, exclude):
        self.full_structure = biopandas.pdb.PandasPdb().read_pdb(filename)

        filtered_atoms = filter_atomnames(pdb=self.full_structure,
                                          excluded_atoms=exclude)

        self.coordinates = to_coordinates(filtered_atoms)


    def set_coordinates(self, coordinates):

        self.full_structure.df['ATOM']['x_coord'] = coordinates.T[0]
        self.full_structure.df['ATOM']['y_coord'] = coordinates.T[1]
        self.full_structure.df['ATOM']['z_coord'] = coordinates.T[2]

    def all_coordinates(self):
        return to_coordinates(self.full_structure.df['ATOM'])


def filter_atomnames(pdb, excluded_atoms):

    rows_with_excluded_atoms = pdb.df['ATOM']['atom_name'].str.contains(
        excluded_atoms, na=False)

    return pdb.df['ATOM'][~rows_with_excluded_atoms]


def to_coordinates(atoms):

    return atoms[['x_coord', 'y_coord', 'z_coord']].to_numpy()




pass
