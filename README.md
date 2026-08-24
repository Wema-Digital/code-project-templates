# python-scripts — Standalone Utility Scripts Collection

> A loose collection of independent Python scripts — deliberately not a packaged app.
> Reach for `python-app` instead if a script grows into something that needs to be installed and imported elsewhere.

---

## Quick Start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install shared dependencies + test tooling
pip install -r requirements.txt -r requirements-dev.txt

# 3. Run the example script
python scripts/csv_report.py --input path/to/data.csv
# → JSON summary printed to stdout

# 4. Or write the report to a file
python scripts/csv_report.py --input path/to/data.csv --output report.json
```

---

## Project Layout

```
python-scripts/
├── scripts/
│   ├── __init__.py       # Makes scripts/ importable for tests
│   └── csv_report.py     # Example: summarize_csv() core function + argparse CLI wrapper
├── tests/
│   └── test_csv_report.py  # Tests summarize_csv() directly, not the CLI wrapper
├── requirements.txt       # Shared runtime deps: pandas, python-dotenv
├── requirements-dev.txt   # Test tooling: pytest
├── .python-version         # Pinned Python version (3.12)
├── CLAUDE.md               # Claude Code context for this template
└── todo.md                 # Task tracking template (symbol system)
```

Each script is standalone and runnable on its own — there's no shared entrypoint or package to install. If a script needs a dependency beyond `requirements.txt`, document that at the top of the script itself rather than adding it here.

---

## Adding a Script

Keep the core logic in a plain function, and keep `main()` as a thin `argparse` wrapper around it — that's what makes it testable without shelling out or capturing stdout:

```python
# scripts/my_script.py
"""What this script does, in one line. Usage: python scripts/my_script.py --input X"""

import argparse
import logging

logger = logging.getLogger(__name__)


def do_the_thing(path: str) -> dict:
    ...  # pure logic — this is what gets tested


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="my_script")
    parser.add_argument("--input", required=True)
    return parser


def main(argv=None) -> None:
    logging.basicConfig(level=logging.INFO)
    args = build_parser().parse_args(argv)
    print(do_the_thing(args.input))


if __name__ == "__main__":
    main()
```

Then add `tests/test_my_script.py` covering `do_the_thing()`, following `tests/test_csv_report.py`.

---

## Testing

```bash
pytest              # run the test suite
pytest -v           # verbose output
```

Test each script's core function directly — not its CLI wrapper:

```python
# tests/test_csv_report.py
from scripts.csv_report import summarize_csv

def test_summarize_csv(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("name,score\nAda,90\n")
    summary = summarize_csv(str(csv_path))
    assert summary["rows"] == 1
```

---

## Working with Claude Code

This template follows the same `todo.md` task-tracking convention as `claude-code-basic`.
See `todo.md` for the full symbol system and task breakdown.

Useful prompts to get started:
- *"Read todo.md and help me add a new script following the csv_report.py convention."*
- *"This script needs config now — add python-dotenv usage and a .env.example."*
- *"Add a shared helpers module once two scripts start duplicating logic."*

---

**Template Version**: 1.0
**Last Updated**: 2026-08-24
**Branch**: `py-script` | **Stack**: Python 3.12 + argparse + pandas + pytest
