"""Avoid using magic numbers with these handy constants
Use the same values in tests, function returns.
Uses errno values: https://docs.python.org/3/library/errno.html
"""

import errno
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef, import-not-found]


# read pyproject.toml and store the version number
with Path("pyproject.toml").open(mode="rb") as pyproject:
    _data = tomllib.load(pyproject)
    _version = _data["tool"]["poetry"]["version"]


PROGRAM_NAME = "xplat"
APP_HELP = "Cross-platform tools for batch file management and conversion"
VERSION = _version

NO_ERROR = 0
MISSING_COMMAND = 2  # defined by typer
NO_FILE = errno.ENOENT  # no such file or directory
NO_DATA = errno.ENODATA  # no data available
BAD_REQUEST = errno.EBADMSG  # not a data message
