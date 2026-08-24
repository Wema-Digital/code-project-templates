# wsl-scripts — Shell Scripting Starter for WSL/Linux

> A loose collection of standalone Bash scripts for WSL/Linux automation — the shell counterpart to `python-scripts`.
> Clone, run, and have a working ShellCheck-clean script with bats tests and CI in minutes.

---

## When to Use This vs. `python-scripts`

Reach for `wsl-scripts` when the task is genuinely shell-shaped: process orchestration, file/environment checks, wrapping other CLI tools, one-liners that would be silly to write in Python. Reach for [`python-scripts`](../python-scripts) instead once there's real data wrangling, JSON/CSV parsing, or logic complex enough that Bash's error-handling starts to hurt more than it helps.

---

## Quick Start

```bash
# No package manifest to install — shell has no runtime deps of its own.
# See DEPENDENCIES.md for what's needed to run vs. develop/test.

# Run the example script
./scripts/check-env.sh
# → OK       git — git version 2.43.0
#   OK       bash — GNU bash, version 5.2.21(1)-release ...
#   OK       curl — curl 8.5.0 ...

# Check a specific list of tools instead of the default
./scripts/check-env.sh git python3 gh
```

---

## Project Layout

```
wsl-scripts/
├── scripts/
│   └── check-env.sh       # Example: verifies required CLI tools are installed
├── tests/
│   └── check-env.bats      # bats-core tests, sourcing check-env.sh's functions directly
├── .github/
│   └── workflows/
│       └── shellcheck.yml   # CI: shellcheck job + bats job
├── DEPENDENCIES.md          # No package manifest for shell — tools documented here instead
├── CLAUDE.md                # Claude Code context for this template
└── todo.md                  # Task tracking template (symbol system)
```

---

## Script Conventions

Every script in this collection follows the same shape:

```bash
#!/usr/bin/env bash
# script-name.sh — one-line description.
# Usage: scripts/script-name.sh [args]
set -euo pipefail

do_the_thing() {
    ...  # the real logic — this is what gets tested
}

main() {
    do_the_thing "$@"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

- `set -euo pipefail` — fail fast, no silent errors, no unset variables
- Functions do the real work; `main()` is a thin entrypoint
- The `BASH_SOURCE` guard means a test file can `load` the script (source it) to call its functions directly, without `main` running

Every script must pass `shellcheck` clean before it's committed.

---

## Testing

```bash
shellcheck scripts/*.sh    # static analysis — required, catches most bugs before they run
bats tests/                # behavioural tests, for scripts with real logic worth testing
```

Not every script needs a `.bats` file — a script that's pure glue with no branching logic is adequately covered by `shellcheck` alone. Add a bats file once a script has functions worth asserting on, following `tests/check-env.bats`:

```bash
setup() {
    load "${BATS_TEST_DIRNAME}/../scripts/check-env.sh"
}

@test "command_exists returns success for a real command" {
    run command_exists bash
    [ "$status" -eq 0 ]
}
```

---

## Working with Claude Code

This template follows the same `todo.md` task-tracking convention as `claude-code-basic`.
See `todo.md` for the full symbol system and task breakdown.

Useful prompts to get started:
- *"Read todo.md and help me add a new script following the check-env.sh convention."*
- *"Write bats tests for the new script's functions."*
- *"Review this script against shellcheck output before I commit."*

---

**Template Version**: 1.0
**Last Updated**: 2026-08-24
**Branch**: `wsl-tools` | **Stack**: Bash 5 + ShellCheck + bats-core
