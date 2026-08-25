# Phase 5, broken down per template

*Prepared 2026-08-23. Elaborates the "Bring X to intermediate" line items already sitting in the GitHub Project (Phase 5 - Intermediate Templates) into template-specific subtasks, per your four-deliverable framework (README, dependency file, todo.md, `.claude/plan.md`) plus a fifth I've folded in: a per-template `CLAUDE.md`: since your scope note said "full details live in each folder's `CLAUDE.md`," and none of the nine templates has one yet. `scripts/update-github-project-phase5.sh` pushes the checklist version of each section below into its matching GitHub Project item.*

Shared framework, restated once instead of nine times: every template below gets the same five documentation deliverables (README.md, dependency file, todo.md, `.claude/plan.md`, CLAUDE.md) plus the same four scaffold deliverables (starter code, tests, `.env.example` where relevant, CI workflow). What differs per template is what actually goes in each: that's the point of this breakdown.

---

## `js-express` (branch `web-js`)

A minimal, idiomatic Express.js REST starter: the Node/JS counterpart to the Python web templates, so a JS project gets the same jump-start.

- **README.md**: Express-specific quick start (`npm install`, `npm run dev`), project layout, note that this is the language-agnostic base template's Node equivalent.
- **package.json** (the `requirements.txt` equivalent): `express`; dev deps `nodemon`, `jest`, `supertest`, `eslint`, `prettier`, `dotenv`. *Suggested improvement:* add an `"engines"` field pinning a Node version, and a `.nvmrc`, since the repo already pins Python via `.python-version`: worth the same discipline here. Also: this template currently still ships a stray `.python-version` file from the generic stub: remove it, it's misleading in a Node project.
- **todo.md**: routing setup, centralised error-handling middleware, request logging (`morgan`), env config loading, testing with `supertest`, CI.
- **`.claude/plan.md`**: doesn't exist yet. Create a short starter plan: build one working route, one test, CI: mirroring the shape of `claude-code-basic`'s plan once merged in via phase 4.
- **CLAUDE.md**: flag this is Node, not Python, despite the repo's Python-heavy root tooling; where routes/middleware live; npm scripts reference.
- **Starter code**: `src/app.js` (Express app + middleware), `src/server.js` (listener), one real route (e.g. `GET /health`).
- **Tests**: `test/health.test.js` via `jest` + `supertest`.
- **`.env.example`**: `PORT`, `NODE_ENV`.
- **CI**: `.github/workflows/test.yml`: `actions/setup-node`, `npm ci`, `npm test`.

## `web-flask` (branch `py-flask`)

Flask app-factory starter: the lightweight Python-web option, deliberately simpler than the Django template.

- **README.md**: app-factory pattern explained, quick start (`venv`, `pip install -r requirements.txt`, `flask run`).
- **requirements.txt**: `Flask`, `python-dotenv`, `pytest`, `pytest-flask`. *Suggested improvement:* split into `requirements.txt` (runtime) and `requirements-dev.txt` (test/lint tooling): common Flask convention, and keeps prod installs lean.
- **todo.md**: app-factory setup, blueprint structure, config classes (dev/prod), error handlers, testing with the Flask test client, CI.
- **`.claude/plan.md`**: create: one blueprint, one route, one test, CI.
- **CLAUDE.md**: where blueprints/config live, how to run the dev server, testing convention.
- **Starter code**: `app/__init__.py` (`create_app` factory), `app/routes.py` (one blueprint, an index/health route), `run.py`.
- **Tests**: `tests/test_app.py` using the Flask test client.
- **`.env.example`**: `FLASK_APP`, `FLASK_ENV`, `SECRET_KEY`.
- **CI**: `.github/workflows/test.yml`: Python setup, `pip install -r requirements.txt -r requirements-dev.txt`, `pytest`.

## `web-django` (branch `py-django`)

Full Django project scaffold: for when a project genuinely wants Django's ORM/admin/auth, not just a lightweight route handler.

- **README.md**: quick start assuming `django-admin startproject` has already been applied (`venv`, `pip install`, `migrate`, `runserver`).
- **requirements.txt**: `Django` (pin to current LTS), `python-dotenv` or `django-environ`, `pytest-django`. *Suggested improvement:* pin the Django major version explicitly rather than leaving it floating: Django LTS upgrades aren't always drop-in.
- **todo.md**: project/app split, models & migrations, admin registration, URL routing, settings split (base/dev/prod), testing with `pytest-django`, CI.
- **`.claude/plan.md`**: create: run `startproject`, add one app (e.g. `core`) with a model + view + test, CI.
- **CLAUDE.md**: `manage.py` command reference, settings-module layout, migration workflow.
- **Starter code**: actual `django-admin startproject` output, plus one app with a model, a view, `urls.py` wiring.
- **Tests**: one `pytest-django` test covering the model/view.
- **`.env.example`**: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DATABASE_URL`.
- **CI**: `.github/workflows/test.yml`: Python setup, `pip install`, `pytest`.

## `python-app` (branch `py-app`)

A general-purpose Python application skeleton: for projects that want real structure without committing to a web framework.

- **README.md**: quick start (`venv`, `pip install -e .`, run the entrypoint).
- **Dependency file**: *suggested improvement:* adopt `pyproject.toml` here instead of `requirements.txt`, matching the root repo's own `uv`-managed convention, rather than the generic stub's flat `requirements.txt`. Deps: a CLI lib (`click` or stdlib `argparse`), `python-dotenv`, `pytest`.
- **todo.md**: `src/` layout, config loading, logging setup, packaging, testing, CI.
- **`.claude/plan.md`**: create: `src/` layout, one CLI command, one test, CI.
- **CLAUDE.md**: note this is the "no framework" template: where real logic goes, the `src/` layout convention.
- **Starter code**: `src/<package>/main.py` with a small CLI entrypoint, `__init__.py`.
- **Tests**: `tests/test_main.py`.
- **`.env.example`**: only if the app genuinely needs config; otherwise skip and say so in the README rather than shipping an empty file.
- **CI**: `.github/workflows/test.yml`: Python setup, install, `pytest`.

## `python-scripts` (branch `py-script`)

A loose collection of standalone utility scripts: deliberately not a packaged app.

- **README.md**: explain this is a scripts collection (not a package), how to run an individual script, shared conventions across scripts.
- **requirements.txt**: minimal shared deps (`pandas`, `python-dotenv`); note in-file that a script needing something extra should document that inline at its own top.
- **todo.md**: one real example script with `argparse`, logging convention, output/error-handling convention, testing individual functions (not the CLI wrapper), CI.
- **`.claude/plan.md`**: create: one real example script + a test on its core function + CI.
- **CLAUDE.md**: convention for adding a new script (naming, `argparse` boilerplate, where shared helpers live).
- **Starter code**: one genuinely useful example script (e.g. a small report/export utility) with `argparse`.
- **Tests**: a test on the script's core function, isolated from its CLI wrapper.
- **`.env.example`**: only if a script needs config.
- **CI**: `.github/workflows/test.yml`.

## `machine-learning` (branch `py-ml`)

A minimal, runnable ML/data pipeline example: not tied to a specific model, just proving the scaffold works end to end.

- **README.md**: what the example pipeline demonstrates, how to swap in real data.
- **requirements.txt**: `pandas`, `scikit-learn`, `numpy`, `matplotlib`, `pytest`. *Suggested improvement:* pin versions more tightly than the other templates: ML reproducibility depends on it more than most.
- **todo.md**: data ingestion, feature prep, train/eval split, model training, evaluation metrics, CI; mention experiment tracking as an optional/advanced follow-on, not required for "intermediate."
- **`.claude/plan.md`**: create: one example pipeline against a small built-in dataset (e.g. an `sklearn` toy dataset, so it needs no external data file), a test on the data-prep step, CI.
- **CLAUDE.md**: where data/notebooks/models live, how to run the pipeline, a reminder not to commit large data/model files (point to `.gitignore`).
- **Starter code**: `src/pipeline.py` (load → prep → train → evaluate) against a toy dataset.
- **Tests**: `tests/test_pipeline.py` on the deterministic data-prep function, not the full training run.
- **`.env.example`**: only if a data source path needs configuring.
- **CI**: `.github/workflows/test.yml`.

## `manuals` (branch `manus`)

A documentation-site starter: distinct in kind from the code templates: this one's product *is* docs.

- **README.md**: quick start for building/serving the site.
- **Dependency file**: `mkdocs` + `mkdocs-material` (or your preferred equivalent): here "dependencies" means doc tooling, not app libraries.
- **todo.md**: site structure/nav, writing style guide, image/media conventions, publishing via CI (GitHub Pages), a CI build-check.
- **`.claude/plan.md`**: create: `mkdocs.yml` + one real starter page (not lorem ipsum) + a CI build check.
- **CLAUDE.md**: doc-writing conventions: worth checking whether Wema.Digital's own house style (UK spelling, enhancement-not-transformation language) belongs here if this template is ever used for actual Wema.Digital content, versus staying neutral if it's meant as a generic reusable template.
- **Starter code**: `mkdocs.yml`, `docs/index.md` with real content.
- **"Tests"**: no unit tests in the usual sense; the CI build check (`mkdocs build --strict`) plays that role.
- **`.env.example`**: not applicable, skip.
- **CI**: `.github/workflows/docs.yml`: `mkdocs build --strict`, optionally deploy to GitHub Pages.

## `wsl-scripts` (branch `wsl-tools`)

Shell-scripting starter for WSL/Linux systems automation: the non-Python counterpart to `python-scripts`.

- **README.md**: quick start, and a note on when to reach for this template vs. `python-scripts`.
- **Dependency file equivalent**: there isn't a package manifest for shell; document required CLI tools (e.g. `jq`, `curl`) in a short header comment or a `DEPENDENCIES.md` instead.
- **todo.md**: one real example script, `shellcheck` linting, error-handling convention (`set -euo pipefail`), logging, CI.
- **`.claude/plan.md`**: create: one real example `.sh` script + `shellcheck` CI.
- **CLAUDE.md**: the shell conventions this template enforces (shebang, `set -euo pipefail`, must pass `shellcheck`).
- **Starter code**: `scripts/example.sh`: something genuinely runnable (e.g. an environment/dependency checker).
- **Tests**: `shellcheck` as static analysis; *suggested improvement:* add `bats-core` for behavioural tests if the example script has real logic worth testing beyond linting.
- **`.env.example`**: skip unless relevant.
- **CI**: `.github/workflows/shellcheck.yml`.

## `claude-code-advance` (branch `claude-code-a`)

The advanced counterpart to `claude-code-basic`: once basic covers todo.md-driven single-session workflows, advance is where custom slash commands, subagents, and hooks belong.

- **README.md**: explicitly frame this as building on `claude-code-basic` (prerequisite reading), and explain what "advanced" adds.
- **requirements.txt**: currently the same generic Python placeholder as every other stub, but this template isn't about running an app. *Suggested improvement:* drop it entirely, or replace with a short note that this template has no runtime dependencies: keeping a Python `requirements.txt` here is misleading.
- **todo.md**: designing a custom slash command, building a subagent, configuring a hook, multi-file refactor workflows, a CI check that validates `.claude/` config files parse.
- **`.claude/plan.md`**: create: one working example custom command, one working example subagent, a short hook example.
- **CLAUDE.md**: this one can point at the repo's own root `CLAUDE.md` (from phase 2) as a live example of what it's teaching.
- **Starter code**: `.claude/commands/example.md`, `.claude/agents/example-agent.md`, a `settings.json` hook snippet.
- **"Tests"**: no unit tests; verification is a walkthrough showing the example command/agent actually runs.
- **`.env.example`**: skip.
- **CI**: optional/minimal: validate `.claude/` config parses as valid JSON/YAML.

---

**Next:** `scripts/update-github-project-phase5.sh` pushes a checklist version of each section above into the matching GitHub Project item's description, so the board itself carries this detail rather than just the one-line titles it has now. Once you've reviewed a given template's section here and want changes, tell me and I'll adjust both this file and its GitHub item together before you start that template's actual work.
