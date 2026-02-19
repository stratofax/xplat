# TASK.md - xplat Current Work Items

## Completed in v0.2.0 (2026-02-19)

### Security Hardening
- [x] **Fix `constants.py` version loading** - Replaced relative `Path("pyproject.toml")` with `importlib.metadata.version("xplat")` — was a release blocker
- [x] **Extension filter validation** - `validate_extension()` rejects glob metacharacters (`*`, `?`, `/`, `..`)
- [x] **Symlink detection** - `rename_file()` refuses to operate on symlinks
- [x] **Batch rename collision handling** - `FileExistsError` caught gracefully (skip + warn, not crash)
- [x] **Replace safety with pip-audit** - Migrated to Python Packaging Authority's actively maintained scanner

### Version & CI
- [x] **Version bumped to 0.2.0**
- [x] **21/21 tests passing** on Ubuntu, macOS, Windows (Python 3.12, 3.13)
- [x] **0 errors** across mypy, ruff, bandit

## Open Items (v0.2.1+)

### Code Quality
- [ ] **Fix `info.py` builtin shadowing** - Rename `property` variable to `value` in `add_list()` to avoid shadowing Python builtin
- [ ] **Add timezone awareness** - `list.py:17` `datetime.fromtimestamp()` should use explicit timezone
- [ ] **Increase test coverage** - Currently 87% (289 stmts, 38 missed). Key gaps: `cli.py` interactive prompts, old rename path

### Refactoring
- [ ] **Decompose `rename` command** - `cli.py` rename function is too long; extract file discovery, validation, and confirmation into helpers
- [ ] **Simplify `print_files()` control flow** - Remove sourcery skip comment, use `len(files)` directly
- [ ] **Split `print_selected_info()`** - Separate input validation, file display, and user prompting
- [ ] **Modernize `check_dir()`/`check_file()` return types** - Replace `(bool, str)` tuples with proper exception raising
- [ ] **Remove stale test docstrings** - References to "should FAIL with current Typer 0.9.x" (tests pass now)

### Documentation
- [ ] **Create CONTRIBUTING.md** - Development setup, testing, code style guide
- [ ] **Add GitHub issue templates** - Bug report, feature request
- [ ] **Remove or refresh BASELINE-REPORT.md** - Frozen at September 2025 state

## Backlog (from ROADMAP.md)

### CLI Enhancements
- [ ] Add logging with verbosity levels
- [ ] Implement plugin architecture
- [ ] `list`: Use current directory as default when no path specified
- [ ] `info`: Separate data collection from formatting
- [ ] `info`: Export to JSON format
- [ ] `rename`: Make source directory the default positional argument
- [ ] `rename`: Use current directory when no source specified (with interactive confirmation)
- [ ] `rename`: Support renaming a single file
- [ ] `rename`: Preserve hyphens in file names
- [ ] `rename`: Strip leading/trailing spaces from file names

### Infrastructure
- [ ] Evaluate replacing `colorama` + raw `typer.secho` with `rich` for better terminal output
- [ ] Consider adding `py.typed` marker for downstream type checking consumers
