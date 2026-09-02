#!/usr/bin/env bash
# setup-env.sh — create this project's Python environment and install the
# dependencies of whichever templates got included. Run from the project root.
#
# Default: ONE shared virtualenv at <root>/.venv, every Python component
# installed into it (editable where it ships a pyproject.toml). This matches how
# coding-project-templates itself works and what the generated .code-workspace
# points python.defaultInterpreterPath at.
#
#   --isolated   give each features/<name>/ its own .venv instead — use only
#                when a component's dependencies genuinely conflict with another's
#
# uv is used when it's on PATH (much faster); otherwise python3 -m venv + pip.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FEATURES_DIR="$ROOT/features"
SHARED_VENV="$ROOT/.venv"
ISOLATED=0

for arg in "$@"; do
  case "$arg" in
    --isolated) ISOLATED=1 ;;
    -h|--help)
      echo "usage: scripts/setup-env.sh [--isolated]"
      echo "  (default) one shared .venv at the project root"
      echo "  --isolated  one .venv per features/<name>/"
      exit 0 ;;
    *) echo "unknown option: $arg (try --help)" >&2; exit 2 ;;
  esac
done

if [ ! -d "$FEATURES_DIR" ]; then
  echo "error: $FEATURES_DIR not found — run this from a generated project root" >&2
  exit 1
fi

HAVE_UV=0
command -v uv >/dev/null 2>&1 && HAVE_UV=1

# bin/ on POSIX, Scripts/ on a Windows-layout venv
venv_bindir() {
  if [ -d "$1/Scripts" ]; then echo "$1/Scripts"; else echo "$1/bin"; fi
}

make_venv() {  # $1 = venv path (no-op if it already exists)
  [ -d "$1" ] && return 0
  if [ "$HAVE_UV" -eq 1 ]; then uv venv "$1"; else python3 -m venv "$1"; fi
}

pip_into() {  # $1 = venv path; rest = pip install args
  local venv="$1"; shift
  if [ "$HAVE_UV" -eq 1 ]; then
    uv pip install -q --python "$(venv_bindir "$venv")/python" "$@"
  else
    "$(venv_bindir "$venv")/pip" install --quiet "$@"
  fi
}

py_component() {  # $1 = component dir; 0 if it has any Python manifest
  [ -f "$1/requirements-dev.txt" ] || [ -f "$1/requirements.txt" ] || [ -f "$1/pyproject.toml" ]
}

install_python() {  # $1 = component dir, $2 = venv path
  local dir="$1" venv="$2"
  if [ -f "$dir/requirements-dev.txt" ]; then
    echo "   requirements-dev.txt"
    pip_into "$venv" -r "$dir/requirements-dev.txt"
  elif [ -f "$dir/requirements.txt" ]; then
    echo "   requirements.txt"
    pip_into "$venv" -r "$dir/requirements.txt"
  elif [ -f "$dir/pyproject.toml" ]; then
    echo "   pyproject.toml (editable)"
    pip_into "$venv" -e "$dir[dev]" 2>/dev/null || pip_into "$venv" -e "$dir"
  fi
}

if [ "$ISOLATED" -eq 0 ]; then
  NEED_PY=0
  for dir in "$FEATURES_DIR"/*/; do py_component "$dir" && NEED_PY=1; done
  if [ "$NEED_PY" -eq 1 ]; then
    echo "== Shared virtualenv: $SHARED_VENV  (uv: $([ "$HAVE_UV" -eq 1 ] && echo yes || echo no)) =="
    make_venv "$SHARED_VENV"
    [ "$HAVE_UV" -eq 0 ] && pip_into "$SHARED_VENV" --upgrade pip
  fi
fi

echo "== Components under $FEATURES_DIR =="
for dir in "$FEATURES_DIR"/*/; do
  dir="${dir%/}"
  name="$(basename "$dir")"
  if [ -f "$dir/package.json" ]; then
    echo "-- $name: Node (package.json)"
    ( cd "$dir" && npm install --silent )
  elif py_component "$dir"; then
    if [ "$ISOLATED" -eq 1 ]; then
      echo "-- $name: Python -> $dir/.venv"
      make_venv "$dir/.venv"
      [ "$HAVE_UV" -eq 0 ] && pip_into "$dir/.venv" --upgrade pip
      install_python "$dir" "$dir/.venv"
    else
      echo "-- $name: Python -> shared .venv"
      install_python "$dir" "$SHARED_VENV"
    fi
  else
    echo "-- $name: no known dependency manifest, skipping"
  fi
done

echo
if [ "$ISOLATED" -eq 0 ] && [ -d "$SHARED_VENV" ]; then
  echo "Done. Shared env:  $(venv_bindir "$SHARED_VENV")/python"
  echo "Activate with:     source $(venv_bindir "$SHARED_VENV")/activate"
else
  echo "Done. See each features/<name>/README.md for anything setup-env.sh doesn't cover."
fi
