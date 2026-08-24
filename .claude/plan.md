> **Status**: Executed 2026-08-24 (Phase 5 — Intermediate Templates). Supersedes the base-template plan below, which was scoped to the generic `claude-code-basic` stub this template started from.

## Context

`web-django` was carrying the language-agnostic base template verbatim (generic `todo.md`, generic `README.md`, a `requirements.txt` with `pandas` in it). The GitHub Project task "Bring web-django to intermediate" (Phase 5) calls for turning it into an actual runnable Django project, per `claude/5-Phase 5 Detailed Breakdown.md`.

## Goal

Real `django-admin startproject` output, plus one app (`core`) with a model, a view, and a test, plus CI — the full-framework counterpart to `web-flask`'s app-factory scaffold, but exercising the ORM/admin that's the whole reason to reach for Django over Flask.

## What was built

- `manage.py`, `config/{settings,urls,wsgi,asgi}.py` — real `django-admin startproject config .` output (Django 5.2 LTS), with `settings.py` adapted to read `DJANGO_SECRET_KEY`/`DJANGO_DEBUG` from the environment via `python-dotenv` instead of hardcoding them
- `core/` app — `Ping` model (id + `created_at`), `GET /health/` view that creates a `Ping` row and returns the running count, `core/urls.py`, `core/admin.py` (registers `Ping`)
- `core/migrations/0001_initial.py` — generated via `manage.py makemigrations core`
- `pytest.ini` — points pytest-django at `config.settings`
- `tests/test_views.py` — one `@pytest.mark.django_db` test on `GET /health/`
- `requirements.txt` (`Django>=5.2,<5.3`, `python-dotenv`) / `requirements-dev.txt` (`pytest`, `pytest-django`) — split runtime vs. test deps, matching `web-flask`
- `.env.example` — `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DATABASE_URL`
- `.github/workflows/test.yml` — installs both requirement files, runs `manage.py migrate` then `pytest`
- `README.md`, `todo.md`, `CLAUDE.md` — rewritten Django-specific (replacing the generic base-template copies)

## Deliberately deferred (left as `todo.md` items, not built now)

- Settings split into `base.py`/`dev.py`/`prod.py` — a single `config/settings.py` is enough for "intermediate"
- Postgres wiring — `DATABASE_URL` is documented in `.env.example` but not parsed; dev stays on SQLite
- A second app / real resource routes beyond `core`
- Custom user model, auth views, DRF — out of scope for this pass

## Verification

- `manage.py migrate --noinput` applies all migrations (including `core.0001_initial`) cleanly against a fresh SQLite DB
- `manage.py check` reports no issues
- `pytest` passes (1 test) from a clean `uv`-managed venv against `requirements.txt` + `requirements-dev.txt`
