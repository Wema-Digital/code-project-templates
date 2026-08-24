# Todo — web-flask

> Flask app-factory project tasks. Uses the same symbol system as the base template.
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
- [x] [!] Initialise git repository and branch (py-flask)
- [x] [!] Create requirements.txt (Flask, python-dotenv) + requirements-dev.txt (pytest, pytest-flask)
- [x] [!] Pin Python version in .python-version (3.12)
- [x] Configure .env.example (FLASK_APP, FLASK_ENV, SECRET_KEY)
- [ ] [@] Decide on folder structure once a second blueprint is added (flat vs. feature-based)
```

---

## App Factory & Blueprints

```markdown
- [x] [!] app/__init__.py — create_app() factory
- [x] [!] app/routes.py — main blueprint, GET /health
- [x] [!] run.py — entry point, loads .env, calls create_app()
- [ ] [!] Centralised error handlers (404, 500 → JSON responses)
- [ ] [#] app/config.py — Dev/Prod/Testing config classes, pass config name into create_app()
- [ ] [@] Decide on API versioning strategy (/api/v1/...) once real routes exist
- [ ] [ ] Add your first real resource blueprint:
  - [ ] GET    /api/v1/<resource>      — list
  - [ ] POST   /api/v1/<resource>      — create
  - [ ] GET    /api/v1/<resource>/:id  — get one
  - [ ] PUT    /api/v1/<resource>/:id  — update
  - [ ] DELETE /api/v1/<resource>/:id  — delete
- [ ] [~] Database layer (Flask-SQLAlchemy) — only if the project actually needs persistence
```

---

## Configuration & Environment

```markdown
- [x] [!] Load env vars with python-dotenv in run.py
- [ ] [#] Config classes read from process env (see App Factory section)
- [ ] [@] Decide on secrets strategy (env vars vs. a secrets manager) before deploying
- [ ] [ ] Document all required env vars in .env.example as they're added
```

---

## Testing

```markdown
- [x] [!] Setup pytest + pytest-flask
- [x] [!] tests/conftest.py — app fixture
- [x] [!] tests/test_app.py — GET /health passing test
- [ ] [!] Write tests for each new route (happy path + error cases)
- [ ] [#] Test error handlers (404/500)
- [ ] [% 0] Reach 80% test coverage
- [ ] [@] Discuss integration vs. unit test split strategy
```

**Claude Code for testing:**
```markdown
- [ ] [!] Ask Claude to generate tests for any new route added above
- [ ] [#] Have Claude review test coverage report and suggest gaps
```

---

## CI / Deployment

```markdown
- [x] [!] .github/workflows/test.yml — installs requirements + requirements-dev, runs pytest
- [ ] [#] Add lint step to CI (ruff or flake8)
- [ ] [@] Choose hosting platform (Railway, Render, Fly.io, AWS, etc.)
- [ ] [ ] Add deployment workflow
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
*Stack: Python 3.12 + Flask 3 + pytest + pytest-flask*
