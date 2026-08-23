# CLAUDE.md — manuals

This is the **documentation site template** of the `coding-project-templates` library. It lives on branch `manus` and is checked out as a git worktree at `features/manuals` within the root repo.

## Role of this template

`manuals` provides a starter scaffold for project documentation sites. It extends the language-agnostic base (`claude-code-basic`, branch `claude-code-b`) with a docs-site structure and tooling for writing, building, and publishing technical documentation.

## Stack

- **Docs framework**: MkDocs + Material theme
- **Language**: Python (MkDocs is Python-based)
- **Hosting**: GitHub Pages (via CI)
- **CI**: GitHub Actions — build and deploy on push to `manus`

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | Language-agnostic task tracking template (from base) |
| `README.md` | Guide to using this template with Claude Code (from base) |
| `requirements.txt` | Python deps example — extend with mkdocs + theme |
| `.claude/plan.md` | Base template plan (for reference) |
| `CLAUDE.md` | This file |

**Planned additions (Phase 5):**
- `mkdocs.yml` — site configuration
- `docs/index.md` — home page skeleton
- `docs/getting-started.md` — starter page
- `requirements.txt` — updated with `mkdocs`, `mkdocs-material`
- `.github/workflows/deploy-docs.yml` — build + deploy to GitHub Pages

## Repo conventions (from root CLAUDE.md)

- **Commits** on this branch: `phase 5 intermediate: <what changed>` or `docs: <what changed>`
- **Push** to `origin manus` from inside this worktree
- **Planning notes** live in the root repo's `claude/` folder (numbered `N-Title.md`), not here
- **GitHub Project**: [Wema-Digital/projects/2](https://github.com/orgs/Wema-Digital/projects/2) — mark tasks Done after committing

## Receiving base updates

When `claude-code-basic` is updated, merge changes into this branch:

```bash
cd features/manuals   # branch manus
git merge claude-code-b
git push origin manus
```
