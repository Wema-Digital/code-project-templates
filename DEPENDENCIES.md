# Dependencies

Shell has no package manifest, so required tools are documented here instead of a `requirements.txt`/`package.json` equivalent.

## To run the scripts

| Tool | Why |
|---|---|
| `bash` >= 5 | All scripts target Bash, not POSIX `sh` — associative arrays, `[[ ]]`, `local` |

Individual scripts may need more — check the usage comment at the top of the script itself before running it.

## To develop / test in this repo

| Tool | Why | Install |
|---|---|---|
| [ShellCheck](https://www.shellcheck.net/) | Static analysis — every script must pass it clean | `apt-get install shellcheck` / `brew install shellcheck` |
| [bats-core](https://bats-core.readthedocs.io/) | Behavioural tests for scripts with real logic worth testing beyond linting | `apt-get install bats` / `brew install bats-core` |

CI installs both fresh on every run (see `.github/workflows/shellcheck.yml`) — no lockfile to keep in sync.
