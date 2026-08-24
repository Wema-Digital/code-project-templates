> **Status**: Executed 2026-08-24 (Phase 5 — Intermediate Templates). Supersedes the base-template plan below, which was scoped to the generic `claude-code-basic` stub this template started from.

## Context

`claude-code-advance` was carrying the language-agnostic base template verbatim (generic `todo.md`, generic `README.md`, a `requirements.txt` with `pandas` in it, and a stray `.python-version`) — none of which fit a template whose entire subject is Claude Code's own advanced features. The GitHub Project task "Design claude-code-advance content" (Phase 5) calls for one working example command, one working example subagent, a short hook example, and a minimal CI check, per `claude/5-Phase 5 Detailed Breakdown.md`.

Before writing any of this, verified the exact current schemas for command/agent frontmatter and the hooks `settings.json` format against the official Claude Code docs (`code.claude.com/docs/en/{skills,sub-agents,hooks}.md`) rather than relying on memory — this template's whole job is teaching those schemas correctly, so getting them wrong here would be worse than not shipping an example at all.

## Goal

Three genuinely working examples — a slash command, a subagent, a hook — that all touch something real about this repo's own conventions (the `todo.md` symbol system, keeping template docs in sync), rather than generic "hello world" stand-ins. Plus a CI check that validates `.claude/` config actually parses.

## What was built

- Removed `requirements.txt` and `.python-version` — this template has no runtime deps and isn't Python-specific; same cleanup class as `js-express`/`wsl-scripts` needed for their stray stub files
- `.claude/commands/todo-next.md` — `/todo-next [section]`: reads `todo.md`, reports the next task in priority-symbol order (`[⚠]` → `[!]` → `[#]` → `[ ]`), optionally scoped to one section. `allowed-tools: Read` since it only needs to read
- `.claude/agents/doc-sync-checker.md` — a read-only subagent (`tools: Read, Glob, Grep`, no `Edit`) that checks a template directory's `README.md`/`CLAUDE.md`/`todo.md` for internal consistency: stale "planned additions" language, references to files that don't exist, contradictions between the two docs. `description` includes "Use proactively" per the docs' auto-invocation convention. This is deliberately not a toy example — it's the exact staleness pattern found and fixed across `web-flask`, `web-django`, `python-app`, `python-scripts`, `machine-learning`, and `wsl-scripts` earlier in Phase 5
- `.claude/settings.json` + `.claude/hooks/validate-json.sh` — a `PostToolUse` hook (matcher `Edit|Write`) that checks any `.claude/*.json` file Claude just touched still parses; exits 2 (surfacing stderr back to Claude) on invalid JSON so it can self-correct immediately rather than only finding out from the next CI run
- `.github/scripts/validate_claude_config.py` + `.github/workflows/validate-config.yml` — CI counterpart to the hook: validates every `.claude/*.json` file is valid JSON and every `.claude/commands/*.md`/`.claude/agents/*.md` file has YAML frontmatter that actually parses (`pyyaml`, installed ad hoc in the CI step — no project-level dependency file for a one-script CI tool)
- `README.md`, `todo.md`, `CLAUDE.md` — rewritten advanced-Claude-Code-specific, `CLAUDE.md` pointing at the repo's own root `CLAUDE.md` as a live example of what this template teaches (per spec)

## Deliberately deferred (left as `todo.md` items, not built now)

- Multi-file refactor workflow guidance — noted in the spec as a `todo.md` topic, not a deliverable to build
- More example commands/agents — one of each establishes the convention; see `todo.md` for what to add next
- `.claude/settings.local.json` — gitignored, left for a developer's own overrides, not shipped

## Verification (no unit tests — this template's own convention is a walkthrough, per spec)

- `bash .claude/hooks/validate-json.sh` tested against three stdin payloads: valid JSON (exit 0), invalid JSON (exit 2, stderr message), and a non-`.claude`/non-JSON path (exit 0, skipped) — all correct
- `python3 .github/scripts/validate_claude_config.py` tested against the real `.claude/` dir (passes), then against deliberately broken JSON and a file with no frontmatter (both correctly caught, exit 1) — restored afterward
- `/todo-next` and the `doc-sync-checker` agent are prompt-only; there's no automated way to "run" them outside a live session, so their correctness rests on the verified frontmatter schema, not a test run
