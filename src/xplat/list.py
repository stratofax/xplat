"""File handling functions."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


def format_bytes(num_bytes: int) -> str:
    """format a number of bytes into a human-readable string"""
    for unit in ["B", "K", "MB", "GB", "TB"]:
        if num_bytes < 1024.0:
            return f"{num_bytes:,.1f} {unit}"
        num_bytes /= 1024.0


def format_timestamp(timestamp: float) -> str:
    """Format a timestamp into a human-readable string"""
    return datetime.fromtimestamp(timestamp).strftime("%B %d, %Y %I:%M:%S %p")


def check_dir(dir_path: Path, dir_label: str = "") -> tuple:
    """
    Return True if a directory exists,
    display error message, return false if not
    dir_label is an optional label to describe
    the purpose of the directory path
    """
    # display directory label if provided
    if dir_label != "":
        dir_label = f"{dir_label}: "

    error_msg = f"{dir_label}'{dir_path}' is a directory."
    dir_exist = dir_path.is_dir()
    if not dir_exist:
        error_msg = f"{dir_label}'{dir_path}' is not a directory."
    return dir_exist, error_msg


def check_file(file_name: Path) -> tuple:
    """
    Return True if a file exists,
    display error message, return False if not
    """
    error_msg = f"{file_name} is a valid file."
    # check if file_name is a Path object
    if not isinstance(file_name, Path):
        error_msg = f"'{file_name}' is not a path to a file."
        return False, error_msg

    # check if file_name is a file
    file_exist = file_name.is_file()
    if not file_exist:
        error_msg = f"'{file_name}' is not a file."
    return file_exist, error_msg


def create_file_list(dir_path: Path, file_glob: str = None) -> list:
    """Create a list of files in a directory, return the sorted list."""
    if file_glob is None:
        return sorted(dir_path.glob("*.*"))
    file_glob = file_glob.lstrip(".")
    globber = f"*.{file_glob}"
    return sorted(dir_path.glob(globber))


@dataclass
class FileInfo:
    """Class to hold file information"""

    file_name: Path
    size: Optional[str] = None
    created: Optional[str] = None
    modified: Optional[str] = None
    accessed: Optional[str] = None

    def __post_init__(self) -> None:
        self.size = format_bytes(self.file_name.stat().st_size)
        self.created = format_timestamp(self.file_name.stat().st_ctime)
        self.modified = format_timestamp(self.file_name.stat().st_mtime)
        self.accessed = format_timestamp(self.file_name.stat().st_atime)
