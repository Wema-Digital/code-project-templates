# Workspace spec: notion_workspace

Status: reviewed 2026-10-12 — approved by user, build run

## Summary
A clean, clonable Python package wrapping the official `notion-client` library, used as the default fallback when the Notion MCP is unavailable (for example when it needs an account upgrade or more resources). It replaces an older, messy repo (`cms_notion_workspace`) whose working code is ported in as the starting base. Requested by the Wema Digital owner.

```yaml
templates:
  - python-app:notion-package
  - claude-code-basic:notion-agent
output_path: /mnt/w/vscode.workspaces/wema.digital.github/notion_workspace
project_name: notion_workspace
target: wsl2
```

## Notes
- **Aliases used:** `python-app:notion-package` is the installable package. `claude-code-basic:notion-agent` is the Claude Code guidance (when to use the MCP, when to use the API client). Aliases were chosen over plain names so the folders say what they are: `features/notion-package`, `features/notion-agent`.
- **No workflow diagram:** no `workflow:` key and no coverage table.
- **Python:** 3.13 (matches the old env), shared root `.venv` via uv (`scripts/setup-env.sh`).
- **Wrapper:** generate with `--init-wrapper`. Wrapper remote: https://github.com/Wema-Digital/notion_workspace (already created, empty). In the generated `.git-store`, `origin` stays pointed at `coding-project-templates` so `sync-templates.sh` keeps working. Push component branches to a separate remote name (as done for youtube-pipeline), not `origin`.
- **Install target:** `uv pip install git+https://github.com/Wema-Digital/notion_workspace@<branch>` must work once the package metadata is in `pyproject.toml`.

## Migration source
- Old repo: `/mnt/w/cms.wema.digital/cms_marketing_mastery/features/cms_notion_workspace/` (branch `wema.main`, remote https://github.com/Wema-Digital/cms_notion_workspace).
- Layout seen: `core/{config,main,models,services,utils,gpt_querry}.py`; `core/pythonlibrary/{NotionWorkspace,decorators,custom_exceptions,draft_processing,smart_writer_workspace,process_directories}.py`; `core/pythonlibrary/notion-api-tools/` (hyphenated, so not importable; has `tests/` with about 20 vcr-style YAML cassettes and `client-integration/` scripts); `core/tests/run_tests_*.py`; sqlite DBs under `core/database/`; `core/jsonfiles/notion_users.json`.
- Intent: transfer the code into the `features/notion-package` worktree as the starting base, then remove the old folder and remote.

## SAFETY (hard requirements)
- The old repo's git history has `.env` files committed and pushed to Wema-Digital/cms_notion_workspace: `core/vault/notion.env`, `core/tests/test.env`, `notion-api-tools/client-integration/.env`, `examples/first_project/.env`, plus sqlite DBs, across commits 6e15323, 83cf9c5 and d1c6252.
- Port **files only**. Never port the old git history into the new repo.
- **Rotate the Notion integration token(s) before or at migration.** Treat every token that was ever in those files as compromised.
- Never copy `*.env`, `.env*`, `*.sqlite3`/DB files, or `vault/` into the new repo. Do not read or print their contents.
- The new `.gitignore` (in `features/notion-package`) must cover `.env*`, `*.sqlite3`, `vault/`. Commit a `.env.example` with `NOTION_TOKEN=` only.
- Archive the old GitHub repo rather than deleting it outright until the port is verified. Remove the old local folder only after the new package passes its tests.

## Dependencies (proposed files, dropped into `features/notion-package` after generation)
Curated from the pasted Windows conda env list: top-level packages only. Dropped: transitive deps and conda/Windows-only binaries (pywin32, pywinpty, winpty, ucrt, vc*, mkl, intel-openmp, qt6/pyside6, lib*, fonts, nodejs, cpython, pip, setuptools). A clonable package should not pull in scikit-learn, hence the split.

- `requirements.txt` (runtime): notion-client>=2.3, httpx>=0.28, pydantic>=2.11, pydantic-settings>=2.8, python-dotenv>=1.0, requests>=2.32, pyyaml>=6.0, python-dateutil>=2.9, python-json-logger>=2.0, beautifulsoup4>=4.13, mistune>=3.1, jinja2>=3.1, jsonschema>=4.23, sqlalchemy>=2.0
- `requirements-analysis.txt` (optional): pandas>=2.2, numpy>=2.2, matplotlib>=3.10, seaborn>=0.13, bokeh>=3.6, scipy>=1.15, scikit-learn>=1.6, statsmodels>=0.14, jupyterlab>=4.3, ipykernel>=6.29
- `requirements-dev.txt`: `-r requirements.txt`, pytest>=8.3, debugpy>=1.8, vcrpy, plus ruff and mypy (suggested)

`setup-env.sh` installs per-component requirements, so these files must be in place before it runs. Later, move them into `pyproject.toml` (`[project] dependencies` plus `[project.optional-dependencies]` `analysis` and `dev`).

## Post-generation checklist
1. Generate with `--init-wrapper`. Add the `Wema-Digital/notion_workspace` remote for the wrapper. Use a separate remote name for component branch pushes.
2. Rotate the Notion token(s). Create `.env` locally (gitignored) and commit `.env.example`.
3. Drop the three requirements files into `features/notion-package`, then run `scripts/setup-env.sh`.
4. Port the old files (no history, no secrets, no DBs). Make the code importable: the hyphenated `notion-api-tools` directory needs a valid package name.
5. Run the tests, using the old cassettes with the token scrubbed or regenerating them. Run `scripts/health-check.sh`.
6. Archive the old GitHub repo. Remove the old local folder after tests pass.

## Phase-3 backlog (later, not generation scope)
- Typed thin wrapper over `notion-client` with retry and rate-limit (429/5xx) handling.
- Interface mirroring the Notion MCP operations (search, fetch, create/update page, query database) so callers can swap MCP and API.
- CLI entry point Claude Code can call from bash.
- `.env`-based `NOTION_TOKEN` with a committed `.env.example`.
- Tests on recorded responses (reuse or regenerate the old cassettes, token scrubbed).
- Usage guidance in `features/notion-agent` (CLAUDE.md or a skill): when to use the MCP, when to fall back to the API client.
