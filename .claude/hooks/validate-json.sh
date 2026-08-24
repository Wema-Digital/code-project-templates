#!/usr/bin/env bash
# PostToolUse hook: after Claude edits or writes a JSON file under .claude/,
# check it actually parses. Wired up via the "PostToolUse" entry in
# .claude/settings.json (matcher: "Edit|Write").
#
# Reads the hook payload as JSON on stdin (session_id, tool_name, tool_input,
# etc. — see https://code.claude.com/docs/en/hooks). Exit 2 on PostToolUse
# surfaces stderr back to Claude as feedback, so it can go fix what it just
# broke, instead of only failing silently until the next CI run.
set -euo pipefail

payload="$(cat)"
file_path="$(python3 -c 'import json, sys; print(json.load(sys.stdin).get("tool_input", {}).get("file_path", ""))' <<< "$payload")"

case "$file_path" in
  *.claude/*.json)
    if ! python3 -m json.tool "$file_path" > /dev/null 2>&1; then
      echo "⚠ $file_path is not valid JSON." >&2
      exit 2
    fi
    ;;
esac

exit 0
