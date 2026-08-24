# CLAUDE.md — python-scripts

This is the **Python utility scripts template** of the `coding-project-templates` library. It lives on branch `py-script` and is checked out as a git worktree at `features/python-scripts` within the root repo.

## Role of this template

`python-scripts` provides a starter scaffold for collections of standalone Python utility scripts — automation, data processing, CLI one-offs, and scheduled tasks. It extends the language-agnostic base (`claude-code-basic`, branch `claude-code-b`) with a lightweight Python structure suited to script-first projects rather than full applications.

## Stack

- **Language**: Python 3.12
- **CLI parsing**: `argparse` (stdlib) — no runtime deps beyond `pandas`/`python-dotenv`
- **Testing**: pytest
- **CI**: GitHub Actions (`pytest` only — this is a Python collection, not shell scripts; don't confuse with `wsl-scripts`, which uses `shellcheck`)

Each script here is standalone and runnable on its own. This template is deliberately **not** a packaged app — there's no `pyproject.toml`, no installable package, no shared entrypoint. If a project's script grows into something that needs to be imported elsewhere or installed, that's a sign to move it to `python-app` instead.

## Project layout

```
scripts/
  __init__.py       ← makes scripts/ importable, so tests can do
                       `from scripts.csv_report import summarize_csv`
  csv_report.py     ← example script: summarize_csv() (pure) + argparse CLI wrapper
tests/
  test_csv_report.py ← tests summarize_csv() directly, not the CLI
.github/
  workflows/
    test.yml         ← CI: pip install (both requirement files) + pytest
```

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | Python-scripts-specific task tracking template |
| `README.md` | Guide to using this template with Claude Code |
| `requirements.txt` | Shared runtime deps (`pandas`, `python-dotenv`) — a script needing more documents that inline at its own top |
| `requirements-dev.txt` | Test deps (`pytest`) — installs runtime deps too via `-r requirements.txt` |
| `.claude/plan.md` | Phase 5 plan for this template, and what was deliberately deferred |
| `CLAUDE.md` | This file |

## Key patterns

**Adding a new script** — one file in `scripts/`, following `csv_report.py`'s shape: a pure core function (the thing that gets tested) plus a thin `argparse` wrapper in `main()`. Use `logging.getLogger(__name__)` inside the script, not bare `print()`, except for the script's actual output.

```python
def do_the_thing(path: str) -> dict:
    ...  # pure logic — tested directly, no argparse/stdout involved

def main(argv=None) -> None:
    logging.basicConfig(level=logging.INFO)
    args = build_parser().parse_args(argv)
    print(do_the_thing(args.input))
```

**Testing** — one test file per script (`tests/test_<script>.py`), importing the core function directly (`from scripts.csv_report import summarize_csv`) and testing it against a `tmp_path` fixture, not the CLI wrapper.

**Deliberately not built yet** (see `todo.md` for the full list): `.env.example` (no script needs config yet), a shared helpers module (add once two scripts duplicate logic, not before), a second example script.

## Repo conventions (from root CLAUDE.md)

- **Commits** on this branch: `phase 5 intermediate: <what changed>` or `feat: <what changed>`
- **Push** to `origin py-script` from inside this worktree
- **Planning notes** live in the root repo's `claude/` folder (numbered `N-Title.md`), not here
- **GitHub Project**: [Wema-Digital/projects/2](https://github.com/orgs/Wema-Digital/projects/2) — mark tasks Done after committing

## Receiving base updates

When `claude-code-basic` is updated, merge changes into this branch:

```bash
cd features/python-scripts   # branch py-script
git merge claude-code-b
git push origin py-script
```
