# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Xplat is a cross-platform Python CLI tool for batch file management and conversion operations. Built with Python 3.9+ using Poetry for dependency management and Typer for the CLI interface.

## Development Commands

### Environment Setup
- `poetry install` - Install dependencies and development tools
- `poetry shell` - Activate virtual environment

### Testing and Quality Assurance
- `pytest` - Run test suite
- `pytest --cov-report term-missing --cov=src/` - Run tests with coverage report
- `poetry run pytest --cov=./ --cov-report=lcov tests/` - Run tests with lcov coverage for CI
- `poetry run flake8 .` - Run linting (syntax errors and undefined names)
- `poetry run flake8 . --exit-zero --max-complexity=10 --max-line-length=127` - Full linting with warnings

### Running the Application
- `xplat --help` - Show available commands after installation
- `poetry run python -m xplat.cli` - Run during development

### Single Test Execution
- `pytest tests/test_specific_module.py` - Run specific test file
- `pytest tests/test_specific_module.py::test_function_name` - Run specific test

## Architecture

### Core Structure  
- **CLI Layer** (`src/xplat/cli.py`): Refactored Typer-based interface with enhanced options and interactive mode
- **Business Logic Modules**:
  - `list.py` - File discovery, listing utilities, and FileInfo class
  - `rename.py` - Enhanced file renaming with `rename_file()`, `make_safe_path()`, and `safe_stem()` functions
  - `info.py` - Platform information reporting
- **Configuration** (`constants.py`): Dynamic version reading from pyproject.toml, error codes, program metadata
- **Development Planning** (`TODO-CLI.md`): Planned improvements and feature roadmap

### Command Architecture
The CLI has been refactored with improved patterns:
1. Modular functions for error handling (`print_error()`)
2. Enhanced file listing with interactive selection (`review_files()`)
3. Structured file information display (`FileInfo` class, `print_file_data()`)
4. Separated concerns: validation, file processing, user interaction
5. Consistent error codes and user prompts

### Key Dependencies
- **Typer**: CLI framework with automatic help generation
- **pathlib**: Modern path handling (Python 3.4+)
- **colorama**: Cross-platform colored terminal output
- **tomli/tomllib**: TOML parsing for dynamic version reading

### File Processing Patterns
- All file operations use pathlib.Path objects
- File filtering by extension is case-sensitive
- Enhanced dry-run output with detailed formatting
- Interactive mode with per-file confirmation
- Improved error handling with proper exceptions (FileNotFoundError, FileExistsError)
- Smart filename transformation: spaces→delimiters, dots→underscores, lowercase normalization

### Available Commands
- `info` - Platform and Python environment information
- `list` - Interactive directory listing with file selection and detailed info display
- `rename` - Enhanced batch file renaming with multiple options:
  - `-s/--source-dir`: Source directory (required)
  - `-o/--output-dir`: Output directory (optional)
  - `-e/--ext`: File extension filter (optional)
  - `-n/--dry-run`: Preview changes without modifying files
  - `-i/--interactive`: Interactive confirmation mode

## Code Style
- Follows Sourcery.yaml rules (no wildcard imports, avoid staticmethod)
- Uses errno constants for exit codes
- Descriptive error messages with colored output
- Type hints throughout codebase