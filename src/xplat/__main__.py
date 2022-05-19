from pathlib import Path
from typing import Optional
from click import secho

import typer

from xplat.info import plat
from xplat.names import inet

__version__ = "0.1.0"

NO_SOURCE_DIR = -10
NO_OUTPUT_DIR = -20
NO_FILE_MATCH = -30
USER_CANCEL = 10


def version_callback(value: bool):
    if value:
        typer.echo(f"xplat CLI Version: {__version__}")
        raise typer.Exit()


def check_dir(dir_path: Path, dir_label: str = "") -> bool:
    if dir_label != "":
        dir_label = f"{dir_label}: "
    if not dir_path.is_dir():
        typer.secho(
            f"{dir_label}{dir_path} is not a directory. Aborted!",
            fg=typer.colors.WHITE,
            bg=typer.colors.RED,
        )
    return dir_path.is_dir()


def create_file_list(dir: Path, file_glob: str = None) -> list:
    globber = "*.*" if file_glob is None else f"*.{file_glob}"
    # returns a list of Path objects
    return sorted(dir.glob(globber))


def print_files(files: list):
    # sourcery skip: remove-unnecessary-else, simplify-empty-collection-comparison, swap-if-else-branches
    # testing for the empty list works reliably, unlike boolean test
    if files == []:
        file_count = 0
    else:
        for file_count, file_name in enumerate(files, start=1):
            typer.secho(Path(file_name).name, fg=typer.colors.GREEN)

    # report the number of files found.
    typer.secho(
        f"Total files found = {file_count}",
        fg=typer.colors.BRIGHT_YELLOW,
    )
    return file_count


def rename_list(
    f_list: list,
    output_dir: Path = None,
):
    for convert_count, f_name in enumerate(f_list, start=1):
        typer.echo("Converting file name:")
        typer.secho(f"{f_name}", fg=typer.colors.CYAN)
        typer.echo("  to:")
        new_file_name = inet.inet_names(f_name, output_dir, dryrun=False)
        typer.secho(f"{new_file_name}", fg=typer.colors.BRIGHT_CYAN)
    return convert_count


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
    if check_dir(dir, "Listing"):
        print_files(create_file_list(dir, ext))


@app.command()
def names(
    source_dir: Path = typer.Option(
        ...,
        help="Source directory containing the files to rename.",
    ),
    output_dir: Path = typer.Option(
        None, help="Output directory to save renamed files."
    ),
    ext: str = typer.Option(None, help="Case-sensitive file extension."),
):
    """Convert names of multiple files for internet compatibility."""
    # use Typer to ensure we get a source directory
    if not check_dir(source_dir, "Source"):
        raise typer.Exit(code=NO_SOURCE_DIR)
    # output directory is optional
    if output_dir is not None and not check_dir(output_dir, "Output"):
        raise typer.Exit(code=NO_OUTPUT_DIR)

    file_list = create_file_list(source_dir, ext)
    files_found = print_files(file_list)
    if files_found == 0:
        typer.secho(
            "  Try a different extension, or skip '--ext' for all files.",
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(code=NO_FILE_MATCH)

    if output_dir is None:
        rename_existing = typer.prompt(
            "No output directory specified. Rename files? [y/N]"
        )
        # everything except y or Y cancels
        if rename_existing.lower() != "y":
            typer.echo("File name conversion cancelled.")
            raise typer.Exit(code=USER_CANCEL)
        else:
            output_dir = source_dir

    typer.echo("Selected files will be renamed and saved to:")
    typer.secho(f"{output_dir}", fg=typer.colors.YELLOW)
    plural = "s" if files_found > 1 else ""
    rename_files = typer.prompt(
        f"Rename {files_found} file{plural} of type '{ext}'? [y/N]",
    )
    # everything except y or Y cancels
    if rename_files.lower() != "y":
        typer.echo("Conversion cancelled.")
        raise typer.Exit(code=USER_CANCEL)
    else:
        rename_total = rename_list(file_list, output_dir)
        plural = "s" if rename_total > 1 else ""
        typer.echo(f"Processed {rename_total} file{plural} of {files_found} found.")


@app.command()
def pdf():
    """Convert PDF files to an image file (supports: PNG)."""
    pass


if __name__ == "__main__":
    app()
