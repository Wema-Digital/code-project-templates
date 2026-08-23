# CLAUDE.md — machine-learning

This is the **Python Machine Learning template** of the `coding-project-templates` library. It lives on branch `py-ml` and is checked out as a git worktree at `features/machine-learning` within the root repo.

## Role of this template

`machine-learning` provides a starter scaffold for Python ML projects: data pipelines, model training, and experiment tracking. It extends the language-agnostic base (`claude-code-basic`, branch `claude-code-b`) with Python/ML-specific structure and dependencies.

## Stack

- **Language**: Python
- **Core libs**: scikit-learn, pandas, numpy
- **Experiment tracking**: (TBD — MLflow / simple logging)
- **Testing**: pytest
- **CI**: GitHub Actions

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | Language-agnostic task tracking template (from base) |
| `README.md` | Guide to using this template with Claude Code (from base) |
| `requirements.txt` | Python deps example — extend with ML-specific packages |
| `.claude/plan.md` | Base template plan (for reference) |
| `CLAUDE.md` | This file |

**Planned additions (Phase 5):**
- `requirements.txt` — updated with scikit-learn, numpy, matplotlib, jupyter
- `src/pipeline.py` — data loading + preprocessing skeleton
- `src/train.py` — model training entrypoint
- `notebooks/exploration.ipynb` — starter notebook
- `tests/` — pytest scaffold
- `.env.example`
- `.github/workflows/test.yml` — CI on push

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
