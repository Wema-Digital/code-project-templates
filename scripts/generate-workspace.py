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
    generate-workspace.py --spec claude/2-my-app.md [--dry-run]
    generate-workspace.py --templates web-flask,python-scripts \\
        --output ~/projects/my-app --project-name my-app --target wsl2 [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

VALID_TARGETS = ("wsl2", "windows")

# Extensions worth recommending per selected template, keyed by folder name.
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


def repo_root_from_script() -> Path:
    # This script lives at <repo>/features/vscode-workspace-gen/scripts/generate-workspace.py
    return Path(__file__).resolve().parents[3]


def discover_templates(source_repo: Path) -> dict[str, str]:
    """Parse root CLAUDE.md's Worktree map table -- the single source of truth
    for which templates exist and which branch each one lives on. Read live
    rather than hardcoded here, so this never drifts out of sync the way this
    repo's own docs have drifted before (see doc-sync-checker's whole reason
    for existing)."""
    claude_md = source_repo / "CLAUDE.md"
    if not claude_md.is_file():
        raise SystemExit(f"error: {claude_md} not found -- is --source-repo pointing at coding-project-templates?")

    templates: dict[str, str] = {}
    row_re = re.compile(r"^\|\s*`features/([\w.-]+)`\s*\|\s*`([\w.-]+)`\s*\|")
    for line in claude_md.read_text().splitlines():
        m = row_re.match(line.strip())
        if m:
            name, branch = m.group(1), m.group(2)
            if name == "vscode-workspace-gen":
                continue  # the generator itself is not a selectable output template
            templates[name] = branch
    if not templates:
        raise SystemExit(f"error: no template rows found in {claude_md}'s Worktree map -- table format may have changed")
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


def validate_selection(templates: list[str], target: str, available: dict[str, str]) -> None:
    unknown = [t for t in templates if t not in available]
    if unknown:
        valid = ", ".join(sorted(available))
        raise SystemExit(f"error: unknown template(s) {unknown} -- valid choices are: {valid}")
    if not templates:
        raise SystemExit("error: no templates selected")
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
    return git_store


def add_worktrees(git_store: Path, output: Path, templates: dict[str, str]) -> dict[str, str]:
    """Returns {template_name: short_commit_sha} for the manifest."""
    commits = {}
    for name, branch in templates.items():
        dest = output / "features" / name
        run(["git", "-C", str(git_store), "worktree", "add", str(dest), branch])
        sha = subprocess.run(
            ["git", "-C", str(dest), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        commits[name] = sha
    return commits


def write_workspace_file(output: Path, project_name: str, templates: list[str], target: str) -> Path:
    folders = [{"path": f"features/{name}"} for name in templates]
    settings = {
        "files.exclude": {"**/.git-store": True},
        "search.exclude": {"**/.git-store": True},
        "files.watcherExclude": {"**/.git-store/**": True},
    }
    if target == "wsl2":
        settings["terminal.integrated.defaultProfile.linux"] = "bash"
    else:
        settings["terminal.integrated.defaultProfile.windows"] = "PowerShell"

    recommendations = sorted({ext for name in templates for ext in EXTENSION_RECOMMENDATIONS.get(name, [])})

    workspace = {
        "folders": folders,
        "settings": settings,
        "extensions": {"recommendations": recommendations},
    }
    # No absolute paths anywhere above -- every folder entry is workspaceFolder-
    # relative ("features/<name>", not an absolute filesystem path). This is
    # the actual portability fix; `target` only ever changes settings values
    # that are genuinely OS-specific (terminal default profile), never a path.

    ws_path = output / ".vscode" / f"{project_name}.code-workspace"
    ws_path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(workspace, indent=4)
    ws_path.write_text(content + "\n")

    # Self-check: re-parse what was just written. Catches a bug in this
    # script immediately rather than shipping a broken workspace file --
    # the exact failure mode that motivated the JSON-validation hook.
    json.loads(ws_path.read_text())
    return ws_path


def write_manifest(output: Path, source_repo: Path, templates: dict[str, str], commits: dict[str, str], target: str) -> None:
    manifest = {
        "source_repo": str(source_repo),
        "target": target,
        "templates": [
            {"name": name, "branch": branch, "commit": commits[name]}
            for name, branch in templates.items()
        ],
    }
    (output / ".workspace-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def write_readme(output: Path, project_name: str, templates: list[str]) -> None:
    lines = [
        f"# {project_name}",
        "",
        "Generated by `vscode-workspace-gen` from [coding-project-templates](https://github.com/Wema-Digital/code-project-templates).",
        "Standalone: this folder carries its own complete git history in `.git-store/` and has no",
        "dependency on the source repo's location after generation.",
        "",
        "## Included templates",
        "",
    ]
    for name in templates:
        lines.append(f"- `features/{name}/`")
    lines += [
        "",
        "## Getting started",
        "",
        "```bash",
        "scripts/setup-env.sh    # bootstraps whichever languages got included",
        "scripts/health-check.sh # smoke-tests each included template's test suite",
        "```",
        "",
        "See `todo.md` for manual follow-ups this generator can't safely do for you,",
        "and `CLAUDE.md` for what's included and how it was assembled.",
        "",
    ]
    (output / "README.md").write_text("\n".join(lines))


def write_claude_md(output: Path, project_name: str, templates: dict[str, str], commits: dict[str, str], target: str) -> None:
    lines = [
        f"# CLAUDE.md — {project_name}",
        "",
        "Generated by `vscode-workspace-gen`. This is a standalone project combining templates from",
        "`coding-project-templates`; each `features/<name>/` is its own git worktree (against the",
        f"bundled `.git-store/`, not the original repo) still checked out on its original branch.",
        "",
        f"Target machine this was generated for: **{target}**.",
        "",
        "## What's included",
        "",
        "| Template | Branch | Commit at generation |",
        "|---|---|---|",
    ]
    for name, branch in templates.items():
        lines.append(f"| `features/{name}` | `{branch}` | `{commits[name]}` |")
    lines += [
        "",
        "Full record in `.workspace-manifest.json`.",
        "",
        "## Scripts",
        "",
        "- `scripts/setup-env.sh` — bootstraps whichever languages got included",
        "- `scripts/health-check.sh` — smoke-tests each included template's own test suite",
        "- `scripts/sync-templates.sh` — pulls upstream template improvements from the source repo",
        "- `scripts/git-sync-all.sh` — status/push helper across every included worktree branch",
        "- `scripts/repair-worktrees.sh` — run this first if you ever move or rename this folder",
        "",
        "## If you move this folder",
        "",
        "Every `features/<name>` is a git worktree, and git worktree links are absolute paths on",
        "both ends (this project's own `.git-store/worktrees/<name>/gitdir` and each",
        "`features/<name>/.git` file). Moving or renaming this folder breaks all of them until you",
        "run `scripts/repair-worktrees.sh`. This is standard git worktree behavior, not something",
        "specific to how this project was generated -- `coding-project-templates` itself would have",
        "the same issue if it were moved.",
    ]
    (output / "CLAUDE.md").write_text("\n".join(lines) + "\n")


def write_todo(output: Path, templates: list[str]) -> None:
    lines = [
        f"# Post-generation todo",
        "",
        "Manual follow-ups this generator can't safely do for you:",
        "",
        "- [ ] Run `scripts/setup-env.sh` to install each template's dependencies",
        "- [ ] Rename the package/project name if `--project-name` was a placeholder",
        "- [ ] Fill in real values for each included template's `.env.example` (if it has one)",
        "- [ ] If you want to version-control the wrapper files (this README, scripts/, .vscode/) themselves,",
        "      run `git init` in this folder -- the generated `.gitignore` already excludes `.git-store/`",
        "      so a wrapper-level `git add .` won't try to commit the bundled bare clone",
        "- [ ] Each `features/<name>/` may need its own `.vscode/settings.json` for a per-folder",
        "      `python.defaultInterpreterPath` once you've created a venv there -- don't set that",
        "      globally in the top-level `.code-workspace`, it's ambiguous across multiple languages",
        "- [ ] Set up a remote for this project's own history if you `git init` the wrapper",
        "- [ ] Run `scripts/health-check.sh` once dependencies are installed",
        "- [ ] If you move or rename this folder after generation, run `scripts/repair-worktrees.sh`",
        "      first thing -- git worktree links are absolute paths on both ends, so every",
        "      `features/<name>` stops working (\"not a git repository\") until they're repaired",
        "",
    ]
    for name in templates:
        lines.append(f"- [ ] Review `features/{name}/README.md` for template-specific setup steps")
    (output / "todo.md").write_text("\n".join(lines) + "\n")


def write_gitignore(output: Path) -> None:
    (output / ".gitignore").write_text(
        "\n".join([
            "# Bundled bare clone backing every features/<name> worktree -- never commit this",
            "# to a wrapper-level git init, it's a full copy of coding-project-templates' history.",
            ".git-store/",
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
    p.add_argument("--templates", help="comma-separated template names (ignored if --spec given)")
    p.add_argument("--output", type=Path, help="output folder path (ignored if --spec given)")
    p.add_argument("--project-name", help="short project name, used in .code-workspace filename (ignored if --spec given)")
    p.add_argument("--target", choices=VALID_TARGETS, help="wsl2 or windows (ignored if --spec given)")
    p.add_argument("--source-repo", type=Path, default=None, help="path to coding-project-templates (default: auto-detected)")
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
    else:
        if not (args.templates and args.output and args.project_name and args.target):
            raise SystemExit("error: without --spec, --templates, --output, --project-name and --target are all required")
        templates_list = [t.strip() for t in args.templates.split(",") if t.strip()]
        output = args.output.expanduser().resolve()
        project_name = args.project_name
        target = args.target

    available = discover_templates(source_repo)
    validate_selection(templates_list, target, available)
    selected = {name: available[name] for name in templates_list}

    print(f"Source repo:  {source_repo}")
    print(f"Output:       {output}")
    print(f"Project name: {project_name}")
    print(f"Target:       {target}")
    print(f"Templates:    {', '.join(f'{n} ({b})' for n, b in selected.items())}")

    if args.dry_run:
        print("\n--dry-run: nothing written.")
        return

    if output.exists() and any(output.iterdir()) and not args.force:
        raise SystemExit(f"error: {output} already exists and is not empty (pass --force to write into it anyway)")
    output.mkdir(parents=True, exist_ok=True)

    print("\nCloning bare store...")
    git_store = clone_bare_store(source_repo, output)

    print("Adding worktrees...")
    commits = add_worktrees(git_store, output, selected)

    print("Writing .vscode, docs, manifest...")
    ws_path = write_workspace_file(output, project_name, list(selected), target)
    write_manifest(output, source_repo, selected, commits, target)
    write_readme(output, project_name, list(selected))
    write_claude_md(output, project_name, selected, commits, target)
    write_todo(output, list(selected))
    write_gitignore(output)
    copy_scripts(output)

    print(f"\nDone. Workspace file: {ws_path}")
    print(f"Next: open {output} in VS Code, then run scripts/setup-env.sh.")


if __name__ == "__main__":
    main()
