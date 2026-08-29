# youtube-pipeline rollout scripts

One-off provisioning scripts for the `youtube-pipeline` workspace described in
[`../../claude/1-YouTube-Pipeline-Workspace-Plan.md`](../../claude/1-YouTube-Pipeline-Workspace-Plan.md).

These are **not** part of the generator template (nothing here is copied into
generated output). They live here because they are specific to this one rollout.

`gh` is authenticated in your own terminal, not in the Claude session, so **you
run these**, same as the root repo's `scripts/setup-github-*.sh`.

## Status: Phase 0 completed 2026-08-29

- Repo: https://github.com/Wema-Digital/youtube-pipeline (private, empty)
- Project #3: https://github.com/orgs/Wema-Digital/projects/3 (Phase field, 19 items)

## Run order (Phase 0)

```bash
ASSUME_YES=1 ./setup-github-project-youtube-pipeline.sh  # 0.2 — Project board, Phase 0–4 field + seeded tasks
./setup-github-repo-youtube-pipeline.sh                  # 0.1 — create repo, main default
```

(`ASSUME_YES=1` skips the interactive sanity-check prompt in the project script;
it verifies the Phase field has 5 options programmatically instead.)

Then structure is verified (`gh repo view`, `gh project view 3 --owner Wema-Digital`)
against what the scripts intended — Phase 0.3.

## Notes

- The repo is created **empty**. The generated workspace's own history
  (`<output>/.git-store`) is pushed later, by hand, in Phase 2.2.
- **Branch protection is NOT applied.** The `Wema-Digital` org is on GitHub's
  free plan, which allows neither branch-protection rules nor rulesets on
  *private* repos. Decision 2026-08-29: keep the repo private, accept no branch
  protection. `setup-github-repo-*.sh`'s step 3 will 403 on a private free-plan
  repo — that's expected. It only does anything if the repo is made public or
  the org upgrades to Team.
- Visibility defaults to `--private` in `setup-github-repo-*.sh`; flip to
  `--public` there if that decision is revisited.
