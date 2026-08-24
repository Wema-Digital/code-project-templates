# web-django — Django Project Starter Template

> The full-framework Python-web option in this library — for projects that want Django's ORM, admin, and auth, not just routing.
> Clone, install, and have a running Django app with tests and CI in minutes.

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

# 4. Apply migrations
python manage.py migrate

# 5. Start the dev server
python manage.py runserver

# 6. Verify it's running
curl http://localhost:8000/health/
# → {"status":"ok","pings":1}
```

---

## Project Layout

```
web-django/
├── config/
│   ├── settings.py     # DJANGO_SECRET_KEY / DJANGO_DEBUG read from env
│   ├── urls.py          # Root URLconf — includes core.urls, wires up /admin/
│   ├── wsgi.py
│   └── asgi.py
├── core/
│   ├── models.py        # Ping model (id, created_at)
│   ├── views.py         # GET /health/ — creates a Ping, returns the count
│   ├── urls.py
│   ├── admin.py          # Registers Ping with the admin site
│   └── migrations/
│       └── 0001_initial.py
├── tests/
│   └── test_views.py    # GET /health/ example test (pytest-django)
├── manage.py
├── pytest.ini            # Points pytest-django at config.settings
├── .env.example           # Environment variable template — copy to .env
├── .python-version        # Pinned Python version (3.12)
├── requirements.txt       # Runtime dependencies (Django, python-dotenv)
├── requirements-dev.txt   # Test tooling (pytest, pytest-django)
├── CLAUDE.md              # Claude Code context for this template
└── todo.md                # Task tracking template (symbol system)
```

---

## Why an ORM Model, Not Just a Route

Unlike `web-flask`, which stops at a `GET /health` route, `core.Ping` is a real model with a migration and an admin registration — the point of reaching for Django is the ORM/admin/auth stack, so the starter exercises all three: `GET /health/` writes a row via the ORM, and that row shows up in `/admin/` once you create a superuser.

```bash
python manage.py createsuperuser
# then visit http://localhost:8000/admin/
```

---

## Adding an App

```bash
python manage.py startapp <name>
```

Then:
1. Add `"<name>"` to `INSTALLED_APPS` in `config/settings.py`
2. Add `path("<name>/", include("<name>.urls"))` to `config/urls.py`
3. `python manage.py makemigrations <name>` after adding models

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DJANGO_SECRET_KEY` | `change-me` | Used for sessions/signing — replace before deploying |
| `DJANGO_DEBUG` | `True` | `True` \| `False` — never `True` in production |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | Reserved for wiring up Postgres later — not parsed yet, dev stays on SQLite |

Copy `.env.example` to `.env` and fill in values. Never commit `.env`.

---

## Testing

Tests use [pytest](https://docs.pytest.org/) + [pytest-django](https://pytest-django.readthedocs.io/). `pytest.ini` points it at `config.settings`; tests that touch the database need `@pytest.mark.django_db`.

```bash
python manage.py migrate --noinput   # CI also does this before testing
pytest                                # run the test suite
pytest -v                             # verbose output
```

```python
# tests/test_views.py
@pytest.mark.django_db
def test_health(client):
    res = client.get("/health/")
    assert res.status_code == 200
```

---

## Working with Claude Code

This template follows the same `todo.md` task-tracking convention as `claude-code-basic`.
See `todo.md` for the full symbol system and task breakdown.

Useful prompts to get started:
- *"Read todo.md and help me add a new app with a model, view, and test."*
- *"Split config/settings.py into base/dev/prod settings modules."*
- *"Wire DATABASE_URL into DATABASES with dj-database-url for Postgres."*

---

**Template Version**: 1.0
**Last Updated**: 2026-08-24
**Branch**: `py-django` | **Stack**: Python 3.12 + Django 5.2 LTS + pytest-django
