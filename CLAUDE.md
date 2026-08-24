# CLAUDE.md — machine-learning

This is the **Python Machine Learning template** of the `coding-project-templates` library. It lives on branch `py-ml` and is checked out as a git worktree at `features/machine-learning` within the root repo.

## Role of this template

`machine-learning` provides a starter scaffold for Python ML projects: data pipelines, model training, and experiment tracking. It extends the language-agnostic base (`claude-code-basic`, branch `claude-code-b`) with Python/ML-specific structure and dependencies.

## Stack

- **Language**: Python 3.12
- **Core libs**: scikit-learn, pandas, numpy, matplotlib — all pinned exactly in `requirements.txt` (see below)
- **Experiment tracking**: none yet — noted in `todo.md` as optional/advanced, add when there's more than one run to compare
- **Testing**: pytest
- **CI**: GitHub Actions

## Where data/models/notebooks live

**Don't commit large files.** `.gitignore` already excludes `data/`, `models/`, `*.png`, `*.csv`, and `.ipynb_checkpoints/`. The pipeline currently runs against scikit-learn's built-in `iris` dataset specifically so the template needs zero data setup — once you swap in real data, put it under `data/` (gitignored) or point `load_data()` at wherever it actually lives (a warehouse table, S3, an API).

## Project layout

```
src/
  __init__.py
  pipeline.py     ← load_data() → prepare_features() → train_model() → evaluate_model()
                     + run_pipeline() (wires them together)
                     + plot_results() (optional matplotlib chart, --plot flag)
tests/
  test_pipeline.py ← prepare_features() determinism/size tests + one run_pipeline() smoke test
.github/
  workflows/
    test.yml        ← CI: pip install (both requirement files) + pytest
```

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | ML-pipeline-specific task tracking template |
| `README.md` | Guide to using this template with Claude Code |
| `requirements.txt` | Runtime deps, pinned exactly (`==`, not `>=`) — reproducibility matters more here than in the other templates |
| `requirements-dev.txt` | Test deps (`pytest`) — installs runtime deps too via `-r requirements.txt` |
| `.claude/plan.md` | Phase 5 plan for this template, and what was deliberately deferred |
| `CLAUDE.md` | This file |

## Key patterns

**Each pipeline stage is a plain function** — `load_data()`, `prepare_features()`, `train_model()`, `evaluate_model()`. `run_pipeline()` composes them. This is what makes `prepare_features()` testable in isolation: same `(X, y)` + `random_state` always produces the same split, so the test asserts on that determinism rather than on model output (which is allowed to change as the model/data changes).

**Test the deterministic step, not the training run** — training/evaluation results are expected to shift as the model or data changes; the train/test split shouldn't. `tests/test_pipeline.py` reflects that split in intent, plus one smoke test that just proves `run_pipeline()` runs end to end.

**Deliberately not built yet** (see `todo.md` for the full list): a real data source (still the `iris` toy dataset), experiment tracking, metrics beyond accuracy, a `notebooks/` directory (the earlier draft of this file mentioned one; the actual Phase 5 spec doesn't call for it, so it wasn't shipped unused).

## Repo conventions (from root CLAUDE.md)

- **Commits** on this branch: `phase 5 intermediate: <what changed>` or `feat: <what changed>`
- **Push** to `origin py-ml` from inside this worktree
- **Planning notes** live in the root repo's `claude/` folder (numbered `N-Title.md`), not here
- **GitHub Project**: [Wema-Digital/projects/2](https://github.com/orgs/Wema-Digital/projects/2) — mark tasks Done after committing

## Receiving base updates

When `claude-code-basic` is updated, merge changes into this branch:

```bash
cd features/machine-learning   # branch py-ml
git merge claude-code-b
git push origin py-ml
```
