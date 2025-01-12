"""
Tests for xplat.cli. Testing here is preferred as the tests
at this level are effectively integration tests, but also
are unit tests for the dependent modules.
"""
import tempfile
from pathlib import Path

import pytest
from typer import Exit
from typer.testing import CliRunner

from xplat import constants
from xplat.cli import app, print_files, print_selected_info, rename_list

_runner = CliRunner()


def test_app():
    """
    Runs a test case on the `app` function by invoking it
    and checking the result.

    Parameters:
    None

    Returns:
    None
    """
    result = _runner.invoke(app)
    assert result.exit_code == constants.MISSING_COMMAND
    assert "Missing command." in result.stdout


def test_version():
    """
    Executes a unit test for both variants of the
    `app` command's version flag.

    Returns:
        None
    """
    result = _runner.invoke(app, ["--version"])
    assert result.exit_code == constants.NO_ERROR
    assert f"xplat version: {constants.VERSION}" in result.stdout

    result = _runner.invoke(app, ["-V"])
    assert result.exit_code == constants.NO_ERROR
    assert f"xplat version: {constants.VERSION}" in result.stdout


def test_info():
    """
    Executes the `info` command of the `app` module
    using `_runner` and asserts that the exit code
    is `constants.NO_ERROR`.
    Also asserts that "System Information" is present
    in the `stdout` of the `result`.

    This function does not take any parameters and does not return anything.
    """
    result = _runner.invoke(app, "info")
    assert result.exit_code == constants.NO_ERROR
    assert "System Information" in result.stdout


def test_list():
    """
    Runs a series of tests for the 'list' command. This includes checking if
    the command works with a required argument, lists files in a given
    directory, lists files in a given directory with a specific extension,
    retrieves information about a single file, removes test files and
    directories, and checks for non-existent directories.

    Args:
    None

    Returns:
    None
    """
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
    # assert check_dir(test_path, "Test") is False


def test_print_files():
    # test for empty list
    test_empty = []
    list_count = print_files(test_empty)
    assert list_count == 0


def test_rename_list():
    """Test the rename_list function with various modes"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        output_dir = temp_dir / "output"
        output_dir.mkdir()

        # Test dry-run mode first
        file_names = ["file with spaces.txt", "file#with#special#chars!.txt"]
        test_files = []
        for name in file_names:
            file_path = temp_dir / name
            file_path.write_text("test content")
            test_files.append(file_path)

        convert_count = rename_list(test_files, output_dir, dryrun=True)
        assert convert_count == 2
        # Original files should still exist
        for file_path in test_files:
            assert file_path.exists()
        # Output files should not exist
        assert not (output_dir / "file_with_spaces.txt").exists()
        assert not (output_dir / "filewithspecialchars.txt").exists()

        # Now test non-interactive mode
        convert_count = rename_list(test_files, output_dir)
        assert convert_count == 2
        # Check renamed files exist
        assert (output_dir / "file_with_spaces.txt").exists()
        assert (output_dir / "filewithspecialchars.txt").exists()


def test_rename_command():
    """Test the rename command with various options"""
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        output_dir = temp_dir / "output"
        output_dir.mkdir()

        # Create a test file
        test_file = temp_dir / "Test File.txt"
        test_file.write_text("test content")

        # Test dry run mode
        result = runner.invoke(app, [
            "rename",
            "--source-dir", str(temp_dir),
            "--output-dir", str(output_dir),
            "--dry-run"
        ])
        assert result.exit_code == 0
        assert "DRY RUN" in result.stdout

        # Test non-interactive mode (default)
        result = runner.invoke(app, [
            "rename",
            "--source-dir", str(temp_dir),
            "--output-dir", str(output_dir)
        ])
        assert result.exit_code == 0
        assert (output_dir / "test_file.txt").exists()

        # Test interactive mode with confirmation
        result = runner.invoke(app, [
            "rename",
            "--source-dir", str(temp_dir),
            "--output-dir", str(output_dir),
            "--interactive"
        ], input="y\n")
        assert result.exit_code == 0

        # Test interactive mode with cancellation
        result = runner.invoke(app, [
            "rename",
            "--source-dir", str(temp_dir),
            "--output-dir", str(output_dir),
            "--interactive"
        ], input="n\n")
        assert result.exit_code == 1


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
