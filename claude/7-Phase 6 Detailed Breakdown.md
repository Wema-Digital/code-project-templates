# Phase 6: broken down - building `vscode-workspace-gen`

*Prepared 2026-08-23, following the three decisions confirmed just now: bare-clone-then-worktree for portability, small composable scripts instead of one monolith, and `claude-code-advance`'s generic examples built before this template extends them. `scripts/update-github-project-phase6.sh` pushes the checklist versions below into the existing three Phase 6 cards in the GitHub Project.*

Prerequisite, not a phase 6 task itself: confirm `claude-code-advance` has at least one working example slash command, subagent, and hook (its own phase 5 task) before starting here, since `vscode-workspace-gen` is meant to extend that content, not duplicate it from scratch.

## Card 1: Scaffold the new template

- [ ] Create the worktree and branch: `git worktree add features/vscode-workspace-gen -b vscode-gen claude-code-a` (branches off the finished `claude-code-advance` content, once that exists)
- [ ] README.md: what this tool does, the 4-step process (Cowork spec Q&A → plan saved to claude/ → your review → build here in Claude Code), how to invoke it
- [ ] CLAUDE.md: orient a Claude Code session opened in this folder: the job here is either (a) interviewing a user to define a new workspace's spec, or (b) reading an already-written `claude/N-*.md` spec and generating the output folder from it; encode the "check current VS Code docs before writing settings" instruction and the Windows-vs-WSL2 question as standing rules, not one-off reminders
- [ ] `.claude/plan.md`: the construction plan for the generator itself: bare-clone+worktree mechanism, output folder shape (`.vscode/`, `features/`, `README.md`, `scripts/`), the Q&A flow, what gets written where

## Card 2: Build the generator's agents, hooks, and scripts

- [ ] `.claude/commands/generate-workspace.md`: a custom slash command that starts the interview flow (which templates, output path, Windows or WSL2)
- [ ] `.claude/agents/workspace-architect.md` (or similar): a subagent whose job is asking the clarifying questions and producing the spec/manifest before any files get written
- [ ] A hook that validates the generated `.vscode/*.code-workspace` file is well-formed JSON before the run is considered done: directly motivated by the JSON syntax bug already found in this repo's own committed workspace file
- [ ] `scripts/generate-workspace.py` (or `.sh`): the core logic: bare-clone the repo into `<output>/.git-store`, `git worktree add` each selected template into `<output>/features/<name>`, write `.vscode/*.code-workspace` with OS-appropriate settings (`${workspaceFolder}`-relative paths, not hardcoded absolutes), write `README.md`, `CLAUDE.md`, `.workspace-manifest.json` (records which templates/commits went in), and a post-generation `todo.md` checklist for manual follow-ups (rename package, fill in `.env`, set up a remote for the new project's own history)
- [ ] `scripts/setup-env.sh`: bootstraps whichever languages actually got included, instead of assuming Python
- [ ] `scripts/sync-templates.sh`: pulls upstream improvements from `code-project-templates` into a generated project's branches after the fact
- [ ] `scripts/health-check.sh`: smoke-tests that each included template's own test suite still passes
- [ ] `scripts/git-sync-all.sh`: reused from phase 2's version, since a generated project can itself have several worktree branches

## Card 3: Test end to end

- [ ] Run the generator for a sample selection (e.g. `web-flask` + `python-scripts`) into a scratch output folder
- [ ] Confirm the output is genuinely standalone: move or rename the original `coding-project-templates` checkout temporarily and confirm the generated folder's worktrees still work (`git status`, `git log` in each `features/<name>`)
- [ ] Confirm `.vscode/*.code-workspace` parses as valid JSON and opens correctly in VS Code
- [ ] Confirm the Windows-path and WSL2-path variants both produce sensible settings (test at least one of the two directly; reason through the other if you can't test both environments here)
- [ ] Run `scripts/health-check.sh` against the generated project and confirm it passes
