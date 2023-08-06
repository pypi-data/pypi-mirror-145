"""run the command line interface if module is run"""
import sys

import mdpeditor.runner

if __name__ == '__main__':
    sys.exit(mdpeditor.runner.run())
