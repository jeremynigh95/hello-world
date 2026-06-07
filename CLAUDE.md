# hello-world

A Python project used as a learning sandbox for Claude Code + Python development workflows.

## Stack
- Language: Python 3.12
- Runner: `python hello.py`

## How to run
```bash
python hello.py
```

## How to test
```bash
pip install pytest pytest-cov   # first time only
python -m pytest                # run all tests with coverage
python -m pytest -v             # verbose output
python -m pytest tests/unit/    # unit tests only
```

Coverage minimum: **80%**. The build fails below this threshold.

## Testing requirements (ALWAYS follow these)

These are non-negotiable for every development task:

1. **New function = new test.** Every new function or method gets at least one unit test covering the happy path and one covering an edge case or error condition.
2. **Bug fix = regression test first.** Before fixing a bug, write a test that reproduces it. Confirm it fails. Fix the bug. Confirm the test passes. Commit both together.
3. **No new code without running the full suite.** Run `python -m pytest` before every commit. Never commit if tests are red.
4. **Test file mirrors source file.** A function in `foo/bar.py` gets tests in `tests/unit/test_bar.py`.
5. **Test behavior, not implementation.** Tests assert on return values and side effects — not on internal variable names or call order.
6. **Name tests as sentences.** `test_greet_returns_hello_world_by_default` — when it fails, the name explains what broke.

## Project structure
```
hello-world/
├── hello.py               # main program
├── pyproject.toml         # pytest + coverage config
├── CLAUDE.md              # this file — always read at session start
├── README.md              # public-facing docs
├── docs/
│   ├── architecture.md    # system design and component map
│   └── decisions/         # architecture decision records (ADRs)
│       ├── 001-python-as-primary-language.md
│       └── 002-pytest-for-testing.md
├── tests/
│   ├── conftest.py        # shared fixtures
│   └── unit/              # unit tests (mirror source structure)
└── .claude/
    ├── PLAN.md            # milestones and task checklist
    └── STATUS.md          # current state snapshot — update before ending a session
```

## Session startup checklist
When starting a new session, read these files in order:
1. `CLAUDE.md` (this file)
2. `docs/architecture.md`
3. `.claude/PLAN.md`
4. `.claude/STATUS.md`
5. `git log --oneline -10`

## Adding an ADR
When a significant technical decision is made, create a new file in `docs/decisions/` following the existing naming pattern (`NNN-short-title.md`) and add a row to the Dependencies table in `docs/architecture.md`.

## Conventions
- Commit after each meaningful unit of work
- Update `.claude/STATUS.md` before ending a session
- Check off completed items in `.claude/PLAN.md` as work finishes
