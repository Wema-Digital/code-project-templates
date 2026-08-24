# CLAUDE.md — wsl-scripts

This is the **WSL/Bash utility scripts template** of the `coding-project-templates` library. It lives on branch `wsl-tools` and is checked out as a git worktree at `features/wsl-scripts` within the root repo.

## Role of this template

`wsl-scripts` provides a starter scaffold for collections of Bash/shell scripts designed to run in WSL (Windows Subsystem for Linux) or any Linux environment. It extends the language-agnostic base (`claude-code-basic`, branch `claude-code-b`) with shell-specific structure and tooling for writing, testing, and linting Bash scripts.

## Stack

- **Shell**: Bash (WSL / Linux)
- **Linting**: ShellCheck
- **Testing**: bats-core (Bash Automated Testing System)
- **CI**: GitHub Actions — ShellCheck + bats on push

This template has **no `requirements.txt` or `.python-version`** — those were leftover from the generic stub and have been removed. Shell has no package manifest; required tools are documented in `DEPENDENCIES.md` instead.

## Shell conventions this template enforces

- **Shebang**: `#!/usr/bin/env bash` on every script (not `sh` — scripts use Bash features: arrays, `[[ ]]`, `local`)
- **`set -euo pipefail`** at the top of every script — fail fast, no silent errors, no unset variables
- **Functions do the work, `main()` is a thin entrypoint**, guarded so the script is sourceable for tests:
  ```bash
  if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
      main "$@"
  fi
  ```
- **Must pass `shellcheck` clean** before committing — no `# shellcheck disable=` without a comment explaining why

## Project layout

```
scripts/
  check-env.sh    ← example script: verifies required CLI tools are installed, reports versions
tests/
  check-env.bats  ← bats-core tests, sourcing check-env.sh's functions directly (main() doesn't run when sourced)
.github/
  workflows/
    shellcheck.yml ← CI: shellcheck job (lints scripts/*.sh) + bats job (runs tests/)
DEPENDENCIES.md    ← required tools: bash 5+ to run scripts; shellcheck + bats-core to develop/test
```

## What this template contains

| File | Purpose |
|---|---|
| `todo.md` | Shell-scripts-specific task tracking template |
| `README.md` | Guide to using this template with Claude Code, incl. when to use this vs. `python-scripts` |
| `DEPENDENCIES.md` | No package manifest for shell — tools documented here instead |
| `.claude/plan.md` | Phase 5 plan for this template, and what was deliberately deferred |
| `CLAUDE.md` | This file |

## Key patterns

**Testing a script without running it** — `tests/check-env.bats`'s `setup()` does `load "${BATS_TEST_DIRNAME}/../scripts/check-env.sh"`, which sources the script. Because `main` is guarded by the `BASH_SOURCE` check above, sourcing doesn't execute it — only the function definitions load, so tests call `command_exists`/`check_tool` directly via bats' `run`.

**Not every script needs a `.bats` file** — pure glue with no branching logic is adequately covered by `shellcheck` alone (per the breakdown's suggested improvement: add `bats-core` only "if the example script has real logic worth testing beyond linting"). `check-env.sh` earned one because it has real branching (tool found vs. missing) worth asserting on.

**Deliberately not built yet** (see `todo.md` for the full list): `scripts/lib/` shared helpers (add once two scripts duplicate logic, not before), a second example script, a shared logging helper.

## Repo conventions (from root CLAUDE.md)

- **Commits** on this branch: `phase 5 intermediate: <what changed>` or `feat: <what changed>`
- **Push** to `origin wsl-tools` from inside this worktree
- **Planning notes** live in the root repo's `claude/` folder (numbered `N-Title.md`), not here
- **GitHub Project**: [Wema-Digital/projects/2](https://github.com/orgs/Wema-Digital/projects/2) — mark tasks Done after committing

## Receiving base updates

When `claude-code-basic` is updated, merge changes into this branch:

```bash
cd features/wsl-scripts   # branch wsl-tools
git merge claude-code-b
git push origin wsl-tools
```
