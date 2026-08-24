# web-flask — Flask App-Factory Starter Template

> The lightweight Python-web option in this library, deliberately simpler than `web-django`.
> Clone, install, and have a running Flask app with tests and CI in minutes.

---

## Quick Start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# 3. Configure environment
cp .env.example .env

# 4. Start the dev server
flask run

# 5. Verify it's running
curl http://localhost:5000/health
# → {"status":"ok"}
```

---

## Project Layout

```
web-flask/
├── app/
│   ├── __init__.py     # create_app() factory — registers blueprints
│   └── routes.py       # main blueprint (GET /health)
├── tests/
│   ├── conftest.py     # pytest-flask `app` fixture
│   └── test_app.py     # GET /health example test
├── run.py                # Entry point — loads .env, calls create_app()
├── .env.example          # Environment variable template — copy to .env
├── .python-version       # Pinned Python version (3.12)
├── requirements.txt      # Runtime dependencies (Flask, python-dotenv)
├── requirements-dev.txt  # Test tooling (pytest, pytest-flask)
├── CLAUDE.md             # Claude Code context for this template
└── todo.md               # Task tracking template (symbol system)
```

---

## The App-Factory Pattern

`app/__init__.py` exposes `create_app()` instead of a module-level `app` object. This keeps the app importable without side effects — tests build a fresh instance per test via the `app` fixture in `tests/conftest.py`, rather than reusing global state.

```python
# app/__init__.py
def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")

    from app.routes import main
    app.register_blueprint(main)

    return app
```

---

## Adding Routes

Add new blueprints under `app/` and register them in `create_app()`:

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

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `FLASK_APP` | `run.py` | Entry point Flask's CLI looks for |
| `FLASK_ENV` | `development` | `development` \| `production` |
| `SECRET_KEY` | `change-me` | Used for sessions/signing — replace before deploying |

Copy `.env.example` to `.env` and fill in values. Never commit `.env`.

---

## Testing

Tests use [pytest](https://docs.pytest.org/) + [pytest-flask](https://pytest-flask.readthedocs.io/), which supplies the `client` fixture automatically once `tests/conftest.py` defines an `app` fixture.

```bash
pytest                 # run the test suite
pytest -v               # verbose output
```

```python
# tests/test_app.py
def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
```

---

## Working with Claude Code

This template follows the same `todo.md` task-tracking convention as `claude-code-basic`.
See `todo.md` for the full symbol system and task breakdown.

Useful prompts to get started:
- *"Read todo.md and help me add a new blueprint with tests."*
- *"Add config classes for dev/prod/testing and wire them into create_app()."*
- *"Add a 404/500 JSON error handler to the app factory."*

---

**Template Version**: 1.0
**Last Updated**: 2026-08-24
**Branch**: `py-flask` | **Stack**: Python 3.12 + Flask 3 + pytest
