# claude-code-advance — Custom Commands, Subagents, and Hooks

> The advanced counterpart to `claude-code-basic`. Read that one first — this template assumes you're already comfortable with the `todo.md`-driven single-session workflow it teaches, and adds the Claude Code features that go beyond it.

---

## Prerequisite

**Start with [`claude-code-basic`](../claude-code-basic)** if you haven't already. It covers the `todo.md` symbol system and single-session Claude Code workflows this template builds on top of. Nothing here replaces that — `todo.md` is still how you track work; the additions below are how you teach Claude to work with it (and with your repo) more automatically.

---

## What "Advanced" Adds

| `claude-code-basic` | `claude-code-advance` |
|---|---|
| You type instructions each session | Slash commands package a recurring instruction into `/name` |
| Claude does everything in the main conversation | Subagents run focused sub-tasks with their own scoped tools/context |
| You review every change yourself | Hooks run automatically on events (after an edit, before a tool call, ...) |

Three real, working examples ship in this template — not "hello world" stand-ins:

- **`/todo-next`** — a slash command that reads `todo.md` and tells you the next task to work on, in priority-symbol order
- **`doc-sync-checker`** — a subagent that checks a template directory's `README.md`/`CLAUDE.md`/`todo.md` for internal consistency (stale claims, broken references) — the exact class of bug this repo's own Phase 5 work kept finding and fixing by hand
- **`validate-json` hook** — a `PostToolUse` hook that checks any `.claude/*.json` file you just edited still parses, with a CI job (`validate-config.yml`) as its non-interactive counterpart

---

## Quick Start

```bash
# Everything here is Claude Code config — no install step, no runtime deps.
# Just open this directory in Claude Code and try the examples:

/todo-next
# → reads todo.md, reports the next task to work on

/todo-next "Slash Commands"
# → same, but scoped to one section
```

To see the subagent in action, ask Claude to use it explicitly (or let it decide, since the description includes "Use proactively"):

> "Use the doc-sync-checker agent on features/web-flask and tell me what it finds."

The hook runs automatically — edit `.claude/settings.json` (or any other `.claude/*.json` file) and watch it get checked after the write.

---

## Project Layout

```
claude-code-advance/
├── .claude/
│   ├── commands/
│   │   └── todo-next.md         # /todo-next — reads todo.md, reports the next task
│   ├── agents/
│   │   └── doc-sync-checker.md  # Read-only subagent: README/CLAUDE.md/todo.md consistency
│   ├── hooks/
│   │   └── validate-json.sh     # PostToolUse hook body — checks .claude/*.json parses
│   └── settings.json             # Wires the hook up (PostToolUse, matcher: Edit|Write)
├── .github/
│   ├── scripts/
│   │   └── validate_claude_config.py  # CI counterpart to the hook
│   └── workflows/
│       └── validate-config.yml         # Runs the validator on every push/PR
├── CLAUDE.md                      # Points at the repo's own root CLAUDE.md as a live example
└── todo.md                        # Task tracking template (symbol system, from claude-code-basic)
```

No `requirements.txt`, no `.env.example` — this template has no runtime dependencies of its own. It's Claude Code configuration, not an application.

---

## Adding Your Own

**A command** — new file under `.claude/commands/`, YAML frontmatter (`description`, `argument-hint` if it takes args, `allowed-tools` to scope permissions) plus a body written as an instruction to Claude. Use `$ARGUMENTS` (or `$1`, `$2`, ...) for positional args.

**A subagent** — new file under `.claude/agents/`, frontmatter needs `name` and `description` (include "Use proactively" if it should auto-invoke without being asked); `tools` is a **comma-separated string**, not a YAML list — scope it to the minimum the agent actually needs, the way `doc-sync-checker` has no `Edit`/`Write` because it only ever reports.

**A hook** — add an entry to `.claude/settings.json` under the right event name (`PreToolUse` to intervene before a tool runs, `PostToolUse` to react after, plus session/turn-level events like `Stop`/`SessionStart`). The hook command receives a JSON payload on stdin (`tool_name`, `tool_input`, ...) and communicates back via exit code — `2` blocks/gives feedback, `0` is a clean pass. Read `.claude/hooks/validate-json.sh` for a worked example, and check the [hooks reference](https://code.claude.com/docs/en/hooks) for exact event/exit-code semantics before relying on one for anything important.

---

## Working with Claude Code

This template follows the same `todo.md` task-tracking convention as `claude-code-basic`.
See `todo.md` for the full symbol system and task breakdown, and `CLAUDE.md` for how this repo's own root `CLAUDE.md` is a live example of what this template teaches.

Useful prompts to get started:
- *"Read todo.md and help me design a new slash command for [some recurring task]."*
- *"Run the doc-sync-checker agent against [some directory] and summarize what it finds."*
- *"I want a hook that [does X] whenever [event Y] happens — help me write it."*

---

**Template Version**: 1.0
**Last Updated**: 2026-08-24
**Branch**: `claude-code-a` | **Stack**: Claude Code (commands, subagents, hooks) — no runtime deps
