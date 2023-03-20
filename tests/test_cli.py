from pathlib import Path

from typer.testing import CliRunner

from xplat import constants
from xplat.cli import app

# create test files & dirs
_test_path = Path.home().joinpath("tmp", "xplat_cli_tests")
_test_path.mkdir(parents=True, exist_ok=True)
_list_file_1 = _test_path / "list_file_1.txt"
_list_file_1.touch(exist_ok=True)
_list_file_2 = _test_path / "list_file_2.txt"
_list_file_2.touch(exist_ok=True)
_list_file_3 = _test_path / "list_file_3.txt"
_list_file_3.touch(exist_ok=True)

runner = CliRunner()


def test_app():
    result = runner.invoke(app)
    assert result.exit_code == constants.MISSING_COMMAND
    assert "Missing command." in result.stdout


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == constants.NO_ERRORS
    assert f"xplat version: {constants.VERSION}" in result.stdout


def test_info():
    result = runner.invoke(app, "info")
    assert result.exit_code == constants.NO_ERRORS
    assert "System Information" in result.stdout


def test_list():
    # check for required argument
    result = runner.invoke(app, "list")
    assert result.exit_code == 0
    # list files in test directory
    result = runner.invoke(app, ["list", _test_path])
    assert result.exit_code == 0
    assert _list_file_1.name in result.stdout
    assert "Total files found = 3" in result.stdout
    result = runner.invoke(app, ["list", str(_test_path), "--ext", "txt"])
    assert result.exit_code == 0
    result = runner.invoke(app, "list", str(_list_file_1))
    assert result.exit_code == 0


# remove test files from test dir
for _file in _test_path.iterdir():
    _file.unlink()
# remove test dir
_test_path.rmdir()
