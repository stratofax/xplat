"""Tests for xplat.list module utility functions."""

import tempfile
from pathlib import Path

from xplat.list import check_dir, check_file, format_bytes


def test_format_bytes_yottabytes():
    """Test format_bytes handles values exceeding zettabyte range."""
    # 1 YB = 1024^8 bytes
    yb = 1024.0**8
    result = format_bytes(yb)
    assert "YB" in result
    assert "1.0 YB" in result


def test_check_dir_with_label():
    """Test check_dir with a label on a real directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        exists, msg = check_dir(Path(temp_dir), "Source")
        assert exists is True
        assert "Source: " in msg
        assert "is a directory" in msg


def test_check_dir_nonexistent():
    """Test check_dir with a non-existent directory."""
    exists, msg = check_dir(Path("/nonexistent/path"))
    assert exists is False
    assert "is not a directory" in msg


def test_check_dir_no_label():
    """Test check_dir without a label."""
    with tempfile.TemporaryDirectory() as temp_dir:
        exists, msg = check_dir(Path(temp_dir))
        assert exists is True
        assert msg.startswith("'")


def test_check_file_not_a_path():
    """Test check_file with a non-Path argument."""
    exists, msg = check_file("just_a_string")  # type: ignore[arg-type]
    assert exists is False
    assert "is not a path to a file" in msg


def test_check_file_nonexistent():
    """Test check_file with a non-existent file path."""
    exists, msg = check_file(Path("/nonexistent/file.txt"))
    assert exists is False
    assert "is not a file" in msg


def test_check_file_valid():
    """Test check_file with a real file."""
    with tempfile.NamedTemporaryFile(suffix=".txt") as tmp:
        exists, msg = check_file(Path(tmp.name))
        assert exists is True
        assert "is a valid file" in msg
