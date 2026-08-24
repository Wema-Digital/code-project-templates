> **Status**: Executed 2026-08-24 (Phase 5 — Intermediate Templates). Supersedes the base-template plan below, which was scoped to the generic `claude-code-basic` stub this template started from.

## Context

`python-scripts` was carrying the language-agnostic base template verbatim (generic `todo.md`, generic `README.md`). The GitHub Project task "Bring python-scripts to intermediate" (Phase 5) calls for one real example script, a test on its core function, and CI — per `claude/5-Phase 5 Detailed Breakdown.md`.

## Goal

One genuinely useful example script (a report/export utility), with its core logic isolated from its CLI wrapper so it's testable, plus CI. This template stays deliberately un-packaged — a loose collection of scripts, not an installable app (that's what `python-app` is for).

## What was built

- `scripts/csv_report.py` — `summarize_csv(path) -> dict` (pure, testable core: row count + per-column stats via pandas) and a thin `argparse` CLI wrapper (`main()`) with stdlib `logging`
- `scripts/__init__.py` — makes `scripts/` importable so tests can do `from scripts.csv_report import summarize_csv` without packaging the whole repo
- `tests/test_csv_report.py` — one test on `summarize_csv()` against a small fixture CSV (`tmp_path`), not on the CLI wrapper
- `requirements.txt` (pandas, python-dotenv — kept as shared deps per the breakdown) / `requirements-dev.txt` (pytest), split runtime vs. test deps
- `.github/workflows/test.yml` — installs both requirement files, runs `pytest`
- `README.md`, `todo.md`, `CLAUDE.md` — rewritten Python-scripts-specific (replacing the generic base-template copies, and fixing a stale `CLAUDE.md` line that mentioned `shellcheck` — copy-paste leakage from the `wsl-scripts` template, not relevant here)

## Deliberately deferred (left as `todo.md` items, not built now)

- `.env.example` / `python-dotenv` usage — `python-dotenv` stays in `requirements.txt` as a shared dep per the breakdown, but `csv_report.py` doesn't need config, so no `.env.example` ships; add one when a script actually needs it
- A second example script — one is enough to establish the convention
- Packaging (`pyproject.toml`) — explicitly out of scope; see `python-app` if a script grows into a real application

## Verification

- `pytest` passes (1 test) from a clean `uv`-managed venv against `requirements.txt` + `requirements-dev.txt`
- `python scripts/csv_report.py --input <csv>` runs end-to-end and prints a correct JSON summary
