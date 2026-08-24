# CLAUDE.md — web-flask

This is the **Flask web application template** of the `coding-project-templates` library. It lives on branch `py-flask` and is checked out as a git worktree at `features/web-flask` within the root repo.

## Role of this template

`web-flask` provides a starter scaffold for Python web applications built with Flask using the app factory pattern. It extends the language-agnostic base (`claude-code-basic`, branch `claude-code-b`) with a Flask-specific structure, blueprints layout, and testing setup.

## Stack

- **Language**: Python 3.12
- **Framework**: Flask 3 (app factory pattern)
- **Testing**: pytest + pytest-flask
- **CI**: GitHub Actions

No database layer is included — `web-flask` stays deliberately simpler than `web-django`. Add `Flask-SQLAlchemy` only if a project actually needs persistence.

## Project layout

```
app/
  __init__.py   ← create_app() factory — registers blueprints, reads SECRET_KEY
  routes.py     ← main blueprint (GET /health)
tests/
  conftest.py   ← pytest-flask `app` fixture
  test_app.py   ← GET /health example test
run.py          ← Entry point: loads .env, calls create_app()
.github/
  workflows/
    test.yml    ← CI: pip install (both requirement files) + pytest
```

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | Flask-specific task tracking template |
| `README.md` | Guide to using this template with Claude Code |
| `requirements.txt` | Runtime deps (Flask, python-dotenv) |
| `requirements-dev.txt` | Test deps (pytest, pytest-flask) — installs runtime deps too via `-r requirements.txt` |
| `.env.example` | `FLASK_APP`, `FLASK_ENV`, `SECRET_KEY` |
| `.claude/plan.md` | Phase 5 plan for this template, and what was deliberately deferred |
| `CLAUDE.md` | This file |

## Key patterns

**App factory** — `app/__init__.py` exports `create_app()` rather than a module-level `app`. Tests build a fresh instance per test via the `app` fixture in `tests/conftest.py`:

```python
# tests/conftest.py
@pytest.fixture
def app():
    app = create_app()
    app.config.update(TESTING=True)
    yield app
```

`pytest-flask` then supplies the `client` fixture automatically for any test that takes it as an argument.

**Adding a blueprint**:
```python
# app/users.py
from flask import Blueprint, jsonify
users = Blueprint("users", __name__)

@users.route("/users")
def list_users():
    return jsonify(users=[])

# app/__init__.py
from app.users import users
app.register_blueprint(users)
```

**Deliberately not built yet** (see `todo.md` for the full list): config classes (Dev/Prod/Testing), centralised error handlers, a second blueprint beyond `/health`.

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
