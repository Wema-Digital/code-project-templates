> **Status**: Executed 2026-08-24 (Phase 5 — Intermediate Templates). Supersedes the base-template plan below, which was scoped to the generic `claude-code-basic` stub this template started from.

## Context

`manuals` was carrying the language-agnostic base template verbatim (generic `todo.md`, generic `README.md`, a `requirements.txt` with `pandas`/`pytest` in it — neither of which has anything to do with building docs). The GitHub Project task "Bring manuals to intermediate" (Phase 5) calls for `mkdocs.yml` + one real starter page + a CI build check, per `claude/5-Phase 5 Detailed Breakdown.md`. This template is a different kind of thing from the code templates: its product *is* the docs, so "Tests" here means a build check, not unit tests.

## Goal

A real, buildable MkDocs + Material site with one genuine starter page (not lorem ipsum) and a strict CI build check.

## What was built

- `mkdocs.yml` — Material theme, `strict: true`, `admonition` + `pymdownx.superfences` markdown extensions, a `nav` with the one real page
- `docs/index.md` — genuine content: how to use *this template* (quick start, adding a page, what's already wired up, what's deliberately not built yet) — the same "document the template itself" pattern used in every other Phase 5 template's `README.md`, just landing on the docs site's own home page instead
- `requirements.txt` — replaced the generic Python placeholder with the real doc-tooling deps: `mkdocs==1.6.1`, `mkdocs-material==9.7.6`, pinned exactly (matches the reasoning behind `machine-learning`'s tight pins: a site that silently changes behavior between visits is worse than a template that pins and gets bumped deliberately)
- `.github/workflows/docs.yml` — `build` job (required, runs `mkdocs build --strict` on every push/PR) + `deploy` job (only on push to `manus`, `mkdocs gh-deploy --force`, needs `contents: write` and GitHub Pages enabled in repo Settings to actually publish anything)
- `.gitignore` — added `site/` (MkDocs' default build output — CI builds it fresh, never commit it)
- `README.md`, `todo.md`, `CLAUDE.md` — rewritten docs-site-specific (replacing the generic base-template copies)

## The house-style question, decided

The breakdown flagged a decision: should this template bake in Wema.Digital's house style (UK spelling, "enhancement not transformation" language) since it might be used for actual Wema.Digital content, or stay neutral as a generic reusable template? **Decided: stay neutral.** This repo's templates (`web-flask`, `python-app`, etc.) don't bake in Wema.Digital-specific conventions either — they're generic scaffolds any project could start from. Baking house style into the *template* (versus a specific site instance built from it) would make it harder to reuse for non-Wema.Digital work. `CLAUDE.md` documents this decision and where house style would go if a specific site instance needs it.

## Deliberately deferred (left as `todo.md` items, not built now)

- More pages / nav sections beyond `index.md` — one real starter page is the spec; add more as real content shows up
- GitHub Pages actually publishing — the `deploy` job exists but needs Pages enabled in repo Settings; that's a one-time manual step outside what a template commit can do
- A house writing style guide — see the decision above
- `mike` (mkdocs versioning plugin) or i18n — noted as advanced/optional, not required for "intermediate"

## Verification

- `mkdocs build --strict` passes cleanly (exit 0) from a clean `uv`-managed venv against `requirements.txt` — no broken links, no nav entries pointing at missing files
- Build output inspected: `index.html`, `sitemap.xml`, `assets/`, `search/` all present as expected
