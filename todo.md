# Todo — claude-code-advance

> Advanced Claude Code configuration tasks. Uses the same symbol system as the base template.
> See the Symbol Guide below for reference.

## Symbol Guide

| Symbol | Meaning | When to use with Claude |
|--------|---------|-------------------------|
| `[ ]` | Unstarted | Default for all new tasks |
| `[x]` | Completed | Ask Claude to mark tasks done |
| `[-]` | In-progress | Claude marks what it's actively working on |
| `[!]` | High priority | Focus here first |
| `[@]` | Needs discussion | Ask Claude for design input |
| `[?]` | Needs research | Have Claude research options |
| `[#]` | Medium priority | After `[!]` tasks |
| `[~]` | On hold | Skip for now |
| `[>]` | Delegated/deferred | Assigned elsewhere or future |
| `[⚠]` | Critical issue | Urgent bug or blocker |
| `[%]` | % complete | Track large in-progress features |

---

## Project Setup

```markdown
- [x] [!] Initialise git repository and branch (claude-code-a)
- [x] [!] Remove stray requirements.txt / .python-version left from the generic stub — no runtime deps here
- [x] Replace the all-Python .gitignore with one appropriate for this template
- [ ] [@] Decide whether to merge claude-code-basic's base files (todo.md/README.md) again once basic changes, or let this template's docs diverge now that they're advanced-specific
```

---

## Slash Commands

```markdown
- [x] [!] .claude/commands/todo-next.md — reads todo.md, reports the next task by priority symbol
- [ ] [ ] Design your next command:
  - [ ] Frontmatter: description, argument-hint if it takes args, allowed-tools to scope permissions
  - [ ] Body: a clear instruction, using $ARGUMENTS / $1 / named args from the `arguments` field as needed
  - [ ] Decide if it should run in the main session or context: fork (isolated subagent)
- [ ] [@] Decide on a naming convention once there are more than a couple commands (verb-noun vs. noun-verb)
```

---

## Subagents

```markdown
- [x] [!] .claude/agents/doc-sync-checker.md — read-only (Read, Grep, Glob), checks README/CLAUDE.md/todo.md consistency
- [ ] [ ] Design your next subagent:
  - [ ] Frontmatter: name, description (include "Use proactively" if it should auto-invoke), tools (comma-separated string, not a list), model
  - [ ] Scope `tools` to the minimum the agent actually needs — doc-sync-checker has no Edit/Write on purpose
  - [ ] Write the system prompt: role, when invoked, what to check/do, how to report back
- [ ] [@] Decide which agents should be proactive (auto-invoked) vs. explicitly called
```

---

## Hooks

```markdown
- [x] [!] .claude/settings.json — PostToolUse hook (matcher: Edit|Write) wired to .claude/hooks/validate-json.sh
- [x] [!] .claude/hooks/validate-json.sh — validates .claude/*.json still parses after an edit; exit 2 surfaces feedback to Claude
- [ ] [ ] Design your next hook:
  - [ ] Pick the right event (PreToolUse to block before it happens, PostToolUse to catch/react after, Stop, SessionStart, etc.)
  - [ ] Pick a matcher (tool name, pipe-separated alternation, or regex)
  - [ ] Read the hook's stdin JSON payload for the fields you need (tool_name, tool_input, tool_result, ...)
  - [ ] Exit 2 to block/give feedback; exit 0 for success; know your event's exact blocking semantics before relying on it
- [ ] [@] Decide whether a hook should live as a one-line command in settings.json or call out to a script under .claude/hooks/ — validate-json.sh does the latter because the logic is too much for one line
```

---

## Multi-File Refactor Workflows

```markdown
- [ ] [@] Decide on a convention for large, multi-file changes: one command that fans out to subagents per file? A single session working sequentially? Depends on whether files are independent or coupled.
- [ ] [?] Research context: fork on commands (runs the command in an isolated subagent) — worth using for a refactor step that shouldn't pollute the main session's context?
- [ ] [ ] Once there's a real refactor workflow, document it here as a worked example, not just a placeholder
```

---

## CI / Validation

```markdown
- [x] [!] .github/scripts/validate_claude_config.py — validates .claude/*.json is valid JSON, command/agent frontmatter is valid YAML
- [x] [!] .github/workflows/validate-config.yml — runs the validator on every push/PR
- [ ] [#] Extend the validator once settings.json grows more hook types — same JSON-parses check covers all of them already, but a schema check (event names, matcher syntax) would catch more
```

---

## Metadata

*Last Updated: 2026-08-24*
*Template Version: 1.0*
*Stack: Claude Code (commands, subagents, hooks) — no runtime language deps*
