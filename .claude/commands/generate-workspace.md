---
description: Interview for a new generated workspace, or build one from an already-reviewed claude/N-*.md spec
argument-hint: "[path to a reviewed claude/N-*.md spec, omit to start a new interview]"
allowed-tools: Agent, Read, Write, Glob, Bash, AskUserQuestion
---

Two modes, chosen by whether `$ARGUMENTS` was given. Never do both in one run — the gap between drafting a spec and building from it is deliberate (see this worktree's `CLAUDE.md`), it's where a misread requirement gets caught before any files exist.

## Mode 1: no arguments — interview

1. Gather whatever's already known about what the user wants from the conversation so far.
2. Use the `workspace-architect` subagent to turn that into a spec, passing along everything gathered.
3. If it reports `NEEDS-INPUT:` with a list of questions — ask the user those questions directly (via `AskUserQuestion` where they're multiple-choice-shaped, e.g. Windows vs WSL2, or plain conversation otherwise). Then invoke `workspace-architect` again with the answers folded in. Repeat until it reports `DRAFT-READY:`.
4. Once `DRAFT-READY: claude/N-title.md` comes back, tell the user the spec is written and ask them to review it before anything gets built. **Stop here.** Do not proceed to Mode 2 automatically, even in the same conversation — that's the point of the gap.

## Mode 2: `$ARGUMENTS` is a spec path — build

1. Confirm the file exists (`Read` it) and looks like a reviewed spec — if its `Status:` line still says `draft` rather than `reviewed`, ask the user to confirm they've actually reviewed it before continuing (don't just proceed on the strength of it existing).
2. Run `python3 scripts/generate-workspace.py --spec "$ARGUMENTS"`. If it fails, report the error plainly — don't retry with guessed fixes.
3. On success, report the output path and the two things to do next: `cd` into it and run `scripts/setup-env.sh`, then open the `.vscode/*.code-workspace` file it printed.
4. Remind the user to look at the generated `todo.md` — it lists manual follow-ups the generator can't safely do for them.
