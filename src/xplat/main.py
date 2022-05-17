from pathlib import Path
from typing import Optional

import typer

__version__ = "0.1.0"


def version_callback(value: bool):
    if value:
        typer.echo(f"xplat CLI Version: {__version__}")
        raise typer.Exit()


app = typer.Typer(help="Cross-platform tools for batch file management and conversion")


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, help="Print the version number."
    ),
):
    pass


@app.command()
def names(source_dir: Optional[Path] = typer.Option(None)):
    """
    Convert file names for cross-platform compatibility
    """
    if source_dir is None:
        typer.echo("No source directory provided.")
        raise typer.Abort()


if __name__ == "__main__":
    app()
