# Roadmap for xplat

## Update dependencies

- [x] Remove Sourcery dependency and replace with ruff
- [x] Update Python version requirements from 3.9 to 3.12
- [x] Resolve Safety + Typer compatibility issue (updated Typer to 0.12.x, downgraded Safety to 1.10.3)
- [x] Fix MyPy pre-commit integration dependency conflicts (using local poetry run mypy)

## Code Quality Improvements

- [ ] Fix remaining type hint issues (add `Optional` where needed)
  - [ ] `src/xplat/cli.py` - 6 implicit Optional parameters
  - [ ] `src/xplat/rename.py` - 2 implicit Optional parameters
  - [ ] `src/xplat/list.py` - 1 implicit Optional parameter
- [ ] Address Ruff linting suggestions (21 remaining issues)
  - [ ] Convert if/else blocks to ternary operators where appropriate
  - [ ] Fix unused loop variables
  - [ ] Simplify nested if statements
  - [ ] Replace `open()` with `Path.open()` in tests and constants
- [ ] Resolve MyPy type checking errors (16 issues)
  - [ ] Fix missing return statements
  - [ ] Add proper type annotations for variables
  - [ ] Fix function type validation issues

## Development Workflow

- [x] Implement modern Python tooling stack (Ruff, Black, Bandit, Pre-commit)
- [x] Create comprehensive pre-commit hooks
- [x] Update documentation (CLAUDE.md, README.md)
- [ ] Create development contribution guide
- [ ] Add GitHub issue templates
