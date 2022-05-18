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
            f"{dir_label}:{dir_path} is not a directory. Aborted!",
            fg=typer.colors.WHITE,
            bg=typer.colors.RED,
        )
    return dir_path.is_dir()


def create_file_list(dir: Path, file_type: str = "*.*") -> list:
    # returns a list of Path objects
    return sorted(dir.glob(file_type))


def print_files(files: list):
    # testing for the empty list works reliably
    if files == []:
        return 0
    else:
        for file_count, file_name in enumerate(files, start=1):
            typer.secho(Path(file_name).name, fg=typer.colors.GREEN)
        return file_count


app = typer.Typer(help="Cross-platform tools for batch file management and conversion")


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, help="Print the version number."
    ),
):
    pass


@app.command()
def info():
    """Display platform information."""
    typer.echo(plat.create_platform_report())


@app.command()
def list(
    dir: Path, ext: str = typer.Option(None, help="Case-sensitive file extension.")
):
    """List files in the specified directory."""
    globber = f"*.{ext}" if ext is not None else "*.*"
    if check_dir(dir, "Listing"):
        file_list = create_file_list(dir, globber)
        f_count = print_files(file_list)
        # report the number of files found.
        plural = "s" if f_count != 1 else ""
        typer.secho(
            f"Total file{plural} found matching filter '{globber}' = {f_count}",
            fg=typer.colors.BRIGHT_YELLOW,
        )


@app.command()
def names(
    source_dir: Path = typer.Option(
        ...,
        help="Source irectory containing the files to rename.",
    ),
    target_dir: Path = typer.Option(
        None, help="Target directory to save renamed files."
    ),
):
    """Convert file names of the specified files."""
    if source_dir is not None and not check_dir(source_dir, "Source"):
        raise typer.Exit(code=NO_SOURCE_DIR)
    if target_dir is not None and not check_dir(target_dir, "Target"):
        raise typer.Exit(code=NO_TARGET_DIR)


@app.command()
def pdf():
    """Convert PDF files to specified output format"""
    pass


if __name__ == "__main__":
    app()
