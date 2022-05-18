"""
Changes filename to avoid platform, path issues:
* Spaces to delimiter
* Dots to underscore
* All lowercase
* web-friendly

Run standalone to convert all files in the current directory
"""

from pathlib import Path


def space_to_delim(
    abs_path: str, target_dir="", delim="-", dots="_", dryrun=False
) -> str:
    """
    if file exists,
    convert
        filename to lower case,
        spaces to delimiter (default = _)
    """
    if not abs_path.is_file():
        return f"ERROR: {abs_path} is not a file."
    if target_dir != "" and not Path(target_dir).is_dir():
        return f"ERROR: {target_dir} is not a directory"

    file_path = Path(abs_path)
    # replace periods in file stem with dots delimiter
    new_stem = file_path.stem.replace(".", dots).lower()
    # replace spaces with specified delimiter
    new_stem = new_stem.replace(" ", delim)
    new_suffix = file_path.suffix.lower()
    new_name = f"{new_stem}{new_suffix}"
    # rename file in existing dir if no target provided
    if target_dir != "":
        new_path = target_dir.joinpath(new_name)
    else:
        new_path = file_path.with_name(new_name)
    if not dryrun:
        file_path.rename(new_path)
    return new_path


if __name__ == "__main__":
    # test in home dir
    test_path = Path.home()
    test_file = test_path / "Space to Delim.test.FILE.TMP"
    test_file.touch(exist_ok=True)
    print(space_to_delim(test_file, delim="-", dryrun=True))
