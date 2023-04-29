from pathlib import Path

from typer.testing import CliRunner

from xplat import constants
from xplat.cli import app, check_dir, print_files

_runner = CliRunner()


def test_app():
    result = _runner.invoke(app)
    assert result.exit_code == constants.MISSING_COMMAND
    assert "Missing command." in result.stdout


def test_version():
    result = _runner.invoke(app, ["--version"])
    assert result.exit_code == constants.NO_ERROR
    assert f"xplat version: {constants.VERSION}" in result.stdout


def test_info():
    result = _runner.invoke(app, "info")
    assert result.exit_code == constants.NO_ERROR
    assert "System Information" in result.stdout


def test_list():
    test_path = Path.home().joinpath("tmp", "xplat_cli_tests")
    test_path.mkdir(parents=True, exist_ok=True)
    # create a large file (20K) to test file size
    list_file_1 = test_path.joinpath("list_file_1.txt")
    list_file_1.touch(exist_ok=True)
    with open(list_file_1, "w") as f:
        f.write("0123456789" * 2048)
    list_file_2 = test_path.joinpath("list_file_2.txt")
    list_file_2.touch(exist_ok=True)
    list_file_3 = test_path.joinpath("list_file_3.txt")
    list_file_3.touch(exist_ok=True)
    # check for required argument
    test_required_arg = _runner.invoke(app, "list", input="q\n")
    assert test_required_arg.exit_code == 0
    assert "Total files found =" in test_required_arg.stdout
    # list files in test directory.
    test_list_dir = _runner.invoke(app, ["list", str(test_path)], input="q\n")
    assert test_list_dir.exit_code == 0
    assert list_file_3.name in test_list_dir.stdout
    assert "Total files found = 3" in test_list_dir.stdout
    # list files in test directory with 'txt' extension
    test_ext = _runner.invoke(app, ["list", str(test_path), "--ext", "txt"],
                              input="q\n")
    assert test_ext.exit_code == 0
    assert list_file_2.name in test_ext.stdout
    assert "Total files found = 3" in test_ext.stdout
    # list info for a single file
    test_file = _runner.invoke(app, ["list", str(list_file_1)], input="q\n")
    assert test_file.exit_code == 0
    assert list_file_1.name in test_file.stdout
    assert "Size:     20.0 K" in test_file.stdout
    # remove test files from test dir
    for file in test_path.iterdir():
        file.unlink()
    # remove test dir
    test_path.rmdir()
    # check for non-existent directory
    assert check_dir(test_path, "Test") is False


def test_print_files():
    # test for empty list
    test_empty = []
    list_count = print_files(test_empty)
    assert list_count == 0
