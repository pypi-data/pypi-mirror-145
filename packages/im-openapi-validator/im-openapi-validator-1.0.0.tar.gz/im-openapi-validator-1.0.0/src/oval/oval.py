#!/usr/bin/env python

"""Creates an OpenAPI validator.
We just create a validator, nothing else.

In doing this we actually test a significant part of the OpenAPI spec,
and the test are better than 'jamescooke/openapi-validator' - which is still
useful because some of the errors are easier to understand - so we'll still use
it.
"""

import argparse
import os.path
import sys
from typing import Any, Dict

from openapi_core import create_spec
from openapi_spec_validator.schemas import read_yaml_file

# Read the version file
_VERSION_FILE: str = os.path.join(os.path.dirname(__file__), 'VERSION')
with open(_VERSION_FILE, 'r', encoding='utf-8') as file_handle:
    _VERSION = file_handle.read().strip()


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------

def main() -> int:
    """The console script entry-point. Called when oval is executed
    or from __main__.py, which is used by the installed console script.
    """

    # Build a command-line parser
    # and process the command-line...
    arg_parser: argparse.ArgumentParser = argparse\
        .ArgumentParser(description='OpenAPI Validator (oval)',
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    arg_parser.add_argument('input',
                            help='The OpenAPI file(s)',
                            nargs='+')

    arg_parser.add_argument('-v', '--version', action='store_true',
                            help='Displays oval version')

    args: argparse.Namespace = arg_parser.parse_args()

    # If a version's been asked for act on it and then leave
    if args.version:
        print(_VERSION)
        return 0

    for input in args.input:
        if not os.path.exists(input) or not os.path.isfile(input):
            arg_parser.error(f'No such file: {input}')
            sys.exit(1)

        api_spec: Dict[str, Any] = read_yaml_file(input)
        try:
            _ = create_spec(api_spec)
        except BaseException as ex:
            print(f'ERROR: {ex}')
            sys.exit(1)

    return 0
