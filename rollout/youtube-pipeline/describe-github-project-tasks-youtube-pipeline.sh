#!/usr/bin/env bash
# describe-github-project-tasks-youtube-pipeline.sh
# Phase 0 follow-up for claude/1-YouTube-Pipeline-Workspace-Plan.md.
#
# setup-github-project-youtube-pipeline.sh seeds 19 draft items with one-line
# titles only. This script fills in a body/description for each, matched by a
# substring of its title (robust to PVTI_/DI_ id churn from re-creating the
# board). Same mechanism as the repo's scripts/update-github-project-phase6.sh.
#
# Idempotent: re-running overwrites each body with the same text.
# It also retitles item 1 (drops the now-obsolete "branch protection" clause).
#
# updateProjectV2DraftIssue rejects a body-only edit with "Title can't be blank",
# so every edit re-sends the title alongside the body.
#
# Requires: gh (authenticated), jq.

set -euo pipefail

OWNER="Wema-Digital"
PROJECT_NUMBER="${1:-3}"

command -v jq >/dev/null || { echo "jq is required (apt install jq)"; exit 1; }

PROJECT_ID=$(gh project list --owner "$OWNER" --format json \
  | jq -r --argjson n "$PROJECT_NUMBER" '.projects[] | select(.number == $n) | .id')
[ -n "$PROJECT_ID" ] && [ "$PROJECT_ID" != "null" ] || { echo "project #$PROJECT_NUMBER not found under $OWNER"; exit 1; }

ITEMS_JSON=$(gh api graphql -f query="
query {
  node(id: \"$PROJECT_ID\") {
    ... on ProjectV2 {
      items(first: 100) {
        nodes { content { ... on DraftIssue { id title } } }
      }
    }
  }
}" | jq '.data.node.items.nodes | map(.content) | map(select(. != null))')

find_id()    { echo "$ITEMS_JSON" | jq -r --arg p "$1" '.[] | select((.title // "") | contains($p)) | .id'    | head -n1; }
find_title() { echo "$ITEMS_JSON" | jq -r --arg p "$1" '.[] | select((.title // "") | contains($p)) | .title' | head -n1; }

# set_body <title-substring> <body> [title-override]
set_body() {
  local pattern="$1" body="$2" title_override="${3:-}"
  local id title
  id=$(find_id "$pattern")
  if [ -z "$id" ] || [ "$id" = "null" ]; then
    echo "  SKIP: no item title contains \"$pattern\""
    return
  fi
  title="${title_override:-$(find_title "$pattern")}"
  gh project item-edit --id "$id" --title "$title" --body "$body" > /dev/null
  echo "  described: $pattern"
}

echo "== Set titles + bodies on project #$PROJECT_NUMBER =="

# ---------- Phase 0 ----------
set_body "setup-github-repo-youtube-pipeline.sh" "$(cat <<'EOF'
**Status: DONE 2026-08-29.**

Creates `Wema-Digital/youtube-pipeline` — private, empty, wiki disabled. The
default branch resolves to `main` on the first push (Phase 2.2), not before.

**Branch protection is intentionally NOT applied.** `Wema-Digital` is on GitHub's
free plan, which allows neither branch-protection rules nor rulesets on *private*
repos ("Upgrade to GitHub Pro or make this repository public"). Decision
2026-08-29: keep the repo private, accept no protection; revisit only if the org
upgrades to Team.

Script: `rollout/youtube-pipeline/setup-github-repo-youtube-pipeline.sh`
Plan: Phase 0.1
EOF
)" "Run setup-github-repo-youtube-pipeline.sh (create repo, main default)"

set_body "create the Project board and Phase field" "$(cat <<'EOF'
**Status: DONE 2026-08-29.**

`setup-github-project-youtube-pipeline.sh` created this board (#3), linked it to
`Wema-Digital/youtube-pipeline`, added the `Phase` single-select field
(options Phase 0-4) and seeded all 19 task items, each tagged with its phase.

Re-running the script creates a *second* board with the same title — delete the
old one in the browser if a clean redo is needed.

Script: `rollout/youtube-pipeline/setup-github-project-youtube-pipeline.sh`
Plan: Phase 0.2
EOF
)"

set_body "Verify structure" "$(cat <<'EOF'
**Status: DONE 2026-08-29.**

`gh repo view` + `gh project view 3 --owner Wema-Digital` confirm:
- repo is private and empty
- `Phase` field has exactly 5 options (Phase 0 ... Phase 4)
- 19 items, distributed 3 / 2 / 5 / 6 / 3 across the phases — matches the seed script

Same "check project structure" verification already used for
`coding-project-templates`' own GitHub Project.

Plan: Phase 0.3
EOF
)"

# ---------- Phase 1 ----------
set_body "DRAFT-READY (all open items resolved)" "$(cat <<'EOF'
**Status: DONE 2026-08-29.**

Both open items resolved:
1. **Template collision** — fixed by `NAME:ALIAS` support in
   `generate-workspace.py` (same template can back multiple `features/<alias>`
   folders). See `.claude/plan.md`'s NAME:ALIAS addendum.
2. **notion-integration scope** — it's a general Notion-API interaction layer for
   Notion workspaces, not yet fully developed; goes in as a scaffold. Template
   locked to `python-app:notion-integration-app` +
   `claude-code-basic:notion-integration-agent` (`python-app` over
   `python-scripts` because real package structure is expected as it grows).

Spec status line flipped `NEEDS-INPUT` -> `DRAFT-READY`. `--dry-run` confirms all
6 worktrees resolve.

Plan: Phase 1.1-1.2
EOF
)"

set_body "Human review + sign-off" "$(cat <<'EOF'
Final human review of the finished spec **before anything is written to disk**.

Check:
- the 6 template rows (`templates:` block)
- `output_path: /mnt/w/wema-studio/vscode_workspace/you_tube`
- `project_name: youtube-pipeline`
- `target: wsl2`

This is the deliberate gap between spec and build — the chance to correct a
misread requirement before any files exist in the output path.

Plan: Phase 1.3
EOF
)"

# ---------- Phase 2 ----------
set_body "Run generate-workspace.py --spec" "$(cat <<'EOF'
From `features/vscode-workspace-gen`:

    /usr/bin/python3 scripts/generate-workspace.py --spec claude/1-YouTube-Pipeline-Workspace-Plan.md --dry-run
    /usr/bin/python3 scripts/generate-workspace.py --spec claude/1-YouTube-Pipeline-Workspace-Plan.md

(Use `/usr/bin/python3` — it has PyYAML; the repo `.venv` python does not.)

Produces `<output>/` with: `.git-store/` bare clone, 6 `features/<alias>/`
worktrees, `.vscode/youtube-pipeline.code-workspace`, `README.md` / `CLAUDE.md` /
`todo.md`, `.workspace-manifest.json`, `.gitignore`, and the copied helper
scripts.

Refuses a non-empty output dir without `--force` — `ls
/mnt/w/wema-studio/vscode_workspace/you_tube` first (only
`coding-project-templates` is connected in the Claude session, not
`wema-studio`).

Before writing `.vscode/*.code-workspace`: re-check current VS Code docs for the
settings keys in use, and confirm target = wsl2 handling.

Plan: Phase 2.1
EOF
)"

set_body "git remote add origin" "$(cat <<'EOF'
After generation, wire the Phase 0 repo onto the bundled bare clone and push
every selected template branch:

    cd <output>/.git-store
    git remote add origin git@github.com:Wema-Digital/youtube-pipeline.git
    git push origin --all

The bare clone already carries full per-branch history (confirmed in Card 3's
portability test). Branches pushed: `claude-code-a`, `py-script`,
`claude-code-b`, `py-app` — note `claude-code-b` and `py-app` each back two
worktrees but are still one branch apiece.

Plan: Phase 2.2
EOF
)"

set_body "Run scripts/health-check.sh against the generated output" "$(cat <<'EOF'
From the generated output root:

    scripts/setup-env.sh      # bootstrap deps for whichever languages got included
    scripts/health-check.sh   # smoke-test each included template's own test suite

`health-check.sh` was passing clean against a real generated project in Card 3.

Plan: Phase 2.3
EOF
)"

set_body "Note repair-worktrees.sh in the generated README/todo" "$(cat <<'EOF'
`generate-workspace.py` already writes the "if you move or rename this folder,
run `scripts/repair-worktrees.sh` first" note into the generated `README.md` and
`todo.md` automatically. This item is just to confirm that text is present and
correct after generation.

Why it matters: git worktree links are absolute paths on *both* ends (the bare
store's `worktrees/<name>/gitdir` and each `features/<alias>/.git` file). Moving
the output breaks every worktree ("not a git repository") until repaired. This is
standard git behaviour, not specific to this generator.

Plan: Phase 2.4
EOF
)"

set_body "create the plain non-git folders" "$(cat <<'EOF'
`generate-workspace.py` only creates `features/<alias>` worktrees plus its
standard docs and scripts. The ownership map's `_templates/`, `_pipeline-docs/`
and `_raw-exports/` are explicitly **not** worktrees — `_raw-exports/` in
particular needs a fixed path outside git so every isolated worktree run can
reach it.

Create them by hand (or with a short follow-up script) after Build.

Plan: Open items #4
EOF
)"

# ---------- Phase 3 ----------
set_body "00_keyword-intelligence: append_snapshot.py" "$(cat <<'EOF'
Content build-out for the keyword-intelligence component
(`features/keyword-intelligence-agent` + `features/keyword-intelligence-scripts`).

Scope (from the ownership map's "Still outstanding" list + the v8 diagram):
- `append_snapshot.py` (diagram node A3)
- the `<750` Search Volume gate + `Insufficient Volume` tag (A_VOL / A_INSUFF)
- the A5 auto-compute formula, once Search Volume is normalised
- the Claude Code Routine config itself (worktree toggle on, biweekly schedule)

Plan: Phase 3.1
EOF
)"

set_body "build W2 (Series Candidates) and W3 (Singles Tracker) skeletons" "$(cat <<'EOF'
Build the `W2` (Series Candidates Workbook) and `W3` (Singles Tracker Workbook)
skeletons — both flagged "needs to be built" in the ownership map.

Component: `features/production-pipeline-app` (openpyxl workbook builders).

Plan: Phase 3.2
EOF
)"

set_body "find_row() label-scan write-back" "$(cat <<'EOF'
- the `find_row()` label-scan write-back between `S1` and `W1` / `W3`
- the `SEO_CHECK` refresh logic against the Keyword Bank

Component: `features/production-pipeline-app`.

Plan: Phase 3.2
EOF
)"

set_body "A7 lane + health clustering logic" "$(cat <<'EOF'
`A7`'s lane and health clustering logic — still the "unopened box" per the
ownership map, and needed before `C1` (which depends on it) can run for real.

This is a **design task**, not just implementation — it should get its own short
`claude/N-*.md` spec before any code.

Plan: Phase 3.3
EOF
)"

set_body "notion-integration: define its concrete job" "$(cat <<'EOF'
The notion-integration worktrees — `features/notion-integration-app` (on
`python-app`) + `features/notion-integration-agent` (on `claude-code-basic`) — go
in at Build as a **scaffold**.

Phase 3 work: define the concrete job — what it reads/writes in a Notion
workspace via the `notion-client` library, and where (if anywhere) it plugs into
the v8 flow — then build the API calls and the driving agent. Likely wants its
own short spec first.

Plan: Phase 3.4
EOF
)"

set_body "OPT1 (Unclaimed Backlog sheet)" "$(cat <<'EOF'
`OPT1` (Unclaimed Backlog sheet) — still an open yes/no per the ownership map,
independent of everything else in this plan. Decide whether to include it.

Plan: Phase 3.5
EOF
)"

# ---------- Phase 4 ----------
set_body "Run doc-sync-checker against the generated output" "$(cat <<'EOF'
Once Phase 3 content exists, run the `doc-sync-checker` subagent against the
generated output to catch drift between what `README.md` / `CLAUDE.md` /
`todo.md` claim and what's actually on disk — the same check
`vscode-workspace-gen` ran on itself during Card 1.

Plan: Phase 4.1
EOF
)"

set_body "Apply the four-item artefact checklist" "$(cat <<'EOF'
Apply the four-item artefact checklist already tracked for
`coding-project-templates` itself to this new repo:
- GitHub Project — DONE (Phase 0)
- VS Code Workspace — Phase 2
- GitHub Repository — DONE (Phase 0)
- Claude Cowork Project — see the next item

Plan: Phase 4.2
EOF
)"

set_body "needs its own Claude Cowork Project or shares one" "$(cat <<'EOF'
The Claude Cowork Project is a plugin and is explicitly not built yet even for
`coding-project-templates` itself. Decide separately whether `youtube-pipeline`
needs its own or can share one.

Plan: Phase 4.2
EOF
)"

echo
echo "Done. Board: https://github.com/orgs/$OWNER/projects/$PROJECT_NUMBER"
