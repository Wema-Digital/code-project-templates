# Plan — vscode-workspace-gen

> **Status**: Card 1 (scaffold), Card 2 (agents/hooks/scripts), and Card 3 (end-to-end test) all executed 2026-08-25 — see addenda below. Phase 6 complete; see `claude/7-Phase 6 Detailed Breakdown.md` at the repo root.

## Context

Phase 6 builds a new template, `vscode-workspace-gen`, whose entire job is generating other projects: interview a user about which `coding-project-templates` templates they want, then produce a standalone folder combining them. `claude/6-Phase 6 Process Design (review).md` settled the shape and the one real technical tension (bare-clone-vs-live-worktree) before any code was written; this plan carries that forward for the scaffold step specifically.

Prerequisite already satisfied: `claude-code-advance` (branch `claude-code-a`) carries one working example command, subagent, and hook (Phase 5) — this template branches from that content rather than duplicating it from scratch.

## Goal (Card 1 scope only)

Stand up the worktree and its orientation docs — `README.md`, `CLAUDE.md`, this plan — accurately describing a tool that doesn't do its actual job yet. Card 2 builds the generation logic; this step just gives a session opened here the right standing rules and mental model before that code exists.

## The bare-clone-then-worktree mechanism

Decided in the process design review, restated here as the thing Card 2's `scripts/generate-workspace.py` must implement:

1. `git clone --bare` this repo into `<output>/.git-store/`
2. For each selected template, `git worktree add <output>/features/<name> <branch>` run **against `<output>/.git-store`**, not against the live `coding-project-templates` checkout
3. Result: the generated folder has the full worktree experience (branch checked out, complete history) with zero dependency on where `coding-project-templates` happens to live afterward

Rejected alternative: `git worktree add` straight from the live checkout into the output folder. Simpler, but ties the generated project to this repo's current path permanently — moving, deleting, or not sharing `coding-project-templates` alongside it breaks every worktree inside.

## Output folder shape

```
<output>/.git-store/            # bare clone, not the live checkout
<output>/.vscode/*.code-workspace
<output>/features/<template>/   # one worktree per selection, against .git-store
<output>/scripts/               # setup-env.sh, git-sync-all.sh, sync-templates.sh, health-check.sh
<output>/.workspace-manifest.json
<output>/README.md
<output>/CLAUDE.md              # generated, summarises what's included
<output>/todo.md                # post-generation manual-follow-up checklist
```

`scripts/` is deliberately several small files, not one script. `ProjectSetup-linux-os.py` in this repo is the cautionary example: five loosely related jobs in one file, and its `docs/` generation step is already broken against current repo state. Card 2 replaces that pattern rather than trimming it.

## The Q&A flow

Two distinct sessions, never collapsed into one turn:

1. **Interview** (Card 2's `workspace-architect` subagent, via `/generate-workspace`): ask which templates, output path, Windows vs WSL2. Write a spec to this worktree's own `claude/N-Title.md`. Stop — do not generate anything yet.
2. **Build** (a later session, after human review of the spec): read the reviewed `claude/N-*.md`, then actually run the bare-clone-and-worktree mechanism and write the output folder.

The gap between the two is deliberate — it's the point where a misread requirement gets caught before any files exist on disk, the same role human review plays for this repo's own `claude/N-*.md` planning docs.

## What gets written where (Card 1)

- `features/vscode-workspace-gen` worktree, branch `vscode-gen`, off `claude-code-a` — done via `git worktree add features/vscode-workspace-gen -b vscode-gen claude-code-a`
- `README.md` — what the tool does, the 4-step process, how to invoke it (plain-English today, `/generate-workspace` once Card 2 ships)
- `CLAUDE.md` — the two-jobs framing (interviewing vs. generating), the VS Code-docs-check and Windows/WSL2 standing rules, the bare-clone mechanism, output shape, and an honest "not yet built" list so a session here doesn't assume Card 2's files already exist
- `.claude/plan.md` — this file
- Inherited unchanged from `claude-code-advance`: `.claude/commands/todo-next.md`, `.claude/agents/doc-sync-checker.md`, `.claude/settings.json` + `.claude/hooks/validate-json.sh`, `.github/` CI, `.gitignore`. Whether these generic examples stay, get removed, or get extended is a Card 2 decision, not this scaffold step's — Card 2 adds `generate-workspace.md`, `workspace-architect.md`, and a second, distinct hook (validates *generated* `.vscode/*.code-workspace`, not this template's own `.claude/*.json`) alongside them.
- `todo.md` — deliberately left as inherited from `claude-code-advance` for now rather than rewritten; Card 1's checklist in `claude/7-Phase 6 Detailed Breakdown.md` doesn't call for a todo.md rewrite, and rewriting it before Card 2's real task list exists would just mean rewriting it twice

## Deliberately deferred (not Card 1's job)

- `.claude/commands/generate-workspace.md`, `.claude/agents/workspace-architect.md` — Card 2
- The generated-output JSON-validation hook — Card 2
- `scripts/generate-workspace.py` and the four generated-project scripts — Card 2
- Running an actual generation end to end — Card 3
- `.devcontainer/` generation — flagged in the process design doc as nice-to-have, not v1

## Verification (Card 1)

- `git worktree list` from the repo root shows `features/vscode-workspace-gen` on branch `vscode-gen`
- `doc-sync-checker` run against this directory once README.md/CLAUDE.md/plan.md are in place, to catch any claim here that doesn't match what's actually on disk
- No automated tests for this step — it's orientation documentation, not executable code

---

## Addendum: Card 2 — Build the generator's agents, hooks, and scripts

Executed 2026-08-25.

### What was built

- `.claude/commands/generate-workspace.md` — `/generate-workspace [spec-path]`. No args: interview mode, delegates to `workspace-architect`, loops questions/answers through `AskUserQuestion` until the subagent reports `DRAFT-READY`, then stops. Spec-path arg: build mode, confirms `Status: reviewed` (or asks first), runs `scripts/generate-workspace.py --spec`.
- `.claude/agents/workspace-architect.md` — `tools: Read, Glob, Write`, no `Edit`/`Bash`. Its actual constraint, confirmed against `code.claude.com/docs/en/sub-agents.md` before writing it: subagents cannot use `AskUserQuestion` or any other interactive tool, and run autonomously to a single final report. So it never "asks" the user itself — it returns `NEEDS-INPUT: <questions>` or `DRAFT-READY: <path>`, and the calling command (running in the main session, which *does* have `AskUserQuestion`) is the one that actually puts questions to the user. This is the accurate design for what Card 2's brief called "a subagent whose job is asking the clarifying questions" — the subagent decides *what* to ask, the main session is the only thing that *can* ask it.
- `.claude/hooks/validate-workspace-json.sh` + a second entry in `.claude/settings.json`'s existing `PostToolUse`/`Edit|Write` hook array — checks any `*.code-workspace` file just touched by the Edit/Write tool still parses. Distinct from the inherited `validate-json.sh` (checks this template's own `.claude/*.json`); this one's for a session hand-editing the *generated output*. `scripts/generate-workspace.py` also self-checks what it writes (re-parses immediately after writing), so the hook's job is specifically the hand-edit path the script doesn't cover.
- `scripts/generate-workspace.py` — the core logic. `discover_templates()` parses root `CLAUDE.md`'s Worktree map table live rather than hardcoding the template→branch mapping, so it can't silently drift the way this repo's docs have drifted before. Accepts either `--spec claude/N-*.md` (parses a ` ```yaml ` fenced block, requires PyYAML) or direct `--templates/--output/--project-name/--target` flags (no extra dependency). Implements the bare-clone-then-worktree mechanism exactly as specced: `git clone --bare <source> <output>/.git-store`, explicit `origin` remote set/added regardless of what clone did on its own, then `git worktree add` per template against `.git-store`. Writes `.vscode/*.code-workspace` with zero absolute paths (`${workspaceFolder}`-relative `features/<name>` entries only) and only genuinely-OS-specific settings gated on `--target` (`terminal.integrated.defaultProfile.linux`/`.windows`) — deliberately does *not* set a global `python.defaultInterpreterPath`, since that's ambiguous across multiple selected templates and was the exact class of bug (hardcoded absolute interpreter path) this repo's own committed workspace file had.
- `scripts/setup-env.sh`, `scripts/health-check.sh`, `scripts/sync-templates.sh`, `scripts/git-sync-all.sh` — the four small, single-purpose scripts from the process design doc, copied into every generated project by `generate-workspace.py`. Verified `setup-env.sh`'s dependency detection against every real template in this repo (`requirements-dev.txt` before plain `requirements.txt`, since most templates' dev tooling — including `pytest` itself — lives there, not in the base file; `pyproject.toml`'s `[dev]` extra for `python-app`; `package.json` for `js-express`) rather than assuming.
- `scripts/repair-worktrees.sh` — **not in the original Card 2 list.** Found while smoke-testing (see below) that moving a generated project breaks every `features/<name>` worktree until `git worktree repair` runs, because worktree links are absolute paths on both ends. Added the script, and documented the caveat in this template's own `CLAUDE.md`, `README.md`, and in every generated project's `README.md`/`todo.md` — the bare-clone mechanism solves independence from the *source* repo's location, it does not make the *output* immune to being moved, and conflating the two would be an overclaim.
- `README.md`, `CLAUDE.md` — updated throughout: real file tables, `/generate-workspace` usage instead of "once it ships", the worktree-move caveat.

### Design decisions and why

- **`git-sync-all.sh` was written fresh, not reused.** The spec says "reused from phase 2", but phase 2's own `scripts/git-sync-all.sh` was never actually built (its GitHub Project card is still "optional"). Rather than block Card 2 on an unbuilt phase 2 deliverable, or silently pretend to reuse something that doesn't exist, wrote it to the same brief (status/push across every worktree branch) and said so plainly in `CLAUDE.md` rather than leaving a stale "reused from phase 2" claim in place.
- **No auto-commit in `git-sync-all.sh`.** Considered a `--commit "msg"` mode; dropped it. Auto-committing with a generic message across multiple unrelated worktrees is exactly the kind of action that should stay a human decision, not a generator default.
- **`sync-templates.sh` is fast-forward only.** A diverged branch is reported, not merged automatically — silently creating merge commits across someone else's generated project on their behalf is worse than making them do it by hand once.

### Verification

- `python3 -m py_compile scripts/generate-workspace.py` and `bash -n` on all five shell scripts — all pass
- Ran the real generator (not dry-run) against this repo with `--templates web-flask,python-scripts --target wsl2`: bare clone succeeded, both worktrees checked out on the correct branch/commit, `.vscode/*.code-workspace` and `.workspace-manifest.json` valid, zero absolute paths in any generated file (grepped for the scratch output path across every generated file, found none)
- Re-ran with `--target windows` — settings correctly swap to `terminal.integrated.defaultProfile.windows`, output still valid JSON
- Moved the generated output to a new path by hand: every `features/<name>` broke (`fatal: not a git repository`) until `git worktree repair` ran — this is what motivated `repair-worktrees.sh`; confirmed the script fixes it
- `.claude/hooks/validate-workspace-json.sh` tested against three stdin payloads (valid `.code-workspace`, invalid one, unrelated file) — exit 0/2/0 respectively, matching `validate-json.sh`'s established pattern
- `.claude/settings.json` re-validated as JSON after adding the second hook entry
- Subagent/command YAML frontmatter checked by hand against the verified schema from Phase 5 (flat `key: value` pairs, comma-separated `tools`, no `Edit`/`Write` beyond what's actually needed) — `.github/scripts/validate_claude_config.py` (this template's own CI check) could not be run locally in this session (no `pyyaml` available and the environment blocks installing it), so this is a manual check, not a CI-equivalent one; the committed CI workflow will run it for real on push. **Correction, found during Card 3**: `pyyaml` *was* available all along via `/usr/bin/python3` (`python3-yaml`, apt-installed system-wide) — `python3` on `PATH` in this session just resolved to this repo's own `.venv/bin/python3` first, which doesn't have it. `/usr/bin/python3 .github/scripts/validate_claude_config.py` runs fine.
- **Not done**: an actual live `/generate-workspace` interview through a real Claude Code session (only the underlying script and the discover/validate logic were exercised directly) — that, plus both OS variants and `health-check.sh` against a real generated project, is Card 3's job

---

## Addendum: Card 3 — Test the generator end to end

Executed 2026-08-25.

### What was tested, and how

- **Ran the CI config validator for real** (`/usr/bin/python3 .github/scripts/validate_claude_config.py`), sidestepping the `python3` PATH shadowing noted above — passed clean: 1 JSON file, 4 command/agent files.
- **Portability, done properly**: made an isolated bare clone of the source repo in scratch space, generated a project from *that copy* (`--source-repo`), then deleted the copy entirely (not moved — deleted). Both `features/web-flask` and `features/python-scripts` in the generated output still worked fully afterward: `git status`, `git log`, and a real test commit all succeeded with the source gone. This is the actual claim the process design doc makes (independence from where `coding-project-templates` lives), tested for real rather than assumed.
  - This required a small fix to `discover_templates()`: it only knew how to read `CLAUDE.md` as a plain file, which doesn't exist in a bare repo. Added a fallback to `git show HEAD:CLAUDE.md` so `--source-repo` works against either a working tree or a bare repo.
- **Windows vs WSL2 settings**: re-verified the exact `terminal.integrated.defaultProfile.windows`/`.linux` values against VS Code's actual current source (`terminalProfiles.ts` on GitHub, not assumed from training knowledge) per this template's own standing rule — `"PowerShell"` and `"bash"` are still the correct, current auto-detected profile names. Generated both target variants for real; both produced valid, sensible JSON.
- **Real dependency install + test run**: `python3 -m venv` fails in this sandbox (`ensurepip`/`python3.12-venv` not installed, and fixing that needs `sudo` — asked the user first rather than assuming it was fine to change system packages). Found `uv` already installed and already what created this repo's own `.venv` (visible in its `pyvenv.cfg`) — used `uv venv` + `uv pip install` instead, which needs no system changes at all. Confirmed real: `setup-env.sh`'s dependency-detection logic (`requirements-dev.txt` before `requirements.txt`, `pyproject.toml[dev]`, `package.json`) is validated as *logic*, even though this specific test run used `uv` rather than the stdlib `venv`+`pip` `setup-env.sh` actually calls.
- **`scripts/health-check.sh` against a real generated project** (`web-flask` + `python-scripts`, per the checklist's own suggested pair): first run failed both templates with `ModuleNotFoundError`. Traced this to a genuine, pre-existing bug in three Phase 5 templates (`python-scripts`, `web-flask`, `machine-learning`), not in this generator — see below. After fixing it upstream and re-running `scripts/sync-templates.sh` to pull the fix into the already-generated project, `health-check.sh` passed clean, exit 0.
- **`.vscode/*.code-workspace` opens correctly in VS Code**: opened the generated workspace file with the `code` CLI (available in this environment as the VS Code remote-cli) — loaded without error.

### Bug found and fixed, outside this template: three Phase 5 templates' CI was silently broken

`python-scripts`, `web-flask`, and `machine-learning` all import their own top-level package bare (`from scripts.csv_report import ...`, `from app import ...`, `from src.pipeline import ...`) with no `pytest.ini`/`pyproject.toml` `pythonpath` setting and no root `conftest.py`. Plain `pytest` — the exact command each template's own `.github/workflows/test.yml` runs — can't import them (`ModuleNotFoundError`); only `python -m pytest` works, because `-m` adds the current directory to `sys.path` itself and the bare `pytest` entrypoint doesn't. Confirmed this wasn't specific to being nested inside `coding-project-templates`'s worktree layout by reproducing it in a fully isolated copy with no git anywhere. Checked GitHub Actions directly: all three branches' most recent CI runs before this fix were genuinely `failure`, confirming this has been silently broken since Phase 5.

Asked the user before touching three already-"Done" Phase 5 templates from a Phase 6 session — confirmed they wanted it fixed now rather than just documented. Added a one-line `pytest.ini` (`pythonpath = .`) to each of the three affected templates' own branches (`py-script`, `py-flask`, `py-ml`), verified real `pytest` passes on all three locally, pushed, and confirmed each branch's real CI went green. `web-django` (pytest-django handles `sys.path` itself) and `python-app` (proper `pip install -e .` via `pyproject.toml`) were unaffected — checked both explicitly rather than assuming.

### Bug found and fixed, in this generator: `sync-templates.sh` silently did nothing

While re-syncing the pytest.ini fix into the already-generated sample project to test `sync-templates.sh` for real, every branch reported "no matching origin/<branch>, skipping" despite `git fetch origin` appearing to succeed. Root cause: `git clone --bare` sets the new "origin" remote's URL but configures no fetch refspec (bare repos aren't expected to track a remote on their own) — my earlier `clone_bare_store()` only handled the URL, so `git fetch origin` with no refspec updated `FETCH_HEAD` but populated zero `refs/remotes/origin/*` refs, and every subsequent `show-ref --verify` check in `sync-templates.sh` failed silently. Fixed two ways: `clone_bare_store()` now explicitly sets `remote.origin.fetch` after creating the remote (fixes it for every project generated from now on), and `sync-templates.sh` now passes the refspec explicitly to `git fetch` itself (fixes it for projects already generated before this patch, without needing to regenerate them). Verified: re-ran `sync-templates.sh` against the Card 3 sample project after the fix, both branches fast-forwarded correctly.

### Verification

- `python3 -m py_compile` clean on the updated `generate-workspace.py`; `bash -n` clean on the updated `sync-templates.sh`
- Full pipeline re-run end to end after all fixes: generate → `setup-env.sh` (via `uv`) → `health-check.sh` (clean pass, exit 0) → `sync-templates.sh` (correctly fast-forwards) → re-run `health-check.sh` again (still clean)
- Everything above was exercised against real output on disk, not dry-run only
- **Not done**: a literal live `/generate-workspace` slash-command interview through a separate real Claude Code session (this session isn't running inside `features/vscode-workspace-gen`, so `workspace-architect` isn't in its own available-agent list) — the underlying mechanics it depends on (subagent tool restrictions, the spec format, `generate-workspace.py`'s `--spec` path) were all verified directly instead. Worth a manual pass by a human opening a session there directly, if maximum confidence is wanted before calling Phase 6 fully closed.

---

## Addendum: NAME:ALIAS support for repeated templates

Executed 2026-08-29, prompted by planning the first real downstream use of this generator (a `youtube-pipeline` workspace, see `claude/1-YouTube-Pipeline-Workspace-Plan.md`).

### The problem

That workspace needs three independent agent-plus-Python pairings (a keyword-intelligence Routine agent, a production-pipeline interactive agent, and a Notion API integration), but `coding-project-templates` only has two agent templates (`claude-code-advance`, `claude-code-basic`) and two Python templates (`python-app`, `python-scripts`). `write_workspace_file` names every worktree folder after the template itself (`features/<name>`), so selecting the same template a second time silently collided on one folder, there was no way to ask for "claude-code-basic, but a second, separately-named copy."

### What changed

- `scripts/generate-workspace.py`: every `--templates` entry (or spec `templates:` list item) may now be `NAME` or `NAME:ALIAS`. A new `Selection` NamedTuple (`alias`, `template`, `branch`) replaces the old `{name: branch}` dict everywhere; `parse_template_selections()` resolves tokens, defaults alias to the template name when omitted, and rejects unknown templates, malformed tokens, unsafe alias characters, and duplicate aliases with a clear error naming both conflicting entries. `add_worktrees`, `write_workspace_file`, `write_manifest`, `write_readme`, `write_claude_md`, and `write_todo` all now key off `alias` for the folder path and `template`/`branch` for everything about what's actually inside it (extension recommendations, branch, commit). The generated `CLAUDE.md`'s template table gained a `Template` column alongside `Folder` so an aliased worktree's real origin is still visible.
- Also fixed in passing: `discover_templates`'s "no template rows found" error referenced an undefined `claude_md` instead of `claude_md_path` (a latent `NameError` that would have fired only on that one error path, found by inspection while making the change above, unrelated to it otherwise).
- Documentation: `README.md` gained a "Repeating a template (NAME:ALIAS)" section with a worked example; `workspace-architect.md`'s completeness check and spec-writing instructions now mention alias syntax and reject a spec that reuses one template's name across two components without an alias.

### Why not one of the other two options considered

- Folding a repeated need into an already-selected worktree as a subpackage (e.g. Notion code living inside `features/python-app` alongside unrelated workbook-builder code) was rejected: it blurs the clean one-worktree-per-component separation the rest of this tool's output already keeps, and ties two unrelated codebases' commit history together.
- A fully separate `generate-workspace.py` run and repo per repeated component was rejected: it works, but contradicts the actual ask (one project, worktrees aligned with how `coding-project-templates` itself is structured), and doubles the number of `.git-store` bare clones for what is otherwise one project.

### Verification

- `/usr/bin/python3 -m py_compile scripts/generate-workspace.py` clean (system Python, sidesteps the `.venv` PATH-shadowing noted in Card 2's addendum).
- `--dry-run` against the actual six-selection case this was motivated by (`claude-code-advance`, `python-scripts`, `claude-code-basic`, `python-app`, each selected once more under an alias) printed six distinct `features/<alias>` lines with the correct source template and branch for each, no collision.
- Three error-path checks: two entries resolving to the same alias (both a bare duplicate and an explicit collision) fails with a clear message naming both entries; an unknown template name still reports cleanly with the valid-choices list.
- A real (non-dry-run) generation with three aliased selections (two of them reusing `claude-code-basic` and `python-app`'s already-tested-once template family) produced correct output end to end: `features/<alias>` worktrees each checked out the right branch (confirmed via `git rev-parse --abbrev-ref HEAD` per folder), `.workspace-manifest.json`, the generated `README.md`, and the generated `CLAUDE.md` all correctly distinguished folder name from source template, and `scripts/health-check.sh` ran against the aliased output without error (skipped, as expected, since no dependencies were installed).
- Confirmed by reading them that `setup-env.sh`, `health-check.sh`, `sync-templates.sh`, `git-sync-all.sh`, and `repair-worktrees.sh` all already iterate `features/*/` and derive each worktree's branch live via `git rev-parse --abbrev-ref HEAD` rather than assuming folder name equals template name -- none of the four generated-project scripts needed any change for aliasing to work.
- Not done: an actual live `/generate-workspace` interview producing an aliased spec through a real Claude Code session opened in this worktree (same gap Card 3 already flagged for the non-aliased case).

### Bug found and fixed 2026-08-29 (during the first real downstream generation)

The verification above was **incomplete and its "end to end" claim was wrong**: the three-aliased-selection test that "produced correct output end to end" used three selections resolving to three *different* source branches. The `youtube-pipeline` spec (`claude/1-YouTube-Pipeline-Workspace-Plan.md`) is the first case where **two selections resolve to the same source branch** -- `claude-code-basic` backs both `production-pipeline-agent` and `notion-integration-agent`, and `python-app` backs both `production-pipeline-app` and `notion-integration-app`.

`add_worktrees` did `git worktree add <path> <branch>` for every selection. git **refuses to check the same branch out in two worktrees at once**, so the first real generation of the six-worktree spec crashed on the fifth worktree:

```
fatal: 'claude-code-b' is already used by worktree at '.../features/production-pipeline-agent'
subprocess.CalledProcessError: ... 'worktree', 'add', '.../features/notion-integration-agent', 'claude-code-b'] returned non-zero exit status 128
```

**Fix:** `add_worktrees` now creates a per-alias branch for any aliased selection (`s.alias != s.template`, plus a `Counter` guard for a same-branch collision without distinct aliases): `git worktree add -b <alias> <path> <source-branch>`. It returns a second dict `{alias: branch_actually_checked_out}`; `write_manifest` (new `source_branch` key alongside `branch`) and `write_claude_md` (Branch column now shows the per-folder branch; an extra paragraph explains the fork when any occurred) were updated to use it. A plain un-aliased selection is unchanged -- still a straight checkout of its template branch.

**Verified:** clean `py_compile`; regenerated the full six-worktree `youtube-pipeline` spec non-dry-run -- all six worktrees created, each on its own branch matching its folder name (`git worktree list` confirmed), manifest records `branch` + `source_branch` correctly, generated `CLAUDE.md` table + fork paragraph correct, `health-check.sh` exit 0 (all skipped, no deps). All six branches then pushed to `Wema-Digital/youtube-pipeline` and the generated `.git-store` given a `github` remote (kept separate from `origin`, which `sync-templates.sh` needs pointed at the source repo).

---

## Addendum: lessons from the first real rollout (`youtube-pipeline`)

Recorded 2026-09-02, after `youtube-pipeline` reached Phase 2 "Build" (6 worktrees generated, 6 branches pushed) and a hardening pass before Phase 3 content work. Root-repo companion note: `claude/8-Generator hardening from first rollout (youtube-pipeline).md`. Propagation tracked as "Phase 2 hardening (f)" on [Project #3](https://github.com/orgs/Wema-Digital/projects/3).

### The problem

The generated output is not workable as-is — it needs hand-finishing, and the hand-finishing drifts. Concretely, on the first real run:

- **`write_workspace_file()` emits a stub.** Only `.git-store` excludes plus a terminal default profile — no `launch`, no `tasks`, no `python.*` wiring (`defaultInterpreterPath`, `envFile`, `analysis.extraPaths`, `testing.pytestEnabled`, venv PATH prepend). The user hand-edited the file and it drifted into a trailing-comma JSON error, two divergent copies (`<root>/*.code-workspace` vs `<root>/.vscode/*.code-workspace`), and overlapping folder roots.
- **No environment strategy.** `setup-env.sh` builds a per-worktree `python3 -m venv` for each Python `features/<alias>`. The project wanted one shared `uv` `.venv` at the wrapper root (the model `coding-project-templates` itself uses). The generator has neither a default opinion nor a switch.
- **The workflow diagram was never an input.** `youtube-pipeline` is built from `keyword_pipeline_integration_v8.mermaid`; neither `generate-workspace.py` nor `workspace-architect` ever saw it, so there is no node→component coverage map and no copy of the diagram in the generated `docs/`.
- **Spec-referenced docs lived only in chat.** `YouTube_Pipeline_Ownership_and_Workspace_Map.md` is cited throughout the plan and exists nowhere on disk.
- **The wrapper folder had no git history.** The glue (`.code-workspace`, `scripts/`, `CLAUDE.md`, `docs/`, manifest) was untracked and unpushed — only the 6 template branches were recoverable.

### What will change (not yet done — this addendum is the scope record)

- `scripts/generate-workspace.py::write_workspace_file()` — emit a full settings/launch/tasks block, modelled on the *structure* of the root `coding-project-templates.code-workspace` but `${workspaceFolder}`-relative throughout (never its hardcoded `/mnt/w/...` absolutes). Fix the folder-roots convention to wrapper `.` + one entry per feature + `docs/`. New optional `--workflow <path>` (copy source diagram(s) into generated `docs/workflows_diagrams/`, link from generated `CLAUDE.md`) and `--init-wrapper` (`git init` the output root, seed a `main` branch, write `push-wrapper.sh`).
- `scripts/setup-env.sh` — default to one shared `uv` `.venv` at the output root (fallback `python3 -m venv` + `pip`), each Python `features/<alias>` installed editable; `--isolated` flag restores the current per-worktree behaviour. Ship the general-purpose `scripts/uv-venv-setup.md` (extracted from the root repo's `scripts/sequence.md`) into generated output.
- `.claude/agents/workspace-architect.md` — a workflow diagram is an explicit, expected spec input for "workspace from a workflow" requests; the written spec must carry a node→component→status table; any doc the spec references must be committed into this worktree's `claude/` or `docs/`.
- `CLAUDE.md` — the above as standing rules (shared uv `.venv` default; full non-stub `.code-workspace`; workflow diagram copied + mapped when one drove the build; wrapper gets its own `git init` + `main` branch).

### Verification (to record when the work lands)

- Dry-run generation produces a `.code-workspace` that opens clean on both WSL2 and native Windows with no hand-editing.
- `setup-env.sh` produces one working shared `.venv`.
- `workspace-architect`'s spec template includes the node→component table.
- This addendum updated with the actual diffs and the root `claude/8` note cross-checked.
