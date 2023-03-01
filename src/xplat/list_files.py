"""File handling functions."""

from pathlib import Path


def check_ext(file_ext: str, format_tuple: tuple) -> bool:
    """Check if a file extension is in a tuple of valid formats."""
    return file_ext in format_tuple


def create_file_list(dir: Path, file_glob: str = None) -> list:
    """Create a list of files in a directory, return the sorted list."""
    globber = "*.*" if file_glob is None else f"*.{file_glob}"
    # returns a list of Path objects
    return sorted(dir.glob(globber))
