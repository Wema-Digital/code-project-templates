# machine-learning — Minimal ML Pipeline Skeleton

> A runnable load → prepare → train → evaluate pipeline, proven end to end against a small built-in dataset.
> Swap `load_data()` for a real data source when you have one — everything downstream just consumes `(X, y)` arrays.

---

## Quick Start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies (pinned tightly — see below)
pip install -r requirements.txt -r requirements-dev.txt

# 3. Run the pipeline
python src/pipeline.py
# → {'accuracy': 0.9666666666666667}

# 4. Optionally save a metrics chart
python src/pipeline.py --plot metrics.png
```

---

## What the Example Pipeline Demonstrates

`src/pipeline.py` runs against scikit-learn's built-in `iris` dataset — no external data file, no setup, no credentials. It exists to prove the scaffold works end to end, not to be a real model:

```
load_data()  →  prepare_features()  →  train_model()  →  evaluate_model()
   (X, y)      deterministic split      LogisticRegression      {"accuracy": ...}
```

Each step is a plain function. `run_pipeline()` wires them together. Nothing after `load_data()` knows or cares that the data came from `sklearn.datasets` — swap that one function for a real data source and the rest keeps working.

---

## Project Layout

```
machine-learning/
├── src/
│   ├── __init__.py
│   └── pipeline.py        # load → prepare → train → evaluate, + optional plot_results()
├── tests/
│   └── test_pipeline.py   # prepare_features() determinism/size tests + one end-to-end smoke test
├── requirements.txt         # Runtime deps, pinned exactly (pandas, scikit-learn, numpy, matplotlib)
├── requirements-dev.txt     # Test tooling (pytest)
├── .python-version           # Pinned Python version (3.12)
├── CLAUDE.md                 # Claude Code context for this template
└── todo.md                   # Task tracking template (symbol system)
```

---

## Swapping in Real Data

Replace `load_data()` — everything else in the pipeline is agnostic to where `(X, y)` came from:

```python
def load_data():
    df = pd.read_csv("data/my_dataset.csv")
    X = df.drop(columns=["target"]).to_numpy()
    y = df["target"].to_numpy()
    return X, y
```

`data/` is already in `.gitignore` — don't commit real datasets or trained models to git.

---

## Why Pinned Exact Versions

Unlike the other templates' `requirements.txt`, this one pins every version exactly (`==`, not `>=`). ML reproducibility depends on it more than most: a minor `scikit-learn` or `numpy` bump can silently change numeric results, not just break an API.

---

## Testing

```bash
pytest              # run the test suite
pytest -v           # verbose output
```

The tests target the **deterministic data-prep step**, not the full training run — training/evaluation *should* vary as the model or data changes, but the split shouldn't:

```python
# tests/test_pipeline.py
def test_prepare_features_is_deterministic():
    X, y = load_data()
    split_1 = prepare_features(X, y)
    split_2 = prepare_features(X, y)
    assert np.array_equal(split_1[0], split_2[0])
```

One additional smoke test runs the full pipeline and checks the result is a valid accuracy — proof the scaffold works end to end, not a claim about model quality.

---

## Working with Claude Code

This template follows the same `todo.md` task-tracking convention as `claude-code-basic`.
See `todo.md` for the full symbol system and task breakdown.

Useful prompts to get started:
- *"Read todo.md and help me swap load_data() for my real dataset."*
- *"Add precision/recall to evaluate_model() and update its test."*
- *"This project needs experiment tracking now — wire up MLflow."*

---

**Template Version**: 1.0
**Last Updated**: 2026-08-24
**Branch**: `py-ml` | **Stack**: Python 3.12 + scikit-learn + pandas + numpy + matplotlib + pytest
