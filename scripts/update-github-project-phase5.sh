#!/usr/bin/env bash
# update-github-project-phase5.sh
# Enriches the 9 existing "Phase 5 - Intermediate Templates" items in the GitHub
# Project (created by setup-github-project.sh) with a template-specific description
# and subtask checklist, instead of just their one-line titles.
#
# Usage: ./update-github-project-phase5.sh <project-number> [owner]
#   project-number  - the number setup-github-project.sh printed when it created
#                      the project (also visible in the project's URL)
#   owner           - defaults to Wema-Digital; pass "@me" if you created the
#                      project under your personal account instead
#
# Full rationale and "suggested improvement" notes for each item live in
# claude/5-Phase 5 Detailed Breakdown.md: this script pushes the condensed,
# checklist version of that file into GitHub.

set -euo pipefail

PROJECT_NUMBER="${1:?Usage: $0 <project-number> [owner]}"
OWNER="${2:-Wema-Digital}"

command -v jq >/dev/null || { echo "jq is required: install it first (apt install jq)"; exit 1; }

echo "== Fetching existing project items (GraphQL — returns DI_ draft issue IDs) =="
# gh project item-list returns PVTI_ item IDs; --title/--body require the DI_
# draft issue content ID instead. Fetch via GraphQL to get both in one call.
PROJECT_ID=$(gh project list --owner "$OWNER" --format json \
  | jq -r --argjson n "$PROJECT_NUMBER" '.projects[] | select(.number == $n) | .id')

ITEMS_JSON=$(gh api graphql -f query="
query {
  node(id: \"$PROJECT_ID\") {
    ... on ProjectV2 {
      items(first: 100) {
        nodes {
          id
          content {
            ... on DraftIssue { id title }
          }
        }
      }
    }
  }
}" | jq '.data.node.items.nodes')

find_draft_id() {
  # Returns the DI_ content ID needed for --title/--body edits.
  local pattern="$1"
  echo "$ITEMS_JSON" | jq -r --arg p "$pattern" \
    '.[] | select((.content.title // "") | test($p)) | .content.id' | head -n1
}

update_item() {
  local pattern="$1" title="$2" body="$3"
  local draft_id
  draft_id=$(find_draft_id "$pattern")
  if [ -z "$draft_id" ] || [ "$draft_id" = "null" ]; then
    echo "  SKIP: no draft item found matching /$pattern/ (did setup-github-project.sh run for this project?)"
    return
  fi
  # Use GraphQL mutation — gh project item-edit --title/--body require DI_ IDs
  # which the CLI now provides correctly via find_draft_id above.
  gh project item-edit --id "$draft_id" --title "$title" --body "$body" > /dev/null
  echo "  updated: $title"
}

echo "== Updating Phase 5 items =="

update_item "js-express" \
"Bring js-express to intermediate (Express+Jest scaffold, CI)" \
"$(cat <<'EOF'
Minimal, idiomatic Express.js REST starter: the Node/JS counterpart to the Python web templates.

- [ ] README.md: Express quick start, project layout, note this is the base template's Node equivalent
- [ ] package.json: express; dev deps nodemon, jest, supertest, eslint, prettier, dotenv; add "engines" + .nvmrc; remove the stray .python-version left from the generic stub
- [ ] todo.md: routing, error-handling middleware, request logging (morgan), env config, testing w/ supertest, CI
- [ ] .claude/plan.md: create: one route + one test + CI, mirroring claude-code-basic's plan
- [ ] CLAUDE.md: flag this is Node not Python; where routes/middleware live; npm scripts reference
- [ ] Starter code: src/app.js, src/server.js, one real route (GET /health)
- [ ] Tests: test/health.test.js (jest + supertest)
- [ ] .env.example: PORT, NODE_ENV
- [ ] CI: .github/workflows/test.yml (setup-node, npm ci, npm test)

Full detail: claude/5-Phase 5 Detailed Breakdown.md
EOF
)"

update_item "web-flask" \
"Bring web-flask to intermediate (Flask app factory, tests, CI)" \
"$(cat <<'EOF'
Flask app-factory starter: the lightweight Python-web option.

- [ ] README.md: app-factory pattern, quick start
- [ ] requirements.txt: Flask, python-dotenv, pytest, pytest-flask; consider splitting into requirements.txt + requirements-dev.txt
- [ ] todo.md: app-factory setup, blueprints, config classes (dev/prod), error handlers, testing, CI
- [ ] .claude/plan.md: create: one blueprint + one route + one test + CI
- [ ] CLAUDE.md: where blueprints/config live, dev server, testing convention
- [ ] Starter code: app/__init__.py (create_app), app/routes.py, run.py
- [ ] Tests: tests/test_app.py (Flask test client)
- [ ] .env.example: FLASK_APP, FLASK_ENV, SECRET_KEY
- [ ] CI: .github/workflows/test.yml

Full detail: claude/5-Phase 5 Detailed Breakdown.md
EOF
)"

update_item "web-django" \
"Bring web-django to intermediate (Django project scaffold, tests, CI)" \
"$(cat <<'EOF'
Full Django project scaffold: for projects that want the ORM/admin/auth, not just routing.

- [ ] README.md: quick start assuming django-admin startproject already applied
- [ ] requirements.txt: Django (pin LTS), django-environ or python-dotenv, pytest-django
- [ ] todo.md: project/app split, models & migrations, admin, URL routing, settings split (base/dev/prod), testing, CI
- [ ] .claude/plan.md: create: startproject + one app (model+view+test) + CI
- [ ] CLAUDE.md: manage.py reference, settings-module layout, migration workflow
- [ ] Starter code: startproject output + one app with model/view/urls
- [ ] Tests: one pytest-django test
- [ ] .env.example: DJANGO_SECRET_KEY, DJANGO_DEBUG, DATABASE_URL
- [ ] CI: .github/workflows/test.yml

Full detail: claude/5-Phase 5 Detailed Breakdown.md
EOF
)"

update_item "python-app" \
"Bring python-app to intermediate (entrypoint, tests, CI)" \
"$(cat <<'EOF'
General-purpose Python application skeleton: structure without committing to a web framework.

- [ ] README.md: quick start (venv, pip install -e ., run entrypoint)
- [ ] Dependency file: consider pyproject.toml (matches root repo's uv convention) over requirements.txt; deps: click/argparse, python-dotenv, pytest
- [ ] todo.md: src/ layout, config loading, logging, packaging, testing, CI
- [ ] .claude/plan.md: create: src/ layout + one CLI command + one test + CI
- [ ] CLAUDE.md: "no framework" template note, src/ layout convention
- [ ] Starter code: src/<package>/main.py (CLI entrypoint), __init__.py
- [ ] Tests: tests/test_main.py
- [ ] .env.example: only if genuinely needed
- [ ] CI: .github/workflows/test.yml

Full detail: claude/5-Phase 5 Detailed Breakdown.md
EOF
)"

update_item "python-scripts" \
"Bring python-scripts to intermediate (example script, tests, CI)" \
"$(cat <<'EOF'
A loose collection of standalone utility scripts: deliberately not a packaged app.

- [ ] README.md: scripts collection (not a package), how to run one, shared conventions
- [ ] requirements.txt: minimal shared deps (pandas, python-dotenv); document per-script extras inline
- [ ] todo.md: one real example script w/ argparse, logging convention, testing core functions, CI
- [ ] .claude/plan.md: create: one real script + a test on its core function + CI
- [ ] CLAUDE.md: convention for adding a new script (naming, argparse boilerplate, shared helpers)
- [ ] Starter code: one genuinely useful example script (e.g. a report/export utility)
- [ ] Tests: test on the script's core function, isolated from its CLI wrapper
- [ ] .env.example: only if a script needs config
- [ ] CI: .github/workflows/test.yml

Full detail: claude/5-Phase 5 Detailed Breakdown.md
EOF
)"

update_item "machine-learning" \
"Bring machine-learning to intermediate (pipeline skeleton, tests, CI)" \
"$(cat <<'EOF'
Minimal, runnable ML/data pipeline example: proves the scaffold works end to end.

- [ ] README.md: what the example pipeline demonstrates, how to swap in real data
- [ ] requirements.txt: pandas, scikit-learn, numpy, matplotlib, pytest; pin versions tightly (reproducibility)
- [ ] todo.md: ingestion, feature prep, train/eval split, training, metrics, CI; experiment tracking noted as optional/advanced
- [ ] .claude/plan.md: create: example pipeline on a small built-in dataset + test on data-prep + CI
- [ ] CLAUDE.md: where data/notebooks/models live, don't commit large files (point to .gitignore)
- [ ] Starter code: src/pipeline.py (load → prep → train → evaluate) on a toy dataset
- [ ] Tests: tests/test_pipeline.py on the deterministic data-prep step
- [ ] .env.example: only if a data source path needs config
- [ ] CI: .github/workflows/test.yml

Full detail: claude/5-Phase 5 Detailed Breakdown.md
EOF
)"

update_item "manuals" \
"Bring manuals to intermediate (docs-site skeleton)" \
"$(cat <<'EOF'
Documentation-site starter: distinct in kind from the code templates: this one's product is docs.

- [ ] README.md: quick start for building/serving the site
- [ ] Dependency file: mkdocs + mkdocs-material (doc tooling, not app libraries)
- [ ] todo.md: site structure/nav, writing style guide, media conventions, publishing via CI, build-check
- [ ] .claude/plan.md: create: mkdocs.yml + one real starter page + CI build check
- [ ] CLAUDE.md: doc-writing conventions; consider whether Wema.Digital house style belongs here
- [ ] Starter code: mkdocs.yml, docs/index.md with real content
- [ ] "Tests": CI build check (mkdocs build --strict) stands in for unit tests
- [ ] .env.example: not applicable
- [ ] CI: .github/workflows/docs.yml (build --strict, optional GH Pages deploy)

Full detail: claude/5-Phase 5 Detailed Breakdown.md
EOF
)"

update_item "wsl-scripts" \
"Bring wsl-scripts to intermediate (example scripts, shellcheck CI)" \
"$(cat <<'EOF'
Shell-scripting starter for WSL/Linux automation: the non-Python counterpart to python-scripts.

- [ ] README.md: quick start, when to use this vs. python-scripts
- [ ] Dependency doc: no package manifest for shell; document required CLI tools in a header comment or DEPENDENCIES.md
- [ ] todo.md: one real example script, shellcheck linting, set -euo pipefail convention, logging, CI
- [ ] .claude/plan.md: create: one real .sh script + shellcheck CI
- [ ] CLAUDE.md: shell conventions this template enforces (shebang, set -euo pipefail, must pass shellcheck)
- [ ] Starter code: scripts/example.sh (something genuinely runnable, e.g. an env/dependency checker)
- [ ] Tests: shellcheck as static analysis; consider bats-core if the example has real logic to test
- [ ] .env.example: skip unless relevant
- [ ] CI: .github/workflows/shellcheck.yml

Full detail: claude/5-Phase 5 Detailed Breakdown.md
EOF
)"

update_item "claude-code-advance" \
"Design claude-code-advance content (subagents/hooks/slash commands)" \
"$(cat <<'EOF'
The advanced counterpart to claude-code-basic: custom slash commands, subagents, and hooks live here.

- [ ] README.md: frame as building on claude-code-basic (prerequisite); explain what "advanced" adds
- [ ] requirements.txt: currently the generic Python placeholder; consider dropping it or noting no runtime deps: this template isn't about running an app
- [ ] todo.md: designing a slash command, building a subagent, configuring a hook, multi-file refactor workflows, a CI check that .claude/ config parses
- [ ] .claude/plan.md: create: one working example command + one working example subagent + a short hook example
- [ ] CLAUDE.md: point at the repo's own root CLAUDE.md as a live example of what this template teaches
- [ ] Starter code: .claude/commands/example.md, .claude/agents/example-agent.md, a settings.json hook snippet
- [ ] "Tests": verification is a walkthrough showing the example command/agent actually runs
- [ ] .env.example: skip
- [ ] CI: optional/minimal: validate .claude/ config parses as valid JSON/YAML

Full detail: claude/5-Phase 5 Detailed Breakdown.md
EOF
)"

echo
echo "Done."
