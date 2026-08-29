# Workspace spec and rollout plan: youtube-pipeline

Status: draft, NEEDS-INPUT (1 open item blocks Build; output_path confirmed 2026-08-28; template collision resolved 2026-08-29)

## Summary

First real use of `vscode-workspace-gen` since Phase 6 closed. Builds the local, multi-worktree workspace for the YouTube keyword-intelligence and production pipeline described in `keyword_pipeline_integration_v8.mermaid` and `YouTube_Pipeline_Ownership_and_Workspace_Map.md`, plus a third component (a Notion.so API integration) confirmed in chat but not yet documented in the ownership map. This file plays two roles at once: it is the `workspace-architect` style spec `generate-workspace.py --spec` will eventually consume, and the broader end-to-end rollout plan (GitHub, content build-out, verification) that sits around it, since this request is bigger than the generator's own four-field spec.

## Resolved so far (this session's Q&A)

- Target machine: `wsl2`.
- "Own repo" in the ownership map means a `features/<name>` git worktree aligned with how `coding-project-templates` itself is structured, not a separate GitHub remote per component. One new repo, multiple worktrees.
- The checklist's "notion workspace" item is a Notion.so API integration: a starter-template pairing (agent plus Python) built to work with the `notion.so` Python client library, not the ownership map's `00_keyword-intelligence`. `00_keyword-intelligence` was offered as the worked example of what "an agent, and a python project" looks like for a `claude code` component, not as the notion component itself.
- First GitHub step creates both a repository and a Project board (mirroring `scripts/setup-github-project.sh`'s pattern for `coding-project-templates` itself: Phase field, seeded tasks).
- Template collision (open item 1 below) resolved: `generate-workspace.py` now accepts `NAME:ALIAS` entries in `templates:`, so the same template can be selected more than once under distinct folder names. Full change and verification recorded in `.claude/plan.md`'s "Addendum: NAME:ALIAS support" (2026-08-29).

## Open items (NEEDS-INPUT)

Item 1 is resolved. Item 2 still blocks Build (well, blocks locking in the notion-integration row of `templates:` below; the other four rows are settled).

1. ~~**Template collision.**~~ RESOLVED 2026-08-29: `generate-workspace.py` now accepts `NAME:ALIAS` selections (e.g. `claude-code-basic:notion-agent`), so the same template can back more than one component without colliding on `features/<name>`. Verified with a real end-to-end generation of three aliased worktrees; see `.claude/plan.md`'s addendum for the full change and test record.
2. **Notion-integration's actual job.** Confirmed it should exist and should use the `notion.so` Python library and API, but not yet what it reads or writes, or where it sits in the v8 diagram's flow (a fourth workbook mirror? a content-calendar sync? something else). Needed before the notion-integration row of the spec below is more than a placeholder, and before any real content build-out in Phase 3. Does not block Phase 0 or generating the other four worktrees.

Not blocking, but worth a conscious decision rather than a silent default:

3. **`features/<name>` vs. the ownership map's flat paths.** The generator always writes `features/<template>/...`. The ownership map's tree shows flat paths with no `features/` wrapper (`you_tube/00_keyword-intelligence/`, not `you_tube/features/00_keyword-intelligence/`). Recommend keeping the generator's convention (consistency with `coding-project-templates` itself, zero generator changes) and updating the ownership map's tree diagram afterward, rather than patching the generator to drop a wrapper folder it also uses for its own bare-clone independence trick.
4. **Plain, non-git folders.** `_templates/`, `_pipeline-docs/`, and `_raw-exports/` in the ownership map's tree are explicitly *not* worktrees (`_raw-exports/` in particular needs a fixed path outside git so every isolated worktree run can reach it). `generate-workspace.py` only creates `features/<name>` worktrees plus its own standard docs and scripts; these three folders need a small manual step or a short follow-up script after Build, not something in scope for the generator itself.

## Draft spec

```yaml
templates:
  - claude-code-advance:keyword-intelligence-agent    # Routine, worktree toggle on, vision-based A2 matching against capture.mp4
  - python-scripts:keyword-intelligence-scripts       # append_snapshot.py and Keyword Bank utilities (A3, A5's Search Volume normalisation)
  - claude-code-basic:production-pipeline-agent       # interactive, no standing Routine, human present every stage
  - python-app:production-pipeline-app                # workbook builders (openpyxl, find_row() write-back, SEO refresh check)
  - claude-code-basic:notion-integration-agent        # PLACEHOLDER pending open item 2 -- interactive agent assumed, not a standing Routine
  - python-scripts:notion-integration-scripts         # PLACEHOLDER pending open item 2 -- python-scripts assumed over python-app until scope is known
output_path: /mnt/w/wema-studio/vscode_workspace/you_tube
project_name: youtube-pipeline
target: wsl2
```

## Notes

- `output_path` confirmed 2026-08-28: base is `W:/wema-studio/`, translated to the WSL2 mount `/mnt/w/wema-studio/vscode_workspace/you_tube` (the ownership map's own tree root). Still not verified for existence or emptiness from this session, since only `coding-project-templates` is connected here, not `wema-studio` -- `generate-workspace.py` refuses a non-empty output dir without `--force`, so a quick `ls` before Build is worth doing.
- Suggested GitHub repo name: `youtube-pipeline` (kebab-case, matches `code-project-templates`'s own naming). Open to a different name.
- `gh` is authenticated in the user's own terminal, not in this session's `device_bash` environment (different shell/PATH, per this repo's own memory notes) -- any GitHub-creating script below is delivered for the user to run, same constraint as the existing `scripts/*.sh` in this repo.
- The two `notion-integration-*` rows in the draft spec are placeholders (`claude-code-basic` + `python-scripts`), not a settled decision -- swap either template, or drop the `python-scripts` choice for `python-app` if the integration turns out to need real package structure, once open item 2 answers what it actually does.

---

# End-to-end rollout plan

## Phase 0: GitHub repository and Project board

- 0.1 Write a `setup-github-repo-youtube-pipeline.sh`, modelled on `scripts/setup-github-project.sh`: `gh repo create Wema-Digital/youtube-pipeline`, default branch `main`, branch protection matching the existing convention.
- 0.2 Write a Project-board script (or extend `setup-github-project.sh`'s pattern) for a new board scoped to this repo: a Phase field covering this plan's phases (0 to 4 below) instead of `coding-project-templates`'s own six.
- 0.3 User runs both scripts (their terminal has `gh` auth). Claude then verifies structure: `gh repo view`, `gh project list --owner Wema-Digital`, confirm the Phase field and seeded tasks match what the scripts intended, the same "check project structure" verification already used for `coding-project-templates`'s own GitHub Project.

## Phase 1: Interview

- 1.1 Resolve open item 2 above (this chat, or a live `/generate-workspace` session opened inside `features/vscode-workspace-gen`, since Card 3's own todo flags that a real live interview through a Claude Code session has never actually been run) -- item 1 no longer applies, see Resolved above.
- 1.2 Once resolved, `workspace-architect` (or this document, updated) reaches `templates` / `output_path` / `project_name` / `target` all unambiguous, and reports `DRAFT-READY` in place of this file's current `NEEDS-INPUT` status.
- 1.3 Human review of the finished spec, the same review step that exists for the tool's own generation runs and for this repo's own `claude/N-*.md` docs.

## Phase 2: Build

- 2.1 `python3 scripts/generate-workspace.py --spec claude/1-YouTube-Pipeline-Workspace-Plan.md` (or `--dry-run` first) from inside `features/vscode-workspace-gen`.
- 2.2 `git remote add origin <Phase-0 repo URL>` against the generated `.git-store`, push every selected template's branch (the bare clone already carries full history per branch, confirmed in Card 3's portability test).
- 2.3 `scripts/health-check.sh` against the generated output.
- 2.4 `scripts/repair-worktrees.sh` is a known follow-up if this generated project is ever moved after Build; worth noting in its own `README.md`/`todo.md`, which `generate-workspace.py` already writes automatically.

## Phase 3: Content build-out (the actual pipeline logic, outside the generator's own scope)

Mapped to the ownership map's own "Still outstanding" list and the v8 diagram:

- 3.1 `00_keyword-intelligence`: `append_snapshot.py` (A3), the `<750` Search Volume gate and `Insufficient Volume` tag (A_VOL/A_INSUFF), the A5 auto-compute formula once volume is normalised, the Claude Code Routine config itself (worktree toggle on, biweekly schedule).
- 3.2 `production_pipeline`: build the `W2` (Series Candidates Workbook) and `W3` (Singles Tracker Workbook) skeletons, both still flagged "needs to be built"; the `find_row()` label-scan write-back between `S1` and `W1`/`W3`; the `SEO_CHECK` refresh logic against the Keyword Bank.
- 3.3 `A7`'s lane and health clustering logic: still the "unopened box" per the ownership map, needed before `C1` (which depends on it) can run for real. This is a design task, not just an implementation one, and should probably get its own short spec before code.
- 3.4 Notion-integration: blocked on open item 2 above.
- 3.5 `OPT1` (Unclaimed Backlog sheet): still an open yes/no per the ownership map, independent of everything else here.

## Phase 4: Verification and the Cowork Project checklist item

- 4.1 Run `doc-sync-checker` against the generated output once Phase 3 content exists, to catch drift between what the docs claim and what's actually on disk (the same check `vscode-workspace-gen` ran on itself during Card 1).
- 4.2 Revisit the four-item artefact checklist already tracked for `coding-project-templates` itself and apply it to this new repo: GitHub Project (Phase 0), VS Code Workspace (Phase 2), GitHub Repository (Phase 0), Claude Cowork Project. The last one is a plugin and is explicitly not built yet even for `coding-project-templates` itself; decide separately whether `youtube-pipeline` needs its own, or can share one.
