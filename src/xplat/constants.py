"""Avoid using magic numbers with these handy constants
   Use the same values in tests, function returns.
   Uses errno values: https://docs.python.org/3/library/errno.html
"""
import errno

PROGRAM_NAME = "xplat"
APP_HELP = "Cross-platform tools for batch file management and conversion"
VERSION = "0.1.1"

NO_ERROR = 0
NO_FILE = errno.ENOENT  # no such file or directory
NO_DATA = errno.ENODATA  # no data available
BAD_REQUEST = errno.EBADRQC
