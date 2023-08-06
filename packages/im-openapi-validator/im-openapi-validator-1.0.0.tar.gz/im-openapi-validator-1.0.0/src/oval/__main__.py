#!/usr/bin/env python3

"""An entry-point that allows the module to be executed.
This also simplifies the distribution as this is the
entry-point for the console script (see setup.py).
"""

import sys
from validator.validate import main as validate_main


def main() -> int:
    """The entry-point of the component."""
    return validate_main()


if __name__ == '__main__':
    sys.exit(main())
