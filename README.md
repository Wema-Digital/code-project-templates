# vscode-workspace-gen — Multi-Template Workspace Generator

> A `coding-project-templates` tool: interview someone about what they want, then produce a standalone project folder combining the templates they picked, ready to open in VS Code.

---

## What this does

`coding-project-templates` holds a dozen independent templates (`web-flask`, `python-scripts`, `js-express`, ...), each its own git worktree branch. Most projects only need two or three of them combined into one place — this tool builds that combination as a real, standalone folder:

- `.vscode/*.code-workspace` — a multi-root workspace file, written for the target machine (native Windows or WSL2), using `${workspaceFolder}`-relative paths only
- `features/<template>/` — one git worktree per selected template, each still a full git branch with history
- `scripts/` — small setup/sync/health-check/repair helpers for the generated project (see "If you move the generated project" below)
- `README.md`, `CLAUDE.md`, `.workspace-manifest.json`, `.gitignore`, `todo.md` — docs and a record of what went in

The output has **no ongoing dependency on this repo's location**: it carries its own bare git clone (`.git-store/`) rather than pointing back at `coding-project-templates`. See `CLAUDE.md` for why that distinction matters and how it's done — and for a real caveat found while building this (moving the *generated* project afterward needs a repair step; standalone from the source repo isn't the same as immune to being moved).

---

## The 4-step process

1. **Interview** — `/generate-workspace` with no arguments. The `workspace-architect` subagent drafts a spec from what's known; the command asks you anything still missing (which templates, output path, Windows or WSL2). Nothing gets written to the output path yet.
2. **Plan saved to `claude/`** — the spec lands at this worktree's own `claude/N-Title.md`, a plain markdown file you can read and edit like any other planning note.
3. **Your review** — check the spec matches what you actually meant before anything gets generated. This step exists specifically to catch a misread requirement before it becomes a folder full of files.
4. **Build** — `/generate-workspace claude/N-title.md`, once you've confirmed it. Runs `scripts/generate-workspace.py`: bare clone, worktrees, `.vscode/`, docs, scripts.

---

## How to invoke it

From a Claude Code session opened in `features/vscode-workspace-gen`:

```
/generate-workspace
```

or hand it context directly:

> "I want a new project with web-flask and python-scripts, output to ~/projects/my-app, targeting WSL2."

Once the resulting `claude/N-*.md` spec looks right:

```
/generate-workspace claude/2-my-app-workspace.md
```

### Repeating a template (NAME:ALIAS)

Each templates entry, in `--templates` or in a spec's `templates:` list, may be `NAME` or
`NAME:ALIAS`. Use `NAME:ALIAS` when one output needs the same template more than once, for
example two independent `claude-code-basic` agents backing two unrelated components: the
worktree still checks out `NAME`'s branch and history, it just lands in `features/<ALIAS>`
instead of `features/<NAME>`, so it doesn't collide with the other selection of the same
template. Every alias in one generation must be unique.

```bash
python3 scripts/generate-workspace.py \
  --templates claude-code-advance:keyword-agent,python-scripts:keyword-scripts,claude-code-basic:notion-agent,python-app:notion-scripts \
  --output ~/projects/youtube-pipeline --project-name youtube-pipeline --target wsl2
```

You can also run the generator directly, without a spec file or a live Claude Code session:

```bash
python3 scripts/generate-workspace.py \
  --templates web-flask,python-scripts \
  --output ~/projects/my-app --project-name my-app --target wsl2
```

Add `--dry-run` to see the plan without writing anything, `--force` to write into a non-empty output directory, `--source-repo <path>` if not run from inside this repo.

---

## Project Layout

```
vscode-workspace-gen/
├── .claude/
│   ├── commands/
│   │   ├── generate-workspace.md      # /generate-workspace — interview or build, by $ARGUMENTS
│   │   └── todo-next.md               # inherited from claude-code-advance
│   ├── agents/
│   │   ├── workspace-architect.md     # drafts the claude/N-*.md spec; reports NEEDS-INPUT/DRAFT-READY
│   │   └── doc-sync-checker.md        # inherited from claude-code-advance
│   ├── hooks/
│   │   ├── validate-json.sh           # inherited — checks this template's own .claude/*.json
│   │   └── validate-workspace-json.sh # checks a hand-edited *.code-workspace still parses
│   ├── settings.json
│   └── plan.md                         # this template's own construction plan
├── scripts/
│   ├── generate-workspace.py          # the core logic — bare-clone, worktrees, docs, manifest
│   ├── setup-env.sh                   # copied into generated output
│   ├── sync-templates.sh              # copied into generated output
│   ├── health-check.sh                # copied into generated output
│   ├── git-sync-all.sh                # copied into generated output
│   └── repair-worktrees.sh            # copied into generated output
├── claude/                             # interview specs land here, one claude/N-*.md per request
├── CLAUDE.md                           # standing rules, output shape, the worktree-move caveat
└── README.md                           # this file
```

Phase 6 complete — Card 3's full checklist ran for real: portability (deleted the isolated source copy entirely, not just moved it — generated worktrees kept working, including a real commit), both Windows and WSL2 target variants, `scripts/health-check.sh` passing clean against a real generated project, and the workspace file opening in VS Code. Testing surfaced and fixed two real bugs: three Phase 5 templates' own CI was silently broken (added `pytest.ini` to `python-scripts`, `web-flask`, `machine-learning`), and `scripts/sync-templates.sh` silently did nothing (`git clone --bare`'s `origin` remote lacks a fetch refspec by default — fixed in both `generate-workspace.py` and `sync-templates.sh`). Full account in `.claude/plan.md`'s Card 3 addendum. Not done: a literal live `/generate-workspace` interview through a separate Claude Code session opened in this worktree.

---

## Working with Claude Code

Useful prompts to get started:
- *"/generate-workspace"* or *"Interview me for a new workspace with [templates]."*
- *"/generate-workspace claude/N-title.md"* once a spec is reviewed
- *"Run the doc-sync-checker agent against the generated output before I open it."*

---

**Template Version**: 1.1 (Phase 6 complete, Card 4: NAME:ALIAS support added 2026-08-29)
**Last Updated**: 2026-08-29
**Branch**: `vscode-gen` | **Stack**: Claude Code (commands, subagents, hooks) + Python 3 (generator script, PyYAML for `--spec` parsing) — no runtime deps for the template itself
