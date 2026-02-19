# Release Notes

## v0.2.0 — Security Hardening & Agentic Red Team (2026-02-19)

We had 32 AI agents try to break our software before we shipped it. Here's what happened.

xplat is an open-source Python CLI tool for batch file management — renaming, listing, and converting files across macOS, Linux, and Windows. If you've ever needed to sanitize a folder of filenames for web upload or script a batch rename across platforms, that's what xplat does.

For v0.2.0, we wanted to see what happens when you treat AI agents as adversaries, not just assistants. Before cutting the release, we ran a red team analysis using 32 adversarial AI agents — each one independently probing the codebase for security weaknesses from a different attack angle.

They found real vulnerabilities:

- Glob injection through user-supplied file extension filters
- Symlink exploitation in the rename pipeline
- Batch rename collision attacks that could crash mid-operation

Every finding was fixed, covered by new tests, and verified before the code hit main.

The full picture for v0.2.0:

- 32-agent adversarial security analysis with all findings resolved
- 21 pytest tests passing at 87% coverage across 3 operating systems and 2 Python versions (3.12, 3.13)
- 18 unused dependencies removed — smaller attack surface, faster installs
- Zero errors from mypy, ruff, and bandit static analysis
- 7 open issues closed in a single PR, some dating back to 2022

We're a small team, and having 32 agents independently stress-test your code before release is the kind of leverage that changes what's possible. Every vulnerability they surfaced was one we could fix before users ever encountered it.

github.com/stratofax/xplat

#OpenSource #Python #AgenticDevelopment #CyberSecurity #RedTeam #AI #DevSecOps
