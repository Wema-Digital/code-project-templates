#!/usr/bin/env bash
# git-sync-all.sh — status/push helper across every features/<name> worktree
# branch in a generated project. A generated project can itself have several
# worktree branches (one per included template), so checking/pushing them
# one at a time gets old fast.
#
# Usage:
#   git-sync-all.sh          # show git status --short for every worktree
#   git-sync-all.sh push     # push origin <branch> for every CLEAN worktree,
#                             # skipping (and reporting) any that are dirty
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FEATURES_DIR="$ROOT/features"
MODE="${1:-status}"

if [ ! -d "$FEATURES_DIR" ]; then
  echo "error: $FEATURES_DIR not found — run this from a generated project root" >&2
  exit 1
fi

if [ "$MODE" != "status" ] && [ "$MODE" != "push" ]; then
  echo "usage: $0 [status|push]" >&2
  exit 1
fi

SKIPPED_DIRTY=()

for dir in "$FEATURES_DIR"/*/; do
  name="$(basename "$dir")"
  branch="$(git -C "$dir" rev-parse --abbrev-ref HEAD)"
  echo "== $name ($branch) =="
  status="$(git -C "$dir" status --short)"

  if [ -n "$status" ]; then
    echo "$status"
  else
    echo "  clean"
  fi

  if [ "$MODE" = "push" ]; then
    if [ -n "$status" ]; then
      echo "  skipping push: uncommitted changes"
      SKIPPED_DIRTY+=("$name")
    else
      git -C "$dir" push origin "$branch"
    fi
  fi
done

if [ "$MODE" = "push" ] && [ "${#SKIPPED_DIRTY[@]}" -gt 0 ]; then
  echo
  echo "Skipped (dirty, not pushed): ${SKIPPED_DIRTY[*]}"
  exit 1
fi
