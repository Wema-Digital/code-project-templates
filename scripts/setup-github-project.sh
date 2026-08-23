#!/usr/bin/env bash
# setup-github-project.sh
# Fully ready to run. Creates the "CodeTemplate: Update-DefaultSetup" GitHub Project,
# links it to Wema-Digital/code-project-templates, adds a "Phase" field, and seeds it
# with the full task breakdown for phases 1-6 (tagged by phase).
#
# Requires: gh (authenticated), jq.
# Safe to re-run steps individually if something fails partway — each step prints
# what it did before moving to the next.

set -euo pipefail

OWNER="Wema-Digital"      # If org-level project creation errors with a permissions
                          # message, change this to "@me" and re-run — everything
                          # below works identically against a personal project.
REPO="Wema-Digital/code-project-templates"
TITLE="CodeTemplate: Update-DefaultSetup"

command -v jq >/dev/null || { echo "jq is required — install it first (apt install jq)"; exit 1; }

echo "== 1. Auth: add the 'project' scope and wire git to use gh's credential =="
gh auth refresh -s project -h github.com
gh auth status
gh auth setup-git

echo
echo "== 2. Create the project =="
PROJECT_JSON=$(gh project create --owner "$OWNER" --title "$TITLE" --format json)
PROJECT_NUMBER=$(echo "$PROJECT_JSON" | jq -r '.number')
PROJECT_ID=$(echo "$PROJECT_JSON" | jq -r '.id')
echo "Created project #$PROJECT_NUMBER ($PROJECT_ID)"

echo
echo "== 3. Link it to the repo =="
gh project link "$PROJECT_NUMBER" --owner "$OWNER" --repo "$REPO"

echo
echo "== 4. Add a 'Phase' field so the board can group tasks by phase =="
gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" \
  --name "Phase" --data-type "SINGLE_SELECT" \
  --single-select-options "Phase 1 - Housekeeping,Phase 2 - Root CLAUDE.md,Phase 3 - Base Template,Phase 4 - Propagate Base,Phase 5 - Intermediate Templates,Phase 6 - Workspace Generator" \
  > /dev/null

echo
echo "== 4b. Sanity check — confirm the field/options look right before we rely on their IDs =="
FIELDS_JSON=$(gh project field-list "$PROJECT_NUMBER" --owner "$OWNER" --format json)
echo "$FIELDS_JSON" | jq '.fields[] | select(.name=="Phase")'
read -r -p "Does the field above show 6 options named Phase 1..6? [y/N] " ok
if [ "$ok" != "y" ]; then
  echo "Stopping here — check the project in the browser and re-run from step 4b if needed."
  exit 1
fi
FIELD_ID=$(echo "$FIELDS_JSON" | jq -r '.fields[] | select(.name=="Phase") | .id')

echo
echo "== 5. Create one task item per line below, tagged with its phase =="
declare -a TASKS=(
  "Phase 1 - Housekeeping|Remove stale .git/index.lock at repo root"
  "Phase 1 - Housekeeping|Run git worktree prune (clears orphaned js-express1)"
  "Phase 1 - Housekeeping|Fix JSON syntax error in coding-project-templates.code-workspace (root + .vscode copy)"
  "Phase 1 - Housekeeping|Run gh auth setup-git so git push/pull use gh credentials"
  "Phase 2 - Root CLAUDE.md|Draft root-level CLAUDE.md (repo purpose, worktree map, commit convention, claude/ notes convention)"
  "Phase 2 - Root CLAUDE.md|Build scripts/git-sync-all.sh helper (optional)"
  "Phase 3 - Base Template|Execute claude-code-basic/.claude/plan.md: rewrite todo.md"
  "Phase 3 - Base Template|Rewrite claude-code-basic/README.md per plan"
  "Phase 3 - Base Template|Update claude-code-basic/requirements.txt comments per plan"
  "Phase 3 - Base Template|Run plan's own verification steps"
  "Phase 3 - Base Template|Commit and push claude-code-b"
  "Phase 4 - Propagate Base|Merge claude-code-b into claude-code-advance (claude-code-a)"
  "Phase 4 - Propagate Base|Merge claude-code-b into js-express (web-js)"
  "Phase 4 - Propagate Base|Merge claude-code-b into machine-learning (py-ml)"
  "Phase 4 - Propagate Base|Merge claude-code-b into manuals (manus)"
  "Phase 4 - Propagate Base|Merge claude-code-b into python-app (py-app)"
  "Phase 4 - Propagate Base|Merge claude-code-b into python-scripts (py-script)"
  "Phase 4 - Propagate Base|Merge claude-code-b into web-django (py-django)"
  "Phase 4 - Propagate Base|Merge claude-code-b into web-flask (py-flask)"
  "Phase 4 - Propagate Base|Merge claude-code-b into wsl-scripts (wsl-tools)"
  "Phase 5 - Intermediate Templates|Bring js-express to intermediate (Express+Jest scaffold, CI)"
  "Phase 5 - Intermediate Templates|Bring web-flask to intermediate (Flask app factory, tests, CI)"
  "Phase 5 - Intermediate Templates|Bring web-django to intermediate (Django project scaffold, tests, CI)"
  "Phase 5 - Intermediate Templates|Bring python-app to intermediate (entrypoint, tests, CI)"
  "Phase 5 - Intermediate Templates|Bring python-scripts to intermediate (example script, tests, CI)"
  "Phase 5 - Intermediate Templates|Bring machine-learning to intermediate (pipeline skeleton, tests, CI)"
  "Phase 5 - Intermediate Templates|Bring manuals to intermediate (docs-site skeleton)"
  "Phase 5 - Intermediate Templates|Bring wsl-scripts to intermediate (example scripts, shellcheck CI)"
  "Phase 5 - Intermediate Templates|Design claude-code-advance content (subagents/hooks/slash commands)"
  "Phase 6 - Workspace Generator|Design generator output folder structure (.vscode, features, README, automation script — script functionality TBD, see claude/4-*)"
  "Phase 6 - Workspace Generator|Extend/rewrite generator to produce that structure per selected templates"
  "Phase 6 - Workspace Generator|Test end-to-end generation for a sample template selection"
)

count=0
for task in "${TASKS[@]}"; do
  PHASE="${task%%|*}"
  TITLE_TXT="${task#*|}"
  ITEM_JSON=$(gh project item-create "$PROJECT_NUMBER" --owner "$OWNER" --title "$TITLE_TXT" --format json)
  ITEM_ID=$(echo "$ITEM_JSON" | jq -r '.id')
  OPTION_ID=$(echo "$FIELDS_JSON" | jq -r --arg p "$PHASE" '.fields[] | select(.name=="Phase") | .options[] | select(.name==$p) | .id')
  gh project item-edit --id "$ITEM_ID" --field-id "$FIELD_ID" --project-id "$PROJECT_ID" --single-select-option-id "$OPTION_ID"
  count=$((count+1))
  echo "  [$count] [$PHASE] $TITLE_TXT"
done

echo
echo "Done — $count tasks created and tagged by phase. Project: https://github.com/orgs/$OWNER/projects/$PROJECT_NUMBER"
