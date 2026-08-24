# Todo — machine-learning

> ML pipeline project tasks. Uses the same symbol system as the base template.
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
- [x] [!] Initialise git repository and branch (py-ml)
- [x] [!] Create requirements.txt (pandas, scikit-learn, numpy, matplotlib), pinned tightly
- [x] [!] Create requirements-dev.txt (pytest)
- [x] [!] Pin Python version in .python-version (3.12)
- [x] [!] .gitignore: data/, models/, *.png, *.csv, .ipynb_checkpoints/
- [ ] [@] Decide where real data will live once load_data() stops using the toy dataset (data/ dir, S3, a warehouse table)
```

---

## Pipeline

```markdown
- [x] [!] src/pipeline.py — load_data() → prepare_features() → train_model() → evaluate_model()
- [x] [!] run_pipeline() — wires the four steps together end to end
- [x] [#] plot_results() — optional matplotlib bar chart, behind --plot (headless-safe: Agg backend)
- [ ] [!] Swap load_data() for a real data source (CSV, database, API) when you have one
- [ ] [#] Feature engineering beyond the raw iris columns, once real data has more to prepare
- [ ] [@] Decide on the model: LogisticRegression is a placeholder — pick a real one once there's a real problem
- [ ] [?] Research whether the toy dataset's stratified split is still the right validation strategy for real data (k-fold? time-based split?)
```

---

## Metrics & Experiment Tracking

```markdown
- [x] [!] evaluate_model() — accuracy, the simplest metric that proves the loop works
- [ ] [#] Add metrics beyond accuracy (precision/recall/F1, or a regression metric if the problem changes)
- [ ] [~] Experiment tracking (MLflow or similar) — optional/advanced, not required for "intermediate"; add once there's more than one model/run to compare
- [ ] [@] Decide on a baseline to compare future models against
```

---

## Testing

```markdown
- [x] [!] Setup pytest
- [x] [!] tests/test_pipeline.py — prepare_features() determinism + split-size tests (the deterministic step, per spec)
- [x] [#] One end-to-end smoke test on run_pipeline() — proves the scaffold works end to end
- [ ] [!] Test any new feature-engineering step the same way: deterministic, isolated from training
- [ ] [#] Test evaluate_model() directly once metrics beyond accuracy are added
- [ ] [% 0] Reach 80% test coverage
```

**Claude Code for testing:**
```markdown
- [ ] [!] Ask Claude to generate tests for any new pipeline step added above
- [ ] [#] Have Claude review test coverage report and suggest gaps
```

---

## CI / Deployment

```markdown
- [x] [!] .github/workflows/test.yml — installs requirements + requirements-dev, runs pytest
- [ ] [#] Add lint step to CI (ruff or flake8)
- [ ] [@] Decide on a deployment target once there's a model worth serving (batch job, API endpoint, scheduled retrain)
- [ ] [~] Dockerise, if the pipeline needs to run somewhere other than a dev machine
```

---

## Code Quality

```markdown
- [ ] [#] Configure ruff (lint + format)
- [ ] [~] Add pre-commit hooks
- [ ] [ ] Add docstrings to public functions as the pipeline grows past this scaffold
```

---

## Metadata

*Last Updated: 2026-08-24*
*Template Version: 1.0*
*Stack: Python 3.12 + scikit-learn + pandas + numpy + matplotlib + pytest*
