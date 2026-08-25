# CLAUDE.md — vscode-workspace-gen

This is the **workspace generator** template of the `coding-project-templates` library. It lives on branch `vscode-gen` and is checked out as a git worktree at `features/vscode-workspace-gen` within the root repo. It is a customised `claude-code-advance` (branch `claude-code-a`): the same subagent/hook/slash-command machinery, aimed at one concrete job instead of staying a generic teaching example.

## What this tool does

It builds a standalone, multi-template project folder: you pick which templates from `coding-project-templates` you want (`web-flask` + `python-scripts`, say), and it produces a folder with `.vscode/`, `features/` (one git worktree per selected template), `README.md`, and `scripts/` — ready to open and work in, with no ongoing dependency on this repo's location.

## Two jobs a session opened here might be doing

A Claude Code session in this folder is always doing one of two things, both entered via `/generate-workspace` (see `.claude/commands/generate-workspace.md`). Work out which before doing anything else:

1. **Interviewing** (`/generate-workspace`, no arguments) — no `claude/N-*.md` spec exists yet for what the user wants. The `workspace-architect` subagent drafts the spec and reports back either `NEEDS-INPUT` (questions to put to the user) or `DRAFT-READY`; the main session is the one that actually asks the user, since subagents can't. Once the spec is written to `claude/N-Title.md` in *this worktree's own* `claude/` folder (not the root repo's), **stop there for review** — this mode never generates files itself.
2. **Generating** (`/generate-workspace claude/N-title.md`) — a reviewed spec already exists. Runs `scripts/generate-workspace.py --spec ...`, which does the actual work: bare-clone, worktrees, `.vscode/`, docs, scripts. This is the only case where anything gets written into the output path.

Never skip straight to generating from an interview in the same turn — the spec gets written, then reviewed, then built. That gap is deliberate: it is the user's chance to correct a misread requirement before any files exist on disk.

## Standing rule: check current VS Code docs before finalising settings

Every run, before writing `.vscode/*.code-workspace` settings, check the current VS Code docs for the settings keys in use (`python.defaultInterpreterPath`, `terminal.integrated.*`, etc. drift between releases). This is not a one-time thing done when this template was built — the schema changes over time, so re-verify it live, every generation.

## Standing rule: ask Windows vs WSL2, but don't rely on it for portability

The generated project's `.vscode/*.code-workspace` needs to work regardless of whether it's opened on native Windows or through WSL2. Ask which one the user's targeting, because a handful of settings genuinely are OS-specific — but the actual portability fix is writing paths as `${workspaceFolder}`-relative wherever the settings schema allows it, not hardcoded absolutes. This repo's own committed workspace file hardcoded a WSL path (`/mnt/w/vscode.workspaces/...`) into several settings and broke the moment someone opened it natively — don't repeat that.

## The bare-clone-then-worktree mechanism

A `git worktree` is not standalone by construction: `features/web-flask/.git` in this repo is a pointer file back to `coding-project-templates/.git/worktrees/web-flask`, which points at the object database in `coding-project-templates/.git`. Running `git worktree add` straight from this live checkout into a generated project would silently tie that project to this repo's exact current path forever.

The fix: generate a fresh **bare clone of this repo inside the output folder** (`<output>/.git-store/`), then run `git worktree add` for each selected template against that local bare clone, not against this live checkout. The generated folder keeps the full worktree experience (branch checked out, complete history, `git worktree list` works) while depending on nothing outside itself.

## Output folder shape

```
<output>/
├── .git-store/            # bare clone of coding-project-templates — not the live checkout
├── .vscode/
│   └── *.code-workspace    # OS-appropriate, ${workspaceFolder}-relative paths
├── features/
│   └── <template>/         # git worktree per selected template, against .git-store
├── scripts/                 # small, single-purpose — see below, not one monolith
├── .workspace-manifest.json # which templates + commit/branch went in
├── .gitignore                # excludes .git-store/ from any wrapper-level git init
├── README.md
├── CLAUDE.md                # generated, summarises what's included and how it was assembled
└── todo.md                  # post-generation checklist: rename package, fill .env, add a remote
```

## `scripts/` philosophy: small and composable, not one monolith

This repo already has a cautionary example: `ProjectSetup-linux-os.py` does five loosely related things in one file (env file, workspace file, csv, docs generation, debug/task config) and its docs generation is already broken. Don't repeat that shape here. Each generated script does one thing:

- `setup-env.sh` — bootstraps whichever languages actually got included, not a one-size-assumes-Python script
- `git-sync-all.sh` — status/push across every worktree branch in the generated project. The spec called this "reused from phase 2", but phase 2's own `scripts/git-sync-all.sh` was never actually built (its GitHub Project card is still "optional"/in progress) — this is a fresh implementation, not a reuse, written to the same brief
- `sync-templates.sh` — pulls upstream template improvements from `coding-project-templates` into the generated project's branches after the fact (fast-forward only; a diverged branch is reported, not silently merged)
- `health-check.sh` — smoke-tests that each included template's own test suite still passes
- `repair-worktrees.sh` — not in the original spec list; added after discovering (see below) that moving a generated project breaks every worktree until this runs

`.devcontainer/` generation is a nice-to-have flagged for later, not a v1 requirement — don't build it unless asked.

## What this template contains

| File | Purpose |
|---|---|
| `.claude/commands/generate-workspace.md` | `/generate-workspace [spec-path]` — interview flow (no args) or build step (spec path) |
| `.claude/agents/workspace-architect.md` | Drafts and writes the `claude/N-*.md` spec; reports `NEEDS-INPUT`/`DRAFT-READY` since subagents can't ask the user directly |
| `.claude/hooks/validate-workspace-json.sh` | `PostToolUse` — checks a hand-edited `*.code-workspace` file still parses |
| `.claude/commands/todo-next.md` | Inherited from `claude-code-advance` — reads `todo.md`, reports the next task |
| `.claude/agents/doc-sync-checker.md` | Inherited from `claude-code-advance` — checks README/CLAUDE.md/todo.md consistency |
| `.claude/settings.json` + `.claude/hooks/validate-json.sh` | Inherited — validates `.claude/*.json` still parses after an edit |
| `scripts/generate-workspace.py` | The core logic: bare-clone, worktrees, `.vscode/`, docs, manifest, copies the scripts below into the output |
| `scripts/setup-env.sh` | Copied into generated output — bootstraps whichever languages got included |
| `scripts/sync-templates.sh` | Copied into generated output — fast-forwards each included branch from `origin` |
| `scripts/health-check.sh` | Copied into generated output — smoke-tests each included template's test suite |
| `scripts/git-sync-all.sh` | Copied into generated output — status/push across every included worktree |
| `scripts/repair-worktrees.sh` | Copied into generated output — fixes worktree links after the generated project is moved (see below) |
| `.claude/plan.md` | This template's own construction plan (bare-clone mechanism, output shape, Q&A flow) |
| `README.md` | What this tool does, the 4-step process, how to invoke it |
| `CLAUDE.md` | This file |

**Phase 6 complete** (Card 3 executed 2026-08-25 — see `.claude/plan.md`'s Card 3 addendum). Real end-to-end run confirmed: portability by deleting an isolated source copy entirely (not just moving it), both Windows/WSL2 target variants, `scripts/health-check.sh` passing clean against a real generated project, and the workspace file opening in VS Code. Found and fixed two real bugs along the way: three Phase 5 templates' CI was silently broken (missing `pytest.ini` `pythonpath`), and `sync-templates.sh` silently did nothing (`git clone --bare`'s `origin` remote has no fetch refspec by default). **Not done**: a literal live `/generate-workspace` interview through a separate real Claude Code session opened in this worktree — worth a manual pass if maximum confidence is wanted.

## A worktree caveat found while building this: moving a generated project breaks it

Confirmed by hand while writing `scripts/generate-workspace.py`: `git worktree` links are absolute paths on *both* ends (the bare store's `worktrees/<name>/gitdir` and each `features/<name>/.git` file). The bare-clone mechanism above solves dependency on where `coding-project-templates` lives — it does not make the generated project itself immune to being moved. Moving or renaming a generated project after creation breaks every `features/<name>` (`fatal: not a git repository`) until `git worktree repair` runs against each one — which is exactly what `scripts/repair-worktrees.sh` does. This is standard git behavior, not a bug specific to this generator (this repo's own `features/*` worktrees would break the same way if `coding-project-templates` itself were moved), but it's easy to assume "standalone" means "movable" and it doesn't, automatically. Documented in the generated project's own `README.md`/`todo.md`, not just here.

## Repo conventions (from root CLAUDE.md)

- **Commits** on this branch: `feat: <what changed>` or `phase 6 workspace generator: <what changed>`
- **Push** to `origin vscode-gen` from inside this worktree
- **Planning notes**: this worktree keeps its own `claude/N-*.md` specs (interview output, one per generated-workspace request) — separate from the root repo's `claude/` folder, which tracks this repo's own phase planning
- **GitHub Project**: [Wema-Digital/projects/2](https://github.com/orgs/Wema-Digital/projects/2), Phase 6 — mark tasks Done after committing

## Receiving base updates

When `claude-code-advance` is updated, merge changes into this branch:

```bash
cd features/vscode-workspace-gen   # branch vscode-gen
git merge claude-code-a
git push origin vscode-gen
```
