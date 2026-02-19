# TASK.md - xplat Current Work Items

## Active Sprint (2026-02-19)

### Security & Quality

- [ ] **Fix `constants.py` version loading** - Replace relative `Path("pyproject.toml")` with `importlib.metadata.version("xplat")` so the tool works when invoked from any directory (HIGH PRIORITY)
- [ ] **Fix `info.py` builtin shadowing** - Rename `property` variable to `value` in `add_list()` to avoid shadowing Python builtin
- [ ] **Add timezone awareness** - `list.py:17` `datetime.fromtimestamp()` should use explicit timezone
- [ ] **Increase test coverage** - Currently 88%, target 95%. Key gaps: `cli.py` lines 221-235 (old rename path), 303-325 (interactive mode)

### Refactoring

- [ ] **Decompose `rename` command** - `cli.py:292-349` is too long; extract file discovery, validation, and confirmation into helper functions
- [ ] **Simplify `print_files()` control flow** - Remove sourcery skip comment, use `len(files)` instead of tracking count through enumerate
- [ ] **Split `print_selected_info()`** - Separate input validation, file display, and user prompting into distinct functions
- [ ] **Modernize `check_dir()`/`check_file()` return types** - Replace `(bool, str)` tuples with proper exception raising
- [ ] **Remove stale code comments** - Update TDD test docstrings that reference "should FAIL with current Typer 0.9.x" (tests pass now)

### Documentation

- [ ] **Create CONTRIBUTING.md** - Development setup, testing, code style guide
- [ ] **Add GitHub issue templates** - Bug report, feature request
- [ ] **Update BASELINE-REPORT.md** - Reflects September 2025 state; needs refresh or removal

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
- [ ] Version bump strategy for 0.2.0 release
