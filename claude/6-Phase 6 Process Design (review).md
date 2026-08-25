# Phase 6: Workspace Generator - Process Design

*Prepared 2026-08-23. This confirms the shape of the plan, names the one real technical tension worth deciding before any code gets written, and proposes answers to the smaller open points. Three genuine forks are asked as a quick multiple-choice alongside this document rather than guessed at.*

## Confirming the shape

The generator becomes a new worktree template, `features/vscode-workspace-gen` (branch `vscode-gen`), built as a customised `claude-code-advance`: its agents, subagents, and hooks exist specifically to interview someone about what they want and produce a standalone project folder as output. This fits the existing pattern well: every capability in this repo lives in its own worktree, and it gives `claude-code-advance` a concrete, real application instead of staying an abstract "advanced techniques" template.

The output, once built, is a folder containing:

- `.vscode/` with a customised `.code-workspace` file
- `features/` with just the selected templates, each ready to work in as its own git branch
- `README.md`
- `scripts/` for automation

## The tension worth naming: "standalone" vs. "still a worktree"

The spec asks for two things that pull in different directions: the output should be standalone, and `features/` inside it should be ready to use as a git worktree branch.

A `git worktree` is not standalone by design: `features/web-flask/.git` is a pointer file back to `coding-project-templates/.git/worktrees/web-flask`, which itself points at the object database in `coding-project-templates/.git`. Running `git worktree add` straight from the live `coding-project-templates` checkout into a generated project folder would make that folder secretly depend on `coding-project-templates` staying at its exact current path forever: move it, delete it, or hand the generated folder to a teammate without also handing them `coding-project-templates`, and it breaks.

**Recommended resolution:** the generator creates a fresh bare clone of the repo *inside* the generated project (e.g. `<output>/.git-store/`), then runs `git worktree add` for each selected template against that local bare clone rather than against the live checkout. The generated folder keeps the full git-worktree experience (branch checked out, complete history, `git worktree list` works normally) while carrying its own complete copy of the repo and having zero dependency on where `coding-project-templates` happens to live.

## VS Code configuration

Asking whether the target is native Windows or WSL2 before writing OS-specific settings is the right instinct: the current committed workspace file already hardcodes WSL-style paths (`/mnt/w/vscode.workspaces/...`) into `terminal.integrated.cwd`, `python.defaultInterpreterPath`, and similar settings, which breaks the moment someone opens the same workspace natively on Windows instead of through WSL. Wherever possible, the generator should write settings using `${workspaceFolder}`-relative paths instead of absolute ones: that's the actual portability fix, and the Windows/WSL2 question then only matters for the handful of settings that are genuinely OS-specific. The "check current VS Code documentation before finalising settings" instruction belongs in the generator's own `CLAUDE.md`, as a standing rule it follows every run, not a one-time thing done now: VS Code's settings schema drifts over time.

## `scripts/` folder: suggestions

- **`setup-env.sh`**: bootstraps whichever languages actually got included (venvs and `pip install` for Python templates, `npm install` for `js-express`), instead of a one-size script assuming Python.
- **`git-sync-all.sh`**: the same status/commit/push-across-every-worktree helper from phase 2, reused here since a composed project can itself have several worktree branches.
- **`sync-templates.sh`**: pulls upstream improvements from `code-project-templates` into whichever branches were used, for when a template gets improved after this project was generated.
- **`health-check.sh`**: smoke-tests that each included template's own test suite still passes, useful right after generation and again after a `sync-templates.sh` pull.

## Keep, trim, or drop the `ProjectSetup-linux-os.py`-style master script?

It currently does five loosely related things in one file (writes `project.env`, generates the workspace file, writes `project.csv`, generates bilingual `docs/` data, defines VS Code debug/task config), and its `docs/` generation is already broken against the current repo state.

**Recommendation:** retire the monolith rather than trim it. Replace it with the small, single-purpose scripts above instead of one script trying to do everything: easier to read, easier to hand to Claude Code to modify, easier to test in isolation.

## Other functionality worth considering

- **A manifest file** (e.g. `.workspace-manifest.json`) recording which templates and which commit/branch of each went into a given generated project.
- **A generated root `CLAUDE.md`** in the output project, summarising what's included and how it was assembled.
- **A short post-generation checklist** (`todo.md`) reminding the person of manual follow-ups the generator can't safely do itself: rename the package, point `.env` files at real values, set up a remote for the new project's own git history.
- **Optional `.devcontainer/`** generation, worth flagging as a "nice to have, not required for v1" rather than building it in from the start.

## What's asked alongside this document

Three real forks: the git-structure approach for `features/`, the fate of the monolithic setup script, and whether `claude-code-advance`'s own generic agent/subagent/hook examples should exist before `vscode-workspace-gen` builds on them. Once those are settled, `claude/7-Phase 6 Detailed Breakdown.md` and `scripts/update-github-project-phase6.sh` follow.
