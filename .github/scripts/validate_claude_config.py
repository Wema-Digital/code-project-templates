#!/usr/bin/env python3
"""Validate that everything under .claude/ parses as the format it claims to be.

- Every *.json under .claude/ must be valid JSON
- Every .claude/commands/*.md and .claude/agents/*.md must have YAML
  frontmatter (delimited by --- lines) that parses as valid YAML

Run locally:
    pip install pyyaml
    python3 .github/scripts/validate_claude_config.py
"""

import json
import sys
from pathlib import Path

import yaml

CLAUDE_DIR = Path(__file__).resolve().parents[2] / ".claude"


def validate_json(path: Path) -> str | None:
    try:
        json.loads(path.read_text())
    except json.JSONDecodeError as e:
        return f"{path}: invalid JSON — {e}"
    return None


def validate_frontmatter(path: Path) -> str | None:
    text = path.read_text()
    if not text.startswith("---\n"):
        return f"{path}: missing YAML frontmatter (file must start with '---')"

    end = text.find("\n---", 4)
    if end == -1:
        return f"{path}: unterminated YAML frontmatter"

    frontmatter = text[4:end]
    try:
        yaml.safe_load(frontmatter)
    except yaml.YAMLError as e:
        return f"{path}: invalid YAML frontmatter — {e}"
    return None


def main() -> int:
    errors = []
    json_files = sorted(CLAUDE_DIR.rglob("*.json"))
    frontmatter_files = sorted(CLAUDE_DIR.glob("commands/*.md")) + sorted(
        CLAUDE_DIR.glob("agents/*.md")
    )

    for path in json_files:
        error = validate_json(path)
        if error:
            errors.append(error)

    for path in frontmatter_files:
        error = validate_frontmatter(path)
        if error:
            errors.append(error)

    if errors:
        print("Config validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"OK — {len(json_files)} JSON file(s), {len(frontmatter_files)} command/agent file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
