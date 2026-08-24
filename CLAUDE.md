# CLAUDE.md — python-app

This is the **Python application template** of the `coding-project-templates` library. It lives on branch `py-app` and is checked out as a git worktree at `features/python-app` within the root repo.

## Role of this template

`python-app` provides a starter scaffold for general-purpose Python applications with a clean entrypoint, configuration management, and test suite. It extends the language-agnostic base (`claude-code-basic`, branch `claude-code-b`) with Python-specific structure and tooling.

## Stack

- **Language**: Python 3.12
- **No framework**: this is the "structure without a web framework" template — a CLI entrypoint, not a server. Reach for `web-flask`/`web-django` instead if the project needs to serve HTTP.
- **Entry point**: `src/app/main.py`, installed as the `app` console script via `pyproject.toml`'s `[project.scripts]`
- **CLI**: stdlib `argparse` — no runtime dependencies. `click` is an open decision in `todo.md` if the CLI surface grows.
- **Testing**: pytest
- **CI**: GitHub Actions

No `.env.example` / `python-dotenv` — the CLI doesn't need config yet. Add config loading only when there's something real to configure (see `todo.md`).

## Project layout

```
src/
  app/
    __init__.py
    main.py    ← greet() (pure, testable) + build_parser()/main() (argparse CLI wrapper)
tests/
  test_main.py ← greet() direct test + main() tests via capsys
.github/
  workflows/
    test.yml   ← CI: pip install -e ".[dev]" + pytest
pyproject.toml  ← project metadata, [project.scripts] entrypoint, [project.optional-dependencies].dev
```

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | Python-app-specific task tracking template |
| `README.md` | Guide to using this template with Claude Code |
| `pyproject.toml` | Project metadata + deps (replaces `requirements.txt` — matches the root repo's own `uv` convention) |
| `.claude/plan.md` | Phase 5 plan for this template, and what was deliberately deferred |
| `CLAUDE.md` | This file |

## Key patterns

**src/ layout, not flat** — `src/app/` forces the package to be installed (`pip install -e .`) rather than accidentally importable from the working directory. This is why `pyproject.toml` has `[tool.setuptools.packages.find] where = ["src"]`.

**Pure logic + thin CLI wrapper** — keep business logic in plain functions (`greet()`), and keep `main()` as an `argparse` wrapper that calls them. This is what makes the logic testable without shelling out; test `main()` itself via `capsys` to cover the wiring.

```python
def test_main_prints_greeting(capsys):
    main(["Ada"])
    assert capsys.readouterr().out.strip() == "Hello, Ada!"
```

**Deliberately not built yet** (see `todo.md` for the full list): config loading (`.env.example` / `python-dotenv`), a `config.py`, logging setup, subcommands beyond the one CLI argument.

## Repo conventions (from root CLAUDE.md)

- **Commits** on this branch: `phase 5 intermediate: <what changed>` or `feat: <what changed>`
- **Push** to `origin py-app` from inside this worktree
- **Planning notes** live in the root repo's `claude/` folder (numbered `N-Title.md`), not here
- **GitHub Project**: [Wema-Digital/projects/2](https://github.com/orgs/Wema-Digital/projects/2) — mark tasks Done after committing

## Receiving base updates

When `claude-code-basic` is updated, merge changes into this branch:

```bash
cd features/python-app   # branch py-app
git merge claude-code-b
git push origin py-app
```
