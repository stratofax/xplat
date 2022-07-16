from pathlib import Path
from xplat import renamer

# test in home dir
test_path = Path.home()
no_dryrun_file = test_path / "Space to Delim.NO-Dry_Run.test.FILE.TXT"
no_dryrun_file.touch(exist_ok=True)

dryrun_file = test_path / "Space to Delim.is Dry_Run.test.FILE.TXT"
dryrun_file.touch(exist_ok=True)


def append_file_name(_file: Path, _dryrun: bool):
    new_name = renamer.inet_names(_file, dry_run=_dryrun)
    with open(_file, "a") as t_file:
        # write the new name to the test file
        t_file.write(f"{new_name} - {_dryrun}")


def test_renamer_dryrun():
    append_file_name(dryrun_file, True)


def test_renamer_no_dryrun():
    append_file_name(no_dryrun_file, False)
