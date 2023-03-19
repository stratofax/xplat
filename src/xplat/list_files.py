"""File handling functions."""
from datetime import datetime
from pathlib import Path


def format_bytes(num_bytes: int) -> str:
    """format a number of bytes into a human-readable string"""
    for unit in ["B", "K", "MB", "GB", "TB"]:
        if num_bytes < 1024.0:
            return f"{num_bytes:,.1f} {unit}"
        num_bytes /= 1024.0


def format_timestamp(timestamp: float) -> str:
    """Format a timestamp into a human-readable string"""
    return datetime.fromtimestamp(timestamp).strftime("%B %d, %Y %I:%M:%S %p")


def check_ext(file_ext: str, format_tuple: tuple) -> bool:
    """Check if a file extension is in a tuple of valid formats."""
    return file_ext in format_tuple


def create_file_list(dir_path: Path, file_glob: str = None) -> list:
    """Create a list of files in a directory, return the sorted list."""
    if file_glob is None:
        return sorted(dir_path.glob("*.*"))
    file_glob = file_glob.lstrip(".")
    globber = f"*.{file_glob}"
    return sorted(dir_path.glob(globber))
