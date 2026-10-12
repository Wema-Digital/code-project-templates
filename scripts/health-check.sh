#!/usr/bin/env bash
# health-check.sh — smoke-tests that each included template's own test suite
# still passes. Run after setup-env.sh (and again after sync-templates.sh).
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FEATURES_DIR="$ROOT/features"

if [ ! -d "$FEATURES_DIR" ]; then
  echo "error: $FEATURES_DIR not found — run this from a generated project root" >&2
  exit 1
fi

FAILED=()
SKIPPED=()

echo "== Health-checking templates under $FEATURES_DIR =="

for dir in "$FEATURES_DIR"/*/; do
  name="$(basename "$dir")"

  # Per-worktree venv (setup-env.sh --isolated) wins; otherwise the shared
  # root .venv that setup-env.sh builds by default.
  venv_bin=""
  if [ -d "$dir/.venv/bin" ]; then venv_bin="$dir/.venv/bin"
  elif [ -d "$ROOT/.venv/bin" ]; then venv_bin="$ROOT/.venv/bin"
  fi

  if [ -n "$venv_bin" ] && [ -f "$venv_bin/pytest" ] && [ -d "$dir/tests" ]; then
    echo "-- $name: pytest"
    if (cd "$dir" && "$venv_bin/pytest" -q); then
      echo "   PASS"
    else
      echo "   FAIL"
      FAILED+=("$name")
    fi

  elif [ -n "$venv_bin" ] && [ -f "$venv_bin/mkdocs" ] && [ -f "$dir/mkdocs.yml" ]; then
    echo "-- $name: mkdocs build --strict"
    if (cd "$dir" && "$venv_bin/mkdocs" build --strict -q); then
      echo "   PASS"
    else
      echo "   FAIL"
      FAILED+=("$name")
    fi

  elif [ -f "$dir/package.json" ] && grep -q '"test"' "$dir/package.json"; then
    echo "-- $name: npm test"
    if (cd "$dir" && npm test --silent); then
      echo "   PASS"
    else
      echo "   FAIL"
      FAILED+=("$name")
    fi

  elif compgen -G "$dir/tests/*.bats" > /dev/null 2>&1; then
    if command -v bats >/dev/null 2>&1; then
      echo "-- $name: bats"
      if (cd "$dir" && bats tests/); then
        echo "   PASS"
      else
        echo "   FAIL"
        FAILED+=("$name")
      fi
    else
      echo "-- $name: bats tests found but 'bats' isn't installed, skipping"
      SKIPPED+=("$name")
    fi

  else
    echo "-- $name: no known test setup, skipping"
    SKIPPED+=("$name")
  fi
done

echo
echo "== Summary =="
echo "Skipped: ${SKIPPED[*]:-none}"
if [ "${#FAILED[@]}" -eq 0 ]; then
  echo "All checked templates passed."
  exit 0
else
  echo "Failed: ${FAILED[*]}"
  exit 1
fi
