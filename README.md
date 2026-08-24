# python-app — General-Purpose Python Application Skeleton

> Structure without committing to a web framework — for CLI tools, workers, and libraries-with-an-entrypoint.
> Clone, install, and have a runnable CLI with tests and CI in minutes.

---

## Quick Start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install the package in editable mode, with test tooling
pip install -e ".[dev]"

# 3. Run the entrypoint
app
# → Hello, world!
app Claude
# → Hello, Claude!
```

---

## Project Layout

```
python-app/
├── src/
│   └── app/
│       ├── __init__.py
│       └── main.py       # greet() — pure logic; build_parser()/main() — CLI wrapper
├── tests/
│   └── test_main.py      # greet() + main() example tests
├── pyproject.toml         # Project metadata, deps, [project.scripts] entrypoint
├── .python-version        # Pinned Python version (3.12)
├── CLAUDE.md              # Claude Code context for this template
└── todo.md                # Task tracking template (symbol system)
```

No `requirements.txt` here — dependencies live in `pyproject.toml`, matching the root repo's own `uv`-managed convention. No `.env.example` either: the CLI doesn't need config yet. Add one when it does (see `todo.md`).

---

## Why `src/` Layout

`src/app/` (not a flat `app/` next to `pyproject.toml`) forces the package to be installed rather than imported by accident from the working directory — the same class of bug an editable install (`pip install -e .`) is meant to catch early instead of only in CI.

---

## Adding a Command

Keep logic in pure functions, and keep `main()` as a thin argparse wrapper around them — that's what makes them testable without shelling out:

```python
# src/app/main.py
def do_thing(x: int) -> int:
    return x * 2

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="app")
    parser.add_argument("name", nargs="?", default="world")
    parser.add_argument("--double", type=int)
    return parser

def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    if args.double is not None:
        print(do_thing(args.double))
    else:
        print(greet(args.name))
```

If the CLI grows past a handful of flags, reach for subparsers (`parser.add_subparsers()`) — or swap `argparse` for `click`, noted as an open decision in `todo.md`.

---

## Testing

```bash
pytest              # run the test suite
pytest -v           # verbose output
```

Test pure functions directly; test the CLI wrapper via `capsys`:

```python
# tests/test_main.py
def test_main_prints_greeting(capsys):
    main(["Ada"])
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello, Ada!"
```

---

## Working with Claude Code

This template follows the same `todo.md` task-tracking convention as `claude-code-basic`.
See `todo.md` for the full symbol system and task breakdown.

Useful prompts to get started:
- *"Read todo.md and help me add a new subcommand with tests."*
- *"This CLI needs config now — add python-dotenv and a .env.example."*
- *"Split main.py into cli.py and the actual logic modules."*

---

**Template Version**: 1.0
**Last Updated**: 2026-08-24
**Branch**: `py-app` | **Stack**: Python 3.12 + argparse + pytest
