# Roadmap for xplat

## Critical Typer Compatibility Issues ✅ RESOLVED

- [x] **Fix Typer help system crashes** - `TypeError: Parameter.make_metavar()` compatibility issue ✅
  - [x] Upgrade Typer from 0.12.5 to 0.17.4 (latest stable version)
  - [x] Test all help functionality: `--help`, `-h`, command-specific help
  - [x] Resolve Click version compatibility (Click 8.2.1 works with Typer 0.17.4)
  - [x] Migrate to modern Annotated syntax for Typer 0.17+ compatibility
- [x] **Resolve TDD test failures** - 5/5 help tests now passing ✅
  - [x] `test_app_help()` - Main application help ✅
  - [x] `test_info_help()` - Info command help ✅
  - [x] `test_list_help()` - List command help ✅
  - [x] `test_rename_help()` - Rename command help ✅
  - [x] `test_help_flag_short()` - Short flag `-h` support ✅

## Update dependencies

- [x] Remove Sourcery dependency and replace with ruff
- [x] Update Python version requirements from 3.9 to 3.12
- [x] Remove unused dependencies (optimize-images, pdf2image, shellingham, importlib-resources)
- [x] Remove redundant dev dependencies (black, flake8, isort, pylint) - replaced by Ruff
- [x] Fix MyPy pre-commit integration dependency conflicts (using local poetry run mypy)
- [x] Resolve remaining Safety + Typer compatibility after Typer upgrade ✅
- [ ] Check for additional outdated dependencies
- [ ] Update old dependencies to modern versions

## Code Quality Improvements

- [x] Fix remaining type hint issues (add `Optional` where needed)
  - [x] `src/xplat/cli.py` - 6 implicit Optional parameters
  - [x] `src/xplat/rename.py` - 2 implicit Optional parameters
  - [x] `src/xplat/list.py` - 1 implicit Optional parameter
- [x] Address critical Ruff linting suggestions (5 core issues)
  - [x] Convert if/else blocks to ternary operators where appropriate (SIM108)
  - [x] Fix unused loop variables (B007)
  - [x] Simplify nested if statements (SIM102)
  - [x] Replace `open()` with `Path.open()` in tests and constants (PTH123)
- [ ] Resolve remaining MyPy type checking errors (12 issues)
  - [ ] Fix missing return statements in `format_bytes()`
  - [ ] Add proper type annotations for loop variables
  - [ ] Fix function type validation issues with `list` command name collision
  - [ ] Resolve `Optional[str]` parameter handling in `print_header()`

## Development Workflow

- [x] Implement modern Python tooling stack (Ruff, Black, Bandit, Pre-commit)
- [x] Create comprehensive pre-commit hooks
- [x] Update documentation (CLAUDE.md, README.md)
- [ ] Create development contribution guide
- [ ] Add GitHub issue templates

## Performance and Maintenance

- [x] **Dependency cleanup completed** - Removed 18 unused dependencies
  - [x] Eliminated image processing dependencies (optimize-images, pdf2image, pillow)
  - [x] Streamlined dev tooling (consolidated to Ruff + MyPy + Bandit + Safety)
  - [x] Reduced security surface area by removing unused packages
- [ ] Address remaining B008 warnings (Typer function calls in defaults)
  - Note: These are standard Typer patterns - may resolve with Typer upgrade
- [ ] Update remaining vulnerable dependencies after Typer upgrade
  - [x] ~~black 23.1.0~~ - Removed (replaced by Ruff)
  - [x] ~~pillow 9.4.0~~ - Removed (not used)
  - [ ] virtualenv 20.21.1 → latest version (dev dependency)
- [ ] Consider pytest dependency updates (ast.Str deprecation warnings)
- [ ] Evaluate test coverage improvement opportunities (currently 88%)
- [ ] **Performance improvements from dependency reduction**
  - [x] Faster installs with 18 fewer dependencies
  - [x] Smaller Docker images / deployment footprint
  - [x] Reduced potential for dependency conflicts

## To Do - CLI

Updates to the CLI interface, by module.

### cli

- [ ] add logging to the CLI
- [ ] implement plugin architecture

### list

- [ ] Use the current directory if no directory is specified

### info

- [ ] separate data collection from formattting
- [ ] export to JSON format

### rename

- [ ] Make the source directory the default (no option flag required)
- [ ] Use the current directory if no source directory is specified (turn on Interactive mode to confirm)
- [ ] Support conversion of a single file
- [ ] Keep hyphens ("-") in file names
- [ ] Remove leading, trailing spaces from file names

## Recent Achievements (2025-09-14)

### ✅ Typer Compatibility Resolution

Successfully resolved critical Typer compatibility issues using Test-Driven Development:

**Technical Achievement:**
- Upgraded Typer from 0.12.5 → 0.17.4 (latest stable)
- Migrated to modern `Annotated[Type, typer.Option(...)]` syntax
- Fixed `Parameter.make_metavar() missing context argument` error
- Enhanced CLI with better help text and `-h` short flag support

**TDD Success:**
- Created 5 comprehensive TDD tests targeting help functionality
- All tests now pass (100% success rate)
- Validated complete fix with full regression testing (17/17 tests pass)

**Impact:**
- Help system fully functional: `--help` and `-h` work for all commands
- Modern codebase compatible with latest Typer best practices
- Improved developer experience and user interface
