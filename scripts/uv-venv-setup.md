# Setting up a Python environment with `uv`

Project-agnostic reference for creating and working with a `uv`-managed virtual
environment. Extracted and generalised from `scripts/sequence.md` (which is
specific to the wema-project baseline). Use this for any Python project or
workspace in this org.

`uv` is a single static binary that replaces `pip`, `virtualenv`, `pip-tools`
and `pyenv` for day-to-day work. Install: <https://docs.astral.sh/uv/> (or
`curl -LsSf https://astral.sh/uv/install.sh | sh`). Everything below assumes
`uv` is on `PATH`.

---

## 1. Which layout are you in?

| Situation | Use |
|---|---|
| A directory with a `pyproject.toml` (or you're willing to add one) | **Project workflow** — `uv sync`, `uv add`, `uv.lock`. Preferred. |
| Loose scripts, a `requirements.txt`, or a folder you don't want to make a package | **Env-only workflow** — `uv venv` + `uv pip install`. |

Both put the environment in `.venv/` in the current directory by default, so it
sits next to the code and VS Code / editors discover it automatically. Always add
`.venv/` to `.gitignore`.

---

## 2. Project workflow (`pyproject.toml` + lock)

### First-time setup

```bash
# in the project root
uv init                     # only if there's no pyproject.toml yet; --bare to skip the sample module
uv add pandas "httpx>=0.27"        # runtime deps -> written into pyproject.toml
uv add --dev pytest ruff          # dev-only deps -> [dependency-groups] / optional 'dev'
uv sync                     # create .venv, resolve, write uv.lock, install everything
```

`uv sync` is the workhorse: it makes `.venv/` if missing, resolves the full
dependency tree, writes/updates `uv.lock` (exact pinned versions, committed to
git), and installs so the env matches the lock exactly — removing anything not in
it. Run it after every dependency change and after every `git pull` that touched
`pyproject.toml` / `uv.lock`.

```bash
uv sync --extra dev         # include an optional-dependency group named 'dev'
uv sync --all-extras        # include every optional group
uv sync --frozen            # install strictly from uv.lock, never re-resolve (CI)
```

### From an existing `requirements.txt`

```bash
uv add -r requirements.txt         # fold them into pyproject.toml, then
uv sync
```

### Day-to-day

```bash
uv add <pkg>            # add a dep (updates pyproject.toml + uv.lock + .venv)
uv remove <pkg>         # drop one
uv lock --upgrade       # re-resolve to newest allowed versions; review the uv.lock diff
uv lock --upgrade-package <pkg>    # bump just one
uv run <cmd>            # run inside the env without activating (uv run pytest, uv run python -m app)
uv tree                 # show the resolved dependency graph
```

### A workspace / non-package project

If the `pyproject.toml` describes an environment rather than something to build
(no `[build-system]`), `uv` treats it as a *virtual* project: `uv sync` still
manages `.venv/` and `uv.lock` from `[project.dependencies]`, it just doesn't try
to install the project itself. This is the right shape for a multi-folder
workspace that needs one shared env. Point `UV_PROJECT_ENVIRONMENT=.venv` (or
accept the default) so the env lands where the editor expects it.

Editable installs of sub-packages that *do* build:

```bash
uv pip install -e ./packages/thing            # into the active/synced .venv
```

---

## 3. Env-only workflow (no `pyproject.toml`)

```bash
uv venv                       # create .venv/ (add a version: `uv venv --python 3.12`)
source .venv/bin/activate     # POSIX;  .venv\Scripts\activate  on Windows
uv pip install -r requirements.txt
uv pip install pandas httpx
uv pip list                   # what's installed
```

`uv venv` does **not** install `pip` into the env. Use `uv pip …` (which targets
`.venv` when it's active, or pass `--python .venv/bin/python`) rather than
`python -m pip`.

### Pin what you installed

```bash
uv pip freeze > requirements.lock                    # quick freeze of the current env
uv pip compile requirements.in -o requirements.txt   # resolve *.in -> fully pinned *.txt (pip-tools style)
uv pip sync requirements.txt                         # make .venv match that file exactly
```

---

## 4. Rebuild / refresh

```bash
rm -rf .venv && uv sync              # project workflow: clean env from the lock
rm -rf .venv && uv venv && uv pip sync requirements.txt   # env-only workflow
uv cache clean                       # only if you suspect a corrupt download cache
```

Never commit `.venv/`. Do commit `pyproject.toml` + `uv.lock` (project workflow)
or the pinned `requirements.txt` (env-only).

---

## 5. VS Code wiring

Pair the env with these settings (in `.vscode/settings.json` for a single folder,
or the `settings` block of a `.code-workspace` for a multi-root setup). Anchor
paths to the folder — `${workspaceFolder}` for a single root, the **named**
`${workspaceFolder:<name>}` in a multi-root workspace (the bare form resolves to
whichever folder is listed first):

```jsonc
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  // Windows: "${workspaceFolder}/.venv/Scripts/python.exe"
  "python.envFile": "${workspaceFolder}/.env",
  "python.terminal.activateEnvironment": true,
  "terminal.integrated.env.linux": { "PATH": "${workspaceFolder}/.venv/bin:${env:PATH}" }
  // Windows: "terminal.integrated.env.windows": { "PATH": "${workspaceFolder}\\.venv\\Scripts;${env:PATH}" }
}
```

For import resolution across sibling folders that aren't installed as packages,
add each to `python.analysis.extraPaths` (e.g.
`"${workspaceFolder}/features/<name>"`).

After changing the interpreter, run **Python: Select Interpreter** and pick the
`.venv` if VS Code doesn't switch on its own.

---

## 6. Quick reference

| Task | Project workflow | Env-only workflow |
|---|---|---|
| Create env | `uv sync` | `uv venv` |
| Add a dependency | `uv add <pkg>` | `uv pip install <pkg>` |
| Add dev-only | `uv add --dev <pkg>` | `uv pip install <pkg>` |
| Install from a file | `uv add -r req.txt` → `uv sync` | `uv pip install -r req.txt` |
| List installed | `uv pip list` / `uv tree` | `uv pip list` |
| Lock / pin | `uv lock` (writes `uv.lock`) | `uv pip compile` / `uv pip freeze` |
| Reproduce exactly | `uv sync --frozen` | `uv pip sync req.txt` |
| Run a command in the env | `uv run <cmd>` | activate, then run |
| Upgrade everything | `uv lock --upgrade` → `uv sync` | edit `*.in`, recompile, `uv pip sync` |
