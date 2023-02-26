from typer.testing import CliRunner

from xplat import constants
from xplat.cli import app

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
    assert result.exit_code == 2
    # list home directory
    # result = runner.invoke(app, "list", "$HOME")
    # assert result.exit_code == 0
