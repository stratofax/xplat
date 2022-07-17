"""
Changes filename to avoid platform, path issues:
* Spaces to delimiter
* Dots to underscore
* All lowercase
* web and internet friendly

"""

from pathlib import Path


def inet_names(
    abs_path: Path,
    target_dir: Path = None,
    delim_chr: str = "_",
    dots: str = "_",
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
        return f"ERROR: {abs_path} is not a file."
    if target_dir is not None and not target_dir.is_dir():
        return f"ERROR: {target_dir} is not a directory."

    # replace periods in file stem with dots delimiter
    new_stem = abs_path.stem.replace(".", dots).lower()
    # update stem: replace spaces with specified delimiter
    new_stem = new_stem.replace(" ", delim_chr)
    # merge the stem with the lowercase suffix
    new_suffix = abs_path.suffix.lower()
    new_name = f"{new_stem}{new_suffix}"
    # rename file in existing dir if no target provided
    if target_dir is not None:
        new_path = target_dir.joinpath(new_name)
    else:
        new_path = abs_path.with_name(new_name)
    if not dry_run:
        abs_path.rename(new_path)
    return new_path
