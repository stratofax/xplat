"""Tests for the rename module functionality."""

from pathlib import Path
import pytest
from xplat import rename

# Setup test directories
@pytest.fixture
def test_dirs():
    """Create and return test directories, cleanup after test."""
    test_path = Path.home().joinpath("tmp", "xplat_renamer_tests")
    test_path.mkdir(parents=True, exist_ok=True)
    
    output_path = test_path.joinpath("target")
    output_path.mkdir(parents=True, exist_ok=True)
    
    yield test_path, output_path
    
    # Cleanup after test
    for file in output_path.iterdir():
        file.unlink()
    output_path.rmdir()
    
    for file in test_path.iterdir():
        file.unlink()
    test_path.rmdir()

@pytest.fixture
def test_files(test_dirs):
    """Create and return test files."""
    test_path, _ = test_dirs
    
    # Create test files with spaces, dots, and mixed case
    file1 = test_path / "Space to Delim.test.FILE.TXT"
    file2 = test_path / "Another.Complex File.NAME.txt"
    
    file1.touch()
    file2.touch()
    
    return file1, file2

def test_safe_stem():
    """Test filename stem transformation."""
    # Test basic transformation
    assert rename.safe_stem("Hello World.test") == "hello_world_test"
    
    # Test multiple spaces and dots
    assert rename.safe_stem("This..Has...Lots.Of..Dots") == "this_has_lots_of_dots"
    
    # Test custom delimiter
    assert rename.safe_stem("Hello World", delim="-") == "hello-world"
    
    # Test multiple delimiters get collapsed
    assert rename.safe_stem("Too__Many___Delims") == "too_many_delims"

def test_make_safe_path(test_dirs):
    """Test safe path creation."""
    test_path, target_dir = test_dirs
    
    # Test in same directory
    orig_path = test_path / "Test File.TXT"
    safe_path = rename.make_safe_path(orig_path)
    assert safe_path.name == "test_file.txt"
    assert safe_path.parent == test_path
    
    # Test with target directory
    safe_path = rename.make_safe_path(orig_path, target_dir)
    assert safe_path.name == "test_file.txt"
    assert safe_path.parent == target_dir

def test_rename_file_errors(test_dirs, test_files):
    """Test error conditions for rename_file."""
    test_path, target_dir = test_dirs
    test_file, _ = test_files
    
    # Test non-existent file
    bad_file = test_path / "not_a_file.tmp"
    with pytest.raises(FileNotFoundError):
        rename.rename_file(bad_file)
    
    # Test invalid target directory
    bad_dir = test_path / "not_a_dir"
    with pytest.raises(NotADirectoryError):
        rename.rename_file(test_file, bad_dir)
    
    # Test file already exists
    # First, create a file with the name that would result from renaming test_file
    existing_file = target_dir / "space_to_delim_test_file.txt"
    existing_file.touch()
    with pytest.raises(FileExistsError):
        rename.rename_file(test_file, target_dir)

def test_rename_file_success(test_dirs, test_files):
    """Test successful file renaming operations."""
    test_path, target_dir = test_dirs
    test_file, _ = test_files
    
    # Test rename in same directory
    new_path = rename.rename_file(test_file)
    assert new_path.exists()
    assert new_path.name == "space_to_delim_test_file.txt"
    assert new_path.parent == test_path
    
    # Create new file for target dir test
    new_file = test_path / "Move.This.File.TXT"
    new_file.touch()
    
    # Test rename to target directory
    moved_path = rename.rename_file(new_file, target_dir)
    assert moved_path.exists()
    assert moved_path.name == "move_this_file.txt"
    assert moved_path.parent == target_dir
