# Execution Runbook — "CodeTemplate: Update-DefaultSetup"

*Prepared 2026-08-23, in response to `claude/2-GitHub and Claude Code Workspace Plan.md` and your terminal output. This is written to be handed phase-by-phase to a local Claude Code CLI session (`claude`, running in a terminal at the repo) — each phase below has either exact commands, or a self-contained prompt you paste in.*

## One reordering I'd suggest before you start

Your six phases were numbered 1–6 with "formalise the root `CLAUDE.md`" last. I'd move it to right after housekeeping instead: it costs almost nothing to write, and every Claude Code session you run for phases 3 onward benefits from the repo having a short orientation file rather than none. Nothing else in your ordering needs to change — phase dependencies are genuinely 1 → (2/6) → base-template → propagate → intermediate, and the generator (old phase 5) can actually be built any time after housekeeping since it only needs the folders to exist, not to be finished. So:

**0** connect + create project → **1** housekeeping → **2** root `CLAUDE.md` (was your 6) → **3** finish base template (was your 2) → **4** propagate base (was your 3) → **5** bring templates to intermediate (was your 4) → **6** workspace generator (was your 5, can start in parallel with 5 if you want).

Everything below uses this order but I've noted your original numbering in brackets so the two line up.

## Phase 0 — Connect to GitHub, create the tracking project

Your `gh auth status` output shows you're already logged in as `pira245` with scopes `gist`, `read:org`, `repo`, `workflow`. That's good enough for everything git-related, but **`gh project` commands need the `project` scope specifically, and it's missing from that list** — `gh project create` will fail with a permission error until you add it:

```bash
gh auth refresh -s project -h github.com
gh auth status                              # confirm 'project' now appears under Token scopes
```

Then create the project and link it to the repo:

```bash
gh project create --owner Wema-Digital --title "CodeTemplate: Update-DefaultSetup"
# note the project NUMBER it returns (and the URL)

gh project link <number> --owner Wema-Digital --repo Wema-Digital/code-project-templates
```

One caveat worth knowing before you run it: creating an **org-owned** project needs Projects write access on the Wema-Digital org for your account, not just repo access. If `--owner Wema-Digital` errors with a permissions message, create it under your own account instead and link it to the repo — functionally equivalent for a one-person project:

```bash
gh project create --owner "@me" --title "CodeTemplate: Update-DefaultSetup"
gh project link <number> --owner "@me" --repo Wema-Digital/code-project-templates
```

Optional but recommended — seed the project with one card per phase so you have a visible board instead of just this document:

```bash
for title in \
  "Phase 1: Housekeeping" \
  "Phase 2: Root CLAUDE.md" \
  "Phase 3: Finish claude-code-basic base template" \
  "Phase 4: Propagate base to other 9 branches" \
  "Phase 5: Bring templates to intermediate level" \
  "Phase 6: Build the workspace generator"; do
  gh project item-create <number> --owner Wema-Digital --title "$title"
done
```

(Swap `--owner Wema-Digital` for `--owner "@me"` here too if you used the fallback above.)

Last thing while you're touching git auth — make sure `git push`/`git pull` over HTTPS actually use the `gh` credential you just verified, instead of prompting separately:

```bash
gh auth setup-git
```

## Phase 1 — Housekeeping

Plain commands, run from the repo root:

```bash
cd /path/to/coding-project-templates
rm .git/index.lock            # only if you're sure no git process is genuinely running
git worktree prune
git worktree list              # should now show 11 clean entries, no js-express1
```

For the `.code-workspace` JSON fix, hand this to Claude Code rather than hand-editing — it's a one-line fix but worth having it verify the result parses:

> Open `coding-project-templates.code-workspace` (both the root copy and the one under `.vscode/`). Both currently have a JSON syntax error: an extra `},` immediately after the `"path": "features"` folder entry, before the `"claude"` entry opens. Remove the stray `},` so the folders array is valid JSON (leave the `//` comments — this is JSONC, VS Code expects them). After editing, strip the comments and confirm the result parses as valid JSON. Show me the diff.

## Phase 2 — Root `CLAUDE.md` *(was your phase 6)*

Claude Code prompt:

> Read `coding-project-templates-summary.md` and `claude/2-GitHub and Claude Code Workspace Plan.md` in the repo root. Using them, write a concise root-level `CLAUDE.md` — aim for well under 100 lines — documenting: (1) this repo is a multi-template VS Code/Claude Code scaffold library; `features/*` are **git worktrees, not submodules**, each checked out on its own branch — include the worktree→folder→branch map table from the summary doc; (2) `claude/` holds sequentially numbered task notes (`claude/N-*.md`) — future sessions should read the latest few in order for context before starting work; (3) commit convention: changes to root-level files commit to `main` from the repo root, changes inside a `features/<name>` folder commit to that worktree's own branch — never mix the two in one commit; (4) once it exists, mention `scripts/git-sync-all.sh` as the way to check status and commit/push across every worktree in one pass. Keep it factual and stable — this file will be read by every future Claude Code session in this repo, so don't restate per-template status here (that lives in the summary doc and will go stale in `CLAUDE.md` the moment any template changes).

Optional, same sitting: if you want the "commit globally and per-worktree" helper script from the earlier plan actually built rather than just described, add:

> Also create `scripts/git-sync-all.sh`: for each worktree from `git worktree list --porcelain`, show `git status -s`, and if it's dirty, prompt before running `git add -A && git commit -m "<message>" && git push`. Make it executable and add a one-line mention in the new `CLAUDE.md`.

## Phase 3 — Finish the base template *(was your phase 2)*

`features/claude-code-basic` already has an approved plan sitting in `.claude/plan.md` — this phase is "execute the plan that's already written," not "design something new."

Claude Code prompt (run with your terminal cd'd into `features/claude-code-basic`, branch `claude-code-b`):

> Read `.claude/plan.md` in this folder in full — it's an already-approved implementation plan for rewriting `todo.md` and `README.md` from SQL-database-specific to language-agnostic, plus adding explanatory comments to `requirements.txt`. Execute that plan exactly as written: rewrite `todo.md` per the new section structure it describes, expand `README.md` per the structure it describes, add the header comments to `requirements.txt` (Option B in the plan). Work through the plan's own "Verification Steps" section before you consider this done. Then commit on the `claude-code-b` branch with a message describing the base-template rewrite, and push.

Review the diff yourself before moving on — everything in phase 4 depends on this content being right, since it's about to get merged into nine other branches.

## Phase 4 — Propagate the base to the other 9 branches *(was your phase 3)*

Because every `features/*` folder is a worktree of the *same* repository, `git merge claude-code-b` from inside another worktree pulls the finished base straight in with full history — no copy-paste, no `--allow-unrelated-histories` needed (these branches already share a common ancestor).

I'd do this one worktree at a time rather than as one unattended loop, since conflicts are possible on `todo.md`/`README.md`/`requirements.txt` (every stub currently has its own copy of the old generic versions). Claude Code prompt, repeated per worktree — or give it the whole list and ask it to pause on conflicts:

> For each of these 9 worktrees — `features/claude-code-advance` (branch `claude-code-a`), `features/js-express` (`web-js`), `features/machine-learning` (`py-ml`), `features/manuals` (`manus`), `features/python-app` (`py-app`), `features/python-scripts` (`py-script`), `features/web-django` (`py-django`), `features/web-flask` (`py-flask`), `features/wsl-scripts` (`wsl-tools`) — `cd` into it and run `git merge claude-code-b`. This brings the finished base `todo.md`/`README.md`/`requirements.txt` in. If a merge conflict occurs, resolve it by keeping the base template's structure — there shouldn't be meaningful folder-specific content to preserve yet, since these are still generic stubs. After each successful merge, `git push origin <branch>` and move to the next worktree. Stop and show me the conflict if resolution isn't obvious, rather than guessing. Report a one-line summary per worktree at the end: clean merge / merged with conflicts resolved / skipped and why.

## Phase 5 — Bring each template to intermediate level *(was your phase 4)*

The biggest phase, and the one your own plan already said doesn't need to happen all at once — do it template-by-template as you actually need each one. Same shape of prompt each time, language specifics differ:

| Template (branch) | What "intermediate" means here |
|---|---|
| `js-express` (`web-js`) | `package.json` (Express + Jest), `src/app.js` with one working route, `test/app.test.js`, `.env.example` |
| `web-flask` (`py-flask`) | App-factory skeleton (`app/__init__.py`, `run.py`), `requirements.txt` with Flask, `tests/test_app.py`, `.env.example` |
| `web-django` (`py-django`) | `django-admin startproject` scaffold, `requirements.txt` with Django, one app with a test, `.env.example` |
| `python-app` (`py-app`) | `src/main.py` entrypoint with a small CLI example, `tests/test_main.py` |
| `python-scripts` (`py-script`) | `scripts/` folder, one real `argparse`-based utility script, a matching test |
| `machine-learning` (`py-ml`) | `src/` pipeline skeleton (e.g. a small scikit-learn example), `requirements.txt` with the ML deps, one test on a data-processing function |
| `manuals` (`manus`) | Docs-site skeleton — `mkdocs.yml` + `docs/index.md` (or your preferred doc generator) |
| `wsl-scripts` (`wsl-tools`) | `scripts/*.sh` examples, `shellcheck` in CI |
| `claude-code-advance` (`claude-code-a`) | Once `claude-code-basic` is the finished "getting started" template, "advance" is the natural place for custom slash commands, subagents, and hooks examples — a step up from basic usage |

Every row also gets: a `.github/workflows/test.yml` that installs deps and runs the test scaffold on push, and keeping the merged base `todo.md`/`README.md` intact (add to it, don't replace the Claude Code guidance sections phase 3/4 brought in).

Claude Code prompt template — fill in the bracketed parts per row above:

> In `features/<folder>` (branch `<branch>`), bring this template to intermediate level: add real starter code for `<language, from the table>`, a matching test scaffold with one passing test, a `.env.example` if the stack needs config, and `.github/workflows/test.yml` that installs dependencies and runs the tests on push/PR. Keep the merged base `todo.md`/`README.md`/`CLAUDE.md` content intact — only add to it. Commit and push to `<branch>` when done.

## Phase 6 — Build the workspace generator *(was your phase 5)*

You said you want this delegated directly to Claude — meaning the generator itself should be something Claude Code can run (or extend), not a manual process you maintain by hand. `ProjectSetup-linux-os.py` already does most of the mechanical work (writing `project.env`, `project.csv`, the `.code-workspace` file); it just doesn't yet know how to pick specific templates or emit one workspace-folder entry per worktree. Claude Code prompt:

> Extend `ProjectSetup-linux-os.py`: add a `--templates` CLI flag accepting a comma-separated list of `features/*` folder names (e.g. `--templates web-flask,python-scripts`). When provided, `VSCodeConfigurator.subfolders` should build the workspace folders list as the existing root entries (`.git`, `.venv`, `.vscode`) plus one entry per selected `features/<name>` — not a single `"features"` entry — and generate per-folder `settings` appropriate to that template's language (Python interpreter/pytest paths for the Python ones, an ESLint-friendly block for `js-express`, etc. — infer these from what phase 5 put in each template). Fix the existing bug where an extra closing brace gets emitted right after the folders array (see `claude/2-GitHub and Claude Code Workspace Plan.md`, §1 and §3.3, for the exact spot). When run with no `--templates` flag, keep the current full-repo behaviour so nothing that depends on it today breaks. Test it by generating a workspace for `--templates web-flask,python-app` and confirming the output is valid JSON and opens the right two folders.

Once this works reliably, a natural follow-on (not required now) is wrapping it as a Claude Code custom slash command — `.claude/commands/generate-workspace.md` — so future sessions can just run `/generate-workspace web-flask,python-app` instead of remembering the flag.

## How to actually run this

I'm not the same process as your local Claude Code CLI — I can't drive your terminal directly. The pattern for each phase above: open a `claude` session at the repo root (or the specific worktree folder named), paste the prompt block, review its diff/commit before moving to the next phase. Phases 4 and 5 especially are worth reviewing worktree-by-worktree rather than trusting a single unattended run across all nine — merge conflicts and language-specific scaffolding are exactly the kind of thing worth a human glance before it's pushed.

If you'd rather I ran phase 0 or phase 1's plain commands myself right now (through this session's connection to your machine) instead of you pasting them into Claude Code, say so — I can do the `gh`/`git` commands directly, I just can't remove `.git/index.lock` without you granting delete permission first.
