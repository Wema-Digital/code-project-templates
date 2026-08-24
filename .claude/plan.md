> **Status**: Executed 2026-08-24 (Phase 5 — Intermediate Templates). Supersedes the base-template plan below, which was scoped to the generic `claude-code-basic` stub this template started from.

## Context

`web-flask` was carrying the language-agnostic base template verbatim (generic `todo.md`, generic `README.md`, a `requirements.txt` with `pandas` in it). The GitHub Project task "Bring web-flask to intermediate" (Phase 5) calls for turning it into an actual runnable Flask app-factory starter, per `claude/5-Phase 5 Detailed Breakdown.md`.

## Goal

Minimum viable Flask scaffold: one app factory, one blueprint, one route, one test, CI — mirroring the shape already delivered for `js-express` (Phase 1/4).

## What was built

- `app/__init__.py` — `create_app()` factory, registers the `main` blueprint
- `app/routes.py` — `main` blueprint with `GET /health`
- `run.py` — entry point; loads `.env`, calls `create_app()`
- `tests/conftest.py` — `app` fixture for `pytest-flask`
- `tests/test_app.py` — one passing test on `GET /health`
- `requirements.txt` / `requirements-dev.txt` — split runtime vs. test deps
- `.env.example` — `FLASK_APP`, `FLASK_ENV`, `SECRET_KEY`
- `.github/workflows/test.yml` — installs both requirement files, runs `pytest`
- `README.md`, `todo.md`, `CLAUDE.md` — rewritten Flask-specific (replacing the generic base-template copies)

## Deliberately deferred (left as `todo.md` items, not built now)

- Config classes (`Dev`/`Prod`/`Testing`) — `create_app()` takes no args yet
- Centralised error handlers (404/500 JSON responses)
- A second blueprint / real resource routes beyond `/health`
- Database layer — out of scope; `web-flask` stays deliberately simpler than `web-django`

## Verification

- `pytest` passes (1 test) from a clean `uv`-managed venv against `requirements.txt` + `requirements-dev.txt`
- `create_app().test_client().get('/health')` → `200 {"status": "ok"}`
