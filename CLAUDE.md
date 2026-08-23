# CLAUDE.md — wsl-scripts

This is the **WSL/Bash utility scripts template** of the `coding-project-templates` library. It lives on branch `wsl-tools` and is checked out as a git worktree at `features/wsl-scripts` within the root repo.

## Role of this template

`wsl-scripts` provides a starter scaffold for collections of Bash/shell scripts designed to run in WSL (Windows Subsystem for Linux) or any Linux environment. It extends the language-agnostic base (`claude-code-basic`, branch `claude-code-b`) with shell-specific structure and tooling for writing, testing, and linting Bash scripts.

## Stack

- **Shell**: Bash (WSL / Linux)
- **Linting**: ShellCheck
- **Testing**: bats-core (Bash Automated Testing System)
- **CI**: GitHub Actions — ShellCheck + bats on push

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | Language-agnostic task tracking template (from base) |
| `README.md` | Guide to using this template with Claude Code (from base) |
| `requirements.txt` | Python deps example — not primary for this stack |
| `.claude/plan.md` | Base template plan (for reference) |
| `CLAUDE.md` | This file |

**Planned additions (Phase 5):**
- `scripts/example.sh` — working example script with argument parsing, logging, and error handling (`set -euo pipefail`)
- `scripts/lib/utils.sh` — shared utility functions (colours, logging helpers)
- `tests/example.bats` — bats-core test scaffold with one passing test
- `.shellcheckrc` — ShellCheck configuration
- `.github/workflows/test.yml` — CI: ShellCheck lint + bats tests on push

## Repo conventions (from root CLAUDE.md)

- **Commits** on this branch: `phase 5 intermediate: <what changed>` or `feat: <what changed>`
- **Push** to `origin wsl-tools` from inside this worktree
- **Planning notes** live in the root repo's `claude/` folder (numbered `N-Title.md`), not here
- **GitHub Project**: [Wema-Digital/projects/2](https://github.com/orgs/Wema-Digital/projects/2) — mark tasks Done after committing

## Receiving base updates

When `claude-code-basic` is updated, merge changes into this branch:

```bash
cd features/wsl-scripts   # branch wsl-tools
git merge claude-code-b
git push origin wsl-tools
```
