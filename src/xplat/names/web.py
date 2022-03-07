"""
Changes filename to avoid platform, path issues:
* Spaces to underscores
* All lowercase
* web-friendly

Run standalone to convert all files in the current directory
"""

from pathlib import Path


def space_to_delim(abs_path: str, delim="_") -> str:
    """
    if file exists,
    convert
        filename to lower case,
        spaces to delimiter (default = _)
    """
    if not abs_path.is_file():
        return f"ERROR: {abs_path} is not a file."
    file_path = Path(abs_path)
    # replace spaces with specified delimiter
    new_name = file_path.name.replace(" ", delim).lower()
    new_path = file_path.with_name(new_name)
    file_path.rename(new_path)
    return f"Converted {abs_path} \nto {new_path}"
