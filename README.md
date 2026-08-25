# vscode-workspace-gen — Multi-Template Workspace Generator

> A `coding-project-templates` tool: interview someone about what they want, then produce a standalone project folder combining the templates they picked, ready to open in VS Code.

---

## What this does

`coding-project-templates` holds a dozen independent templates (`web-flask`, `python-scripts`, `js-express`, ...), each its own git worktree branch. Most projects only need two or three of them combined into one place — this tool builds that combination as a real, standalone folder:

- `.vscode/*.code-workspace` — a multi-root workspace file, written for the target machine (native Windows or WSL2)
- `features/<template>/` — one git worktree per selected template, each still a full git branch with history
- `scripts/` — small setup/sync/health-check helpers for the generated project
- `README.md`, `CLAUDE.md`, `.workspace-manifest.json`, `todo.md` — docs and a record of what went in

The output has **no ongoing dependency on this repo's location**: it carries its own bare git clone (`.git-store/`) rather than pointing back at `coding-project-templates`. See `CLAUDE.md` for why that distinction matters and how it's done.

---

## The 4-step process

1. **Interview** — a Claude Code session here asks which templates, what output path, and whether the target is native Windows or WSL2. It writes the answers as a spec to this worktree's own `claude/N-Title.md` — it does not touch the output path yet.
2. **Plan saved to `claude/`** — the spec is a plain markdown file you can read and edit like any other planning note.
3. **Your review** — check the spec matches what you actually meant before anything gets generated. This step exists specifically to catch a misread requirement before it becomes a folder full of files.
4. **Build** — once you confirm the spec, a Claude Code session here reads it and generates the output folder: bare clone, worktrees, `.vscode/`, docs, scripts.

---

## How to invoke it

```bash
# from features/vscode-workspace-gen
```

Start an interview:

> "I want a new project with web-flask and python-scripts, output to ~/projects/my-app, targeting WSL2."

Once the resulting `claude/N-*.md` spec looks right, ask for the build step explicitly:

> "The spec in claude/2-my-app-workspace.md looks right — generate it."

(Once `.claude/commands/generate-workspace.md` ships — Phase 6, Card 2 — this becomes `/generate-workspace` instead of a plain-English request for both steps.)

---

## Project Layout

```
vscode-workspace-gen/
├── .claude/
│   ├── commands/
│   │   └── todo-next.md          # inherited from claude-code-advance
│   ├── agents/
│   │   └── doc-sync-checker.md   # inherited from claude-code-advance
│   ├── hooks/
│   │   └── validate-json.sh      # inherited — checks this template's own .claude/*.json
│   ├── settings.json
│   └── plan.md                    # this template's own construction plan
├── claude/                        # interview specs land here, one claude/N-*.md per request
├── CLAUDE.md                      # standing rules: VS Code docs check, Windows/WSL2, bare-clone mechanism
└── README.md                      # this file
```

Not yet built: the interview command, the `workspace-architect` subagent, the generated-output JSON-validation hook, and the generator scripts themselves. See `CLAUDE.md`'s "Not yet built" table and `claude/7-Phase 6 Detailed Breakdown.md` at the repo root for the full Card 2/Card 3 checklist.

---

## Working with Claude Code

Useful prompts to get started:
- *"Interview me for a new workspace with [templates]."*
- *"Read claude/N-*.md and generate the output folder."*
- *"Run the doc-sync-checker agent against the generated output before I open it."*

---

**Template Version**: 0.1 (Card 1 — scaffold only)
**Last Updated**: 2026-08-25
**Branch**: `vscode-gen` | **Stack**: Claude Code (commands, subagents, hooks) — no runtime deps of its own
