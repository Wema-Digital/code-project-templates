# CLAUDE.md — coding-project-templates

This is the root-level context file for Claude Code. Keep it short and factual — per-template detail lives in each worktree's own `CLAUDE.md` once that template matures.

## Repo purpose

A multi-template scaffold library for Wema Digital projects. Each template lives on its own branch and is checked out as a **git worktree** under `features/` — not a submodule, not a separate clone. All worktrees share one `.git` database at the repo root.

## Worktree map

| Folder | Branch | Stack |
|---|---|---|
| *(repo root)* | `main` | Shared config, scripts, planning docs |
| `features/claude-code-basic` | `claude-code-b` | Base template — language-agnostic scaffold |
| `features/claude-code-advance` | `claude-code-a` | Advanced Claude Code (subagents, hooks, slash commands) |
| `features/js-express` | `web-js` | Node.js + Express |
| `features/machine-learning` | `py-ml` | Python ML pipeline |
| `features/manuals` | `manus` | Documentation site (MkDocs) |
| `features/python-app` | `py-app` | Python application |
| `features/python-scripts` | `py-script` | Python utility scripts |
| `features/vscode-workspace-gen` | `vscode-gen` | Workspace generator — interviews a user, produces a standalone multi-template project |
| `features/web-django` | `py-django` | Django web app |
| `features/web-flask` | `py-flask` | Flask web app |
| `features/wsl-scripts` | `wsl-tools` | WSL/Bash utility scripts |

## Commit convention

Prefix commits with the phase or scope they belong to:

```
phase 1 housekeeping: <what changed>
phase 3 base template: <what changed>
feat(web-flask): <what changed>
fix: <what changed>
```

Root commits (`main`) cover shared files. Per-template commits happen inside that template's worktree on its own branch and are pushed separately (`git push origin <branch>`).

## claude/ notes convention

`claude/` at the repo root holds numbered planning and session documents:

```
claude/N-Title.md
```

Files are read in order. Each new task or planning session gets the next number. These are working notes — not a changelog, not documentation.

## GitHub Project: phase tracking

Project: **CodeTemplate: Update-DefaultSetup** → [github.com/orgs/Wema-Digital/projects/2](https://github.com/orgs/Wema-Digital/projects/2)

Tasks are grouped by a **Phase** single-select field (Phase 1–6). Workflow:

1. Pick the next `Todo` task in the current phase
2. Set status → `In Progress` when starting
3. Set status → `Done` when the work is committed and pushed
4. Add a short description to the item summarising what was actually done

Phases in order: Housekeeping → Root CLAUDE.md → Base Template → Propagate Base → Intermediate Templates → Workspace Generator.

## Key scripts

| Script | Purpose |
|---|---|
| `scripts/setup-github-project.sh` | Creates the GitHub Project, Phase field, and seeds all tasks |
| `ProjectSetup-linux-os.py` | Generates `.code-workspace`, `project.env`, `project.csv` from the repo layout |

## Where things live

| Path | Contents |
|---|---|
| `claude/` | Numbered session and planning notes |
| `features/` | One git worktree per template |
| `scripts/` | Repo-level automation scripts |
| `coding-project-templates.code-workspace` | VS Code multi-root workspace for the full repo |
