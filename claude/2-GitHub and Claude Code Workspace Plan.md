# GitHub & Claude Code Workspace Plan — coding-project-templates

*Prepared 2026-08-23, in response to `claude/1-Check External Connections.md`. This is a plan to work from, not a record of changes already made — nothing in your repo has been modified while putting this together, beyond reading files.*

## 1. What I actually found in the repo

Before planning anything, I connected to `coding-project-templates` and checked the real state rather than assuming. Three things are worth knowing before you touch git:

| Finding | Detail |
|---|---|
| Remote is already correct | `origin` → `https://github.com/Wema-Digital/code-project-templates.git` (both fetch and push). The GitHub connection itself is not broken. |
| `gh` CLI is not installed | The environment your worktrees live in (the Linux VM behind your `W:\` mount) has git, but no `gh`. `git remote -v` works; `gh auth status` returns "command not found". |
| A stale `.git/index.lock` is blocking git operations | `git status` currently fails with `unable to unlink '.git/index.lock': Operation not permitted`. Until this file is removed, commits, checkouts, and worktree operations at the repo root will keep failing. This is almost always left behind by a crashed git process (often VS Code's Git extension or an interrupted `git worktree add`) rather than an actual concurrent operation. |

Two more structural things came out of the repo's own `coding-project-templates-summary.md` (dated today) plus a direct check I ran:

- **An orphaned worktree registration**, `js-express1`, points at a folder that doesn't exist (`features/features/js-express`) and duplicates the branch already checked out in `features/js-express`. Harmless but worth pruning before it causes a confusing error later.
- **`coding-project-templates.code-workspace` has a JSON syntax error.** After the `"features"` folder entry there's a stray extra `},` before the `"claude"` entry is opened — that's an unmatched closing brace. VS Code's JSONC parser may tolerate it silently or may reject the file depending on version; either way it should be fixed before you use this file as the basis for a generator (see §3.3).

None of this needs deep investigation to fix — it's listed here because a workflow plan built without checking this first would have told you to `git commit` into a repo that can't currently accept one.

## 2. GitHub repository: connection, and a real push/pull/commit workflow

### 2.1 Get `gh` working against Wema-Digital

Run these in the same shell where your worktrees live (the one `git remote -v` succeeded in):

```bash
# install (pick the one that matches that environment)
sudo apt install gh          # Debian/Ubuntu-style Linux VM
# or: winget install --id GitHub.cli   # if you'd rather drive this from native Windows/PowerShell

gh auth login                 # interactive — choose GitHub.com, HTTPS, browser login
gh auth status                 # confirms you're logged in and which account/org scopes you have
gh repo set-default Wema-Digital/code-project-templates
gh repo view                   # sanity check — should show the Wema-Digital repo
```

`gh auth login` is interactive (it opens a browser or asks for a device code), so this is the one step I can't do for you — but once it's done, `gh` remembers the credential and every command below works non-interactively.

### 2.2 Clear the two blockers first

```bash
cd /path/to/coding-project-templates
rm .git/index.lock            # only if no other git process is actually running — check first
git worktree prune             # clears the orphaned js-express1 registration
git worktree list              # confirm you're back to 11 clean entries (root + 10 features/*)
```

(In this session I could not remove `index.lock` myself — the device bridge I'm using doesn't have delete permission on your local files by default. Either delete it yourself with the command above, or tell me to request delete permission and I'll do it.)

### 2.3 The "global vs per-worktree" commit model

Because `features/*` are **git worktrees of the same repository**, not submodules, there's no special tooling needed — every worktree is a normal working copy on its own branch, all sharing one `.git` database. That gives you two natural commit scopes:

**Global (root, `main` branch)** — anything that isn't specific to one template: `ProjectSetup-linux-os.py`, the root `README.md`/`CONTRIBUTING.md`, `project.env`, `project.csv`, the `.code-workspace` file, this `claude/` planning folder.

```bash
cd coding-project-templates              # root worktree, branch main
git add <files>
git commit -m "..."
git push origin main
git pull origin main
```

**Individual (per feature worktree/branch)** — changes scoped to one template.

```bash
cd coding-project-templates/features/web-flask   # branch py-flask
git add <files>
git commit -m "..."
git push origin py-flask
git pull origin py-flask
```

Because every worktree shares the same object database, `git fetch` at the root updates refs for *all* branches at once — you only need to `pull`/`push` inside the specific worktree whose branch you're moving.

### 2.4 A "commit/push everywhere" helper

For the "globally... and individually to each worktree branch" case you described — e.g. after a batch update that touches several templates — a short script beats doing it by hand ten times. Something like:

```bash
#!/usr/bin/env bash
# scripts/git-sync-all.sh — status, then optional commit+push, across root + every worktree
set -e
MSG="${1:-sync: routine update}"

git worktree list --porcelain | awk '/^worktree /{print $2}' | while read -r wt; do
  echo "── $wt"
  git -C "$wt" status -s
  if [ -n "$(git -C "$wt" status -s)" ]; then
    read -p "  commit & push here with message \"$MSG\"? [y/N] " ans
    if [ "$ans" = "y" ]; then
      git -C "$wt" add -A
      git -C "$wt" commit -m "$MSG"
      git -C "$wt" push
    fi
  fi
done
```

Deliberately interactive (asks before each push) rather than fully automatic — safer while several templates are still mid-edit. Worth adding to the root repo once you're happy with it; I can write and commit this for you if you want it.

### 2.5 Branch/folder naming

Not urgent, but noted in the repo's own summary: folder names (`python-app`, `web-flask`) and branch names (`py-app`, `py-flask`) don't follow one convention, and two are non-obvious (`manuals` → `manus`, `claude-code-advance`/`basic` → `claude-code-a`/`b`). Worth aligning next time you touch `git branch -m`, or just keep this document as the mapping reference in the meantime.

## 3. Connect the workspace to Claude Code

### 3.1 What "a small Claude Code project" should mean here

Reading between the lines of what's already in the repo: you've started a convention of dropping numbered instruction files into `claude/` (`1-Check External Connections.md` is this very prompt) — that's effectively a lightweight Claude Code project already. I'd formalise it rather than replace it:

- Add a root-level `CLAUDE.md` (small, on purpose) that tells Claude Code: what this repo is (a multi-template scaffold library using git worktrees, not submodules), where the worktree map lives (`coding-project-templates-summary.md`), and that `claude/` holds sequential task notes it should read in order.
- Keep `claude/` as the running log — each new ask becomes `claude/N-Title.md`, each answer/plan can live alongside it (this document is `claude/2-...`, following that pattern).
- Don't scaffold more than that yet. A big `CLAUDE.md` with rules for ten different template types will go stale the moment any one template changes — better to add per-template `CLAUDE.md` files as each template matures (see 3.2), and keep the root one focused on repo-wide facts (worktree layout, branch map, the `git-sync-all.sh` convention once it exists).

### 3.2 Boilerplate → intermediate: what to actually add

Right now, 9 of 10 templates under `features/` are identical stubs: the same 2-line `README.md`, the same generic `requirements.txt` (pytest/python-dotenv/pandas regardless of language), and the same SQL-flavoured `todo.md` dated 2023-12-01. Only `claude-code-basic` has moved past that, and its own `.claude/plan.md` already lays out a good language-agnostic rewrite of `todo.md`/`README.md`.

"Intermediate" for the *other* nine means giving each template what it's named for, instead of the shared placeholder:

- **Real dependency files for the actual language** — `js-express` gets a `package.json` (Express + a test runner), `web-flask` gets a Flask app-factory skeleton and `requirements.txt` that actually lists Flask, `web-django` gets a `manage.py` + starter app via `django-admin startproject`, `machine-learning` gets a notebook or `src/` skeleton with a real ML dependency set, `python-app`/`python-scripts` get an actual entrypoint file, `wsl-scripts` gets example `.sh` scripts, `manuals` gets a docs-site skeleton (e.g. MkDocs) instead of an empty stub.
- **A minimal working example, not just config** — one runnable "hello" route/script/notebook per template, so cloning it and running one command proves the scaffold works.
- **A test scaffold matching the language** (pytest for Python ones, jest for `js-express`) with one passing example test.
- **A `.env.example`** where the template plausibly needs secrets/config (Flask, Django, Express), instead of committing `project.env`-style real values.
- **Basic CI** — one GitHub Actions workflow per template (`.github/workflows/test.yml`) that installs deps and runs the test scaffold on push. Cheap to add, and it turns "template" into "template that proves itself."
- **A short, template-specific `CLAUDE.md`** once the template has real content — this is where `claude-code-basic`'s in-progress language-agnostic `todo.md` becomes genuinely useful as the shared base (see 3.4).
- **Recommended VS Code extensions** (`.vscode/extensions.json`) scoped to that template's language, so opening just that worktree folder prompts the right tooling.

None of this needs to happen all at once or in every template simultaneously — see the phased roadmap in §4 for a sane order.

### 3.3 Generating a customised, ready-to-use VS Code workspace — yes, and you already have half of it

`ProjectSetup-linux-os.py` already generates `project.env`, `project.csv`, and the `.code-workspace` file from a `subfolders` scan — it's just currently scanning only direct children of the repo root, so it produces one `"features"` folder entry instead of one entry per template. Two changes make this a real "pick your templates, get a workspace" generator:

1. **Fix the existing bug first** — the malformed JSON in the current `.code-workspace` (the stray `},` noted in §1) should be corrected regardless, or any generator that reads/patches this file inherits the bug.
2. **Extend `VSCodeConfigurator.subfolders`** to recurse one level into `features/`, and add a selection step — either a CLI flag (`--templates web-flask,python-app`) or an interactive prompt — so the script writes a `.code-workspace` containing only the folders you actually want open, each as its own multi-root entry with language-appropriate `settings` (interpreter path for Python templates, `eslint`/`prettier` config for `js-express`, etc.) rather than the current one-size Python-only `settings` block.

That gets you: "I'm starting a Flask + a shared Python-scripts project" → run the generator → open one `.code-workspace` with both worktrees, correctly configured, no manual VS Code folder-adding.

### 3.4 How a starter template evolves and becomes complementary to others

Because every template is a branch of the *same* repository (not a separate repo), you're not limited to copy-pasting files between them — you can use real git history:

- **Treat `claude-code-basic` as the base layer.** Once its `todo.md`/`README.md` rewrite (per its own `.claude/plan.md`) lands, it becomes the canonical "any language, start here" scaffold — the piece every other template is currently missing.
- **Propagate it with `git merge`, not copy-paste.** From inside e.g. `features/web-flask` (branch `py-flask`): `git merge claude-code-b --allow-unrelated-histories` (or cherry-pick the specific commit) pulls the finished base `todo.md`/`README.md`/`CLAUDE.md` into that branch while preserving that this history came from the base template — future improvements to the base can be merged forward the same way instead of re-copied by hand.
- **Layer, don't overwrite.** Order per template: base (`claude-code-basic`) → language layer (real deps, entrypoint, tests — §3.2) → optional feature layer (e.g. `machine-learning` could later merge in something `python-app` develops, since they share a language layer). This is exactly what "complementary" should mean in practice: a change to the shared base template flows outward to every specific template via merge, and a genuinely reusable piece built in one specific template (a good `.github/workflows/test.yml` pattern, say) can flow sideways into siblings the same way.
- **Worktrees make this cheap to try** — since `features/web-flask` and `features/claude-code-basic` are worktrees of the same repo, testing a merge doesn't need cloning anything new; it's a normal `git merge` inside the worktree you want to update.

## 4. Suggested order of work

1. **Housekeeping (one sitting).** Remove `.git/index.lock`, `git worktree prune`, fix the `.code-workspace` JSON, install and authenticate `gh` against `Wema-Digital/code-project-templates`.
2. **Finish the base template.** Complete `claude-code-basic`'s existing `.claude/plan.md` (its `todo.md`/`README.md` rewrite) — everything in §3.4 depends on this being done first.
3. **Propagate the base.** Merge the finished base into each of the other nine branches.
4. **Bring each template to "intermediate."** Add the real language scaffolding, tests, CI, `.env.example` per §3.2 — can be done template-by-template as you actually need each one, doesn't have to be all nine before moving on.
5. **Build the workspace generator.** Extend `ProjectSetup-linux-os.py` per §3.3 once there are enough real templates worth selecting between.
6. **Formalise the Claude Code project.** Add the root `CLAUDE.md`, keep numbering `claude/N-*.md` for future asks (this document is `claude/2-...`).

## 5. What I can do right now, if you want me to

- Remove `.git/index.lock` (needs delete permission on your machine — I don't have it by default; say the word and I'll request it)
- Run `git worktree prune`
- Fix the JSON syntax error in `coding-project-templates.code-workspace`
- Draft the root `CLAUDE.md`
- Write `scripts/git-sync-all.sh`

I've held off doing any of these since you asked for a plan first — tell me which of the above to actually execute and I'll do it in this session.
