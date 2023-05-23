""" The Command Line Interface (CLI) code for xplat
Uses the typer package to implement sub-commands, command options
and help text.
Only CLI code should be in this module, input and output for the user.
TODO: add logging, verbosity
"""

from pathlib import Path
from typing import Optional

import typer

from xplat import constants, plat_info, renamer
from xplat.list_files import FileInfo, create_file_list

# numeric constants
PROGRAM_NAME = constants.PROGRAM_NAME
VERSION = constants.VERSION
APP_HELP = constants.APP_HELP
NO_ERROR = constants.NO_ERROR
NO_FILE = constants.NO_FILE
BAD_REQUEST = constants.BAD_REQUEST


def version_callback(is_version_requested: bool) -> None:
    """Display the version number and exit"""
    if is_version_requested:
        typer.echo(f"{PROGRAM_NAME} version: {VERSION}")
        raise typer.Exit(code=NO_ERROR)


def check_dir(dir_path: Path, dir_label: str = "") -> bool:
    """
    Check if a directory exists, display error message if not
    dir_label is an optional label to describe
    the purpose of the directory path
    """
    # display directory label if provided
    if dir_label != "":
        dir_label = f"{dir_label}: "

    dir_exist = dir_path.is_dir()
    if not dir_exist:
        print_error(f"{dir_label}'{dir_path}' is not a directory.")
    return dir_exist


def check_file(file_name: Path) -> bool:
    """
    Check if a file exists, display error message if not
    file_label is an optional label to describe
    the purpose of the file path
    """
    # check if file_name is a Path object
    if not isinstance(file_name, Path):
        print_error(f"'{file_name}' is not a path to a file.")
        return False

    file_exist = file_name.is_file()
    if not file_exist:
        print_error(f"'{file_name}' is not a file.")
    return file_exist


def print_error(msg: str) -> None:
    """
    Display an error message
    """
    typer.secho(
        msg,
        fg=typer.colors.BRIGHT_WHITE,
        bg=typer.colors.RED,
    )


def print_header(ext: str) -> None:
    """
    Print a header for the file list
    """
    if ext is not None:
        list_label = f"Listing files with extension '.{ext}':"
    else:
        list_label = "Listing all files (no directories):"

    label_border = "-" * len(list_label)
    typer.echo(label_border)
    typer.secho(
        list_label,
        fg=typer.colors.BRIGHT_YELLOW,
    )
    typer.echo(label_border)


def print_files(files: list) -> int:
    """
    Print a list of files,
    return the number of files found
    """
    # sourcery skip: simplify-empty-collection-comparison
    # testing for the empty list works reliably, unlike boolean test
    if files == []:
        file_count = 0
    else:
        for file_count, file_name in enumerate(files, start=1):
            typer.secho(
                f"{file_count}) {Path(file_name).name}", fg=typer.colors.GREEN
            )

    # report the number of files found.
    file_report = f"Total files found = {file_count}"
    typer.echo("-" * len(file_report))
    typer.secho(file_report, fg=typer.colors.BRIGHT_YELLOW)

    return file_count


def print_file_data(file_info: FileInfo) -> None:
    """
    Print file properties in indented table format
    """
    typer.secho(f"{file_info.file_name}", fg=typer.colors.BRIGHT_GREEN)
    typer.echo(f"  Size:     {file_info.size}")
    typer.echo(f"  Created:  {file_info.created}")
    typer.echo(f"  Modified: {file_info.modified}")
    typer.echo(f"  Accessed: {file_info.accessed}")


def print_file_info(file_name: Path) -> None:
    """
    Display file information for a file
    """
    if check_file(file_name):
        print_file_data(FileInfo(file_name))


def print_selected_info(files: list, index: str) -> str:
    """Display file information for a selected file."""
    try:
        file_index = int(index) - 1
    except ValueError:
        return "Invalid input, please enter a number or 'q'.\n"

    if file_index < 0 or file_index > len(files) - 1:
        message = f"The number {index} is out of range.\n"
        message += "Please enter a matching number.\n"
        return message

    print_file_info(files[file_index])
    user_input = typer.prompt("Enter 'q' to quit, 'c' to continue")

    if user_input == "q":
        raise typer.Exit(code=NO_ERROR)

    return "Select another file to examine.\n"


def rename_list(
    f_list: list, output_dir: Path = None, dryrun: bool = False
) -> int:
    """
    Rename a list of file paths to internet-friendly names, display results
    """
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


def review_files(directory: Path, extension: str = None) -> None:
    """
    Displays a list of files and prompts for file selection
    """
    files = create_file_list(directory, extension)
    basic_prompt = "Enter a number to show file info, or 'q' to quit"
    full_prompt = basic_prompt

    # repeat until the user quits
    while True:
        print_header(extension)
        print_files(files)

        file_selector = typer.prompt(full_prompt)

        if file_selector == "q":
            break

        full_prompt = print_selected_info(files, file_selector) + basic_prompt


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
        None, help="Directory to list files from (current if none)."
    ),
    ext: str = typer.Option(
        None, "--ext", "-x", help="Case-sensitive file extension."
    ),
) -> None:
    """List files in a directory, or info for a file."""
    if path is None:
        path = Path.cwd()
    if path.is_file():
        """list file information"""
        print_file_info(path)
    else:
        """list directory contents"""
        if not check_dir(path, "File list"):
            raise typer.Exit(code=NO_FILE)

        review_files(path, ext)


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
    """
    Convert file names for cross-platform compatibility
    """
    # use Typer to ensure we get a source directory
    if not check_dir(source_dir, "Source"):
        raise typer.Exit(code=NO_FILE)
    # output directory is optional
    if output_dir is not None and not check_dir(output_dir, "Output"):
        raise typer.Exit(code=NO_FILE)

    files = create_file_list(source_dir, ext)
    files_found = print_files(files)
    if files_found == 0:
        typer.secho(
            "  Try a different extension, or skip '--ext' for all files.",
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(code=NO_FILE)

    if output_dir is None:
        rename_existing = typer.prompt(
            "No output directory specified. Rename files? [y/n]"
        )
        # everything except y or Y cancels
        if rename_existing.lower() != "y":
            typer.echo("File name conversion cancelled.")
            raise typer.Exit(code=NO_ERROR)

        output_dir = source_dir

    typer.echo("Selected files will be renamed and saved to:")
    typer.secho(f"{output_dir}", fg=typer.colors.YELLOW)
    plural = "s" if files_found > 1 else ""
    rename_files = typer.prompt(
        f"Rename {files_found} file{plural} of type '{ext}'? [y/n]",
    )
    # everything except y or Y cancels
    if rename_files.lower() != "y":
        typer.echo("Conversion cancelled.")
        raise typer.Exit(code=NO_ERROR)

    rename_total = rename_list(files, output_dir, dryrun=dry_run)
    plural = "s" if rename_total > 1 else ""
    typer.echo(
        f"Processed {rename_total} file{plural} of {files_found} found."
    )


if __name__ == "__main__":
    app()
