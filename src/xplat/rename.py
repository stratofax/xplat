"""
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


def safe_stem(orig_stem: str, delim: str = "_") -> str:
    """
    Change spaces to delimiter (default = _, or -)
    Change dots to underscore
    Change all to lowercase
    Remove all other special characters
    Replace double delimiters with single
    """
    new_stem = orig_stem.replace(" ", delim).lower()
    new_stem = new_stem.replace(".", "_")
    # remove all special characters
    new_stem = "".join([c for c in new_stem if c.isalnum() or c == delim])
    # replace double delimiters with single
    return new_stem.replace(delim + delim, delim)


def safe_renamer(
    abs_path: Path,
    target_dir: Path = None,
    dry_run: bool = False,
) -> str:
    """
    if file exists,
    convert
        filename to lower case,
        dots to
        spaces to delimiter (default = _)
    if target dir exists, move renamed file to it
    """
    if not abs_path.is_file():
        raise FileNotFoundError(f"{abs_path} is not a file.")
    # may not be needed:
    if target_dir is not None and not target_dir.is_dir():
        raise NotADirectoryError(f"{target_dir} is not a directory.")

    # rename file stem
    # new_stem = safe_stem(abs_path.stem, delim_chr)
    new_stem = safe_stem(abs_path.stem)
    # merge the stem with the lowercase suffix
    new_suffix = abs_path.suffix.lower()
    new_filename = f"{new_stem}{new_suffix}"
    # copy file to target dir if provided
    if target_dir is not None:
        new_path = target_dir.joinpath(new_filename)
    # rename file in existing dir if no target provided
    else:
        new_path = abs_path.with_name(new_filename)
    if not dry_run:
        # check to see if file exists
        if new_path.exists():
            return f"{new_filename} already exists, skipped."
        else:
            abs_path.rename(new_path)
    return new_path
