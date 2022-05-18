from pathlib import Path
from typing import Optional

import typer

__version__ = "0.1.0"


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
    pass


@app.command()
def names(dir_path: Optional[Path] = typer.Option(None)):
    """
    Convert file names for cross-platform compatibility
    """
    if dir_path is None:
        typer.echo("No source directory provided.")
        raise typer.Abort()


if __name__ == "__main__":
    app()
