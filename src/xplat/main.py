from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(help="Cross-platform tools for batch file management and conversion")


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
