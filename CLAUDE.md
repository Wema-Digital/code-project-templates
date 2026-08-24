# CLAUDE.md — claude-code-advance

This is the **advanced Claude Code template** of the `coding-project-templates` library. It lives on branch `claude-code-a` and is checked out as a git worktree at `features/claude-code-advance` within the root repo.

## Role of this template

`claude-code-advance` builds on `claude-code-basic` (branch `claude-code-b`) and adds Claude Code-specific power features: custom subagents, hooks, and slash commands. It is intended for developers who want a pre-configured, production-ready Claude Code setup beyond the language-agnostic starter.

Base layer changes from `claude-code-basic` are merged in via `git merge claude-code-b` and then extended with advanced Claude Code configuration here.

Keep `todo.md` in sync with `claude-code-b` conceptually (same symbol system), but this template's own `todo.md` content is advanced-Claude-Code-specific, not the generic base copy. There is no `requirements.txt` here — this template has no runtime dependencies of its own; it's Claude Code configuration, not an application.

## A live example: this repo's own root CLAUDE.md

The best illustration of what this template teaches isn't hypothetical — it's the file at the root of this repo, `/CLAUDE.md`. Read it. It's a real, working example of:
- A **repo-purpose section** written for Claude Code to load automatically at session start (no command/hook needed for this part — Claude Code reads any `CLAUDE.md` in the working directory tree on its own)
- A **commit-message convention** and a **GitHub Project workflow** that this repo's own sessions have followed literally, commit after commit, across every template in Phase 5
- A **worktree map** that a subagent like this template's own `doc-sync-checker` could just as easily be pointed at to check for staleness

If you're designing your own advanced Claude Code setup, `/CLAUDE.md` at this repo's root is worth reading end to end before writing your first command or hook — it shows what a `CLAUDE.md` earns its keep by doing, versus what's just documentation nobody reads.

## What this template contains

| File | Purpose |
|---|---|
| `.claude/commands/todo-next.md` | `/todo-next` — reads `todo.md`, reports the next task by priority symbol |
| `.claude/agents/doc-sync-checker.md` | Read-only subagent — checks README/CLAUDE.md/todo.md consistency |
| `.claude/settings.json` + `.claude/hooks/validate-json.sh` | `PostToolUse` hook — checks `.claude/*.json` still parses after an edit |
| `.github/scripts/validate_claude_config.py` + `.github/workflows/validate-config.yml` | CI counterpart to the hook |
| `todo.md` | Advanced-Claude-Code-specific task tracking template |
| `README.md` | Guide to using this template, framed as building on `claude-code-basic` |
| `.claude/plan.md` | Phase 5 plan for this template, and what was deliberately deferred |
| `CLAUDE.md` | This file |

## Key patterns

**Subagent `tools` is a comma-separated string, not a YAML list** — `tools: Read, Grep, Glob`, not `tools: [Read, Grep, Glob]`. Easy to get wrong copying from other frontmatter conventions; `doc-sync-checker.md` gets it right.

**Scope a subagent's tools to what it actually needs** — `doc-sync-checker` has no `Edit`/`Write` because it only ever reports findings back to the calling session, never changes files itself. If a future agent needs to fix what it finds, that's a deliberate, visible choice in its `tools` line, not an accident.

**A hook's `command` type reads its payload from stdin as JSON**, not as arguments — `tool_name`, `tool_input`, `tool_result`, `session_id`, `cwd`, etc. `validate-json.sh` pulls `tool_input.file_path` out with `python3 -c '...'` rather than assuming shell-friendly argv. Exit code `2` is the one that blocks/gives feedback; `0` is a clean pass; other non-zero codes are non-blocking. On `PostToolUse` specifically, exit-2 stderr is surfaced back to Claude as feedback — that's what makes the hook self-correcting instead of just a silent no-op.

**`allowed-tools` in a command's frontmatter narrows, it doesn't grant** — `/todo-next` sets `allowed-tools: Read` because that's genuinely all it needs; it doesn't expand what the session could already do.

**Deliberately not built yet** (see `todo.md` for the full list): more example commands/agents beyond one of each, a documented multi-file refactor workflow (noted as a `todo.md` discussion topic, not a shipped deliverable).

## Repo conventions (from root CLAUDE.md)

- **Commits** on this branch: `feat: <what changed>` or `phase 5 intermediate: <what changed>`
- **Push** to `origin claude-code-a` from inside this worktree
- **Planning notes** live in the root repo's `claude/` folder (numbered `N-Title.md`), not here
- **GitHub Project**: [Wema-Digital/projects/2](https://github.com/orgs/Wema-Digital/projects/2) — mark tasks Done after committing

## Receiving base updates

When `claude-code-basic` is updated, merge changes into this branch:

```bash
cd features/claude-code-advance   # branch claude-code-a
git merge claude-code-b
git push origin claude-code-a
```
