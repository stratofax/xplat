# from xplat import __version__

from typer.testing import CliRunner
from xplat import __version__
from xplat.__main__ import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0


def test_version():
    assert __version__ == "0.1.0"
