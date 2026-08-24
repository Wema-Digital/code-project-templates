# manuals — Documentation Site Starter

> A working MkDocs + Material site, not a placeholder — different in kind from the other templates in this library, because this one's product *is* the docs.
> Clone, install, and have a real docs site building (and, once Pages is enabled, deploying) in minutes.

---

## Quick Start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install doc-tooling dependencies
pip install -r requirements.txt

# 3. Serve locally with live reload
mkdocs serve
# → open http://127.0.0.1:8000

# 4. Build (what CI runs — fails on broken links/nav)
mkdocs build --strict
```

---

## Project Layout

```
manuals/
├── docs/
│   └── index.md            # Real starter content — replace with your actual docs
├── mkdocs.yml                # Site config: Material theme, nav, strict mode
├── requirements.txt           # mkdocs + mkdocs-material, pinned exactly
├── .python-version             # Pinned Python version (3.12) — mkdocs is Python-based
├── .github/
│   └── workflows/
│       └── docs.yml             # CI: build (required) + deploy (manus branch only)
├── CLAUDE.md                    # Claude Code context for this template
└── todo.md                      # Task tracking template (symbol system)
```

---

## Adding a Page

1. Create a new Markdown file under `docs/`.
2. Add it to `nav` in `mkdocs.yml`.
3. Run `mkdocs build --strict` before committing — `strict: true` in `mkdocs.yml` means a `nav` entry pointing at a file that doesn't exist, or a broken internal link, fails the build instead of quietly shipping a 404.

```yaml
# mkdocs.yml
nav:
  - Home: index.md
  - Guides:
      - Deployment: guides/deployment.md
```

---

## Why "Tests" Means a Build Check Here

There's no `tests/` directory and no test framework in `requirements.txt` — this template's product is the site itself, so `mkdocs build --strict` *is* the test. It catches the failure modes that actually matter for docs: broken internal links, a `nav` entry referencing a page that was renamed or deleted, malformed Markdown. CI (`.github/workflows/docs.yml`) runs it on every push and PR.

---

## Publishing to GitHub Pages

The `deploy` job in `.github/workflows/docs.yml` runs `mkdocs gh-deploy --force` on every push to `manus`, but it needs one manual, one-time step first: enable GitHub Pages in the repo's **Settings → Pages**, with source set to the `gh-pages` branch. Until that's done, the job runs and pushes the branch, but nothing serves it.

---

## Working with Claude Code

This template follows the same `todo.md` task-tracking convention as `claude-code-basic`.
See `todo.md` for the full symbol system and task breakdown.

Useful prompts to get started:
- *"Read todo.md and help me add a new docs section with a real page and nav entry."*
- *"Run mkdocs build --strict and fix whatever it flags."*
- *"This site needs Wema.Digital house style now — add a STYLE.md and apply it to index.md."*

---

**Template Version**: 1.0
**Last Updated**: 2026-08-24
**Branch**: `manus` | **Stack**: MkDocs 1.6 + Material 9.7
