#!/usr/bin/env bash
# update-github-project-phase6.sh
# Enriches the 3 existing "Phase 6 - Workspace Generator" items in the GitHub
# Project (created by setup-github-project.sh) with the detailed breakdown from
# claude/7-Phase 6 Detailed Breakdown.md, replacing their one-line titles/bodies.
#
# Usage: ./update-github-project-phase6.sh <project-number> [owner]

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
  gh project item-edit --id "$draft_id" --title "$title" --body "$body" > /dev/null
  echo "  updated: $title"
}

echo "== Updating Phase 6 items =="

update_item "Design generator output folder structure" \
"Scaffold the vscode-workspace-gen template" \
"$(cat <<'EOF'
Prerequisite: claude-code-advance has at least one working example command, subagent, and hook (its own phase 5 task) before this starts.

- [ ] Create worktree + branch: git worktree add features/vscode-workspace-gen -b vscode-gen claude-code-a
- [ ] README.md: what this tool does, the 4-step process, how to invoke it
- [ ] CLAUDE.md: orient a Claude Code session here (interview flow vs. reading a saved spec); encode "check current VS Code docs" and "ask Windows vs WSL2" as standing rules
- [ ] .claude/plan.md: bare-clone+worktree mechanism, output folder shape, the Q&A flow, what gets written where

Full detail: claude/7-Phase 6 Detailed Breakdown.md
EOF
)"

update_item "Extend/rewrite generator" \
"Build the generator's agents, hooks, and scripts" \
"$(cat <<'EOF'
- [ ] .claude/commands/generate-workspace.md: slash command starting the interview flow
- [ ] .claude/agents/workspace-architect.md: subagent that asks clarifying questions and produces the spec/manifest
- [ ] A hook validating the generated .vscode/*.code-workspace is well-formed JSON before finishing (motivated by this repo's own JSON bug)
- [ ] scripts/generate-workspace.py: bare-clone the repo into <output>/.git-store, git worktree add each selected template, write .vscode/ (${workspaceFolder}-relative paths, OS-appropriate), README.md, CLAUDE.md, .workspace-manifest.json, post-generation todo.md
- [ ] scripts/setup-env.sh: bootstraps whichever languages got included
- [ ] scripts/sync-templates.sh: pulls upstream template improvements into a generated project
- [ ] scripts/health-check.sh: smoke-tests each included template's test suite
- [ ] scripts/git-sync-all.sh: reused from phase 2

Full detail: claude/7-Phase 6 Detailed Breakdown.md
EOF
)"

update_item "Test end-to-end generation" \
"Test the generator end to end" \
"$(cat <<'EOF'
- [ ] Generate a sample selection (e.g. web-flask + python-scripts) into a scratch output folder
- [ ] Confirm portability: move/rename coding-project-templates temporarily, confirm the generated worktrees still work
- [ ] Confirm .vscode/*.code-workspace is valid JSON and opens correctly
- [ ] Confirm Windows-path and WSL2-path variants both produce sensible settings
- [ ] Run scripts/health-check.sh against the generated project and confirm it passes

Full detail: claude/7-Phase 6 Detailed Breakdown.md
EOF
)"

echo
echo "Done."
