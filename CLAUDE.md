# CLAUDE.md — vscode-workspace-gen

This is the **workspace generator** template of the `coding-project-templates` library. It lives on branch `vscode-gen` and is checked out as a git worktree at `features/vscode-workspace-gen` within the root repo. It is a customised `claude-code-advance` (branch `claude-code-a`): the same subagent/hook/slash-command machinery, aimed at one concrete job instead of staying a generic teaching example.

## What this tool does

It builds a standalone, multi-template project folder: you pick which templates from `coding-project-templates` you want (`web-flask` + `python-scripts`, say), and it produces a folder with `.vscode/`, `features/` (one git worktree per selected template), `README.md`, and `scripts/` — ready to open and work in, with no ongoing dependency on this repo's location.

## Two jobs a session opened here might be doing

A Claude Code session in this folder is always doing one of two things. Work out which before doing anything else:

1. **Interviewing** — no `claude/N-*.md` spec exists yet for what the user wants. Ask: which templates, output path, target machine (native Windows or WSL2 — see below), any naming/branch preferences. Write the answers as a spec to `claude/N-Title.md` in *this worktree's own* `claude/` folder (not the root repo's) and stop there for review — this session does not generate files itself.
2. **Generating** — a reviewed `claude/N-*.md` spec already exists. Read it, then actually build the output folder: bare-clone, worktrees, `.vscode/`, docs, scripts. This is the only case where this session writes into the output path.

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
├── README.md
├── CLAUDE.md                # generated, summarises what's included and how it was assembled
└── todo.md                  # post-generation checklist: rename package, fill .env, add a remote
```

## `scripts/` philosophy: small and composable, not one monolith

This repo already has a cautionary example: `ProjectSetup-linux-os.py` does five loosely related things in one file (env file, workspace file, csv, docs generation, debug/task config) and its docs generation is already broken. Don't repeat that shape here. Each generated script does one thing:

- `setup-env.sh` — bootstraps whichever languages actually got included, not a one-size-assumes-Python script
- `git-sync-all.sh` — status/commit/push across every worktree branch in the generated project; reused from this repo's own phase 2 version
- `sync-templates.sh` — pulls upstream template improvements from `coding-project-templates` into the generated project's branches after the fact
- `health-check.sh` — smoke-tests that each included template's own test suite still passes

`.devcontainer/` generation is a nice-to-have flagged for later, not a v1 requirement — don't build it unless asked.

## What this template contains

| File | Purpose |
|---|---|
| `.claude/commands/todo-next.md` | Inherited from `claude-code-advance` — reads `todo.md`, reports the next task |
| `.claude/agents/doc-sync-checker.md` | Inherited from `claude-code-advance` — checks README/CLAUDE.md/todo.md consistency |
| `.claude/settings.json` + `.claude/hooks/validate-json.sh` | Inherited — validates `.claude/*.json` still parses after an edit |
| `.claude/plan.md` | This template's own construction plan (bare-clone mechanism, output shape, Q&A flow) |
| `README.md` | What this tool does, the 4-step process, how to invoke it |
| `CLAUDE.md` | This file |

**Not yet built** (Phase 6, Card 2 — see `claude/7-Phase 6 Detailed Breakdown.md` at the repo root): `.claude/commands/generate-workspace.md` (starts the interview), `.claude/agents/workspace-architect.md` (asks the clarifying questions, writes the spec), a hook validating the *generated* `.vscode/*.code-workspace` is well-formed JSON (distinct from the inherited hook above, which only checks this template's own `.claude/*.json`), and the `scripts/generate-workspace.py` core logic plus the four generated-project scripts described above.

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
