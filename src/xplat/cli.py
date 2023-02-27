""" The Command Line Interface (CLI) code for xplat
Uses the typer package to implement sub-commands, command options
and help text.
"""
import subprocess
from pathlib import Path
from typing import Optional

import typer

from xplat import constants, pdf2img, plat_info, renamer

NO_FILE_MATCH = -30
BAD_FORMAT = -40
USER_CANCEL = 10
VERSION = constants.VERSION


def version_callback(value: bool) -> None:
    """Display the version number and exit."""
    if value:
        typer.echo(f"xplat version: {VERSION}")
        raise typer.Exit


def check_dir(dir_path: Path, dir_label: str = "") -> bool:
    """Check if a directory exists, display error message if not.
    dir_label is an optional label to describe the purpose of the directory path.
    """
    if dir_label != "":
        dir_label = f"{dir_label}: "
    if not dir_path.is_dir():
        typer.secho(
            f"{dir_label}'{dir_path}' is not a directory. Aborted!",
            fg=typer.colors.WHITE,
            bg=typer.colors.RED,
        )
    return dir_path.is_dir()


def check_formats(file_ext: str, format_tuple: tuple) -> bool:
    """Check if a file extension is in a tuple of valid formats."""
    return file_ext in format_tuple


def create_file_list(dir: Path, file_glob: str = None) -> list:
    """Create a list of files in a directory, return the sorted list."""
    globber = "*.*" if file_glob is None else f"*.{file_glob}"
    # returns a list of Path objects
    return sorted(dir.glob(globber))


def print_files(files: list) -> int:
    """Print a list of files, return the number of files found."""
    # sourcery skip: remove-unnecessary-else, simplify-empty-collection-comparison, swap-if-else-branches
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
    """Rename a list of file paths to internet-friendly names, display results"""
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
        new_file_name = renamer.inet_names(f_name, output_dir, dryrun)
        typer.secho(f"{new_file_name}", fg=typer.colors.BRIGHT_CYAN)
    return convert_count


def convert_pdfs(
    f_list: list,
    output_dir: Path = None,
    image_ext: str = "png",
    img_width: int = 512,
    gray: bool = False,
) -> int:
    for convert_count, f_name in enumerate(f_list, start=1):
        typer.echo("Converting PDF file:")
        typer.secho(f"{f_name}", fg=typer.colors.CYAN)
        convert_results = pdf2img.pdf2img(
            f_name,
            output_dir,
            format=image_ext,
            width=img_width,
            grayscale=gray,
        )
        typer.echo("  to:")
        for result in convert_results:
            typer.secho(f"{result}", fg=typer.colors.CYAN)

        # new_file_name = renamer.inet_names(f_name, output_dir, dryrun)
        # typer.secho(f"{new_file_name}", fg=typer.colors.BRIGHT_CYAN)
    return convert_count


def convert_text(
    full_file_name: str, output_dir: str = None, convert_ext: str = "html"
) -> str:
    """
    Convert text file to specified file type with pandoc
    """
    if not Path(full_file_name).is_file():
        typer.echo(f"ERROR: {full_file_name} is not a file", err=True)
        return None
    # set file type for glob
    file_stem = Path(full_file_name).stem
    if output_dir is None:
        working_dir = Path(full_file_name).parent
    else:
        working_dir = Path(output_dir)
    output_name = f"{working_dir}/{file_stem}.{convert_ext}"
    convert_cmd = [
        "pandoc",
        "--wrap=none",
        full_file_name,
        "-o" f"{output_name}",
    ]
    convert_result = subprocess.run(convert_cmd)
    if convert_result.returncode == 0:
        return output_name
    typer.echo(
        f"Error {convert_result.returncode} converting {full_file_name} to {convert_ext}",
        err=True,
    )
    return None


app = typer.Typer(
    help="Cross-platform tools for batch file management and conversion"
)


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
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
    dir: Path,
    ext: str = typer.Option(None, help="Case-sensitive file extension."),
) -> None:
    """List files in the specified directory."""
    if check_dir(dir, "File list"):
        if ext is not None:
            # remove leading period if present
            ext = ext.lstrip(".")
            typer.secho(
                f"Listing files with extension '.{ext}':",
                fg=typer.colors.BRIGHT_YELLOW,
            )
        print_files(create_file_list(dir, ext))
    else:
        raise typer.Exit(code=constants.NO_FILE)


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

    files = create_file_list(source_dir, ext)
    files_found = print_files(files)
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
        rename_total = rename_list(files, output_dir, dryrun=dry_run)
        plural = "s" if rename_total > 1 else ""
        typer.echo(
            f"Processed {rename_total} file{plural} of {files_found} found."
        )


@app.command()
def pdfs(
    source_dir: Path = typer.Option(
        ...,
        help="Source directory containing the PDF files to rename.",
    ),
    output_dir: Path = typer.Option(
        ..., help="Output directory to save image files."
    ),
    image_ext: str = typer.Option(
        None, help="Image file extension [jpeg, png, tiff or ppm]"
    ),
    width: int = typer.Option(
        None, help="Image width in pixels, skip for max width"
    ),
    full_color: bool = typer.Option(
        True, help="Convert to color or grayscale"
    ),
):
    """Convert PDF files to image files (formats: JPEG, PNG, TIFF or PPM)."""
    # use Typer to ensure we get a source directory

    if not check_dir(source_dir, "Source"):
        raise typer.Exit(code=constants.NO_FILE)
    # output directory is optional
    if not check_dir(output_dir, "Output"):
        raise typer.Exit(code=constants.NO_FILE)

    if image_ext is None:
        typer.secho("No image format specified; using default: png")
        convert_format = "png"
    else:
        convert_format = image_ext.lower()
        formats = ("jpeg", "png", "tiff", "ppm")
        if not check_formats(convert_format, formats):
            typer.secho(
                "Image format must be one of the following:",
                fg=typer.colors.BRIGHT_YELLOW,
            )
            for ext in formats:
                typer.echo(f"  {ext}")
            raise typer.Exit(code=BAD_FORMAT)
    grayscale = not full_color
    typer.echo(f"Converting PDFs to '{convert_format}' format ...")
    pdf_list = create_file_list(source_dir, "pdf")
    files_found = print_files(pdf_list)
    if files_found == 0:
        typer.secho(
            f"  No PDFs found in directory: {source_dir}",
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(code=NO_FILE_MATCH)

    typer.echo("Selected PDFs will be converted and saved to:")
    typer.secho(f"{output_dir}", fg=typer.colors.YELLOW)
    plural = "s" if files_found > 1 else ""
    pdfs_2_img = typer.prompt(
        f"Convert {files_found} PDF file{plural} to images of type '{convert_format}'? [y/N]",
    )
    # everything except y or Y cancels
    if pdfs_2_img.lower() != "y":
        typer.echo("PDF conversion cancelled.")
        raise typer.Exit(code=USER_CANCEL)
    else:
        image_total = convert_pdfs(
            pdf_list,
            output_dir,
            convert_format,
            img_width=width,
            gray=grayscale,
        )
        plural = "s" if image_total > 1 else ""
        typer.echo(
            f"Processed {image_total} file{plural} of {files_found} found."
        )


@app.command()
def text(
    source_dir: Path = typer.Option(
        ...,
        help="Source directory containing the text files to rename.",
    ),
    output_dir: Path = typer.Option(
        None, help="Output directory to save converted text files."
    ),
    source_ext: str = typer.Option(
        "docx", help="Extension of source text files to convert."
    ),
    convert_ext: str = typer.Option(
        "markdown", help="Extension of converted text files."
    ),
):
    """Convert text files to a different text format."""
    # use Typer to ensure we get a source directory
    if not check_dir(source_dir, "Source"):
        raise typer.Exit(code=constants.NO_FILE)
    # output directory is optional
    if output_dir is not None and not check_dir(output_dir, "Output"):
        raise typer.Exit(code=constants.NO_FILE)

    convert_from = source_ext.lower()
    convert_to = convert_ext.lower()
    typer.echo(f"Converting {convert_from} files to {convert_to} format ...")
    text_list = create_file_list(source_dir, convert_from)
    files_found = print_files(text_list)
    if files_found == 0:
        typer.secho(
            f"  No {convert_from} files found in directory: {source_dir}",
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(code=NO_FILE_MATCH)

    typer.echo(
        f"Selected {convert_from} files will be converted and saved as {convert_to}."
    )
    plural = "s" if files_found > 1 else ""
    confirm_convert = typer.prompt(
        f"Convert {files_found} '{convert_from}' file{plural} to file{plural} of type '{convert_to}'? [y/N]",
    )
    # everything except y or Y cancels
    if confirm_convert.lower() != "y":
        typer.echo("Text conversion cancelled.")
        raise typer.Exit(code=USER_CANCEL)
    else:
        for text_total, file_name in enumerate(text_list, start=1):
            typer.secho(f"Converting: {file_name} ...", fg=typer.colors.CYAN)
            new_name = convert_text(
                file_name, output_dir, convert_ext=convert_to
            )
            if new_name is not None:
                typer.secho(f"to:         {new_name}", fg=typer.colors.CYAN)
        plural = "s" if text_total > 1 else ""
        typer.echo(
            f"Processed {text_total} file{plural} of {files_found} found."
        )


if __name__ == "__main__":
    app()
