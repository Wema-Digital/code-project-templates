#!/usr/bin/env bash
# setup-env.sh — bootstraps whichever languages actually got included in this
# generated project, instead of assuming Python. Run from the project root
# (the folder this script's own parent scripts/ lives in).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FEATURES_DIR="$ROOT/features"

if [ ! -d "$FEATURES_DIR" ]; then
  echo "error: $FEATURES_DIR not found — run this from a generated project root" >&2
  exit 1
fi

echo "== Setting up environments under $FEATURES_DIR =="

for dir in "$FEATURES_DIR"/*/; do
  name="$(basename "$dir")"

  if [ -f "$dir/requirements-dev.txt" ]; then
    echo "-- $name: Python (requirements-dev.txt, includes requirements.txt + test tooling)"
    python3 -m venv "$dir/.venv"
    "$dir/.venv/bin/pip" install --quiet --upgrade pip
    "$dir/.venv/bin/pip" install --quiet -r "$dir/requirements-dev.txt"

  elif [ -f "$dir/requirements.txt" ]; then
    echo "-- $name: Python (requirements.txt)"
    python3 -m venv "$dir/.venv"
    "$dir/.venv/bin/pip" install --quiet --upgrade pip
    "$dir/.venv/bin/pip" install --quiet -r "$dir/requirements.txt"

  elif [ -f "$dir/pyproject.toml" ]; then
    echo "-- $name: Python (pyproject.toml)"
    python3 -m venv "$dir/.venv"
    "$dir/.venv/bin/pip" install --quiet --upgrade pip
    if "$dir/.venv/bin/pip" install --quiet -e "$dir[dev]" 2>/dev/null; then
      :
    else
      "$dir/.venv/bin/pip" install --quiet -e "$dir"
    fi

  elif [ -f "$dir/package.json" ]; then
    echo "-- $name: Node (package.json)"
    (cd "$dir" && npm install --silent)

  else
    echo "-- $name: no known dependency manifest, skipping"
  fi
done

echo
echo "Done. See each features/<name>/README.md for anything setup-env.sh doesn't cover."
