#!/usr/bin/env bash
# sync-templates.sh — pulls upstream improvements from coding-project-templates
# into this generated project's own branches, for when a template gets
# improved after this project was generated. Fast-forward only: a diverged
# branch is reported, not silently merged, so you decide how to reconcile it.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GIT_STORE="$ROOT/.git-store"
FEATURES_DIR="$ROOT/features"

if [ ! -d "$GIT_STORE" ]; then
  echo "error: $GIT_STORE not found — run this from a generated project root" >&2
  exit 1
fi

echo "== Fetching from origin ($(git -C "$GIT_STORE" remote get-url origin)) =="
# Explicit refspec, not just `fetch origin`: a bare clone's "origin" remote
# has no fetch refspec configured by git itself, and a project generated
# before this was discovered would still be missing it in its stored config.
# Passing the refspec here works regardless of what's actually stored.
git -C "$GIT_STORE" fetch origin '+refs/heads/*:refs/remotes/origin/*'

UP_TO_DATE=()
UPDATED=()
DIVERGED=()

for dir in "$FEATURES_DIR"/*/; do
  name="$(basename "$dir")"
  branch="$(git -C "$dir" rev-parse --abbrev-ref HEAD)"

  if ! git -C "$GIT_STORE" show-ref --verify --quiet "refs/remotes/origin/$branch"; then
    echo "-- $name ($branch): no matching origin/$branch, skipping"
    continue
  fi

  before="$(git -C "$dir" rev-parse HEAD)"
  if git -C "$dir" merge --ff-only "origin/$branch" > /dev/null 2>&1; then
    after="$(git -C "$dir" rev-parse HEAD)"
    if [ "$before" = "$after" ]; then
      echo "-- $name ($branch): up to date"
      UP_TO_DATE+=("$name")
    else
      echo "-- $name ($branch): fast-forwarded $before -> $after"
      UPDATED+=("$name")
    fi
  else
    echo "-- $name ($branch): diverged from origin/$branch, needs a manual merge"
    DIVERGED+=("$name")
  fi
done

echo
echo "== Summary =="
echo "Up to date: ${UP_TO_DATE[*]:-none}"
echo "Updated:    ${UPDATED[*]:-none}"
echo "Diverged:   ${DIVERGED[*]:-none}"

[ "${#DIVERGED[@]}" -eq 0 ]
