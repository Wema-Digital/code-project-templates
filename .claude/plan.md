> **Status**: Executed 2026-08-24 (Phase 5 — Intermediate Templates). Supersedes the base-template plan below, which was scoped to the generic `claude-code-basic` stub this template started from.

## Context

`machine-learning` was carrying the language-agnostic base template verbatim (generic `todo.md`, generic `README.md`, a `requirements.txt` with just `pandas`/`pytest`/`python-dotenv`). The GitHub Project task "Bring machine-learning to intermediate" (Phase 5) calls for a minimal, runnable pipeline example that proves the scaffold works end to end, per `claude/5-Phase 5 Detailed Breakdown.md`.

## Goal

`src/pipeline.py`: load → prepare → train → evaluate, against a small built-in dataset (no external data file needed), plus a test on the deterministic data-prep step, plus CI.

## What was built

- `src/pipeline.py` — `load_data()` (sklearn's `iris` toy dataset), `prepare_features()` (deterministic train/test split, `random_state=42`), `train_model()` (`LogisticRegression`), `evaluate_model()` (accuracy), `run_pipeline()` wiring them together, plus an optional `plot_results()` (matplotlib, `Agg` backend so it works headless in CI) behind a `--plot` CLI flag
- `src/__init__.py` — makes `src/` importable so tests can do `from src.pipeline import ...`
- `tests/test_pipeline.py` — two tests on `prepare_features()` (determinism + split sizes, per spec: test the deterministic step, not a full training run) plus one end-to-end smoke test on `run_pipeline()` — since the task title itself frames the point as proving the scaffold works end to end
- `requirements.txt` — pinned exactly (`pandas==3.0.3`, `scikit-learn==1.8.0`, `numpy==2.4.4`, `matplotlib==3.10.9`), per the breakdown's suggestion that ML reproducibility depends on exact versions more than the other templates
- `requirements-dev.txt` — `pytest==9.0.3`
- `.github/workflows/test.yml` — installs both requirement files, runs `pytest`
- `.gitignore` — added `data/`, `models/`, `*.png`, `*.csv`, `.ipynb_checkpoints/` — never commit generated data/model/plot artifacts
- `README.md`, `todo.md`, `CLAUDE.md` — rewritten ML-pipeline-specific (replacing the generic base-template copies)

## Deliberately deferred (left as `todo.md` items, not built now)

- Experiment tracking (MLflow or similar) — explicitly called out in the breakdown as optional/advanced, not required for "intermediate"
- `notebooks/` — the stale `CLAUDE.md` mentioned a starter notebook; the actual breakdown spec doesn't ask for one, so it's dropped rather than shipped unused
- `.env.example` — no data source path needs configuring yet; the pipeline uses a built-in dataset
- A real external data source — swapping `load_data()` for one is a `todo.md` item, deliberately not built so the template stays runnable with zero setup

## Verification

- `pytest` passes (3 tests) from a clean `uv`-managed venv against `requirements.txt` + `requirements-dev.txt`
- `python src/pipeline.py --plot metrics.png` runs end-to-end and writes a real PNG (accuracy ~0.97 on this split)
