# Plan — vscode-workspace-gen

> **Status**: Card 1 (Scaffold the vscode-workspace-gen template) executed 2026-08-25. Card 2 (agents/hooks/scripts) and Card 3 (end-to-end test) are not started — see `claude/7-Phase 6 Detailed Breakdown.md` at the repo root.

## Context

Phase 6 builds a new template, `vscode-workspace-gen`, whose entire job is generating other projects: interview a user about which `coding-project-templates` templates they want, then produce a standalone folder combining them. `claude/6-Phase 6 Process Design (review).md` settled the shape and the one real technical tension (bare-clone-vs-live-worktree) before any code was written; this plan carries that forward for the scaffold step specifically.

Prerequisite already satisfied: `claude-code-advance` (branch `claude-code-a`) carries one working example command, subagent, and hook (Phase 5) — this template branches from that content rather than duplicating it from scratch.

## Goal (Card 1 scope only)

Stand up the worktree and its orientation docs — `README.md`, `CLAUDE.md`, this plan — accurately describing a tool that doesn't do its actual job yet. Card 2 builds the generation logic; this step just gives a session opened here the right standing rules and mental model before that code exists.

## The bare-clone-then-worktree mechanism

Decided in the process design review, restated here as the thing Card 2's `scripts/generate-workspace.py` must implement:

1. `git clone --bare` this repo into `<output>/.git-store/`
2. For each selected template, `git worktree add <output>/features/<name> <branch>` run **against `<output>/.git-store`**, not against the live `coding-project-templates` checkout
3. Result: the generated folder has the full worktree experience (branch checked out, complete history) with zero dependency on where `coding-project-templates` happens to live afterward

Rejected alternative: `git worktree add` straight from the live checkout into the output folder. Simpler, but ties the generated project to this repo's current path permanently — moving, deleting, or not sharing `coding-project-templates` alongside it breaks every worktree inside.

## Output folder shape

```
<output>/.git-store/            # bare clone, not the live checkout
<output>/.vscode/*.code-workspace
<output>/features/<template>/   # one worktree per selection, against .git-store
<output>/scripts/               # setup-env.sh, git-sync-all.sh, sync-templates.sh, health-check.sh
<output>/.workspace-manifest.json
<output>/README.md
<output>/CLAUDE.md              # generated, summarises what's included
<output>/todo.md                # post-generation manual-follow-up checklist
```

`scripts/` is deliberately several small files, not one script. `ProjectSetup-linux-os.py` in this repo is the cautionary example: five loosely related jobs in one file, and its `docs/` generation step is already broken against current repo state. Card 2 replaces that pattern rather than trimming it.

## The Q&A flow

Two distinct sessions, never collapsed into one turn:

1. **Interview** (Card 2's `workspace-architect` subagent, via `/generate-workspace`): ask which templates, output path, Windows vs WSL2. Write a spec to this worktree's own `claude/N-Title.md`. Stop — do not generate anything yet.
2. **Build** (a later session, after human review of the spec): read the reviewed `claude/N-*.md`, then actually run the bare-clone-and-worktree mechanism and write the output folder.

The gap between the two is deliberate — it's the point where a misread requirement gets caught before any files exist on disk, the same role human review plays for this repo's own `claude/N-*.md` planning docs.

## What gets written where (Card 1)

- `features/vscode-workspace-gen` worktree, branch `vscode-gen`, off `claude-code-a` — done via `git worktree add features/vscode-workspace-gen -b vscode-gen claude-code-a`
- `README.md` — what the tool does, the 4-step process, how to invoke it (plain-English today, `/generate-workspace` once Card 2 ships)
- `CLAUDE.md` — the two-jobs framing (interviewing vs. generating), the VS Code-docs-check and Windows/WSL2 standing rules, the bare-clone mechanism, output shape, and an honest "not yet built" list so a session here doesn't assume Card 2's files already exist
- `.claude/plan.md` — this file
- Inherited unchanged from `claude-code-advance`: `.claude/commands/todo-next.md`, `.claude/agents/doc-sync-checker.md`, `.claude/settings.json` + `.claude/hooks/validate-json.sh`, `.github/` CI, `.gitignore`. Whether these generic examples stay, get removed, or get extended is a Card 2 decision, not this scaffold step's — Card 2 adds `generate-workspace.md`, `workspace-architect.md`, and a second, distinct hook (validates *generated* `.vscode/*.code-workspace`, not this template's own `.claude/*.json`) alongside them.
- `todo.md` — deliberately left as inherited from `claude-code-advance` for now rather than rewritten; Card 1's checklist in `claude/7-Phase 6 Detailed Breakdown.md` doesn't call for a todo.md rewrite, and rewriting it before Card 2's real task list exists would just mean rewriting it twice

## Deliberately deferred (not Card 1's job)

- `.claude/commands/generate-workspace.md`, `.claude/agents/workspace-architect.md` — Card 2
- The generated-output JSON-validation hook — Card 2
- `scripts/generate-workspace.py` and the four generated-project scripts — Card 2
- Running an actual generation end to end — Card 3
- `.devcontainer/` generation — flagged in the process design doc as nice-to-have, not v1

## Verification

- `git worktree list` from the repo root shows `features/vscode-workspace-gen` on branch `vscode-gen`
- `doc-sync-checker` run against this directory once README.md/CLAUDE.md/plan.md are in place, to catch any claim here that doesn't match what's actually on disk
- No automated tests for this step — it's orientation documentation, not executable code
