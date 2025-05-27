"""
tbr is a small, easy to use, and fast app to read the Bible from your terminal
"""

from typing import Any
from sys import exit as sysexit
import os
import argparse
import iniconfig
import importlib.resources
import gettext
import re
from .utils.status import LogLevel, Logger


# Custom type for argparse return type
type Arguments = argparse.Namespace
type ConfigDict = dict[str, dict[str, str]]

# Meta
__app_name__: str = "tbr"
__author__: str = "idealtitude"
__version__: str = "0.0.1"
__license__: str = "MT108"

# Constants
EXIT_SUCCESS: int = 0
EXIT_FAILURE: int = 1
# Paths used by the app
# APP_PATH: str = os.path.dirname(os.path.realpath(__file__))
USER_CWD: str = os.getcwd()
USER_HOME: str = os.path.expanduser("~")


def get_args(_) -> Arguments:
    """Parsing command line arguments using subparsers"""
    parser = argparse.ArgumentParser(
        prog=__app_name__,
        description=_("A minimalist app"),
        epilog=_("Help") + f" {__app_name__}",
    )
    parser.add_argument("-i", "--input", action="store_true", help=_("Help string"))
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    return parser.parse_args()


def load_config() -> Any:
    """Loading configuration and settings path to db"""
    config_path: Any = importlib.resources.files("tbr").joinpath("data/tbr.conf")
    ini: Any = iniconfig.IniConfig(config_path)
    conf: ConfigDict = {}
    conf["app"] = {}
    conf["app"]["lang"] = ini["app"]["lang"]
    conf["bible"] = {}
    conf["bible"]["version"] = ini["bible"]["version"]

    return conf


def setup_gettext(
    package_name: str, translation_domain: str, user_language: str | None = None
):
    localedir_path: Any = importlib.resources.files(package_name).joinpath("locales")

    try:
        translator = gettext.translation(
            domain=translation_domain,
            localedir=localedir_path,
            languages=[user_language] if user_language else None,
            fallback=True,
        )
        return translator.gettext
    except Exception as e:
        print(f"ERROR: Failed to set up translations: {e}")
        return gettext.gettext


def main() -> int:
    """Main entry point"""
    config: Any = load_config()

    _ = setup_gettext("tbr", "messages", config["app"]["lang"])

    args: Arguments = get_args(_)
    logger: Logger = Logger()

    if args.input:
        logger.set_log(LogLevel.WARNING, "no commands implemented yet")
        print(logger.get_log())

    return EXIT_SUCCESS


if __name__ == "__main__":
    sysexit(main())
