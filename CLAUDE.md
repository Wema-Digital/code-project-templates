# CLAUDE.md — manuals

This is the **documentation site template** of the `coding-project-templates` library. It lives on branch `manus` and is checked out as a git worktree at `features/manuals` within the root repo.

## Role of this template

`manuals` provides a starter scaffold for project documentation sites. It extends the language-agnostic base (`claude-code-basic`, branch `claude-code-b`) with a docs-site structure and tooling for writing, building, and publishing technical documentation.

## Stack

- **Docs framework**: MkDocs 1.6 + Material 9.7 theme
- **Language**: Python 3.12 (MkDocs is Python-based — `.python-version` matters here, unlike the shell/config-only templates in this library)
- **Hosting**: GitHub Pages, via `mkdocs gh-deploy` (needs Pages enabled in repo Settings — one manual step, see `README.md`)
- **CI**: GitHub Actions — `build` (required, `mkdocs build --strict`) + `deploy` (only on push to `manus`)

## Doc-writing conventions

**No unit tests here** — `mkdocs build --strict` is the test. `strict: true` in `mkdocs.yml` turns broken internal links and `nav` entries pointing at missing files into build failures, not silent 404s.

**This template stays style-neutral** — it deliberately does not bake in Wema.Digital's house style (UK spelling, "enhancement not transformation" language). The other templates in this library (`web-flask`, `python-app`, ...) are generic scaffolds too; a docs template that hardcoded one organization's voice would be harder to reuse for anything else built from it. If a specific site instance built from this template needs house style, add a `STYLE.md` to *that* site — not to the template. See `.claude/plan.md` for the full reasoning behind this decision.

## Project layout

```
docs/
  index.md      ← real starter content — quick start, adding a page, what's already wired up
mkdocs.yml       ← Material theme, strict: true, nav
requirements.txt ← mkdocs==1.6.1, mkdocs-material==9.7.6, pinned exactly
.github/
  workflows/
    docs.yml     ← CI: build (required, every push/PR) + deploy (manus branch only)
```

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | Docs-site-specific task tracking template |
| `README.md` | Guide to using this template with Claude Code |
| `requirements.txt` | Doc-tooling deps (mkdocs + theme) — not app libraries |
| `.claude/plan.md` | Phase 5 plan for this template, and what was deliberately deferred |
| `CLAUDE.md` | This file |

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
