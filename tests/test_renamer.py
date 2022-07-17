from pathlib import Path
from xplat import renamer

# test in home dir
# create test & output dir
test_path = Path.home().joinpath("tmp", "xplat_tests")
test_path.mkdir(parents=True, exist_ok=True)
output_path = test_path.joinpath("target")
output_path.mkdir(parents=True, exist_ok=True)

# create test files
no_dryrun_file = test_path / "Space to Delim.NO-Dry_Run.test.FILE.TXT"
no_dryrun_file.touch(exist_ok=True)

dryrun_file = test_path / "Space to Delim.is Dry_Run.test.FILE.TXT"
dryrun_file.touch(exist_ok=True)


def append_file_name(_file: Path, _dryrun: bool):
    new_name = renamer.inet_names(_file, dry_run=_dryrun)
    with open(_file, "w") as t_file:
        # write the new name to the test file
        t_file.write(f"{new_name} - {_dryrun}")


def test_bad_file():
    bad_file = test_path / "not_a_file.tmp"
    bad_file_results = renamer.inet_names(bad_file, dry_run=True)
    assert bad_file_results.startswith("ERROR: ") and bad_file_results.endswith(
        "not a file."
    )


def test_bad_dir():
    bad_dir = test_path.joinpath("not_a_dir")
    bad_dir_results = renamer.inet_names(dryrun_file, target_dir=bad_dir, dry_run=True)
    assert bad_dir_results.startswith("ERROR: ")  # and bad_dir_results.endswith(
    #  "not a directory."
    # )


def test_renamer_dryrun():
    append_file_name(dryrun_file, True)


def test_renamer_no_dryrun():
    new_name = renamer.inet_names(no_dryrun_file, target_dir=output_path, dry_run=False)
