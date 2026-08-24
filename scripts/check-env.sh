#!/usr/bin/env bash
# check-env.sh — verify required CLI tools are installed and report their versions.
#
# Usage:
#   scripts/check-env.sh                  # check the default tool list
#   scripts/check-env.sh git python3 gh   # check a specific list of tools
#
# Exits non-zero if any checked tool is missing.
set -euo pipefail

DEFAULT_TOOLS=(git bash curl)

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

tool_version() {
    local tool="$1"
    "$tool" --version 2>&1 | head -n 1
}

check_tool() {
    local tool="$1"
    if command_exists "$tool"; then
        echo "OK       $tool — $(tool_version "$tool")"
        return 0
    else
        echo "MISSING  $tool"
        return 1
    fi
}

main() {
    local tools=("$@")
    if [[ ${#tools[@]} -eq 0 ]]; then
        tools=("${DEFAULT_TOOLS[@]}")
    fi

    local missing=0
    for tool in "${tools[@]}"; do
        check_tool "$tool" || missing=$((missing + 1))
    done

    if [[ "$missing" -gt 0 ]]; then
        echo "Error: $missing required tool(s) missing" >&2
        exit 1
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
