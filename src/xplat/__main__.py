from pathlib import Path
from typing import Optional

import typer

from xplat.info import plat

__version__ = "0.1.0"

NO_SOURCE_DIR = -1
NO_TARGET_DIR = -2


def version_callback(value: bool):
    if value:
        typer.echo(f"xplat CLI Version: {__version__}")
        raise typer.Exit()


def check_dir(dir_path: Path, dir_label: str = "") -> bool:
    if not dir_path.is_dir():
        typer.secho(
            f"{dir_label}{dir_path} is not a directory. Aborted!",
            fg=typer.colors.WHITE,
            bg=typer.colors.RED,
        )
    return dir_path.is_dir()


app = typer.Typer(help="Cross-platform tools for batch file management and conversion")


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, help="Print the version number."
    ),
    source_dir: Path = typer.Option(
        None,
        help="Directory that contains the source files.",
    ),
    target_dir: Path = typer.Option(
        None, help="Target directory to store processed files."
    ),
):
    if source_dir is not None and not check_dir(source_dir, "Source"):
        raise typer.Exit(code=NO_SOURCE_DIR)
    if target_dir is not None and not check_dir(target_dir, "Target"):
        raise typer.Exit(code=NO_TARGET_DIR)


@app.command()
def info():
    """Display platform information."""
    typer.echo(plat.create_platform_report())


@app.command()
def list():
    """List files in specified directories."""
    pass


@app.command()
def names():
    """Convert file names of the specified files."""
    pass


@app.command()
def pdf():
    """Convert PDF files to specified output format"""
    pass


if __name__ == "__main__":
    app()
