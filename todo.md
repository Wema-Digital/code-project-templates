# Todo — python-scripts

> Python utility scripts collection tasks. Uses the same symbol system as the base template.
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
- [x] [!] Initialise git repository and branch (py-script)
- [x] [!] Create requirements.txt (pandas, python-dotenv — shared deps) + requirements-dev.txt (pytest)
- [x] [!] Pin Python version in .python-version (3.12)
- [ ] [@] Decide whether a script that needs an extra dep documents it inline (current convention) or gets its own requirements-<script>.txt
```

---

## Scripts

```markdown
- [x] [!] scripts/csv_report.py — summarize_csv() core function + argparse CLI wrapper
- [x] [!] scripts/__init__.py — makes scripts/ importable for tests
- [ ] [ ] Add your next real script:
  - [ ] Pure core function(s), isolated from argparse/stdout
  - [ ] Thin argparse wrapper in main()
  - [ ] logging.getLogger(__name__) — don't use print() for anything but the final output
  - [ ] Docstring at the top: what it does, example usage
- [ ] [@] Decide on a naming convention once there are more than a couple scripts (verb_noun.py vs. noun_verb.py)
- [ ] [#] Shared helpers module (scripts/_common.py) once two scripts duplicate logic — not before
```

---

## Configuration & Logging

```markdown
- [x] [!] logging.basicConfig() in each script's main() — not a shared config yet
- [ ] [#] .env.example + python-dotenv usage — only once a script needs actual config (API keys, paths)
- [ ] [@] Decide on a shared logging format if scripts start running in the same pipeline/cron
```

---

## Testing

```markdown
- [x] [!] Setup pytest
- [x] [!] tests/test_csv_report.py — summarize_csv() tested via a tmp_path fixture CSV, not the CLI
- [ ] [!] Test the core function of each new script added above the same way
- [ ] [#] Consider one CLI-level smoke test per script (subprocess or capsys) if the argparse wiring gets complex
- [ ] [% 0] Reach 80% test coverage
```

**Claude Code for testing:**
```markdown
- [ ] [!] Ask Claude to generate a test for any new script's core function
- [ ] [#] Have Claude review test coverage report and suggest gaps
```

---

## CI / Distribution

```markdown
- [x] [!] .github/workflows/test.yml — installs requirements + requirements-dev, runs pytest
- [ ] [#] Add lint step to CI (ruff or flake8)
- [ ] [~] If a script needs to run on a schedule, document the cron/Task Scheduler setup here (not in code)
```

---

## Code Quality

```markdown
- [ ] [#] Configure ruff (lint + format)
- [ ] [~] Add pre-commit hooks
- [ ] [ ] Keep each script's docstring accurate as it changes
```

---

## Metadata

*Last Updated: 2026-08-24*
*Template Version: 1.0*
*Stack: Python 3.12 + argparse + pandas + pytest (loose scripts, not a package)*
