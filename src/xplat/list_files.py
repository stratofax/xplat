"""File handling functions."""

from pathlib import Path


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
