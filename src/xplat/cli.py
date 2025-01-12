""" The Command Line Interface (CLI) code for xplat
Uses the typer package to implement sub-commands, command options
and help text.
Only CLI code should be in this module, input and output for the user.
TODO: add logging, verbosity
"""

from pathlib import Path
from typing import Optional

import typer

from xplat import constants
from xplat.info import create_platform_report
from xplat.list import FileInfo, check_dir, check_file, create_file_list
from xplat.rename import rename_file, make_safe_path

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
    check_file_result = check_file(file_name)
    if check_file_result[0]:
        print_file_data(FileInfo(file_name))
    else:
        print_error(check_file_result[1])


def print_selected_info(files: list, selected: str) -> str:
    """
    Display file information for a selected file.

    Args:
        files (list): list of files to display
        selected (str): selected file number

    Returns:
        str: prompt to display, depending on input
    """

    # input should be an integer
    try:
        file_index = int(selected) - 1
    except ValueError:
        return "Invalid input, please enter a number or 'q'.\n"

    # is the number valid?
    if file_index < 0 or file_index > len(files) - 1:
        message = f"The number {selected} is out of range.\n"
        message += f"Please enter a number between 1 and {len(files)}.\n"
        return message

    print_file_info(files[file_index])

    # prompt to continue
    user_input = typer.prompt("Enter 'q' to quit, 'c' to continue")
    if user_input == "q":
        raise typer.Exit(code=NO_ERROR)

    # continue with default prompt
    return "Select another file to examine.\n"


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


def rename_file_with_output(
    file_name: Path,
    output_dir: Path = None,
    dry_run: bool = False,
    label: str = "",
) -> None:
    """
    Renames a file with the given name to a new name
    and outputs both names.
    """
    typer.echo(label)
    typer.secho(f"{file_name}", fg=typer.colors.CYAN)
    typer.echo("  to:")
    new_path = rename_file(file_name, output_dir, dry_run)
    typer.secho(f"{new_path}", fg=typer.colors.BRIGHT_CYAN)


def rename_list(
    files: list, output_dir: Path = None, dryrun: bool = False
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

    for convert_count, current_name in enumerate(files, start=1):
        rename_file_with_output(current_name, output_dir, dryrun, start_label)

    return convert_count


def rename_files(
    files: list,
    files_found: int,
    output_dir: Path,
    ext: str,
    dry_run: bool = False,
) -> None:
    """
    Rename selected files
    """
    typer.echo("Selected files will be renamed and saved to:")
    typer.secho(f"{output_dir}", fg=typer.colors.YELLOW)
    plural = "s" if files_found > 1 else ""
    confirm_rename = typer.prompt(
        f"Rename {files_found} file{plural} of type '{ext}'? [y/n]",
    )
    # everything except y or Y cancels
    if confirm_rename.lower() != "y":
        typer.echo("Conversion cancelled.")
        raise typer.Exit(code=NO_ERROR)

    rename_total = rename_list(files, output_dir, dryrun=dry_run)
    plural = "s" if rename_total > 1 else ""
    typer.echo(
        f"Processed {rename_total} file{plural} of {files_found} found."
    )


# CLI interface
# sourcery skip: avoid-global-variables
# module level variables are required by typer
app = typer.Typer(help=constants.APP_HELP)


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
    typer.echo(create_platform_report())


@app.command()
def list(
    path: Optional[Path] = typer.Argument(
        None, help="Directory to list files from (current if none)."
    ),
    ext: str = typer.Option(
        None, "--ext", "-x", help="Case-sensitive file extension."
    ),
) -> None:
    """
    List files in a directory, or info for a file
    """
    error_code = NO_FILE
    if path is None:
        path = Path.cwd()
    if path.is_file():
        # list file information for a single file
        print_file_info(path)
    elif path.is_dir():
        review_files(path, ext)
    else:
        raise typer.Exit(code=error_code)


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

    rename_files(files, files_found, output_dir, ext, dry_run)


if __name__ == "__main__":
    app()
