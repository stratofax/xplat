from pathlib import Path

import pytest

from xplat import renamer

# test in home dir
# create test & output dir
_test_path = Path.home().joinpath("tmp", "xplat_renamer_tests")
_test_path.mkdir(parents=True, exist_ok=True)
_output_path = _test_path.joinpath("target")
_output_path.mkdir(parents=True, exist_ok=True)

# create test files
_no_dryrun_file = _test_path / "Space to Delim.NO-Dry_Run.test.FILE.TXT"
_no_dryrun_file.touch(exist_ok=True)

_dryrun_file = _test_path / "Space to Delim.is Dry_Run.test.FILE.TXT"
_dryrun_file.touch(exist_ok=True)


def append_file_name(_file: Path, _dryrun: bool):
    new_name = renamer.safe_renamer(_file, dry_run=_dryrun)
    with open(_file, "w") as t_file:
        # write the new name to the test file
        t_file.write(f"{new_name} - {_dryrun}")


def test_bad_file():
    bad_file = _test_path / "not_a_file.tmp"
    with pytest.raises(FileNotFoundError):
        renamer.safe_renamer(bad_file, dry_run=True)


def test_bad_dir():
    bad_dir = _test_path.joinpath("not_a_dir")
    with pytest.raises(FileNotFoundError):
        renamer.safe_renamer(_dryrun_file, target_dir=bad_dir, dry_run=True)


# def test_renamer_dryrun():
#     append_file_name(_dryrun_file, True)


# def test_renamer_no_dryrun():
#     renamer.safe_renamer(
#         _no_dryrun_file, target_dir=_output_path, dry_run=False
#     )


# remove test files & dirs
# remove files from output dir
for _file in _output_path.iterdir():
    _file.unlink()
# remove output dir
_output_path.rmdir()

# remove test files from test dir
for _file in _test_path.iterdir():
    _file.unlink()
# remove test dir
_test_path.rmdir()
