"""
Functions for transforming filenames to be platform and web-friendly.
Handles conversion of spaces, dots, and case in filenames.

Changes filename to avoid platform, path, URL issues:
* Spaces to delimiter
* Dots to underscore
* All lowercase
* web and internet friendly

Characters allowed in a URL:
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
0123456789
Special characters:
safe  $-_.+
reserved  ;/?:@&=
extra  ,[]
https://www.rfc-editor.org/rfc/rfc3986
or
https://www.ietf.org/rfc/rfc1738.txt
"""

from pathlib import Path


def safe_stem(name: str, delim: str = "_") -> str:
    """Transform a filename stem to be platform and web-friendly.

    Args:
        name: Original filename stem
        delim: Delimiter to use (default: underscore)

    Returns:
        Transformed filename stem:
        - Spaces replaced with delimiter
        - Dots replaced with underscore
        - All lowercase
        - Only alphanumeric and delimiter chars
        - No double delimiters
    """
    # Convert to lowercase and replace spaces
    new_name = name.replace(" ", delim).lower()
    # Replace dots with underscore (preserve delim if different)
    new_name = new_name.replace(".", "_")
    # Keep only alphanumeric and delimiter chars
    new_name = "".join(c for c in new_name if c.isalnum() or c == delim)
    # Remove double delimiters
    while delim + delim in new_name:
        new_name = new_name.replace(delim + delim, delim)
    return new_name


def make_safe_path(orig_path: Path, target_dir: Path = None) -> Path:
    """Create a new Path with safe filename in target directory.

    Args:
        orig_path: Original file path
        target_dir: Optional target directory for new path

    Returns:
        New Path with safe filename in original or target directory
    """
    # Create safe filename
    new_name = safe_stem(orig_path.stem) + orig_path.suffix.lower()
    # Return path in target dir if specified, otherwise same dir
    return (
        target_dir.joinpath(new_name) if target_dir else orig_path.with_name(new_name)
    )


def rename_file(
    orig_path: Path, target_dir: Path = None, dry_run: bool = False
) -> Path:
    """Rename file to be platform and web-friendly.

    Args:
        orig_path: Path to original file
        target_dir: Optional target directory for renamed file
        dry_run: If True, only return the new path without performing rename

    Returns:
        Path to renamed file (or would-be path if dry_run=True)

    Raises:
        FileNotFoundError: If original path is not a file
        NotADirectoryError: If target directory is specified but invalid
        FileExistsError: If target path already exists (unless dry_run=True)
    """
    # Validate inputs
    if not orig_path.is_file():
        raise FileNotFoundError(f"Not a file: {orig_path}")
    if target_dir and not target_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {target_dir}")

    # Get new path
    new_path = make_safe_path(orig_path, target_dir)

    # Check if target exists (skip if dry_run)
    if not dry_run and new_path.exists():
        raise FileExistsError(f"File already exists: {new_path}")

    # Perform rename unless dry_run
    if not dry_run:
        orig_path.rename(new_path)

    return new_path
