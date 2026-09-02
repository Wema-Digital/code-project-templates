# Generator hardening: lessons from the first real rollout (`youtube-pipeline`)

*Prepared 2026-09-02. Phase 6 built `vscode-workspace-gen` and closed with a synthetic end-to-end
test. `youtube-pipeline` (see `features/vscode-workspace-gen/claude/1-YouTube-Pipeline-Workspace-Plan.md`)
is the first real downstream use. It got as far as Phase 2 "Build" — 6 worktrees generated,
6 branches pushed to `Wema-Digital/youtube-pipeline` — then a hardening pass before Phase 3
content work surfaced a set of gaps in the generator itself. This note records the findings and
the decisions; the propagation work is tracked as "Phase 2 hardening (f)" on
[Project #3](https://github.com/orgs/Wema-Digital/projects/3).*

## Why this note exists

The Phase 6 close-out explicitly flagged that a live `/generate-workspace` run through a real
Claude Code session had never happened — only the underlying mechanics were verified. The first
real run confirmed the mechanics hold, but also that the *output* needs hand-finishing before
it is workable, and that hand-finishing drifts. Everything below is a generator improvement, not
a `youtube-pipeline`-specific fix.

## What the first rollout exposed

1. **Generated `.code-workspace` is a stub.** `write_workspace_file()` emits only
   `files.exclude` / `search.exclude` / `files.watcherExclude` for `.git-store` plus a terminal
   default profile. No `launch`, no `tasks`, no `python.*` wiring. The user hand-edited it and
   the result drifted: a trailing-comma JSON error, two divergent copies
   (`vscode_workspace/youtube-pipeline.code-workspace` and
   `vscode_workspace/.vscode/youtube-pipeline.code-workspace`), and overlapping folder roots
   (`.`, `you_tube`, all six `you_tube/features/*`, and `docs` all listed at once).

2. **No environment strategy.** `scripts/setup-env.sh` builds a *per-worktree*
   `python3 -m venv` + `pip` env for every `features/<alias>` with a Python manifest. The
   project actually wanted **one shared `uv` `.venv`** at the wrapper root — the same model
   `coding-project-templates` itself uses. The generator has no opinion and no switch.

3. **The workflow diagram was never a spec input.** `youtube-pipeline` is built from
   `keyword_pipeline_integration_v8.mermaid`, but `generate-workspace.py` / `workspace-architect`
   never saw it. There is no node→component coverage map, so "Phase 2 hardening (e)" has to
   reconstruct one after the fact.

4. **Supporting docs lived only in chat.** The plan repeatedly references
   `YouTube_Pipeline_Ownership_and_Workspace_Map.md`; it exists nowhere on disk. Anything the
   spec depends on must be committed into the worktree's own `claude/` or `docs/`.

5. **The wrapper folder had no history.** The generated glue (`.code-workspace`, `scripts/`,
   `CLAUDE.md`, `docs/`, `.workspace-manifest.json`) was untracked and unpushed. If the machine
   died, only the 6 template branches survived.

6. **A board card was marked Done for work that never happened.** The Phase 2 card for the
   plain non-git folders (`_templates/`, `_pipeline-docs/`, `_raw-exports/`) is "Done"; the
   folders are not in `you_tube/`.

## Decisions made this session

- **Wrapper version control.** `git init` at `/mnt/w/wema-studio/vscode_workspace` (the wrapper
  root, not `you_tube/`); track the glue; push a `main` branch to
  `Wema-Digital/youtube-pipeline`. Wrapper `.gitignore` excludes `.git-store/` and `.venv/`.
- **Repo default branch → `main`** (was `keyword-intelligence-agent`, an arbitrary artefact of
  the first push). The 6 component branches stay.
- **One shared `uv` `.venv`** at the wrapper root; per-worktree isolation only if a real
  dependency conflict shows up.
- **General-purpose uv guide.** `scripts/sequence.md` (written for the wema-project baseline)
  has the uv workflow buried in "Phase 0 step 1". Extract a standalone, project-agnostic
  `scripts/uv-venv-setup.md`, and have the generator ship it into generated workspaces.
- **Starter library set** for `youtube-pipeline` (refined as Phase 3 firms up): `openpyxl`,
  `pandas`, `pydantic`, `notion-client`, `httpx` + `tenacity`, `python-dotenv`; `pytest` +
  `ruff` tooling; `typer`/`click`, `google-api-python-client`, `rich`, `pandera` deferred.

## Propagation targets (card "Phase 2 hardening (f)")

Branch `vscode-gen` unless noted:

- `scripts/generate-workspace.py::write_workspace_file()` — full settings/launch/tasks block,
  modelled on the *structure* of the root `coding-project-templates.code-workspace` but
  `${workspaceFolder}`-relative throughout; fixed folder-roots convention; new
  `--workflow <path>` (copy source diagram into generated `docs/`) and `--init-wrapper`
  (`git init` + `main` branch + `push-wrapper.sh`) options.
- `scripts/setup-env.sh` — default to one shared `uv` `.venv`; `--isolated` for the old
  per-worktree behaviour.
- `.claude/agents/workspace-architect.md` — workflow diagram is an explicit spec input; the
  spec must carry a node→component→status table; referenced docs must be committed.
- `features/vscode-workspace-gen/CLAUDE.md` — the above as standing rules.
- `features/vscode-workspace-gen/.claude/plan.md` — "Lessons from first real rollout" addendum.
- `coding-project-templates.code-workspace` (branch `main`) — de-hardcode the `/mnt/w/...`
  absolutes; it is currently pointed at as the "good structure" example while embodying the
  documented anti-pattern.
- `scripts/uv-venv-setup.md` (branch `main`) — the general-purpose uv guide.
