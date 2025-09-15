# Roadmap for xplat

## Critical Typer Compatibility Issues (URGENT)

- [ ] **Fix Typer help system crashes** - `TypeError: Parameter.make_metavar()` compatibility issue
  - [ ] Upgrade Typer from 0.9.x to latest stable version (0.12+)
  - [ ] Test all help functionality: `--help`, `-h`, command-specific help
  - [ ] Resolve Click version compatibility (currently Click 8.2.1)
  - [ ] Fix 287+ deprecation warnings from Click/Typer version mismatch
- [ ] **Resolve TDD test failures** - 5/5 help tests currently failing
  - [ ] `test_app_help()` - Main application help
  - [ ] `test_info_help()` - Info command help
  - [ ] `test_list_help()` - List command help
  - [ ] `test_rename_help()` - Rename command help
  - [ ] `test_help_flag_short()` - Short flag `-h` support

## Update dependencies

- [x] Remove Sourcery dependency and replace with ruff
- [x] Update Python version requirements from 3.9 to 3.12
- [x] Remove unused dependencies (optimize-images, pdf2image, shellingham, importlib-resources)
- [x] Remove redundant dev dependencies (black, flake8, isort, pylint) - replaced by Ruff
- [x] Fix MyPy pre-commit integration dependency conflicts (using local poetry run mypy)
- [ ] Resolve remaining Safety + Typer compatibility after Typer upgrade

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
