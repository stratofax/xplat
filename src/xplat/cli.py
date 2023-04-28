""" The Command Line Interface (CLI) code for xplat
Uses the typer package to implement sub-commands, command options
and help text.
Only CLI code should be in this module, input and output for the user.
TODO: add logging, verbosity
"""

from pathlib import Path
from typing import Optional

import typer

from xplat import constants, list_files, plat_info, renamer

PROGRAM_NAME = constants.PROGRAM_NAME
VERSION = constants.VERSION
APP_HELP = constants.APP_HELP
NO_ERROR = constants.NO_ERROR
NO_FILE = constants.NO_FILE
BAD_REQUEST = constants.BAD_REQUEST


def version_callback(value: bool) -> None:
    """Display the version number and exit."""
    if value:
        typer.echo(f"{PROGRAM_NAME} version: {VERSION}")
        raise typer.Exit


def show_file_info(file_name: Path) -> None:
    """Display file information for a file."""
    file_size = list_files.format_bytes(file_name.stat().st_size)
    typer.secho(f"{file_name}", fg=typer.colors.BRIGHT_GREEN)
    typer.echo(f"  Size: {file_size}")
    typer.echo(
        f"  Modified: {list_files.format_timestamp(file_name.stat().st_mtime)}"
    )
    typer.echo(
        f"  Created:  {list_files.format_timestamp(file_name.stat().st_ctime)}"
    )
    typer.echo(
        f"  Accessed: {list_files.format_timestamp(file_name.stat().st_atime)}"
    )


def check_dir(dir_path: Path, dir_label: str = "") -> bool:
    """
    Check if a directory exists, display error message if not.
    dir_label is an optional label to describe
    the purpose of the directory path.
    """
    if dir_label != "":
        dir_label = f"{dir_label}: "
    if not dir_path.is_dir():
        typer.secho(
            f"{dir_label}'{dir_path}' is not a directory.",
            fg=typer.colors.BRIGHT_WHITE,
            bg=typer.colors.RED,
        )
    return dir_path.is_dir()


def print_files(files: list) -> int:
    """Print a list of files, return the number of files found."""
    # sourcery skip: simplify-empty-collection-comparison
    # testing for the empty list works reliably, unlike boolean test
    if files == []:
        file_count = 0
    else:
        for file_count, file_name in enumerate(files, start=1):
            typer.secho(Path(file_name).name, fg=typer.colors.GREEN)

    # report the number of files found.
    typer.secho(
        f"Total files found = {file_count}", fg=typer.colors.BRIGHT_YELLOW
    )
    return file_count


def rename_list(
    f_list: list, output_dir: Path = None, dryrun: bool = False
) -> int:
    """
    Rename a list of file paths to internet-friendly names, display results"""
    if dryrun:
        typer.secho(
            "Dry run is active, proposed changes won't be saved.",
            fg=typer.colors.BRIGHT_WHITE,
        )
        start_label = "Proposing file name change from:"
    else:
        start_label = "Converting file name:"
    for convert_count, f_name in enumerate(f_list, start=1):
        typer.echo(start_label)
        typer.secho(f"{f_name}", fg=typer.colors.CYAN)
        typer.echo("  to:")
        new_file_name = renamer.safe_renamer(f_name, output_dir, dryrun)
        typer.secho(f"{new_file_name}", fg=typer.colors.BRIGHT_CYAN)
    return convert_count


# CLI interface
# sourcery skip: avoid-global-variables
# module level variables are required by typer
app = typer.Typer(help=APP_HELP)


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        callback=version_callback,
        help="Print the version number.",
    ),
) -> None:
    """Empty function required for version callback"""
    pass


@app.command()
def info() -> None:
    """Display platform information."""
    typer.echo(plat_info.create_platform_report())


@app.command()
def list(
    path: Optional[Path] = typer.Argument(
        None,
        help="Directory to list files from (current if none)."
    ),
    ext: str = typer.Option(
        None,
        "--ext",
        "-x",
        help="Case-sensitive file extension."
    ),
) -> None:
    """List files in the specified or current directory."""
    if path is None:
        path = Path.cwd()
    if path.is_file():
        """list file information"""
        show_file_info(path)
    else:
        """list directory contents"""
        if not check_dir(path, "File list"):
            raise typer.Exit(code=constants.NO_FILE)
        if ext is not None:
            typer.secho(
                f"Listing files with extension '.{ext}':",
                fg=typer.colors.BRIGHT_YELLOW,
            )
        print_files(list_files.create_file_list(path, ext))


@app.command()
def rename(
    source_dir: Path = typer.Option(
        ...,
        help="Source directory containing the files to rename.",
    ),
    output_dir: Path = typer.Option(
        None, help="Output directory to save renamed files."
    ),
    ext: str = typer.Option(None, help="Case-sensitive file extension."),
    dry_run: bool = typer.Option(
        False, help="Only display (don't save) proposed name changes"
    ),
) -> None:
    """Convert file names for cross-platform compatibility."""
    # use Typer to ensure we get a source directory
    if not check_dir(source_dir, "Source"):
        raise typer.Exit(code=constants.NO_FILE)
    # output directory is optional
    if output_dir is not None and not check_dir(output_dir, "Output"):
        raise typer.Exit(code=constants.NO_FILE)

    files = list_files.create_file_list(source_dir, ext)
    files_found = print_files(files)
    if files_found == 0:
        typer.secho(
            "  Try a different extension, or skip '--ext' for all files.",
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(code=NO_FILE)

    if output_dir is None:
        rename_existing = typer.prompt(
            "No output directory specified. Rename files? [y/N]"
        )
        # everything except y or Y cancels
        if rename_existing.lower() != "y":
            typer.echo("File name conversion cancelled.")
            raise typer.Exit(code=NO_ERROR)
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
        raise typer.Exit(code=NO_ERROR)
    else:
        rename_total = rename_list(files, output_dir, dryrun=dry_run)
        plural = "s" if rename_total > 1 else ""
        typer.echo(
            f"Processed {rename_total} file{plural} of {files_found} found."
        )


if __name__ == "__main__":
    app()
