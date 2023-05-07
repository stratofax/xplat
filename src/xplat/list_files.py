"""File handling functions."""
from dataclasses import InitVar, dataclass
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

    name: InitVar[Path]
    size: Optional[str] = None
    created: Optional[str] = None
    modified: Optional[str] = None
    accessed: Optional[str] = None

    def __post_init__(self, name):
        self.size = format_bytes(name.stat().st_size)
        self.created = format_timestamp(name.stat().st_ctime)
        self.modified = format_timestamp(name.stat().st_mtime)
        self.accessed = format_timestamp(name.stat().st_atime)
