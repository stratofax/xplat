# from xplat import __version__

from typer.testing import CliRunner
from xplat import __version__
from xplat.cli import app

runner = CliRunner()


def test_version_string():
    assert __version__.__version__ == "0.1.0"


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"xplat version: {__version__.__version__}" in result.stdout


def test_info():
    result = runner.invoke(app, "info")
    assert result.exit_code == 0
    assert "System Information" in result.stdout


def test_list():
    # check for required argument
    result = runner.invoke(app, "list")
    assert result.exit_code == 2
    # list home directory
    # result = runner.invoke(app, "list", "$HOME")
    # assert result.exit_code == 0
