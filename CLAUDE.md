# CLAUDE.md — web-django

This is the **Django web application template** of the `coding-project-templates` library. It lives on branch `py-django` and is checked out as a git worktree at `features/web-django` within the root repo.

## Role of this template

`web-django` provides a starter scaffold for Python web applications built with Django. It extends the language-agnostic base (`claude-code-basic`, branch `claude-code-b`) with a Django project structure, settings pattern, and testing setup.

## Stack

- **Language**: Python 3.12
- **Framework**: Django 5.2 LTS
- **Database**: SQLite (dev). Postgres is not wired up — `DATABASE_URL` is documented in `.env.example` but unused until a project needs it.
- **Testing**: pytest + pytest-django
- **CI**: GitHub Actions

## Project layout

```
config/
  settings.py   ← DJANGO_SECRET_KEY / DJANGO_DEBUG read from env via python-dotenv
  urls.py       ← Root URLconf — includes core.urls, wires up /admin/
  wsgi.py / asgi.py
core/
  models.py     ← Ping model (id, created_at)
  views.py      ← GET /health/ — creates a Ping row, returns the running count
  urls.py
  admin.py      ← Registers Ping with the admin site
  migrations/
    0001_initial.py
tests/
  test_views.py ← @pytest.mark.django_db test on GET /health/
manage.py
pytest.ini      ← DJANGO_SETTINGS_MODULE = config.settings
.github/
  workflows/
    test.yml    ← CI: pip install (both requirement files) + migrate + pytest
```

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | Django-specific task tracking template |
| `README.md` | Guide to using this template with Claude Code |
| `requirements.txt` | Runtime deps (Django, python-dotenv) |
| `requirements-dev.txt` | Test deps (pytest, pytest-django) — installs runtime deps too via `-r requirements.txt` |
| `.env.example` | `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DATABASE_URL` |
| `.claude/plan.md` | Phase 5 plan for this template, and what was deliberately deferred |
| `CLAUDE.md` | This file |

## Key patterns

**Adding an app**:
```bash
python manage.py startapp <name>
```
Then add `"<name>"` to `INSTALLED_APPS` in `config/settings.py`, wire its URLs into `config/urls.py` via `include()`, and run `python manage.py makemigrations <name>` after adding models.

**Why `core.Ping` is a real model, not just a route** — the point of reaching for Django over `web-flask` is the ORM/admin/auth stack, so `GET /health/` writes through the ORM instead of just returning a static JSON blob. `python manage.py createsuperuser` + `/admin/` shows the rows it creates.

**Deliberately not built yet** (see `todo.md` for the full list): settings split into base/dev/prod modules, Postgres wiring via `DATABASE_URL`, a second app beyond `core`, a custom user model, DRF.

## Repo conventions (from root CLAUDE.md)

- **Commits** on this branch: `phase 5 intermediate: <what changed>` or `feat: <what changed>`
- **Push** to `origin py-django` from inside this worktree
- **Planning notes** live in the root repo's `claude/` folder (numbered `N-Title.md`), not here
- **GitHub Project**: [Wema-Digital/projects/2](https://github.com/orgs/Wema-Digital/projects/2) — mark tasks Done after committing

## Receiving base updates

When `claude-code-basic` is updated, merge changes into this branch:

```bash
cd features/web-django   # branch py-django
git merge claude-code-b
git push origin py-django
```
