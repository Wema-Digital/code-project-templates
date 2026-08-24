> **Status**: Executed 2026-08-24 (Phase 5 — Intermediate Templates). Supersedes the base-template plan below, which was scoped to the generic `claude-code-basic` stub this template started from.

## Context

`python-app` was carrying the language-agnostic base template verbatim (generic `todo.md`, generic `README.md`, a `requirements.txt` with `pandas` in it). The GitHub Project task "Bring python-app to intermediate" (Phase 5) calls for turning it into an actual runnable Python application skeleton — structure without committing to a web framework — per `claude/5-Phase 5 Detailed Breakdown.md`.

## Goal

`src/` layout, one CLI command, one test file, CI — the "no framework" counterpart to `web-flask`/`web-django`.

## What was built

- `pyproject.toml` — replaces `requirements.txt` per the breakdown's suggested improvement, matching the root repo's own `uv`-managed convention. `[project.scripts]` registers an `app` console script; `[project.optional-dependencies].dev` holds `pytest`
- `src/app/__init__.py`, `src/app/main.py` — `greet()` (pure, testable) + `build_parser()`/`main()` (argparse CLI wrapper); stdlib `argparse` chosen over `click` to keep the "no framework" template dependency-free at runtime
- `tests/test_main.py` — three tests: `greet()` directly, and `main()` via `capsys` (default arg + explicit arg)
- `.github/workflows/test.yml` — `pip install -e ".[dev]"`, then `pytest`
- `README.md`, `todo.md`, `CLAUDE.md` — rewritten Python-app-specific (replacing the generic base-template copies)

## Deliberately deferred (left as `todo.md` items, not built now)

- `.env.example` / `python-dotenv` config loading — the breakdown says only add this if the app genuinely needs config; the CLI entrypoint doesn't yet, so it's skipped rather than shipping an empty file
- `src/app/config.py` — same reasoning; add it when a real config need shows up
- Logging setup — noted in `todo.md`, not wired in for a one-command CLI
- Packaging/publishing (PyPI) — out of scope for "intermediate"

## Verification

- `pip install -e ".[dev]"` succeeds (editable install builds cleanly via setuptools `src` layout)
- `pytest` passes (3 tests) from a clean `uv`-managed venv
- The installed `app` console script runs: `app` → `Hello, world!`, `app Claude` → `Hello, Claude!`
