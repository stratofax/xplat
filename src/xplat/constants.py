"""Avoid using magic numbers with these handy constants
   Use the same values in tests, function returns. 
"""
import errno

PROGRAM_NAME = "Xplat"
VERSION = "0.1.1"

NO_ERRORS = 0
MISSING_COMMAND = 2
NO_FILE = errno.ENOENT
NO_DATA = errno.ENODATA
