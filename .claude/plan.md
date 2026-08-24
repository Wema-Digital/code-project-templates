> **Status**: Executed 2026-08-24 (Phase 5 — Intermediate Templates). Supersedes the base-template plan below, which was scoped to the generic `claude-code-basic` stub this template started from.

## Context

`wsl-scripts` was carrying the language-agnostic base template verbatim (generic `todo.md`, generic `README.md`) plus a stray Python `requirements.txt` and `.python-version` left over from the stub — misleading in a shell template, the same class of leftover that `js-express` had to clean up in Phase 5. The GitHub Project task "Bring wsl-scripts to intermediate" (Phase 5) calls for one real `.sh` script and ShellCheck CI, per `claude/5-Phase 5 Detailed Breakdown.md`.

## Goal

One genuinely runnable example script, passing ShellCheck clean, plus CI. Per the breakdown's suggested improvement, add `bats-core` tests too, since the chosen example (an environment/dependency checker) has real logic worth testing beyond linting.

## What was built

- Removed `requirements.txt` and `.python-version` — this is not a Python template
- `scripts/check-env.sh` — checks a list of CLI tools are installed and reports their versions (`command_exists()`, `tool_version()`, `check_tool()`, `main()`); `set -euo pipefail`, and a `[[ "${BASH_SOURCE[0]}" == "${0}" ]]` guard around `main` so the script's functions can be sourced and tested without running it
- `tests/check-env.bats` — 4 bats-core tests on `command_exists()`/`check_tool()`, sourcing the script rather than shelling out to it
- `DEPENDENCIES.md` — the shell equivalent of a manifest: what's needed to run scripts (bash 5+) vs. develop/test in this repo (shellcheck, bats-core)
- `.github/workflows/shellcheck.yml` — two jobs: `shellcheck` (lints `scripts/*.sh`) and `bats` (runs `tests/`), each installing its own tool fresh via `apt-get` rather than assuming it's preinstalled on the runner or pinning a third-party action
- `.gitignore` — replaced the all-Python one with a minimal shell-appropriate version
- `README.md`, `todo.md`, `CLAUDE.md` — rewritten shell-specific (replacing the generic base-template copies)

## Deliberately deferred (left as `todo.md` items, not built now)

- `scripts/lib/` shared helpers — the earlier draft of `CLAUDE.md` mentioned a `utils.sh`; not built because there's only one script so far and nothing to share yet
- `.env.example` — no script needs config; skipped per spec rather than shipping an empty file
- A second example script — one is enough to establish the convention

## Verification

- `shellcheck scripts/check-env.sh` — clean, no warnings
- `bats tests/check-env.bats` — 4/4 passing
- `./scripts/check-env.sh` and `./scripts/check-env.sh git totally-not-a-real-tool` both run correctly (exit 0 vs. exit 1 with a MISSING line)
