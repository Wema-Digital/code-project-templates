# CLAUDE.md — python-app

This is the **Python application template** of the `coding-project-templates` library. It lives on branch `py-app` and is checked out as a git worktree at `features/python-app` within the root repo.

## Role of this template

`python-app` provides a starter scaffold for general-purpose Python applications with a clean entrypoint, configuration management, and test suite. It extends the language-agnostic base (`claude-code-basic`, branch `claude-code-b`) with Python-specific structure and tooling.

## Stack

- **Language**: Python
- **Entry point**: `src/main.py`
- **Config**: `python-dotenv` (`.env` files)
- **Testing**: pytest
- **Linting**: Ruff (or Pylint)
- **CI**: GitHub Actions

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | Language-agnostic task tracking template (from base) |
| `README.md` | Guide to using this template with Claude Code (from base) |
| `requirements.txt` | Python deps example — extend with app-specific packages |
| `.claude/plan.md` | Base template plan (for reference) |
| `CLAUDE.md` | This file |

**Planned additions (Phase 5):**
- `src/__init__.py` + `src/main.py` — application entrypoint
- `src/config.py` — environment/config loader
- `tests/test_main.py` — pytest scaffold with one passing test
- `.env.example`
- `pyproject.toml` — project metadata + tool config
- `.github/workflows/test.yml` — CI on push

## Repo conventions (from root CLAUDE.md)

- **Commits** on this branch: `phase 5 intermediate: <what changed>` or `feat: <what changed>`
- **Push** to `origin py-app` from inside this worktree
- **Planning notes** live in the root repo's `claude/` folder (numbered `N-Title.md`), not here
- **GitHub Project**: [Wema-Digital/projects/2](https://github.com/orgs/Wema-Digital/projects/2) — mark tasks Done after committing

## Receiving base updates

When `claude-code-basic` is updated, merge changes into this branch:

```bash
cd features/python-app   # branch py-app
git merge claude-code-b
git push origin py-app
```
