"""Convert PDF to image(s)"""
from pathlib import Path

from pdf2image import convert_from_path


def pdf_to_img(
    pdf_file: Path,
    output_dir: Path,
    format: str,
    width: int = 600,
    grayscale: bool = False,
) -> list:
    """Convert PDF to image(s)"""
    # create output name
    wide = "max_" if width is None else width
    color = "gray_" if grayscale else ""
    pdf_stem = f"{pdf_file.stem}_{wide}w_{color}"
    # use None to preserve aspect ratio
    size_tuple = (width, None)
    with output_dir:
        images_from_path = convert_from_path(
            f"{pdf_file}",
            output_folder=output_dir,
            fmt=format,
            output_file=pdf_stem,
            size=size_tuple,
            grayscale=grayscale,
            paths_only=True,
        )
    return images_from_path
