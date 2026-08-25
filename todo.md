# Todo — vscode-workspace-gen

> Workspace-generator-specific task tracking. Uses the same symbol system as `claude-code-advance`.

## Symbol Guide

| Symbol | Meaning | When to use with Claude |
|--------|---------|-------------------------|
| `[ ]` | Unstarted | Default for all new tasks |
| `[x]` | Completed | Ask Claude to mark tasks done |
| `[-]` | In-progress | Claude marks what it's actively working on |
| `[!]` | High priority | Focus here first |
| `[@]` | Needs discussion | Ask Claude for design input |
| `[?]` | Needs research | Have Claude research options |
| `[#]` | Medium priority | After `[!]` tasks |
| `[~]` | On hold | Skip for now |
| `[>]` | Delegated/deferred | Assigned elsewhere or future |
| `[⚠]` | Critical issue | Urgent bug or blocker |
| `[%]` | % complete | Track large in-progress features |

---

## Card 1 — Scaffold (done)

```markdown
- [x] [!] Worktree + branch: features/vscode-workspace-gen, branch vscode-gen, off claude-code-a
- [x] [!] README.md, CLAUDE.md, .claude/plan.md
```

---

## Card 2 — Generator content (done)

```markdown
- [x] [!] .claude/commands/generate-workspace.md — /generate-workspace, interview or build by $ARGUMENTS
- [x] [!] .claude/agents/workspace-architect.md — drafts claude/N-*.md, NEEDS-INPUT/DRAFT-READY contract
- [x] [!] .claude/hooks/validate-workspace-json.sh + settings.json entry — checks generated *.code-workspace parses
- [x] [!] scripts/generate-workspace.py — bare-clone + worktree mechanism, template discovery from root CLAUDE.md
- [x] scripts/setup-env.sh, health-check.sh, sync-templates.sh, git-sync-all.sh — copied into generated output
- [x] scripts/repair-worktrees.sh — not originally scoped; added after the move-breaks-worktrees finding (see plan.md)
```

---

## Card 3 — End-to-end test (done)

```markdown
- [x] [!] Generate a sample selection into a real scratch output folder — web-flask + python-scripts, kept around long enough to open in actual VS Code
- [x] Confirm .vscode/*.code-workspace opens correctly in VS Code (code CLI), not just that it's valid JSON
- [x] Confirm Windows-path and WSL2-path target variants both produce sensible settings — both generated for real; terminal.integrated.defaultProfile values re-verified against VS Code's current source
- [x] [!] Confirm portability properly: generated from an isolated bare copy of the source, then deleted that copy entirely (stronger than "moved") — worktrees kept working, including a real test commit
- [x] Run scripts/health-check.sh against the generated project with dependencies actually installed (via uv, no sudo needed), confirm it passes — required fixing two real bugs first, see plan.md's Card 3 addendum
- [>] [!] Run a full /generate-workspace interview through a live Claude Code session opened in this worktree (not just the script directly) — this orchestrating session isn't opened in features/vscode-workspace-gen, so workspace-architect isn't in its own available-agent list; deferred to a manual pass by a human here
- [ ] [?] Decide whether scripts/repair-worktrees.sh needs a mention in the top-level coding-project-templates README, since the underlying "worktrees break on move" fact applies to this repo's own features/* too
```

---

## Known gaps / discussion

```markdown
- [@] Phase 2's scripts/git-sync-all.sh was never built — this template's copy was written fresh instead of reused. Worth closing the loop: should the root repo now adopt this template's version verbatim, or does the root repo's own multi-worktree layout need something different?
- [ ] [?] .devcontainer/ generation — flagged nice-to-have in the process design doc, not built, no todo item to build it yet
- [ ] [@] Should generate-workspace.py support re-running against an existing output (add a template to an already-generated project) or is that out of scope for v1?
```

---

## Metadata

*Last Updated: 2026-08-25*
*Template Version: 0.2*
*Stack: Claude Code (commands, subagents, hooks) + Python 3 generator script*
