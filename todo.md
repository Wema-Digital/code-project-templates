# Todo — wsl-scripts

> Shell script collection tasks. Uses the same symbol system as the base template.
> See the Symbol Guide below for reference.

## Symbol Guide

| Symbol | Meaning | When to use with Claude |
|--------|---------|-------------------------|
| `[ ]` | Unstarted | Default for all new tasks |
| `[x]` | Completed | Ask Claude to mark tasks done |
| `[-]` | In-progress | Claude marks what it's actively working on |
| `[!]` | High priority | Focus here first |
| `[@]` | Needs discussion | Ask Claude for design input |
| `[?]` | Needs research | Have Claude research options |
| `[#]` | Medium priority | After `[!]` tasks |
| `[~]` | On hold | Skip for now |
| `[>]` | Delegated/deferred | Assigned elsewhere or future |
| `[⚠]` | Critical issue | Urgent bug or blocker |
| `[%]` | % complete | Track large in-progress features |

---

## Project Setup

```markdown
- [x] [!] Initialise git repository and branch (wsl-tools)
- [x] [!] Remove stray requirements.txt / .python-version left from the generic stub — this isn't Python
- [x] [!] DEPENDENCIES.md — documents required tools (bash 5+ to run, shellcheck + bats-core to develop/test)
- [x] Replace the all-Python .gitignore with a minimal shell-appropriate one
- [ ] [@] Decide when this crosses into "should be python-scripts instead" (data wrangling, JSON parsing → probably Python)
```

---

## Scripts

```markdown
- [x] [!] scripts/check-env.sh — checks required CLI tools are installed, reports versions
- [x] [!] set -euo pipefail at the top of every script
- [x] [!] [[ "${BASH_SOURCE[0]}" == "${0}" ]] guard around main() — makes functions sourceable/testable
- [ ] [ ] Add your next real script:
  - [ ] Same shape: functions doing the real work, main() as the thin entrypoint, guarded so it's sourceable
  - [ ] Usage comment block at the top (what it does, example invocations)
  - [ ] Must pass `shellcheck` clean
- [ ] [#] scripts/lib/ shared helpers — only once two scripts actually duplicate logic
- [ ] [@] Decide on an argument-parsing convention once a script needs real flags (getopts vs. manual `case`)
```

---

## Logging & Error Handling

```markdown
- [x] [!] set -euo pipefail convention (fail fast, no silent errors, no unset vars)
- [ ] [#] Shared logging helper (timestamped stderr messages) once more than one script wants it
- [ ] [@] Decide on exit-code convention beyond 0/1 if scripts need to distinguish failure modes
```

---

## Testing

```markdown
- [x] [!] shellcheck as static analysis — every script must pass clean
- [x] [!] tests/check-env.bats — bats-core tests on command_exists()/check_tool(), sourcing the script
- [ ] [!] Add a bats file for each new script that has real logic worth testing beyond linting
- [ ] [~] For scripts that are pure glue with no branching logic, shellcheck alone may be enough — don't force a bats file that just re-tests shellcheck's job
```

**Claude Code for testing:**
```markdown
- [ ] [!] Ask Claude to generate bats tests for any new script's functions
- [ ] [#] Have Claude review a script against shellcheck output before committing
```

---

## CI / Distribution

```markdown
- [x] [!] .github/workflows/shellcheck.yml — shellcheck job (lints scripts/*.sh) + bats job (runs tests/)
- [ ] [@] Decide how scripts get distributed/run in practice (curl | bash from a release? checked out directly? cron on a specific box?)
```

---

## Metadata

*Last Updated: 2026-08-24*
*Template Version: 1.0*
*Stack: Bash 5 + ShellCheck + bats-core*
