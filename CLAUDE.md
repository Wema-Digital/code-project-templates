# CLAUDE.md — js-express

This is the **Node.js + Express template** of the `coding-project-templates` library. It lives on branch `web-js` and is checked out as a git worktree at `features/js-express` within the root repo.

## Role of this template

`js-express` provides a starter scaffold for Node.js web applications built with Express. It extends the language-agnostic base (`claude-code-basic`, branch `claude-code-b`) with JavaScript/Node.js-specific structure, dependencies, and tooling.

## Stack

- **Runtime**: Node.js
- **Framework**: Express
- **Testing**: Jest
- **Linting**: ESLint + Prettier
- **CI**: GitHub Actions

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | Language-agnostic task tracking template (from base) |
| `README.md` | Guide to using this template with Claude Code (from base) |
| `requirements.txt` | Python deps example — **replace with `package.json`** for this stack |
| `.claude/plan.md` | Base template plan (for reference) |
| `CLAUDE.md` | This file |

**Planned additions (Phase 5):**
- `package.json` — Express + Jest + ESLint dependencies
- `src/app.js` — Express app factory
- `src/routes/` — example route
- `tests/` — Jest test scaffold
- `.env.example`
- `.github/workflows/test.yml` — CI on push

## Repo conventions (from root CLAUDE.md)

- **Commits** on this branch: `phase 5 intermediate: <what changed>` or `feat: <what changed>`
- **Push** to `origin web-js` from inside this worktree
- **Planning notes** live in the root repo's `claude/` folder (numbered `N-Title.md`), not here
- **GitHub Project**: [Wema-Digital/projects/2](https://github.com/orgs/Wema-Digital/projects/2) — mark tasks Done after committing

## Receiving base updates

When `claude-code-basic` is updated, merge changes into this branch:

```bash
cd features/js-express   # branch web-js
git merge claude-code-b
git push origin web-js
```
