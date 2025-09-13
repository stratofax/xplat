# Roadmap for xplat

## Update dependencies

- [x] Remove Sourcery dependency and replace with ruff
- [x] Update Python version requirements from 3.9 to 3.12
- [x] Resolve Safety + Typer compatibility issue (updated Typer to 0.12.x, downgraded Safety to 1.10.3)
- [x] Fix MyPy pre-commit integration dependency conflicts (using local poetry run mypy)

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

- [ ] Address remaining B008 warnings (Typer function calls in defaults)
  - Note: These are standard Typer patterns and may not need fixing
- [ ] Update vulnerable dependencies identified by Safety
  - [ ] black 23.1.0 → latest version
  - [ ] pillow 9.4.0 → latest version
  - [ ] virtualenv 20.21.1 → latest version
- [ ] Consider pytest dependency updates (ast.Str deprecation warnings)
- [ ] Evaluate test coverage improvement opportunities (currently 88%)
