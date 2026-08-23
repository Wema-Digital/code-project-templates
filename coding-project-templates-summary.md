# coding-project-templates — Repository Summary Report

*Generated: 2026-08-23*
*Repository root: `W:\vscode.workspaces\wema.digital.github\coding-project-templates`*
*Remote: https://github.com/Wema-Digital/code-project-templates.git*

## 1. Purpose

This repository is Wema.Digital's base VS Code / Claude Code project scaffold. Its job is to spin up a ready-to-use, multi-language VS Code workspace (`.vscode` + `ProjectSetup-linux-os.py`) and to hold a library of starter templates (`features/`) that can be used standalone or layered on top of the generic workspace when starting a new project or a new project component.

## 2. Root-level structure

| Item | Type | Role |
|---|---|---|
| `ProjectSetup-linux-os.py` | script | Linux/macOS setup script. Builds `project.env`, generates the `.vscode/*.code-workspace` file, writes `project.csv` metadata, and creates bilingual `docs/*/data.csv` project data. Also defines the VS Code Python/pytest interpreter paths, debug config, and a placeholder "My Dummy Task". |
| `coding-project-templates.code-workspace` (root and duplicated under `.vscode/`) | config | The generated VS Code multi-root workspace file. |
| `project.env` | config | Environment variables (`ProjectName`, `ProjectDir`, `ProjectEnv`, `ProjectCsv`, `PYTHONPATH`, `vscode_workspace`) consumed by the setup script and VS Code's Python extension. |
| `project.csv` | data | One-row project metadata table (name, repo link, image, category, description) used to populate documentation. |
| `pyproject.toml` | config | `coding-project-templates` package, Python ≥3.12, deps: `pandas`, `pytest`, `python-dotenv`. |
| `uv.lock` | lockfile | uv-managed dependency lock for the above. |
| `folder_tree.md` | doc | A previously captured folder-tree snapshot. **Stale** — see §5. |
| `README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` | doc | Standard repo boilerplate; `README.md` is a 2-line placeholder. |
| `.venv/` | env | Local Python virtualenv (Linux `bin/`, `lib`, `lib64` symlink). |
| `.vscode/` | config | Contains only a copy of the `.code-workspace` file — no `settings.json`/`launch.json`/`tasks.json` at this level (those live *inside* the workspace file's `settings`/`launch`/`tasks` keys instead). |
| `features/` | dir | The starter-template library — see §4. |

## 3. Git configuration: worktrees, not submodules

`features/` is **not** a set of git submodules or independent clones — the root repository uses **`git worktree`**. Each subfolder under `features/` is a linked worktree of the single root repo, each checked out on its own branch. This is confirmed by three things: every `features/<name>/.git` is a small pointer *file* (not a directory) containing a `gitdir:` reference back to the root `.git/worktrees/<name>/` metadata folder; the root `.git/worktrees/` folder lists one metadata subfolder per linked worktree; and each worktree's own `HEAD` file resolves to a branch that also appears in `.git/config` and `.git/refs/heads/`.

### 3.1 Worktree → folder → branch map

| Working folder | Worktree metadata (`.git/worktrees/…`) | Checked-out branch | Notes |
|---|---|---|---|
| *(repo root)* | *(primary worktree — no entry needed)* | `main` | Tracks `origin/main`. |
| `features/claude-code-advance` | `claude-code-advance` | `claude-code-a` | |
| `features/claude-code-basic` | `claude-code-basic` | `claude-code-b` | Actively developed — see §4. |
| `features/js-express` | `js-express` | `web-js` | |
| `features/machine-learning` | `machine-learning` | `py-ml` | |
| `features/manuals` | `manuals` | `manus` | |
| `features/python-app` | `python-app` | `py-app` | |
| `features/python-scripts` | `python-scripts` | `py-script` | |
| `features/web-django` | `web-django` | `py-django` | |
| `features/web-flask` | `web-flask` | `py-flask` | |
| `features/wsl-scripts` | `wsl-scripts` | `wsl-tools` | |
| *(none — orphaned)* | `js-express1` | `web-js` | **Broken/stale**, see §5. |

All 11 branches (`main`, `claude-code-a`, `claude-code-b`, `web-js`, `py-ml`, `manus`, `py-app`, `py-script`, `py-django`, `py-flask`, `wsl-tools`) are configured in `.git/config` with `remote = origin` and a matching `merge = refs/heads/<branch>`; several also carry a `vscode-merge-base = origin/main` entry (added by VS Code's Git Graph/branch tooling), namely `py-flask`, `web-js`, `py-ml`, `py-app`, `py-django`, `wsl-tools`.

### 3.2 Naming mismatch

Folder names under `features/` and their branch names don't follow one consistent convention — folders are descriptive (`python-app`, `web-flask`), branches are short slugs (`py-app`, `py-flask`), and in two cases the branch name doesn't match the folder topic at all in an obvious way (`manuals` → `manus`, `claude-code-advance`/`claude-code-basic` → `claude-code-a`/`claude-code-b`). Worth standardising if more worktrees get added.

## 4. `features/` — starter template inventory

Ten template folders plus one stray file (`features/prompts.md`, currently empty).

| Folder | Contents | Status |
|---|---|---|
| `claude-code-basic` | `.gitignore`, `.python-version` (3.12), `README.md` (21 KB), `requirements.txt` (724 B), `todo.md` (12 KB), `.claude/plan.md` (10 KB) | **Actively customized.** This is the only feature template that has moved past the generic stub — the `.claude/plan.md` records a live plan to rewrite `todo.md` from a SQL-database-specific template into a language-agnostic Claude Code starter template, and to expand the README with Claude Code usage guidance. `README.md` already documents that language-agnostic template (Quick Start, per-language dependency setup, Claude Code workflow instructions). |
| `claude-code-advance` | `.gitignore`, `.python-version`, `README.md` (71 B), `requirements.txt` (27 B), `todo.md` (3.7 KB) | Generic stub, not yet customized (same generic content as the plain templates below). Presumably intended as the "advanced" counterpart to `claude-code-basic` once that one is finished. |
| `js-express` | same generic file set | Generic stub — no Express/Node-specific files (`package.json`, etc.) yet added. |
| `machine-learning` | same generic file set | Generic stub — no ML-specific scaffolding yet. |
| `manuals` | same generic file set | Generic stub. |
| `python-app` | same generic file set | Generic stub. |
| `python-scripts` | same generic file set | Generic stub. |
| `web-django` | same generic file set | Generic stub — no Django project scaffold yet. |
| `web-flask` | same generic file set | Generic stub — no Flask scaffold yet. |
| `wsl-scripts` | same generic file set | Generic stub. |
| `prompts.md` | empty (3 blank lines) | Placeholder, unused. |

Across every stub (all except `claude-code-basic`): `README.md` is the same 2-line repo placeholder as the root README, `requirements.txt` is the same 3-line Python list (`pytest`, `python-dotenv`, `pandas`), and `todo.md` is the same generic **"Todo Template for SQL Database Projects"** (a symbol-based task-tracking template — `[ ]`/`[x]`/`[!]`/`[?]` etc. — dated *2023-12-01, Template Version 2.1*). In other words, most `features/` folders are still at "freshly created worktree, template not yet specialised for its named purpose" stage; `claude-code-basic` is the one template actively being adapted into something folder-name-specific (a generic Claude Code project starter), and it is meant to become the general-purpose language-agnostic template that the still-generic `todo.md` in the other folders should eventually be replaced by/derived from.

## 5. Inconsistencies found

- **`folder_tree.md` is stale.** It documents a snapshot taken from inside `features/python-app`, and shows a `docs/` folder (with `.pytest_cache`, `media`, `readme_en`, `readme_es`) at the project root. No `docs/` folder exists anywhere in the current tree, even though `ProjectSetup-linux-os.py`'s `ProjectDataHandler` still writes to `docs/readme_en/data.csv` and `docs/readme_es/data.csv`, and the workspace file still lists `docs` as one of its folders. Either `docs/` was deleted after that snapshot, or the script has never been run to completion in the current tree state — either way, running `ProjectSetup-linux-os.py` right now would fail at `ProjectDataHandler.generate_data()` (`FileNotFoundError`, since `docs/readme_en/` and `docs/readme_es/` don't exist to be written into).
- **The committed `.code-workspace` file predates the worktree setup.** It lists top-level folders `.git`, `.venv`, `.vscode`, `docs`, `features` — a single `features` entry, not one per worktree. If the intent is for each `features/<name>` worktree to appear as its own folder in the VS Code multi-root workspace, the workspace file needs regenerating (and `ProjectSetup-linux-os.py`'s `subfolders` scan, which only looks at direct children of `project_dir`, would need to recurse into `features/` to pick up each worktree individually).
- **Orphaned worktree registration: `js-express1`.** `.git/worktrees/js-express1` exists with `HEAD` on branch `web-js` (the same branch already checked out in the legitimate `features/js-express` worktree) and a `gitdir` pointer to a path that doesn't exist: `.../coding-project-templates/features/features/js-express/.git` (note the doubled `features/features`). There is no corresponding `features/js-express1` folder in the working tree. This is a broken/leftover worktree record — most likely from an earlier rename or an aborted `git worktree add`. Recommend running `git worktree prune` (or `git worktree remove --force js-express1` if prune doesn't clear it) from the root repo to clean it up.
- **Two branches with no dedicated worktree folder shown for their obvious name pairing:** none beyond the above — every other branch maps 1:1 to a `features/` folder.

## 6. Recommendations

1. Run `git worktree prune` at the repo root to remove the stale `js-express1` registration.
2. Regenerate `docs/` (or remove the `docs`-writing code paths and the `docs` folder reference in the workspace file) so `ProjectSetup-linux-os.py` runs cleanly end-to-end again.
3. Refresh `folder_tree.md` and the `.code-workspace` file so they reflect the current worktree-based `features/` layout — consider extending `VSCodeConfigurator.subfolders` in `ProjectSetup-linux-os.py` to enumerate `features/*` as separate workspace folders.
4. Decide whether `claude-code-basic`'s in-progress language-agnostic `todo.md`/`README.md` rewrite (per `.claude/plan.md`) should become the new baseline stub copied into the still-generic templates (`js-express`, `machine-learning`, `manuals`, `python-app`, `python-scripts`, `web-django`, `web-flask`, `wsl-scripts`), replacing the dated (2023-12-01) SQL-specific `todo.md` they currently all share.
5. Consider aligning branch names with folder names (e.g. `py-app` → `python-app`) for clarity, or documenting the mapping (this report can serve as that reference in the meantime).
