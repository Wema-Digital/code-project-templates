#!/usr/bin/env bash
# setup-github-project-youtube-pipeline.sh
# Phase 0.2 of claude/1-YouTube-Pipeline-Workspace-Plan.md.
#
# Creates a GitHub Project board for the youtube-pipeline repo, mirroring the
# pattern of coding-project-templates' own scripts/setup-github-project.sh:
# a "Phase" single-select field, then one draft item per task seeded from the
# rollout plan's Phase 0-4 breakdown and tagged with its phase.
#
# Requires: gh (authenticated, with the 'project' scope), jq.
# The user runs this -- gh auth lives in their terminal, not the Claude session.
#
# Re-running creates a *second* project with the same title; delete the first
# in the browser if you need a clean redo.

set -euo pipefail

OWNER="Wema-Digital"      # if org-level project creation errors on permissions,
                          # set this to "@me" and re-run -- everything else works
                          # identically against a personal project.
REPO="Wema-Digital/youtube-pipeline"
TITLE="YouTube Pipeline: Rollout"

command -v jq >/dev/null || { echo "jq is required -- install it first (apt install jq)"; exit 1; }

# Set ASSUME_YES=1 to skip the interactive sanity-check prompt (step 4b).
ASSUME_YES="${ASSUME_YES:-0}"

echo "== 1. Auth: ensure the 'project' scope is present and wire git to use gh's credential =="
if gh auth status 2>&1 | grep -q "'project'"; then
  echo "  token already has the 'project' scope"
else
  echo "  requesting the 'project' scope (interactive)..."
  gh auth refresh -s project -h github.com
fi
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
echo "== 4. Add a 'Phase' field grouping tasks by this plan's phases (0-4) =="
gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" \
  --name "Phase" --data-type "SINGLE_SELECT" \
  --single-select-options "Phase 0 - GitHub Setup,Phase 1 - Interview,Phase 2 - Build,Phase 3 - Content Build-out,Phase 4 - Verification" \
  > /dev/null

echo
echo "== 4b. Sanity check the field before relying on its option IDs =="
FIELDS_JSON=$(gh project field-list "$PROJECT_NUMBER" --owner "$OWNER" --format json)
echo "$FIELDS_JSON" | jq '.fields[] | select(.name=="Phase")'
PHASE_OPT_COUNT=$(echo "$FIELDS_JSON" | jq '[.fields[] | select(.name=="Phase") | .options[]] | length')
if [ "$ASSUME_YES" = "1" ]; then
  if [ "$PHASE_OPT_COUNT" != "5" ]; then
    echo "Stopping -- Phase field has $PHASE_OPT_COUNT options, expected 5. Check the project in the browser."
    exit 1
  fi
  echo "  (ASSUME_YES=1) Phase field has 5 options -- continuing."
else
  read -r -p "Does the field above show 5 options named Phase 0..4? [y/N] " ok
  if [ "$ok" != "y" ]; then
    echo "Stopping -- check the project in the browser and re-run from step 4b if needed."
    exit 1
  fi
fi
FIELD_ID=$(echo "$FIELDS_JSON" | jq -r '.fields[] | select(.name=="Phase") | .id')

echo
echo "== 5. Seed one task item per line, tagged with its phase =="
declare -a TASKS=(
  "Phase 0 - GitHub Setup|Run setup-github-repo-youtube-pipeline.sh (create repo, main default, branch protection)"
  "Phase 0 - GitHub Setup|Run this script to create the Project board and Phase field"
  "Phase 0 - GitHub Setup|Verify structure: gh repo view, gh project list --owner Wema-Digital, confirm Phase field + seeded tasks"
  "Phase 1 - Interview|Confirm claude/1-YouTube-Pipeline-Workspace-Plan.md is DRAFT-READY (all open items resolved)"
  "Phase 1 - Interview|Human review + sign-off on the finished spec before Build"
  "Phase 2 - Build|Run generate-workspace.py --spec claude/1-YouTube-Pipeline-Workspace-Plan.md (try --dry-run first)"
  "Phase 2 - Build|cd <output>/.git-store; git remote add origin <repo>; push every selected template branch"
  "Phase 2 - Build|Run scripts/health-check.sh against the generated output"
  "Phase 2 - Build|Note repair-worktrees.sh in the generated README/todo (already auto-written) as the move-recovery step"
  "Phase 2 - Build|Manual step: create the plain non-git folders (_templates/, _pipeline-docs/, _raw-exports/)"
  "Phase 3 - Content Build-out|00_keyword-intelligence: append_snapshot.py (A3), <750 Search Volume gate + Insufficient Volume tag, A5 auto-compute, the Routine config"
  "Phase 3 - Content Build-out|production_pipeline: build W2 (Series Candidates) and W3 (Singles Tracker) skeletons"
  "Phase 3 - Content Build-out|production_pipeline: find_row() label-scan write-back S1 <-> W1/W3; SEO_CHECK refresh against Keyword Bank"
  "Phase 3 - Content Build-out|A7 lane + health clustering logic (design task -- own short spec before code); unblocks C1"
  "Phase 3 - Content Build-out|notion-integration: define its concrete job (reads/writes, place in v8 flow), then build notion-client calls + driving agent"
  "Phase 3 - Content Build-out|OPT1 (Unclaimed Backlog sheet): decide yes/no"
  "Phase 4 - Verification|Run doc-sync-checker against the generated output once Phase 3 content exists"
  "Phase 4 - Verification|Apply the four-item artefact checklist to youtube-pipeline (Project, Workspace, Repo, Cowork Project)"
  "Phase 4 - Verification|Decide whether youtube-pipeline needs its own Claude Cowork Project or shares one"
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
echo "Done -- $count tasks created and tagged by phase."
echo "Project: https://github.com/orgs/$OWNER/projects/$PROJECT_NUMBER"
