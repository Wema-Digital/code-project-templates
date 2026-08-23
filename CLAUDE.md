# CLAUDE.md — web-django

This is the **Django web application template** of the `coding-project-templates` library. It lives on branch `py-django` and is checked out as a git worktree at `features/web-django` within the root repo.

## Role of this template

`web-django` provides a starter scaffold for Python web applications built with Django. It extends the language-agnostic base (`claude-code-basic`, branch `claude-code-b`) with a Django project structure, settings pattern, and testing setup.

## Stack

- **Language**: Python
- **Framework**: Django
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Testing**: pytest + pytest-django
- **Linting**: Ruff
- **CI**: GitHub Actions

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | Language-agnostic task tracking template (from base) |
| `README.md` | Guide to using this template with Claude Code (from base) |
| `requirements.txt` | Python deps example — extend with Django + db packages |
| `.claude/plan.md` | Base template plan (for reference) |
| `CLAUDE.md` | This file |

**Planned additions (Phase 5):**
- `manage.py` — Django management entrypoint
- `config/settings/` — split settings (base, dev, prod)
- `config/urls.py` — root URL configuration
- `apps/core/` — starter Django app with a health-check view
- `tests/test_views.py` — pytest-django scaffold with one passing test
- `.env.example` — `SECRET_KEY`, `DATABASE_URL`, `DEBUG`
- `requirements.txt` — updated with `django`, `psycopg2-binary`, `pytest-django`
- `.github/workflows/test.yml` — CI on push

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
