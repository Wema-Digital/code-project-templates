# Todo — web-django

> Django project tasks. Uses the same symbol system as the base template.
> See the Symbol Guide below for reference.

## Symbol Guide

| Symbol | Meaning | When to use with Claude |
|--------|---------|-------------------------|
| `[ ]` | Unstarted | Default for all new tasks |
| `[x]` | Completed | Ask Claude to mark tasks done |
| `[-]` | In-progress | Claude marks what it's actively working on |
| `[!]` | High priority | Focus here first |
| `[@]` | Needs discussion | Ask Claude for design input |
| `[?]` | Needs research | Have Claude research options |
| `[#]` | Medium priority | After `[!]` tasks |
| `[~]` | On hold | Skip for now |
| `[>]` | Delegated/deferred | Assigned elsewhere or future |
| `[⚠]` | Critical issue | Urgent bug or blocker |
| `[%]` | % complete | Track large in-progress features |

---

## Project Setup

```markdown
- [x] [!] Initialise git repository and branch (py-django)
- [x] [!] django-admin startproject config . (Django 5.2 LTS)
- [x] [!] Create requirements.txt (Django, python-dotenv) + requirements-dev.txt (pytest, pytest-django)
- [x] [!] Pin Python version in .python-version (3.12)
- [x] Configure .env.example (DJANGO_SECRET_KEY, DJANGO_DEBUG, DATABASE_URL)
- [ ] [@] Decide on app-split strategy once a second app is needed (apps/ package vs. flat)
```

---

## Project / App Structure

```markdown
- [x] [!] config/ — settings.py, urls.py, wsgi.py, asgi.py
- [x] [!] core app — Ping model, GET /health/ view, urls.py, admin.py
- [x] [!] core/migrations/0001_initial.py — generated via makemigrations
- [ ] [!] Settings split into config/settings/{base,dev,prod}.py — a single settings.py is enough for now
- [ ] [#] Custom user model (only if auth requirements need one — must be done before first migrate on a real project)
- [ ] [ ] Add your first real app beyond core:
  - [ ] Model(s) + makemigrations
  - [ ] Admin registration
  - [ ] Views + urls.py
  - [ ] Wire into config/urls.py via include()
- [ ] [~] Django REST Framework, if the project needs an API rather than server-rendered views
```

---

## Configuration & Environment

```markdown
- [x] [!] Load env vars with python-dotenv in settings.py (DJANGO_SECRET_KEY, DJANGO_DEBUG)
- [ ] [!] Wire DATABASE_URL into DATABASES once Postgres is needed (dj-database-url or django-environ)
- [ ] [@] Decide on secrets strategy (env vars vs. a secrets manager) before deploying
- [ ] [ ] Document all required env vars in .env.example as they're added
```

---

## Testing

```markdown
- [x] [!] Setup pytest + pytest-django (pytest.ini → DJANGO_SETTINGS_MODULE=config.settings)
- [x] [!] tests/test_views.py — GET /health/ passing test (@pytest.mark.django_db)
- [ ] [!] Write tests for each new model/view added above
- [ ] [#] Test admin registration (staff-only access, list display)
- [ ] [% 0] Reach 80% test coverage
- [ ] [@] Discuss integration vs. unit test split strategy
```

**Claude Code for testing:**
```markdown
- [ ] [!] Ask Claude to generate tests for any new model/view added above
- [ ] [#] Have Claude review test coverage report and suggest gaps
```

---

## CI / Deployment

```markdown
- [x] [!] .github/workflows/test.yml — installs requirements + requirements-dev, runs migrate then pytest
- [ ] [#] Add lint step to CI (ruff or flake8)
- [ ] [@] Choose hosting platform + Postgres provider (Railway, Render, Fly.io, AWS RDS, etc.)
- [ ] [ ] Add deployment workflow (collectstatic, migrate, gunicorn)
- [ ] [~] Dockerise (Dockerfile + .dockerignore)
- [ ] [>] Setup staging environment
```

---

## Code Quality

```markdown
- [ ] [#] Configure ruff (lint + format)
- [ ] [~] Add pre-commit hooks
- [ ] [ ] Add docstrings to public functions
```

---

## Metadata

*Last Updated: 2026-08-24*
*Template Version: 1.0*
*Stack: Python 3.12 + Django 5.2 LTS + pytest + pytest-django*
