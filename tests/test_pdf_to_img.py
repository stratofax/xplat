import tempfile
from pathlib import Path

from importlib_resources import files

import xplat.samples
from xplat.pdf_to_img import pdf_to_img


def test_pdf_to_img():
    # Input PDF file
    pdf_file = files(xplat.samples).joinpath("ttvp_tabulator.pdf")

    # Output directory
    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = Path(temp_dir)

        # Test the function with default width and color
        image_paths = pdf_to_img(pdf_file, output_dir, "png")

        assert len(image_paths) > 0, "No images were generated."
        for image_path in image_paths:
            assert image_path.endswith(
                ".png"
            ), "Output file has incorrect format."
            # assert (
            # output_dir in image_path.parents
            # ), "Output file is not in the correct directory."

        # Test the function with custom width and grayscale
        custom_width = 800
        grayscale = True
        image_paths_gray = pdf_to_img(
            pdf_file, output_dir, "png", custom_width, grayscale
        )

        assert len(image_paths_gray) > 0, "No grayscale images were generated."
        for image_path in image_paths_gray:
            assert image_path.endswith(
                ".png"
            ), "Output file has incorrect format."
            # assert (
            # output_dir in image_path.parents
            # ), "Output file is not in the correct directory."
            # assert (
            # f"_{custom_width}w_gray_" in image_path.name
            # ), "Output file has incorrect naming convention."
