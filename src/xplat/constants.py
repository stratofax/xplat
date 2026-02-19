"""Avoid using magic numbers with these handy constants
Use the same values in tests, function returns.
Uses errno values: https://docs.python.org/3/library/errno.html
"""

import errno
from importlib.metadata import PackageNotFoundError, version


def _get_version() -> str:
    """Get package version from installed metadata, with fallback."""
    try:
        return version("xplat")
    except PackageNotFoundError:
        return "0.0.0-dev"


PROGRAM_NAME = "xplat"
APP_HELP = "Cross-platform tools for batch file management and conversion"
VERSION = _get_version()

NO_ERROR = 0
MISSING_COMMAND = 2  # defined by typer
NO_FILE = errno.ENOENT  # no such file or directory
NO_DATA = errno.ENODATA  # no data available
BAD_REQUEST = errno.EBADMSG  # not a data message
