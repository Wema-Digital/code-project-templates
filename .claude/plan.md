# Plan — vscode-workspace-gen

> **Status**: Card 1 (scaffold) executed 2026-08-25. Card 2 (agents/hooks/scripts) executed 2026-08-25, see addendum below. Card 3 (end-to-end test) not started — see `claude/7-Phase 6 Detailed Breakdown.md` at the repo root.

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

## Verification (Card 1)

- `git worktree list` from the repo root shows `features/vscode-workspace-gen` on branch `vscode-gen`
- `doc-sync-checker` run against this directory once README.md/CLAUDE.md/plan.md are in place, to catch any claim here that doesn't match what's actually on disk
- No automated tests for this step — it's orientation documentation, not executable code

---

## Addendum: Card 2 — Build the generator's agents, hooks, and scripts

Executed 2026-08-25.

### What was built

- `.claude/commands/generate-workspace.md` — `/generate-workspace [spec-path]`. No args: interview mode, delegates to `workspace-architect`, loops questions/answers through `AskUserQuestion` until the subagent reports `DRAFT-READY`, then stops. Spec-path arg: build mode, confirms `Status: reviewed` (or asks first), runs `scripts/generate-workspace.py --spec`.
- `.claude/agents/workspace-architect.md` — `tools: Read, Glob, Write`, no `Edit`/`Bash`. Its actual constraint, confirmed against `code.claude.com/docs/en/sub-agents.md` before writing it: subagents cannot use `AskUserQuestion` or any other interactive tool, and run autonomously to a single final report. So it never "asks" the user itself — it returns `NEEDS-INPUT: <questions>` or `DRAFT-READY: <path>`, and the calling command (running in the main session, which *does* have `AskUserQuestion`) is the one that actually puts questions to the user. This is the accurate design for what Card 2's brief called "a subagent whose job is asking the clarifying questions" — the subagent decides *what* to ask, the main session is the only thing that *can* ask it.
- `.claude/hooks/validate-workspace-json.sh` + a second entry in `.claude/settings.json`'s existing `PostToolUse`/`Edit|Write` hook array — checks any `*.code-workspace` file just touched by the Edit/Write tool still parses. Distinct from the inherited `validate-json.sh` (checks this template's own `.claude/*.json`); this one's for a session hand-editing the *generated output*. `scripts/generate-workspace.py` also self-checks what it writes (re-parses immediately after writing), so the hook's job is specifically the hand-edit path the script doesn't cover.
- `scripts/generate-workspace.py` — the core logic. `discover_templates()` parses root `CLAUDE.md`'s Worktree map table live rather than hardcoding the template→branch mapping, so it can't silently drift the way this repo's docs have drifted before. Accepts either `--spec claude/N-*.md` (parses a ` ```yaml ` fenced block, requires PyYAML) or direct `--templates/--output/--project-name/--target` flags (no extra dependency). Implements the bare-clone-then-worktree mechanism exactly as specced: `git clone --bare <source> <output>/.git-store`, explicit `origin` remote set/added regardless of what clone did on its own, then `git worktree add` per template against `.git-store`. Writes `.vscode/*.code-workspace` with zero absolute paths (`${workspaceFolder}`-relative `features/<name>` entries only) and only genuinely-OS-specific settings gated on `--target` (`terminal.integrated.defaultProfile.linux`/`.windows`) — deliberately does *not* set a global `python.defaultInterpreterPath`, since that's ambiguous across multiple selected templates and was the exact class of bug (hardcoded absolute interpreter path) this repo's own committed workspace file had.
- `scripts/setup-env.sh`, `scripts/health-check.sh`, `scripts/sync-templates.sh`, `scripts/git-sync-all.sh` — the four small, single-purpose scripts from the process design doc, copied into every generated project by `generate-workspace.py`. Verified `setup-env.sh`'s dependency detection against every real template in this repo (`requirements-dev.txt` before plain `requirements.txt`, since most templates' dev tooling — including `pytest` itself — lives there, not in the base file; `pyproject.toml`'s `[dev]` extra for `python-app`; `package.json` for `js-express`) rather than assuming.
- `scripts/repair-worktrees.sh` — **not in the original Card 2 list.** Found while smoke-testing (see below) that moving a generated project breaks every `features/<name>` worktree until `git worktree repair` runs, because worktree links are absolute paths on both ends. Added the script, and documented the caveat in this template's own `CLAUDE.md`, `README.md`, and in every generated project's `README.md`/`todo.md` — the bare-clone mechanism solves independence from the *source* repo's location, it does not make the *output* immune to being moved, and conflating the two would be an overclaim.
- `README.md`, `CLAUDE.md` — updated throughout: real file tables, `/generate-workspace` usage instead of "once it ships", the worktree-move caveat.

### Design decisions and why

- **`git-sync-all.sh` was written fresh, not reused.** The spec says "reused from phase 2", but phase 2's own `scripts/git-sync-all.sh` was never actually built (its GitHub Project card is still "optional"). Rather than block Card 2 on an unbuilt phase 2 deliverable, or silently pretend to reuse something that doesn't exist, wrote it to the same brief (status/push across every worktree branch) and said so plainly in `CLAUDE.md` rather than leaving a stale "reused from phase 2" claim in place.
- **No auto-commit in `git-sync-all.sh`.** Considered a `--commit "msg"` mode; dropped it. Auto-committing with a generic message across multiple unrelated worktrees is exactly the kind of action that should stay a human decision, not a generator default.
- **`sync-templates.sh` is fast-forward only.** A diverged branch is reported, not merged automatically — silently creating merge commits across someone else's generated project on their behalf is worse than making them do it by hand once.

### Verification

- `python3 -m py_compile scripts/generate-workspace.py` and `bash -n` on all five shell scripts — all pass
- Ran the real generator (not dry-run) against this repo with `--templates web-flask,python-scripts --target wsl2`: bare clone succeeded, both worktrees checked out on the correct branch/commit, `.vscode/*.code-workspace` and `.workspace-manifest.json` valid, zero absolute paths in any generated file (grepped for the scratch output path across every generated file, found none)
- Re-ran with `--target windows` — settings correctly swap to `terminal.integrated.defaultProfile.windows`, output still valid JSON
- Moved the generated output to a new path by hand: every `features/<name>` broke (`fatal: not a git repository`) until `git worktree repair` ran — this is what motivated `repair-worktrees.sh`; confirmed the script fixes it
- `.claude/hooks/validate-workspace-json.sh` tested against three stdin payloads (valid `.code-workspace`, invalid one, unrelated file) — exit 0/2/0 respectively, matching `validate-json.sh`'s established pattern
- `.claude/settings.json` re-validated as JSON after adding the second hook entry
- Subagent/command YAML frontmatter checked by hand against the verified schema from Phase 5 (flat `key: value` pairs, comma-separated `tools`, no `Edit`/`Write` beyond what's actually needed) — `.github/scripts/validate_claude_config.py` (this template's own CI check) could not be run locally in this session (no `pyyaml` available and the environment blocks installing it), so this is a manual check, not a CI-equivalent one; the committed CI workflow will run it for real on push
- **Not done**: an actual live `/generate-workspace` interview through a real Claude Code session (only the underlying script and the discover/validate logic were exercised directly) — that, plus both OS variants and `health-check.sh` against a real generated project, is Card 3's job
