#!/usr/bin/env bash
# repair-worktrees.sh — run after moving or renaming this generated project.
#
# git worktree links are absolute paths on both sides (the worktree's own
# .git file, and .git-store/worktrees/<name>/gitdir), so moving this folder
# breaks every features/<name> worktree until those links are repointed.
# `git worktree repair` fixes both sides in one pass. Confirmed by hand
# during Phase 6 Card 2: move a generated project, every `git status` inside
# features/<name> fails with "not a git repository" until this runs.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GIT_STORE="$ROOT/.git-store"
FEATURES_DIR="$ROOT/features"

if [ ! -d "$GIT_STORE" ]; then
  echo "error: $GIT_STORE not found — run this from a generated project root" >&2
  exit 1
fi

paths=()
for dir in "$FEATURES_DIR"/*/; do
  paths+=("${dir%/}")
done

git -C "$GIT_STORE" worktree repair "${paths[@]}"
echo "Repaired ${#paths[@]} worktree(s)."
