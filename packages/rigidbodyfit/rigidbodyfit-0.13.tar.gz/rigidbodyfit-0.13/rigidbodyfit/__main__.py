"""run the command line interface if module is run"""
import sys

import rigidbodyfit.runner

if __name__ == '__main__':
    sys.exit(rigidbodyfit.runner.run())
