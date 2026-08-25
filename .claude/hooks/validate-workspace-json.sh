#!/usr/bin/env bash
# PostToolUse hook: after Claude edits or writes a *.code-workspace file,
# check it actually parses. Wired up via the "PostToolUse" entry in
# .claude/settings.json (matcher: "Edit|Write"), alongside validate-json.sh.
#
# Distinct from validate-json.sh: that one checks this template's own
# .claude/*.json config; this one checks the *generated output* workspace
# file, for the case where a session hand-edits it directly with the Edit/
# Write tool instead of going through scripts/generate-workspace.py (which
# already self-checks what it writes). Directly motivated by the JSON syntax
# bug already found in this repo's own committed coding-project-templates.code-workspace.
set -euo pipefail

payload="$(cat)"
file_path="$(python3 -c 'import json, sys; print(json.load(sys.stdin).get("tool_input", {}).get("file_path", ""))' <<< "$payload")"

case "$file_path" in
  *.code-workspace)
    if ! python3 -m json.tool "$file_path" > /dev/null 2>&1; then
      echo "⚠ $file_path is not valid JSON." >&2
      exit 2
    fi
    ;;
esac

exit 0
