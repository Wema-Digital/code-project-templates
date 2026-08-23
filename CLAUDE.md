# CLAUDE.md — claude-code-advance

This is the **advanced Claude Code template** of the `coding-project-templates` library. It lives on branch `claude-code-a` and is checked out as a git worktree at `features/claude-code-advance` within the root repo.

## Role of this template

`claude-code-advance` builds on `claude-code-basic` (branch `claude-code-b`) and adds Claude Code-specific power features: custom subagents, hooks, and slash commands. It is intended for developers who want a pre-configured, production-ready Claude Code setup beyond the language-agnostic starter.

Base layer changes from `claude-code-basic` are merged in via `git merge claude-code-b` and then extended with advanced Claude Code configuration here.

Keep the base files (todo.md, README.md, requirements.txt) in sync with `claude-code-b`. Advanced features go in `.claude/` only.

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | Language-agnostic task tracking template (from base) |
| `README.md` | Guide to using this template with Claude Code (from base) |
| `requirements.txt` | Example Python dependencies with language comments (from base) |
| `.claude/plan.md` | Original base template plan (executed 2026-02-12, updated 2026-08-24) |
| `CLAUDE.md` | This file — advanced template context |

**Planned additions (Phase 5):**
- `.claude/agents/` — custom subagent definitions
- `.claude/hooks/` — pre/post tool hooks
- `.claude/commands/` — slash command definitions
- Expanded `CLAUDE.md` with advanced workflow guidance

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
