"""
Python tbr_tmpect
"""

from typing import Any
from sys import exit as sysexit
import os
import argparse
import iniconfig
import importlib.resources

# import re


# Custom type for argparse return type
type Arguments = argparse.Namespace
type ConfigDict = dict[str, dict[str, str]]

# Meta
__app_name__: str = "tbr_tmp"
__author__: str = "idealtitude"
__version__: str = "0.0.1"
__license__: str = "MT108"

# Constants
EXIT_SUCCESS: int = 0
EXIT_FAILURE: int = 1
# Paths used by the app
APP_PATH: str = os.path.dirname(os.path.realpath(__file__))
USER_CWD: str = os.getcwd()
USER_HOME: str = os.path.expanduser("~")


def get_args() -> Arguments:
    """Parsing command line arguments using subparsers"""
    parser = argparse.ArgumentParser(
        prog=f"{__app_name__}",
        description=f"A minimalist app for taking notes. Read the documentation to discover the features of {
            __app_name__}",
        epilog=f"Read the documentation to learn how to use {__app_name__}",
    )
    parser.add_argument("-i", "--input", action="store_true", help="Help string")
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    return parser.parse_args()


def load_config() -> Any:
    """Loading configuration and settings path to db"""
    config_path: Any = importlib.resources.files("tbr_tmp").joinpath(
        "data/tbr_tmp.conf"
    )
    ini: Any = iniconfig.IniConfig(config_path)
    conf: ConfigDict = {}
    conf["bible"] = {}
    conf["bible"]["item"] = ini["bible"]["version"]

    return conf


def main() -> int:
    """Main entry point"""
    args: Arguments = get_args()
    config: Any = load_config()
    print("Printing config:")

    for k, v in config.items():
        print(f"\n\033[1mSection\033[0m {k}:")
        for sk, sv in v.items():
            print(f"\t{sk}: {sv}")

    if args.input:
        print("No commands implemented yet")

    return EXIT_SUCCESS


if __name__ == "__main__":
    sysexit(main())
