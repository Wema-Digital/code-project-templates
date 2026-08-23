# CLAUDE.md — python-scripts

This is the **Python utility scripts template** of the `coding-project-templates` library. It lives on branch `py-script` and is checked out as a git worktree at `features/python-scripts` within the root repo.

## Role of this template

`python-scripts` provides a starter scaffold for collections of standalone Python utility scripts — automation, data processing, CLI one-offs, and scheduled tasks. It extends the language-agnostic base (`claude-code-basic`, branch `claude-code-b`) with a lightweight Python structure suited to script-first projects rather than full applications.

## Stack

- **Language**: Python
- **CLI parsing**: `argparse` (stdlib) or `click`
- **Config**: `python-dotenv` (`.env` files)
- **Testing**: pytest
- **Linting**: Ruff
- **CI**: GitHub Actions

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | Language-agnostic task tracking template (from base) |
| `README.md` | Guide to using this template with Claude Code (from base) |
| `requirements.txt` | Python deps example — extend with script-specific packages |
| `.claude/plan.md` | Base template plan (for reference) |
| `CLAUDE.md` | This file |

**Planned additions (Phase 5):**
- `scripts/example_script.py` — a working example script with argparse + logging
- `tests/test_example_script.py` — pytest scaffold with one passing test
- `.env.example`
- `requirements.txt` — updated with `click`, `python-dotenv`
- `.github/workflows/test.yml` — CI on push (shellcheck + pytest)

## Repo conventions (from root CLAUDE.md)

- **Commits** on this branch: `phase 5 intermediate: <what changed>` or `feat: <what changed>`
- **Push** to `origin py-script` from inside this worktree
- **Planning notes** live in the root repo's `claude/` folder (numbered `N-Title.md`), not here
- **GitHub Project**: [Wema-Digital/projects/2](https://github.com/orgs/Wema-Digital/projects/2) — mark tasks Done after committing

## Receiving base updates

When `claude-code-basic` is updated, merge changes into this branch:

```bash
cd features/python-scripts   # branch py-script
git merge claude-code-b
git push origin py-script
```
