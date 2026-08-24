# manuals — Documentation Site Starter

This is a working [MkDocs](https://www.mkdocs.org/) + [Material](https://squidfunk.github.io/mkdocs-material/) site, not a placeholder. Replace this page's content with your real docs; keep the structure.

## Quick Start

```bash
pip install -r requirements.txt
mkdocs serve
```

Then open <http://127.0.0.1:8000> — the site live-reloads as you edit files under `docs/`.

## Adding a Page

1. Create a new Markdown file under `docs/` (e.g. `docs/guides/deployment.md`).
2. Add it to the `nav` list in `mkdocs.yml`:

    ```yaml
    nav:
      - Home: index.md
      - Guides:
          - Deployment: guides/deployment.md
    ```

3. Run `mkdocs build --strict` before committing — it fails the build on broken internal links or nav entries pointing at files that don't exist, which is exactly the kind of doc rot that's easy to miss in review.

!!! tip "Strict mode is not optional here"
    `mkdocs.yml` sets `strict: true`, and CI runs `mkdocs build --strict` on every push. A docs site with silently broken links isn't much of a docs site — this template treats that as a build failure, not a warning.

## What's Already Wired Up

- **Material theme** with instant navigation and one-click code-block copying
- **`admonition`** and **`pymdownx.superfences`** Markdown extensions — the tip box above is one of them
- **CI build check** (`.github/workflows/docs.yml`) — every push runs `mkdocs build --strict`

## Deliberately Not Built Yet

- More pages / nav sections beyond this one — add them as the real content shows up, following the pattern above
- GitHub Pages deployment — the CI workflow's build job is required; a `deploy` job is included but only runs on the default branch, and needs Pages enabled in the repo's Settings before it does anything
- A house writing style guide — see `CLAUDE.md` for why this template stays style-neutral rather than baking in Wema.Digital conventions by default
