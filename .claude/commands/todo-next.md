---
description: Read todo.md and report the next task to work on, respecting priority symbols
argument-hint: "[section name, optional]"
allowed-tools: Read
---

Read todo.md. If an argument was given ("$ARGUMENTS"), only look at tasks under that section heading; otherwise consider the whole file.

Find the single next task to work on, in this priority order:
1. Any task marked `[⚠]` (critical issue)
2. Any task marked `[!]` (high priority)
3. Any task marked `[#]` (medium priority)
4. Any other unstarted `[ ]` task, in file order

Skip anything marked `[~]` (on hold), `[>]` (delegated), or `[x]` (completed).

Report:
- The task itself, with its section heading
- Which priority tier it matched
- Any `[@]` discussion markers nearby worth resolving before starting
