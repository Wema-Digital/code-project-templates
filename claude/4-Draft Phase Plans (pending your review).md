# Draft phase plans — pending your review

*Prepared 2026-08-23. Companion to `scripts/setup-github-project.sh`, which is the one piece that's fully execution-ready right now. Everything below is deliberately a draft outline, not a Claude Code prompt — the idea is you review/edit each phase here first, and I turn the approved version into an execution prompt right before that phase runs.*

## Phase 1 — Housekeeping

- Remove the stale `.git/index.lock` at the repo root
- `git worktree prune` (clears the orphaned `js-express1` registration)
- Fix the JSON syntax error in `coding-project-templates.code-workspace` — root copy and the `.vscode/` copy both have it
- `gh auth setup-git`, now that `gh` is authenticated, so pushes/pulls don't prompt separately

Open question: none really — this is mechanical. Flag if you'd rather I skip the JSON fix here and fold it into phase 6 instead, since the generator is going to rewrite that file anyway.

## Phase 2 — Root `CLAUDE.md`

- Draft a short root-level `CLAUDE.md`: repo purpose, the worktree→branch map, the root-vs-per-worktree commit convention, and the `claude/N-*.md` numbered-notes convention
- Optional: build `scripts/git-sync-all.sh` (status/commit/push across every worktree in one pass) at the same time, since it's the kind of thing `CLAUDE.md` would want to mention

Open question: do you want `CLAUDE.md` to also document the GitHub Project/phase-tracking convention we're setting up right now, once it exists?

## Phase 3 — Finish the base template (`claude-code-basic`)

- Execute the plan already sitting in `features/claude-code-basic/.claude/plan.md` — rewrite `todo.md`, expand `README.md`, comment `requirements.txt`, run its own verification steps, commit + push on `claude-code-b`

Open question: that plan is from an earlier session — worth a quick skim before I execute it verbatim, in case anything in it is now out of date (e.g. it doesn't yet know about the `claude/` numbered-notes convention or the GitHub Project).

## Phase 4 — Propagate the base into the other 9 branches

- Per worktree: `git merge claude-code-b`, resolve conflicts (unlikely to be substantial — they're still generic stubs), push
- Nine merges, one per branch (listed in the project board)

Open question: merge one at a time and pause for your review each time, or batch all nine and give you one combined report to review before any of them push? (Last runbook proposed pause-per-conflict; batching with a final report might suit "review before execution" better if you'd rather see the whole set at once.)

## Phase 5 — Bring each template to intermediate level

- Real starter code + tests + `.env.example` (where relevant) + a CI workflow, per template — the language specifics from the last runbook still apply (Express/Jest for `js-express`, Flask app-factory for `web-flask`, Django scaffold for `web-django`, etc.)
- Nine templates, doable one at a time as you actually need each one — not a "do all nine now" phase

Open question: which template first? Given `claude-code-basic`/`advance` are the ones your own numbering treats as foundational, and the others are generic language stubs, I'd suggest starting with whichever one you actually have a real project waiting on — tell me and that becomes the first draft I write in full.

## Phase 6 — Workspace generator

This is the one where you specifically want to design further before I write anything, so this section is intentionally the thinnest. Your spec so far, restated:

A generator run produces a **standalone, workable folder** (not just a `.code-workspace` file) containing:

- `.vscode/` — the customised workspace file for the templates you picked
- `features/` — copies of just the customised starter templates you picked, not the whole library
- `README.md`
- an automation script, playing the same role `ProjectSetup-linux-os.py` plays for this repo, but scoped to the generated project — exact functionality still open, to define together

Questions I'd want answered before turning this into an execution prompt:

- Does the generated `features/` folder keep the worktree/branch structure (so the new folder is itself a clone with worktrees), or does it become plain copied files with no git history — i.e. is the output a new git repo of its own, or a non-git scaffold the person then `git init`s themselves?
- Where does the generated folder get created — a path you pick each run, or always alongside `coding-project-templates`?
- For "fewer or new functionality" on the automation script — is the instinct to strip down `ProjectSetup-linux-os.py` (drop the `docs/` bilingual generation, keep the `.code-workspace`/`.env`/`.csv` generation), or is there something genuinely new you want it to do that today's script doesn't?
- Is this generator meant to run from inside `coding-project-templates` (`python ProjectSetup-linux-os.py --templates ...`), or eventually as its own installable CLI/Claude Code slash command independent of this repo?

Once you've got answers (or corrections) to those, I'll write phase 6's execution prompt the same way I did for the others.

---

**How to use this file:** edit or comment inline on whichever phase you want to adjust, or just tell me in chat — "phase 4, batch with one report" or "phase 6, output is a fresh git repo, script drops the docs/ generation entirely." Once a phase is approved, I'll write that phase's execution prompt (in the same style as the earlier runbook) as its own numbered file.
