#!/usr/bin/env python3
"""Generate a standalone multi-template project from coding-project-templates.

Implements the mechanism settled in claude/6-Phase 6 Process Design (review).md:
bare-clone the source repo into <output>/.git-store, then `git worktree add`
each selected template against that local bare clone (never against the live
source checkout). The result carries its own complete git history and has no
ongoing dependency on where the source repo happens to live.

Requires PyYAML (`pip install pyyaml`) only when reading a --spec file; the
--templates/--output CLI path has no extra dependency.

Usage:
    generate-workspace.py --spec claude/2-my-app.md [--dry-run] [--init-wrapper]
    generate-workspace.py --templates web-flask,python-scripts \\
        --output ~/projects/my-app --project-name my-app --target wsl2 \\
        [--workflow docs/flow.mermaid] [--init-wrapper] [--dry-run]

--workflow copies a diagram the workspace is derived from into
<output>/docs/workflows_diagrams/ and links it from the generated CLAUDE.md; a
--spec supplies the same thing via a `workflow:` list (paths relative to the
spec file). --init-wrapper runs `git init` on the output folder on a `main`
branch and adds scripts/push-wrapper.sh, so the wrapper's own glue files
(scripts/, *.code-workspace, docs/, CLAUDE.md, ...) get a history of their own;
the features/<alias> worktrees are gitignored there, each keeping its history
in .git-store/.

Each --templates entry (or each item in a --spec's `templates:` list) may be
either `NAME` or `NAME:ALIAS`. Use `NAME:ALIAS` when you want the same
template included more than once in one output, for example two independent
claude-code-basic agents backing two unrelated components: the worktree still
checks out `NAME`'s branch and history, but lands in `features/<ALIAS>`
instead of `features/<NAME>`, so it doesn't collide with another selection of
the same template. Aliases must be unique within one generation, and must
still be a safe folder name (letters, digits, `.`, `_`, `-`).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import NamedTuple

VALID_TARGETS = ("wsl2", "windows")

# Extensions worth recommending per selected template, keyed by the template
# itself (not the alias) -- an aliased worktree still runs the same stack.
EXTENSION_RECOMMENDATIONS = {
    "web-flask": ["ms-python.python"],
    "python-app": ["ms-python.python"],
    "python-scripts": ["ms-python.python"],
    "web-django": ["ms-python.python", "batisteo.vscode-django"],
    "machine-learning": ["ms-python.python", "ms-toolsai.jupyter"],
    "manuals": ["ms-python.python"],
    "js-express": ["dbaeumer.vscode-eslint"],
    "claude-code-basic": [],
    "claude-code-advance": [],
    "wsl-scripts": ["timonwong.shellcheck"],
}


class Selection(NamedTuple):
    """One resolved --templates/spec entry: the folder it will be written to
    (alias, defaults to template when no :alias was given), the source
    template it comes from, and the branch that template lives on."""
    alias: str
    template: str
    branch: str


def repo_root_from_script() -> Path:
    # This script lives at <repo>/features/vscode-workspace-gen/scripts/generate-workspace.py
    return Path(__file__).resolve().parents[3]


def discover_templates(source_repo: Path) -> dict[str, str]:
    """Parse root CLAUDE.md's Worktree map table -- the single source of truth
    for which templates exist and which branch each one lives on. Read live
    rather than hardcoded here, so this never drifts out of sync the way this
    repo's own docs have drifted before (see doc-sync-checker's whole reason
    for existing)."""
    claude_md_path = source_repo / "CLAUDE.md"
    if claude_md_path.is_file():
        claude_md_text = claude_md_path.read_text()
    else:
        # --source-repo may point at a bare repository (no working tree, so
        # CLAUDE.md isn't a plain file) -- fall back to reading it straight
        # out of the object database instead of assuming a checkout exists.
        result = subprocess.run(
            ["git", "-C", str(source_repo), "show", "HEAD:CLAUDE.md"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise SystemExit(
                f"error: no CLAUDE.md found at {claude_md_path} or via 'git show HEAD:CLAUDE.md' in {source_repo} "
                "-- is --source-repo pointing at coding-project-templates (working tree or bare)?"
            )
        claude_md_text = result.stdout

    templates: dict[str, str] = {}
    row_re = re.compile(r"^\|\s*`features/([\w.-]+)`\s*\|\s*`([\w.-]+)`\s*\|")
    for line in claude_md_text.splitlines():
        m = row_re.match(line.strip())
        if m:
            name, branch = m.group(1), m.group(2)
            if name == "vscode-workspace-gen":
                continue  # the generator itself is not a selectable output template
            templates[name] = branch
    if not templates:
        raise SystemExit(f"error: no template rows found in {claude_md_path}'s Worktree map -- table format may have changed")
    return templates


def parse_spec(spec_path: Path) -> dict:
    try:
        import yaml
    except ImportError:
        raise SystemExit("error: PyYAML is required to read --spec files: pip install pyyaml")

    text = spec_path.read_text()
    m = re.search(r"```yaml\n(.*?)\n```", text, re.DOTALL)
    if not m:
        raise SystemExit(f"error: no ```yaml fenced block found in {spec_path}")
    data = yaml.safe_load(m.group(1))
    for key in ("templates", "output_path", "project_name", "target"):
        if key not in data:
            raise SystemExit(f"error: {spec_path}'s yaml block is missing required key '{key}'")
    return data


def parse_template_selections(tokens: list[str], available: dict[str, str]) -> list[Selection]:
    """Resolve each `NAME` or `NAME:ALIAS` token against the available
    templates. Alias defaults to the template name when omitted. Every alias
    across the whole list must be unique -- that's what actually avoids the
    features/<name> folder collision that motivated :ALIAS in the first
    place, so it's checked here rather than left to git worktree add to fail
    on later with a much less clear error."""
    selections: list[Selection] = []
    seen_aliases: dict[str, str] = {}  # alias -> the token that claimed it
    unknown: list[str] = []

    for token in tokens:
        name, sep, alias = token.partition(":")
        name = name.strip()
        alias = alias.strip() if sep else name
        if not name or (sep and not alias):
            raise SystemExit(f"error: malformed template selection {token!r} -- expected NAME or NAME:ALIAS")
        if not re.fullmatch(r"[\w.-]+", alias):
            raise SystemExit(
                f"error: alias {alias!r} in {token!r} is not a safe folder name "
                "(letters, digits, '.', '_', '-' only)"
            )
        if name not in available:
            unknown.append(name)
            continue
        if alias in seen_aliases:
            raise SystemExit(
                f"error: alias {alias!r} is claimed by both {seen_aliases[alias]!r} and {token!r} -- "
                "each selection needs its own folder name, give one of them an explicit NAME:ALIAS"
            )
        seen_aliases[alias] = token
        selections.append(Selection(alias=alias, template=name, branch=available[name]))

    if unknown:
        valid = ", ".join(sorted(available))
        raise SystemExit(f"error: unknown template(s) {unknown} -- valid choices are: {valid}")
    if not selections:
        raise SystemExit("error: no templates selected")
    return selections


def validate_target(target: str) -> None:
    if target not in VALID_TARGETS:
        raise SystemExit(f"error: target must be one of {VALID_TARGETS}, got {target!r}")


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, **kw)


def clone_bare_store(source_repo: Path, output: Path) -> Path:
    git_store = output / ".git-store"
    run(["git", "clone", "--bare", str(source_repo), str(git_store)])
    # Guarantee an "origin" remote pointing at the source repo regardless of
    # what `git clone --bare` set up on its own -- sync-templates.sh depends
    # on this name being stable and correct.
    result = subprocess.run(
        ["git", "-C", str(git_store), "remote", "set-url", "origin", str(source_repo)],
        capture_output=True,
    )
    if result.returncode != 0:
        run(["git", "-C", str(git_store), "remote", "add", "origin", str(source_repo)])
    # `git clone --bare` does NOT configure a fetch refspec for the "origin"
    # it creates (bare repos aren't expected to track a remote) -- confirmed
    # by hand while testing sync-templates.sh: without this, `git fetch origin`
    # updates FETCH_HEAD only and silently populates no refs/remotes/origin/*
    # refs at all, so every branch in sync-templates.sh looks like "no
    # matching origin/<branch>" even right after a successful-looking fetch.
    run([
        "git", "-C", str(git_store), "config", "remote.origin.fetch",
        "+refs/heads/*:refs/remotes/origin/*",
    ])
    return git_store


def add_worktrees(
    git_store: Path, output: Path, selections: list[Selection]
) -> tuple[dict[str, str], dict[str, str]]:
    """Add one worktree per selection at features/<alias>. Returns
    ({alias: short_commit_sha}, {alias: branch_actually_checked_out}).

    An aliased selection (alias != template name) gets its own branch, forked
    from the template's source branch and named after the alias: an alias means
    "this is its own component", so it should own its history -- and when two
    selections share one source branch (e.g. two claude-code-basic agents for
    two unrelated parts of the project) git can't check that branch out in both
    worktrees anyway. A plain, un-aliased selection keeps the straight checkout
    of its template branch, so that path is byte-for-byte unchanged. The
    Counter is a belt-and-braces guard for the pathological case of two
    selections colliding on a source branch without distinct aliases."""
    branch_users = Counter(s.branch for s in selections)
    commits: dict[str, str] = {}
    branches: dict[str, str] = {}
    for s in selections:
        dest = output / "features" / s.alias
        if s.alias != s.template or branch_users[s.branch] > 1:
            run(["git", "-C", str(git_store), "worktree", "add", "-b", s.alias, str(dest), s.branch])
            branches[s.alias] = s.alias
        else:
            run(["git", "-C", str(git_store), "worktree", "add", str(dest), s.branch])
            branches[s.alias] = s.branch
        sha = subprocess.run(
            ["git", "-C", str(dest), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        commits[s.alias] = sha
    return commits, branches


def _is_python(template: str) -> bool:
    """Treat a template as Python-backed when it recommends the Python
    extension -- keeps one source of truth (EXTENSION_RECOMMENDATIONS) rather
    than a second hardcoded list that could drift from it."""
    return "ms-python.python" in EXTENSION_RECOMMENDATIONS.get(template, [])


def write_workspace_file(
    output: Path, project_name: str, selections: list[Selection],
    target: str, has_docs: bool = False,
) -> Path:
    # The .code-workspace goes at the OUTPUT ROOT, not <output>/.vscode/ --
    # folder paths in a workspace file resolve relative to the file's own
    # directory, so a file under .vscode/ makes every "features/<alias>" point
    # at .vscode/features/<alias> and load broken. Root placement is also the
    # VS Code convention (a .vscode/ folder is for settings.json / launch.json,
    # not the workspace file).
    #
    # Settings/launch/tasks reference the root via the NAMED multi-root variable
    # ${workspaceFolder:<project_name>}, not the bare ${workspaceFolder}. In a
    # multi-root workspace the bare form resolves to whichever folder happens to
    # be first and is unreliable across extensions; the named form is anchored to
    # the "." folder's explicit `name` below, so it always points at the output
    # root regardless of folder order or the output directory's basename.
    root = f"${{workspaceFolder:{project_name}}}"
    folders = [{"path": ".", "name": project_name}]
    folders += [{"path": f"features/{s.alias}"} for s in selections]
    if has_docs:
        folders.append({"path": "docs"})

    py = [s for s in selections if _is_python(s.template)]
    if target == "wsl2":
        venv_python = f"{root}/.venv/bin/python"
        venv_bin = f"{root}/.venv/bin"
    else:
        venv_python = f"{root}/.venv/Scripts/python.exe"
        venv_bin = f"{root}/.venv/Scripts"

    settings: dict = {
        "files.exclude": {"**/.git-store": True},
        "search.exclude": {"**/.git-store": True, "**/.venv": True},
        "files.watcherExclude": {"**/.git-store/**": True, "**/.venv/**": True},
        "files.autoSave": "afterDelay",
    }
    if target == "wsl2":
        settings["terminal.integrated.defaultProfile.linux"] = "bash"
        settings["terminal.integrated.env.linux"] = {"PATH": f"{venv_bin}:${{env:PATH}}"}
    else:
        settings["terminal.integrated.defaultProfile.windows"] = "PowerShell"
        settings["terminal.integrated.env.windows"] = {"PATH": f"{venv_bin};${{env:PATH}}"}

    if py:
        # One shared root .venv (see scripts/setup-env.sh). A features/<alias>
        # that needs its own interpreter overrides this in its own
        # features/<alias>/.vscode/settings.json, not here.
        settings["python.defaultInterpreterPath"] = venv_python
        settings["python.envFile"] = f"{root}/.env"
        settings["python.analysis.extraPaths"] = [
            f"{root}/features/{s.alias}" for s in py
        ]
        settings["python.testing.pytestEnabled"] = True
        settings["python.testing.unittestEnabled"] = False
        settings["python.testing.pytestArgs"] = [f"{root}/features/{s.alias}" for s in py]

    recommendations = {
        ext for s in selections for ext in EXTENSION_RECOMMENDATIONS.get(s.template, [])
    }
    if py:
        recommendations |= {"ms-python.debugpy", "charliermarsh.ruff"}

    launch: dict = {"version": "0.2.0", "configurations": []}
    if py:
        launch["configurations"].append({
            "name": "Python: current file",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
        })
        for s in py:
            launch["configurations"].append({
                "name": f"Pytest: {s.alias}",
                "type": "debugpy",
                "request": "launch",
                "module": "pytest",
                "args": [f"{root}/features/{s.alias}"],
                "console": "integratedTerminal",
            })

    def _task(label: str, script: str) -> dict:
        # `bash scripts/<x>` (not a bare ./ path) so the same task definition
        # runs under a wsl2 shell and under Git Bash on native Windows.
        return {
            "label": label,
            "type": "shell",
            "command": f"bash scripts/{script}",
            "options": {"cwd": root},
            "problemMatcher": [],
        }

    tasks = {
        "version": "2.0.0",
        "tasks": [
            _task("setup-env", "setup-env.sh"),
            _task("health-check", "health-check.sh"),
            _task("git-sync-all", "git-sync-all.sh"),
        ],
    }

    workspace = {
        "folders": folders,
        "settings": settings,
        "extensions": {"recommendations": sorted(recommendations)},
        "launch": launch,
        "tasks": tasks,
    }
    # Every path above is anchored to ${workspaceFolder:<project_name>} or is a
    # bare relative path -- never an absolute filesystem path. `target` only
    # switches genuinely OS-specific values (venv layout, terminal profile,
    # PATH separator).

    ws_path = output / f"{project_name}.code-workspace"
    content = json.dumps(workspace, indent=4)
    ws_path.write_text(content + "\n")

    # Self-check: re-parse what was just written. Catches a bug in this
    # script immediately rather than shipping a broken workspace file --
    # the exact failure mode that motivated the JSON-validation hook.
    json.loads(ws_path.read_text())
    return ws_path


def copy_workflow_docs(output: Path, files: list[Path]) -> list[str]:
    """Copy each workflow diagram into <output>/docs/workflows_diagrams/.
    Returns the copied paths relative to <output>, for linking in CLAUDE.md."""
    dest_dir = output / "docs" / "workflows_diagrams"
    dest_dir.mkdir(parents=True, exist_ok=True)
    rel: list[str] = []
    for f in files:
        dest = dest_dir / f.name
        shutil.copy2(f, dest)
        rel.append(str(dest.relative_to(output)))
    return rel


def write_manifest(
    output: Path, source_repo: Path, selections: list[Selection],
    commits: dict[str, str], branches: dict[str, str], target: str,
) -> None:
    manifest = {
        "source_repo": str(source_repo),
        "target": target,
        "templates": [
            {
                "folder": s.alias,
                "template": s.template,
                "branch": branches[s.alias],
                "source_branch": s.branch,
                "commit": commits[s.alias],
            }
            for s in selections
        ],
    }
    (output / ".workspace-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def write_readme(output: Path, project_name: str, selections: list[Selection]) -> None:
    lines = [
        f"# {project_name}",
        "",
        "Generated by `vscode-workspace-gen` from [coding-project-templates](https://github.com/Wema-Digital/code-project-templates).",
        "Standalone: this folder carries its own complete git history in `.git-store/` and has no",
        "dependency on the source repo's location after generation.",
        "",
        f"Open `{project_name}.code-workspace` (at this folder's root) in VS Code to load every",
        "component as one multi-root workspace.",
        "",
        "## Included templates",
        "",
    ]
    for s in selections:
        if s.alias != s.template:
            lines.append(f"- `features/{s.alias}/` (from `{s.template}`)")
        else:
            lines.append(f"- `features/{s.alias}/`")
    lines += [
        "",
        "## Getting started",
        "",
        "```bash",
        "scripts/setup-env.sh    # creates one shared .venv and installs whichever languages got included",
        "scripts/health-check.sh # smoke-tests each included template's test suite",
        "```",
        "",
        "See `todo.md` for manual follow-ups this generator can't safely do for you,",
        "and `CLAUDE.md` for what's included and how it was assembled.",
        "",
    ]
    (output / "README.md").write_text("\n".join(lines))


def write_claude_md(
    output: Path, project_name: str, selections: list[Selection],
    commits: dict[str, str], branches: dict[str, str], target: str,
    workflow_docs: list[str] | None = None, wrapper_inited: bool = False,
) -> None:
    forked = any(branches[s.alias] != s.branch for s in selections)
    lines = [
        f"# CLAUDE.md — {project_name}",
        "",
        "Generated by `vscode-workspace-gen`. This is a standalone project combining templates from",
        "`coding-project-templates`; each `features/<alias>/` is its own git worktree against the",
        f"bundled `.git-store/`, not the original repo.",
        "",
        f"Target machine this was generated for: **{target}**.",
        "",
        "## What's included",
        "",
        "| Folder | Template | Branch | Commit at generation |",
        "|---|---|---|---|",
    ]
    for s in selections:
        lines.append(f"| `features/{s.alias}` | `{s.template}` | `{branches[s.alias]}` | `{commits[s.alias]}` |")
    lines += [
        "",
        "A folder whose Template column differs from its own name was generated with an explicit",
        "`NAME:ALIAS` selection -- typically because this project needed the same template more than",
        "once (e.g. two independent agents for two unrelated components).",
    ]
    if forked:
        lines += [
            "",
            "Each aliased folder is on its **own branch**, named after the alias and forked from the",
            "template's source branch at the commit above -- an alias marks an independent component,",
            "so it owns its history rather than sharing the template's branch (which also lets two",
            "components come from one template without git refusing to check the same branch out",
            "twice). The Branch column shows that per-folder branch; the Template column shows where",
            "the code came from; `.workspace-manifest.json` records the `source_branch` for each.",
        ]
    lines += [
        "",
        "Full record in `.workspace-manifest.json`.",
    ]
    if workflow_docs:
        lines += [
            "",
            "## Workflow",
            "",
            "This workspace was generated from a workflow diagram. The source copy lives here:",
            "",
        ]
        lines += [f"- `{p}`" for p in workflow_docs]
        lines += [
            "",
            "Each component above maps to one or more nodes in that diagram; the spec's",
            '"Workflow coverage" table records the node-to-component mapping and per-node status.',
        ]
    lines += [
        "",
        "## Scripts",
        "",
        "- `scripts/setup-env.sh` — creates one shared `.venv` and installs whichever languages got included",
        "- `scripts/health-check.sh` — smoke-tests each included template's own test suite",
        "- `scripts/sync-templates.sh` — pulls upstream template improvements from the source repo",
        "- `scripts/git-sync-all.sh` — status/push helper across every included worktree branch",
        "- `scripts/repair-worktrees.sh` — run this first if you ever move or rename this folder",
    ]
    if wrapper_inited:
        lines.append(
            "- `scripts/push-wrapper.sh <remote-url> [branch]` — commit + push this wrapper's own "
            "glue files (not the worktrees) to a remote"
        )
    lines += [
        "",
        "## If you move this folder",
        "",
        "Every `features/<alias>` is a git worktree, and git worktree links are absolute paths on",
        "both ends (this project's own `.git-store/worktrees/<alias>/gitdir` and each",
        "`features/<alias>/.git` file). Moving or renaming this folder breaks all of them until you",
        "run `scripts/repair-worktrees.sh`. This is standard git worktree behavior, not something",
        "specific to how this project was generated -- `coding-project-templates` itself would have",
        "the same issue if it were moved.",
    ]
    (output / "CLAUDE.md").write_text("\n".join(lines) + "\n")


def write_todo(output: Path, project_name: str, selections: list[Selection], wrapper_inited: bool = False) -> None:
    wrapper_line = (
        "- [ ] Wrapper git repo is initialised on `main`; push it with "
        "`scripts/push-wrapper.sh <remote-url>` when you have one"
        if wrapper_inited else
        "- [ ] Version-control the wrapper glue (this README, `scripts/`, `*.code-workspace`, `docs/`): "
        "run `git init` here, or re-generate with `--init-wrapper`. `.gitignore` already excludes "
        "`.git-store/`, `.venv/`, and `features/` (each worktree keeps its own history in `.git-store/`)"
    )
    lines = [
        f"# Post-generation todo",
        "",
        "Manual follow-ups this generator can't safely do for you:",
        "",
        "- [ ] Run `scripts/setup-env.sh` to create the shared `.venv` and install dependencies",
        "- [ ] Rename the package/project name if `--project-name` was a placeholder",
        "- [ ] Fill in real values for each included template's `.env.example` (if it has one)",
        wrapper_line,
        "- [ ] The `.code-workspace` points `python.defaultInterpreterPath` at the one shared",
        f"      `${{workspaceFolder:{project_name}}}/.venv` (named multi-root variable, anchored to the",
        "      `.` folder). If a `features/<alias>/` needs its own interpreter, add",
        "      `features/<alias>/.vscode/settings.json` with a per-folder path -- don't change the global one",
        "- [ ] Run `scripts/health-check.sh` once dependencies are installed",
        "- [ ] If you move or rename this folder after generation, run `scripts/repair-worktrees.sh`",
        "      first thing -- git worktree links are absolute paths on both ends, so every",
        "      `features/<alias>` stops working (\"not a git repository\") until they're repaired",
        "",
    ]
    for s in selections:
        if s.alias != s.template:
            lines.append(f"- [ ] Review `features/{s.alias}/README.md` (from `{s.template}`) for template-specific setup steps")
        else:
            lines.append(f"- [ ] Review `features/{s.alias}/README.md` for template-specific setup steps")
    (output / "todo.md").write_text("\n".join(lines) + "\n")


def write_gitignore(output: Path) -> None:
    (output / ".gitignore").write_text(
        "\n".join([
            "# Bundled bare clone backing every features/<name> worktree -- never commit this",
            "# to a wrapper-level git init, it's a full copy of coding-project-templates' history.",
            ".git-store/",
            "",
            "# Each features/<name> is a git worktree with its own history in .git-store/.",
            "# A wrapper-level repo (see scripts/push-wrapper.sh) tracks only the glue files,",
            "# never the worktrees themselves.",
            "features/",
            "",
            ".venv/",
            "node_modules/",
            "__pycache__/",
            "*.pyc",
            ".DS_Store",
            "Thumbs.db",
            "",
        ])
    )


PUSH_WRAPPER_SH = """\
#!/usr/bin/env bash
# Commit and push this wrapper's own glue files (scripts/, *.code-workspace,
# docs/, README.md, CLAUDE.md, todo.md, .workspace-manifest.json) to a remote.
# The features/<alias> worktrees are NOT pushed from here -- they are gitignored
# in this repo and have their own history in .git-store/ (push those with
# scripts/git-sync-all.sh).
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

REMOTE_URL="${1:-}"
BRANCH="${2:-main}"
if [ -z "$REMOTE_URL" ]; then
  echo "usage: scripts/push-wrapper.sh <git-remote-url> [branch]   (default branch: main)" >&2
  exit 2
fi

git add -A
git diff --cached --quiet || git commit -m "wrapper: update workspace glue"
if git remote get-url wrapper >/dev/null 2>&1; then
  git remote set-url wrapper "$REMOTE_URL"
else
  git remote add wrapper "$REMOTE_URL"
fi
git push -u wrapper "HEAD:$BRANCH"
"""


def init_wrapper(output: Path) -> None:
    """git init the output folder on a 'main' branch and stage the glue files,
    so the wrapper's own history exists from the start. Uses `symbolic-ref`
    rather than `git init -b` so it works on git older than 2.28. The
    features/<alias> worktrees are gitignored here -- each keeps its own
    history in .git-store/."""
    push_helper = output / "scripts" / "push-wrapper.sh"
    push_helper.write_text(PUSH_WRAPPER_SH)
    push_helper.chmod(push_helper.stat().st_mode | 0o111)
    run(["git", "-C", str(output), "init", "-q"])
    run(["git", "-C", str(output), "symbolic-ref", "HEAD", "refs/heads/main"])
    run(["git", "-C", str(output), "add", "-A"])


def copy_scripts(output: Path) -> None:
    src_dir = Path(__file__).resolve().parent
    dest_dir = output / "scripts"
    dest_dir.mkdir(parents=True, exist_ok=True)
    for name in ("setup-env.sh", "sync-templates.sh", "health-check.sh", "git-sync-all.sh", "repair-worktrees.sh"):
        src = src_dir / name
        if not src.is_file():
            raise SystemExit(f"error: expected {src} to exist -- run this from the vscode-workspace-gen worktree")
        dest = dest_dir / name
        shutil.copy2(src, dest)
        dest.chmod(dest.stat().st_mode | 0o111)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--spec", type=Path, help="claude/N-*.md spec file with a ```yaml block")
    p.add_argument("--templates", help="comma-separated NAME or NAME:ALIAS entries (ignored if --spec given)")
    p.add_argument("--output", type=Path, help="output folder path (ignored if --spec given)")
    p.add_argument("--project-name", help="short project name, used in .code-workspace filename (ignored if --spec given)")
    p.add_argument("--target", choices=VALID_TARGETS, help="wsl2 or windows (ignored if --spec given)")
    p.add_argument("--source-repo", type=Path, default=None, help="path to coding-project-templates (default: auto-detected)")
    p.add_argument("--workflow", action="append", type=Path, default=None,
                   help="workflow diagram this workspace derives from; copied into "
                        "<output>/docs/workflows_diagrams/ and linked from CLAUDE.md. Repeatable. "
                        "With --spec, the spec's `workflow:` list is used too (paths relative to the spec file).")
    p.add_argument("--init-wrapper", action="store_true",
                   help="git init the output folder on a 'main' branch and add scripts/push-wrapper.sh, "
                        "so the wrapper glue is version-controlled (worktrees stay gitignored there)")
    p.add_argument("--force", action="store_true", help="allow writing into a non-empty output directory")
    p.add_argument("--dry-run", action="store_true", help="print the plan and exit without writing anything")
    args = p.parse_args()

    source_repo = (args.source_repo or repo_root_from_script()).resolve()

    if args.spec:
        spec = parse_spec(args.spec)
        templates_list = spec["templates"]
        output = Path(spec["output_path"]).expanduser().resolve()
        project_name = spec["project_name"]
        target = spec["target"]
        spec_wf = spec.get("workflow") or []
        if isinstance(spec_wf, str):
            spec_wf = [spec_wf]
        workflow_files = [(args.spec.parent / w).expanduser().resolve() for w in spec_wf]
    else:
        if not (args.templates and args.output and args.project_name and args.target):
            raise SystemExit("error: without --spec, --templates, --output, --project-name and --target are all required")
        templates_list = [t.strip() for t in args.templates.split(",") if t.strip()]
        output = args.output.expanduser().resolve()
        project_name = args.project_name
        target = args.target
        workflow_files = []

    for w in (args.workflow or []):
        rw = w.expanduser().resolve()
        if rw not in workflow_files:
            workflow_files.append(rw)

    missing = [str(w) for w in workflow_files if not w.is_file()]
    if missing:
        raise SystemExit("error: workflow file(s) not found: " + ", ".join(missing))

    available = discover_templates(source_repo)
    selections = parse_template_selections(templates_list, available)
    validate_target(target)

    # The workspace file names the root folder after project_name and points
    # ${workspaceFolder:<project_name>} at it; a component folder with the same
    # name would make that variable ambiguous.
    if project_name in {s.alias for s in selections}:
        raise SystemExit(
            f"error: project name {project_name!r} collides with component folder "
            f"features/{project_name} -- choose a different project name"
        )

    print(f"Source repo:  {source_repo}")
    print(f"Output:       {output}")
    print(f"Project name: {project_name}")
    print(f"Target:       {target}")
    print("Templates:")
    for s in selections:
        if s.alias != s.template:
            print(f"  - features/{s.alias}  (from {s.template} @ {s.branch})")
        else:
            print(f"  - features/{s.alias}  ({s.branch})")
    if workflow_files:
        print("Workflow docs:")
        for w in workflow_files:
            print(f"  - {w}")
    if args.init_wrapper:
        print("Wrapper:      git init on 'main' + scripts/push-wrapper.sh")

    if args.dry_run:
        print("\n--dry-run: nothing written.")
        return

    if output.exists() and any(output.iterdir()) and not args.force:
        raise SystemExit(f"error: {output} already exists and is not empty (pass --force to write into it anyway)")
    output.mkdir(parents=True, exist_ok=True)

    print("\nCloning bare store...")
    git_store = clone_bare_store(source_repo, output)

    print("Adding worktrees...")
    commits, branches = add_worktrees(git_store, output, selections)

    print("Writing workspace file, docs, manifest...")
    workflow_docs = copy_workflow_docs(output, workflow_files) if workflow_files else []
    ws_path = write_workspace_file(output, project_name, selections, target, has_docs=bool(workflow_docs))
    write_manifest(output, source_repo, selections, commits, branches, target)
    write_readme(output, project_name, selections)
    write_claude_md(output, project_name, selections, commits, branches, target,
                    workflow_docs, args.init_wrapper)
    write_todo(output, project_name, selections, args.init_wrapper)
    write_gitignore(output)
    copy_scripts(output)

    if args.init_wrapper:
        print("Initialising wrapper git repo (branch: main)...")
        init_wrapper(output)

    print(f"\nDone. Workspace file: {ws_path}")
    nxt = f"open {ws_path.name} in VS Code, then run scripts/setup-env.sh"
    if args.init_wrapper:
        nxt += "; push the wrapper with scripts/push-wrapper.sh <remote-url>"
    print(f"Next: {nxt}.")


if __name__ == "__main__":
    main()
