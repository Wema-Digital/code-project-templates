# CLAUDE.md — web-flask

This is the **Flask web application template** of the `coding-project-templates` library. It lives on branch `py-flask` and is checked out as a git worktree at `features/web-flask` within the root repo.

## Role of this template

`web-flask` provides a starter scaffold for Python web applications built with Flask using the app factory pattern. It extends the language-agnostic base (`claude-code-basic`, branch `claude-code-b`) with a Flask-specific structure, blueprints layout, and testing setup.

## Stack

- **Language**: Python
- **Framework**: Flask (app factory pattern)
- **Database**: SQLite (dev) / PostgreSQL (prod) via SQLAlchemy
- **Testing**: pytest + pytest-flask
- **Linting**: Ruff
- **CI**: GitHub Actions

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | Language-agnostic task tracking template (from base) |
| `README.md` | Guide to using this template with Claude Code (from base) |
| `requirements.txt` | Python deps example — extend with Flask packages |
| `.claude/plan.md` | Base template plan (for reference) |
| `CLAUDE.md` | This file |

**Planned additions (Phase 5):**
- `src/__init__.py` — app factory (`create_app()`)
- `src/blueprints/main.py` — example blueprint with a health-check route
- `src/config.py` — config classes (Dev, Prod, Testing)
- `tests/conftest.py` — pytest-flask fixtures
- `tests/test_routes.py` — scaffold with one passing test
- `.env.example` — `SECRET_KEY`, `DATABASE_URL`, `FLASK_ENV`
- `requirements.txt` — updated with `flask`, `flask-sqlalchemy`, `pytest-flask`
- `.github/workflows/test.yml` — CI on push

## Repo conventions (from root CLAUDE.md)

- **Commits** on this branch: `phase 5 intermediate: <what changed>` or `feat: <what changed>`
- **Push** to `origin py-flask` from inside this worktree
- **Planning notes** live in the root repo's `claude/` folder (numbered `N-Title.md`), not here
- **GitHub Project**: [Wema-Digital/projects/2](https://github.com/orgs/Wema-Digital/projects/2) — mark tasks Done after committing

## Receiving base updates

When `claude-code-basic` is updated, merge changes into this branch:

```bash
cd features/web-flask   # branch py-flask
git merge claude-code-b
git push origin py-flask
```
