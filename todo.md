# Todo — manuals

> Documentation-site project tasks. Uses the same symbol system as the base template.
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
- [x] [!] Initialise git repository and branch (manus)
- [x] [!] Create mkdocs.yml (Material theme, strict: true)
- [x] [!] Create requirements.txt (mkdocs, mkdocs-material), pinned exactly
- [x] [!] .python-version (3.12) — mkdocs is Python-based, so this one actually matters here (unlike wsl-scripts/claude-code-advance)
- [x] [!] .gitignore: site/ (build output, never commit)
```

---

## Site Structure & Nav

```markdown
- [x] [!] docs/index.md — real starter content: quick start, adding a page, what's wired up
- [x] [!] nav in mkdocs.yml lists index.md
- [ ] [ ] Add your first real section:
  - [ ] New page(s) under docs/
  - [ ] Add to nav in mkdocs.yml (build fails strict if nav points at a missing file — that's intentional)
  - [ ] Decide on folder structure once there's more than a handful of pages (flat vs. guides/ + reference/ + ...)
- [ ] [@] Decide on a versioning strategy (mike plugin) once there's more than one version of the docs to maintain
```

---

## Writing Style Guide

```markdown
- [x] [@] Decided: this template stays style-neutral (no baked-in Wema.Digital house style) — see .claude/plan.md and CLAUDE.md for the reasoning
- [ ] [ ] If a specific site built from this template needs Wema.Digital house style (UK spelling, enhancement-not-transformation language), add a STYLE.md at that point — not in the template itself
- [ ] [#] Decide on a heading-capitalisation convention (sentence case vs. title case) once there's enough content for it to matter
```

---

## Media Conventions

```markdown
- [ ] [#] Where do images live? (docs/assets/ is the MkDocs convention — not created yet, no images to put there)
- [ ] [@] Decide on a max image size / whether to optimise before committing, once real screenshots show up
```

---

## Testing / Build Check

```markdown
- [x] [!] mkdocs build --strict — stands in for unit tests here; catches broken links and nav entries pointing at missing files
- [ ] [!] Run mkdocs build --strict locally before every commit that touches docs/ or mkdocs.yml
- [ ] [#] Consider a link checker for external URLs once the site has enough of them to matter (strict mode only catches internal/nav links)
```

---

## CI / Publishing

```markdown
- [x] [!] .github/workflows/docs.yml — build job (mkdocs build --strict, every push/PR)
- [x] [!] deploy job (mkdocs gh-deploy --force, only on push to manus)
- [ ] [!] Enable GitHub Pages in repo Settings (Source: gh-pages branch) — one-time manual step, the deploy job can't do this itself
- [ ] [@] Decide on a custom domain / CNAME once the site is actually published somewhere real
```

---

## Metadata

*Last Updated: 2026-08-24*
*Template Version: 1.0*
*Stack: MkDocs 1.6 + Material 9.7 (Python 3.12 tooling, not an app)*
