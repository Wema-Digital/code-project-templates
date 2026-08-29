# Workspace spec and rollout plan: youtube-pipeline

Status: DRAFT-READY (all open items resolved 2026-08-29; output_path confirmed 2026-08-28; template collision resolved 2026-08-29; notion-integration scope + template resolved 2026-08-29)

## Summary

First real use of `vscode-workspace-gen` since Phase 6 closed. Builds the local, multi-worktree workspace for the YouTube keyword-intelligence and production pipeline described in `keyword_pipeline_integration_v8.mermaid` and `YouTube_Pipeline_Ownership_and_Workspace_Map.md`, plus a third component (a Notion.so API integration) confirmed in chat but not yet documented in the ownership map. This file plays two roles at once: it is the `workspace-architect` style spec `generate-workspace.py --spec` will eventually consume, and the broader end-to-end rollout plan (GitHub, content build-out, verification) that sits around it, since this request is bigger than the generator's own four-field spec.

## Resolved so far (this session's Q&A)

- Target machine: `wsl2`.
- "Own repo" in the ownership map means a `features/<name>` git worktree aligned with how `coding-project-templates` itself is structured, not a separate GitHub remote per component. One new repo, multiple worktrees.
- The checklist's "notion workspace" item is a Notion.so API integration: a starter-template pairing (agent plus Python) built to work with the `notion.so` Python client library, not the ownership map's `00_keyword-intelligence`. `00_keyword-intelligence` was offered as the worked example of what "an agent, and a python project" looks like for a `claude code` component, not as the notion component itself.
- First GitHub step creates both a repository and a Project board (mirroring `scripts/setup-github-project.sh`'s pattern for `coding-project-templates` itself: Phase field, seeded tasks).
- Template collision (open item 1 below) resolved: `generate-workspace.py` now accepts `NAME:ALIAS` entries in `templates:`, so the same template can be selected more than once under distinct folder names. Full change and verification recorded in `.claude/plan.md`'s "Addendum: NAME:ALIAS support" (2026-08-29).
- Notion-integration scope (open item 2 below) resolved: the integration is a general Notion-API interaction layer for working with Notion workspaces; the project is not yet fully developed, so it goes in as a scaffold to grow into. Template choice confirmed 2026-08-29 as `python-app` (not `python-scripts`) — real package structure is expected as the integration matures — paired with a `claude-code-basic` agent.

## Open items

All items resolved. Build is unblocked.

1. ~~**Template collision.**~~ RESOLVED 2026-08-29: `generate-workspace.py` now accepts `NAME:ALIAS` selections (e.g. `claude-code-basic:notion-agent`), so the same template can back more than one component without colliding on `features/<name>`. Verified with a real end-to-end generation of three aliased worktrees; see `.claude/plan.md`'s addendum for the full change and test record.
2. ~~**Notion-integration's actual job.**~~ RESOLVED 2026-08-29: it is a general Notion-API interaction layer for Notion workspaces, not yet fully developed. It goes in now as a scaffold (a `claude-code-basic` agent + a `python-app` Python module built against the `notion-client` library); its precise reads/writes and its place in the v8 diagram flow are deferred to Phase 3 content build-out. `python-app` chosen over `python-scripts` because the integration is expected to grow into a real package.

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
  - claude-code-basic:notion-integration-agent        # interactive agent (no standing Routine) for driving the Notion-API layer
  - python-app:notion-integration-app                 # Notion-API interaction module, built against notion-client; scaffold to grow into (scope firms up in Phase 3)
output_path: /mnt/w/wema-studio/vscode_workspace/you_tube
project_name: youtube-pipeline
target: wsl2
```

## Notes

- `output_path` confirmed 2026-08-28: base is `W:/wema-studio/`, translated to the WSL2 mount `/mnt/w/wema-studio/vscode_workspace/you_tube` (the ownership map's own tree root). Still not verified for existence or emptiness from this session, since only `coding-project-templates` is connected here, not `wema-studio` -- `generate-workspace.py` refuses a non-empty output dir without `--force`, so a quick `ls` before Build is worth doing.
- Suggested GitHub repo name: `youtube-pipeline` (kebab-case, matches `code-project-templates`'s own naming). Open to a different name.
- `gh` is authenticated in the user's own terminal, not in this session's `device_bash` environment (different shell/PATH, per this repo's own memory notes) -- any GitHub-creating script below is delivered for the user to run, same constraint as the existing `scripts/*.sh` in this repo.
- The two `notion-integration-*` rows are now settled: `claude-code-basic:notion-integration-agent` + `python-app:notion-integration-app`. The `python-app` choice anticipates the integration growing into a real package; its concrete job (what it reads/writes in Notion, where it plugs into the v8 flow) is still open and lands in Phase 3, but that no longer blocks Build — the worktree goes in as a scaffold.

---

# End-to-end rollout plan

## Phase 0: GitHub repository and Project board — DONE 2026-08-29

Scripts live in `rollout/youtube-pipeline/` (not `scripts/` — that folder is generator machinery copied into output; these are one-off rollout provisioning).

- 0.1 ~~Write `setup-github-repo-youtube-pipeline.sh`~~ DONE. Repo **`Wema-Digital/youtube-pipeline`** created: private, wiki disabled, empty (default branch resolves to `main` on the Phase 2.2 push). https://github.com/Wema-Digital/youtube-pipeline
  - **Branch protection: NOT applied — known limitation.** `Wema-Digital` is on GitHub's free plan, which allows neither branch-protection rules nor rulesets on *private* repos ("Upgrade to GitHub Pro or make this repository public"). Decision 2026-08-29: keep the repo private, accept no branch protection for now, revisit only if the org upgrades to Team. The script's "re-run after the Phase 2.2 push" fallback does not apply while the repo stays private on this plan.
- 0.2 ~~Write the Project-board script~~ DONE. `setup-github-project-youtube-pipeline.sh` created **Project #3 "YouTube Pipeline: Rollout"**, linked to the repo, with a `Phase` single-select field (options Phase 0–4) and 19 seeded task items (3 / 2 / 5 / 6 / 3 across the phases). https://github.com/orgs/Wema-Digital/projects/3
- 0.3 ~~Verify structure~~ DONE. `gh repo view` and `gh project view 3` confirm: repo private+empty, Phase field has exactly the 5 expected options, 19 items distributed across phases matching the script's intent.

## Phase 1: Interview

- 1.1 ~~Resolve open item 2~~ DONE 2026-08-29 (this chat): notion-integration is a Notion-API interaction layer, not fully developed, going in as a scaffold; template locked to `python-app:notion-integration-app` + `claude-code-basic:notion-integration-agent`. Item 1 no longer applies, see Resolved above.
- 1.2 DONE: `templates` / `output_path` / `project_name` / `target` all unambiguous; status above flipped to `DRAFT-READY`.
- 1.3 Human review of the finished spec — the same review step that exists for the tool's own generation runs and for this repo's own `claude/N-*.md` docs. (Pending sign-off before running Phase 2.)

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
- 3.4 Notion-integration: the worktree exists after Phase 2 as a scaffold. Phase 3 work is defining its concrete job — what it reads/writes in Notion, and where (if anywhere) it plugs into the v8 flow — then building the `notion-client` calls in `features/notion-integration-app/` and the driving agent in `features/notion-integration-agent/`. Likely wants its own short spec before code.
- 3.5 `OPT1` (Unclaimed Backlog sheet): still an open yes/no per the ownership map, independent of everything else here.

## Phase 4: Verification and the Cowork Project checklist item

- 4.1 Run `doc-sync-checker` against the generated output once Phase 3 content exists, to catch drift between what the docs claim and what's actually on disk (the same check `vscode-workspace-gen` ran on itself during Card 1).
- 4.2 Revisit the four-item artefact checklist already tracked for `coding-project-templates` itself and apply it to this new repo: GitHub Project (Phase 0), VS Code Workspace (Phase 2), GitHub Repository (Phase 0), Claude Cowork Project. The last one is a plugin and is explicitly not built yet even for `coding-project-templates` itself; decide separately whether `youtube-pipeline` needs its own, or can share one.
