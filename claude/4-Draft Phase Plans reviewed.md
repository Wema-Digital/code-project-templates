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


## Phase 5: Bring Each Template to Intermediate Level

**Scope per template:**
- Real starter code + tests + `.env.example` (where relevant) + a CI workflow. Language-specific conventions from the last runbook still apply (e.g., Express/Jest for `js-express`, Flask app-factory for `web-flask`, Django scaffold for `web-django`, etc.)
- Full details live in each folder's `CLAUDE.md`

**Deliverables per template:**
1. **README.md**: Rewrite to match the project's language and type. Replace the generic description with a compact, clear synthesis specific to that template.
2. **requirements.txt** (or language-equivalent): Replace the current placeholder/copy-paste example with dependencies that actually fit the project. Suggest improvements where you see an opportunity to raise quality.
3. **todo.md**: Replace the generic template with tasks customized to the project's type and language, informed by your knowledge and relevant research.
4. **.claude/plan.md** : check the file and tell if we can add some update to improve the quality, or a simple starter plan aligned with the project type, the file is still generic.

**Pacing:** Nine templates total, but this isn't a "do all nine now" phase, work through them one at a time, as each is actually needed.

This is a substantial work package, so here's how we'll organize it.

**Next step:** Let's add concrete detail to Phase 5 (The github project) before starting. Each task above is currently written at a global, per-template level. Can we break each one down into smaller subtasks tailored to the specific characteristics of each project?

For example: 
"Bring js-express to intermediate (Express+Jest scaffold, CI)" is a high level title: can we add a description to each of the task, and smaller subtasks tailored to the specific characteristics of each project.

Based on all the description above, first write a small plan for claude code to update the project details on github.


Open question: which template first? Given `claude-code-basic`/`advance` are the ones your own numbering treats as foundational, and the others are generic language stubs, I'd suggest starting with whichever one you actually have a real project waiting on — tell me and that becomes the first draft I write in full.




## Phase 6 : vscode workspace generator

This is the one where you specifically want to design further before I write anything, so this section is intentionally the thinnest. Your spec so far, restated:

A generator run produces a **standalone, workable folder** as output (not just a `.code-workspace` file) containing:

- `.vscode/` : the customised workspace file for the templates you picked
    - with the customised `.code-workspace` file: Please always check for latest, robust, safe and ready configurations for vscode workspace attributes. Always check if the worskpace will run under a windows or a linux (WSL2) environement, (Ask to the user).

- `features/` : The customised starter templates you picked, not the whole library
    - starter template as ready to use as a git worktree branch

- `README.md`
- `scripts/` : for automation scripts
    - we can make useful scripts native to the new workspace. Make some suggestions.

- (I think we can get rid of this script, was useful in the past, but now seems to be over complications. What do you suggest ?) an automation script, playing the same role `ProjectSetup-linux-os.py` plays for this repo, but scoped to the generated project

- Exact functionality still open, to define together: There are any helpful additional functionality you would suggest or add to this project ?

Questions I'd want answered before turning this into an execution prompt:

- Does the generated `features/` folder keep the worktree/branch structure (so the new folder is itself a clone with worktrees), or does it become plain copied files with no git history — i.e. is the output a new git repo of its own, or a non-git scaffold the person then `git init`s themselves?

Yes, details above !

- Where does the generated folder get created — a path you pick each run, or always alongside `coding-project-templates`?

Good, question: Let's define the whole process as a customised version of ´claude-code-advance´ where the goal of the agent, subagent, hooks, etc ... is the to help the user via a claude code session to generate the workspace folder as output.

The process would start with a pre plan created during a claude cowork session, where claude suggest to the user what (generic workspace or customised workspace) is possible to create. This plan can be saved as ready to review and execute document in ´claude/´ folder. 

I also think here, that we can create a specific feature project called "vscode-workspace-gen" for example, with a git worktree branch, like all others worktree branch and project.

What do you suggest about this process ?

- For "fewer or new functionality" on the automation script — is the instinct to strip down `ProjectSetup-linux-os.py` (drop the `docs/` bilingual generation, keep the `.code-workspace`/`.env`/`.csv` generation), or is there something genuinely new you want it to do that today's script doesn't?

Answer, above.

- Is this generator meant to run from inside `coding-project-templates` (`python ProjectSetup-linux-os.py --templates ...`), or eventually as its own installable CLI/Claude Code slash command independent of this repo?

Yes, as per the current proposal above. I think we can structure as follow:

First the user : make some research on the current cowork project, with a Q&A session to fully define the specifications of the 
workspace. 

Then, after all clarification and specifications are clear, cowork create a preliminary plan, to be saved in folder ´claude/´ with the "N-title" style. 

The user review the plan and make necessary modifications. 

Finally, the user open a claude code session from folder ´features/vscode-workspace-gen´ on terminal and both collaborate to create the workspace as an output.


I think, that's all for now. 

What do you suggest ? 

When the process is clear, we can create a plan like "5-Phase 5 Detailed Breakdown.md", "6-Phase 6 Detailed Breakdown.md". Remmenber that the first thing, we need to do with the plan is to update and create the required tasks for phase 6, similar to what was done with phase 5.


---

**How to use this file:** edit or comment inline on whichever phase you want to adjust, or just tell me in chat — "phase 4, batch with one report" or "phase 6, output is a fresh git repo, script drops the docs/ generation entirely." Once a phase is approved, I'll write that phase's execution prompt (in the same style as the earlier runbook) as its own numbered file.



