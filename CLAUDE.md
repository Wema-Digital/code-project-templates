# CLAUDE.md — claude-code-basic

This is the **base template** of the `coding-project-templates` library. It lives on branch `claude-code-b` and is checked out as a git worktree at `features/claude-code-basic` within the root repo.

## Role of this template

`claude-code-basic` is the language-agnostic foundation that every other template is built on. When this template changes, improvements are propagated to the other 9 template branches via `git merge claude-code-b` (Phase 4 of the project plan).

Keep it generic and universally applicable — no language-specific code or dependencies belong here.

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | Language-agnostic task tracking template with the full symbol system |
| `README.md` | Guide to using this template with Claude Code |
| `requirements.txt` | Example Python dependencies with comments for other languages |
| `.claude/plan.md` | Original plan that produced the current files (executed 2026-02-12, updated 2026-08-24) |

## Repo conventions (from root CLAUDE.md)

- **Commits** on this branch: `phase 3 base template: <what changed>` or `feat: <what changed>`
- **Push** to `origin claude-code-b` from inside this worktree
- **Planning notes** live in the root repo's `claude/` folder (numbered `N-Title.md`), not here
- **GitHub Project**: [Wema-Digital/projects/2](https://github.com/orgs/Wema-Digital/projects/2) — mark tasks Done after committing

## Propagation note

After changes here are committed and pushed, Phase 4 merges them into each sibling template:

```bash
# Example: propagate to web-flask
cd features/web-flask     # branch py-flask
git merge claude-code-b
git push origin py-flask
```

Run this for all 9 sibling branches (see the Phase 4 tasks on the project board).
