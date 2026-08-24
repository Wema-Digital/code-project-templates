# Todo — python-app

> Python application project tasks. Uses the same symbol system as the base template.
> See the Symbol Guide below for reference.

## Symbol Guide

| Symbol | Meaning | When to use with Claude |
|--------|---------|-------------------------|
| `[ ]` | Unstarted | Default for all new tasks |
| `[x]` | Completed | Ask Claude to mark tasks done |
| `[-]` | In-progress | Claude marks what it's actively working on |
| `[!]` | High priority | Focus here first |
| `[@]` | Needs discussion | Ask Claude for design input |
| `[?]` | Needs research | Have Claude research options |
| `[#]` | Medium priority | After `[!]` tasks |
| `[~]` | On hold | Skip for now |
| `[>]` | Delegated/deferred | Assigned elsewhere or future |
| `[⚠]` | Critical issue | Urgent bug or blocker |
| `[%]` | % complete | Track large in-progress features |

---

## Project Setup

```markdown
- [x] [!] Initialise git repository and branch (py-app)
- [x] [!] Create pyproject.toml (replaces requirements.txt — uv-managed convention)
- [x] [!] Pin Python version in .python-version (3.12)
- [ ] [@] Decide on a real package name once this stops being a template (rename src/app/)
```

---

## src/ Layout & Entrypoint

```markdown
- [x] [!] src/app/__init__.py + src/app/main.py
- [x] [!] greet() — pure, testable core function
- [x] [!] build_parser() / main() — argparse CLI wrapper
- [x] [!] [project.scripts] app = "app.main:main" — installs as a console script
- [ ] [#] Split main.py once it grows: cli.py (argument parsing) vs. the actual logic modules
- [ ] [ ] Add your first real subcommand:
  - [ ] Pure function with its own test
  - [ ] Wire into build_parser() (subparsers if more than one command)
- [ ] [@] Decide: stdlib argparse vs. click, if the CLI surface grows (subcommands, flags, help text)
```

---

## Configuration & Logging

```markdown
- [ ] [#] src/app/config.py — only add once the app genuinely needs config (env vars, config file)
- [ ] [#] .env.example + python-dotenv — same: add when there's something to configure
- [ ] [#] Logging setup (stdlib logging, or structlog if structured logs are needed)
- [ ] [@] Decide on log level strategy (env-driven vs. a --verbose flag)
```

---

## Testing

```markdown
- [x] [!] Setup pytest (via pyproject.toml [project.optional-dependencies].dev)
- [x] [!] tests/test_main.py — greet() + main() (default arg + explicit arg), 3 passing tests
- [ ] [!] Write tests for each new function/subcommand added above
- [ ] [% 0] Reach 80% test coverage
- [ ] [@] Discuss unit vs. integration test split once the app talks to external systems
```

**Claude Code for testing:**
```markdown
- [ ] [!] Ask Claude to generate tests for any new function added above
- [ ] [#] Have Claude review test coverage report and suggest gaps
```

---

## CI / Packaging

```markdown
- [x] [!] .github/workflows/test.yml — pip install -e ".[dev]", runs pytest
- [ ] [#] Add lint step to CI (ruff or flake8)
- [ ] [~] Publish to an internal/PyPI index, if this stops being a template
- [ ] [>] Dockerise, if the app needs to run somewhere other than a dev machine
```

---

## Code Quality

```markdown
- [ ] [#] Configure ruff (lint + format)
- [ ] [~] Add pre-commit hooks
- [ ] [ ] Add docstrings to public functions
```

---

## Metadata

*Last Updated: 2026-08-24*
*Template Version: 1.0*
*Stack: Python 3.12 + argparse + pytest (src layout, pyproject.toml)*
