import tempfile
from pathlib import Path

import pytest
from typer import Exit
from typer.testing import CliRunner

from xplat import constants
from xplat.cli import (
    app,
    check_dir,
    print_files,
    print_selected_info,
    rename_list,
)

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
    test_ext = _runner.invoke(
        app, ["list", str(test_path), "--ext", "txt"], input="q\n"
    )
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
    # attempt to list files in non-existent directory
    test_list_dir = _runner.invoke(app, ["list", str(test_path)], input="q\n")
    assert test_list_dir.exit_code == constants.NO_FILE
    # check for non-existent directory
    assert check_dir(test_path, "Test") is False


def test_print_files():
    # test for empty list
    test_empty = []
    list_count = print_files(test_empty)
    assert list_count == 0


def test_rename_list():
    # Create sample files with unfriendly names
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)

        # Create list of file names
        file_names = ["file with spaces.txt", "file#with#special#chars!.txt"]
        new_names = []

        # Create the actual files in the temporary directory
        for file_name in file_names:
            file_path = temp_dir / file_name
            with file_path.open("w") as f:
                f.write("Sample content")
            new_names.append(file_path)

        # Test the function in dryrun mode
        convert_count = rename_list(
            new_names, output_dir=temp_dir, dryrun=True
        )
        assert convert_count == len(
            new_names
        ), "Incorrect number of files processed in dryrun mode."

        # Check that the original files are still present and unchanged
        for file_path in new_names:
            assert (
                file_path.exists()
            ), f"File {file_path} should not have \
                                         been renamed in dryrun mode."

        # Test the function without dryrun mode
        convert_count = rename_list(
            new_names, output_dir=temp_dir, dryrun=False
        )
        assert convert_count == len(
            new_names
        ), "Incorrect number of files processed in normal mode."

        # Check that the original files have been renamed
        for file_path in new_names:
            assert (
                not file_path.exists()
            ), f"File {file_path} should have been renamed."


def test_print_selected_info(monkeypatch):
    # Sample files list
    files = ["file1.txt", "file2.txt", "file3.txt"]

    # Test for invalid input
    file_selector = "invalid"
    result = print_selected_info(files, file_selector)
    assert (
        result == "Invalid input, please enter a number or 'q'.\n"
    ), "Incorrect error message for invalid input."

    # Test for out-of-range input
    file_selector = "5"
    result = print_selected_info(files, file_selector)
    expected_result = f"The number {file_selector} is out of range."
    assert (
        expected_result in result
    ), "Incorrect error message for out-of-range input."

    # The files in the files list are not real files
    # Test for non-existent path, user choosing to continue
    file_selector = "1"
    monkeypatch.setattr("typer.prompt", lambda _: "c")
    expected_result = "Select another file to examine.\n"
    result = print_selected_info(files, file_selector)
    assert expected_result in result, "Expected error message not found."
    # Test for non-existent path, user choosing to quit
    monkeypatch.setattr("typer.prompt", lambda _: "q")
    expected_error = "is not a path to a file."
    with pytest.raises(Exit):
        result = print_selected_info(files, file_selector)
        assert expected_error in result, "Expected error message not found."
