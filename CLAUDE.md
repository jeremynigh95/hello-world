# hello-world / Phrasebook

A deliberately over-structured Python desktop app, used as a sandbox for
practicing Claude Code + layered-architecture workflows. The app itself is
simple; the structure around it is intentionally richer than the app needs.

## What the app does
A PySide6 desktop app for building phrases from existing ones:
- Type in the search box; the closest stored phrase is suggested (type-ahead).
- Pick a phrase (dropdown or Select), then append text to build a new one.
- Live character counts and a length-based color are shown for both strings.
- Save the new phrase to the database, or Clear to start over.
- Ships primed with "hello world" and "bye world".

## Stack
- Language: Python 3.12
- GUI: PySide6 (Qt)
- Database: SQLite (WAL mode) behind a swappable repository interface
- Tests: pytest + pytest-cov + pytest-qt

## Architecture: layered, dependencies flow DOWN only
```
gui  ──▶  core  ──▶  db
```
- **`src/gui/`** — Qt widgets. Wiring only, no business rules. Imports core + db.
- **`src/core/`** — business logic (counts, colors, suggestion ranking). Pure
  Python: no Qt, no SQL, no I/O. Imports nothing from gui or db.
- **`src/db/`** — persistence behind `PhraseRepository`. Imports neither.

**The rule:** a layer may only import from layers below it. `core` never
imports `gui`; `db` never imports `core`. If logic about lengths/colors/ranking
shows up in `gui`, it belongs in `core`. See `docs/architecture.md`.

Each layer has its own `CLAUDE.md` describing what it owns and what it must not do.

## How to run
```bash
pip install -r requirements.txt   # first time only
python src/main.py
```
The database defaults to `phrases.db` in the working directory; override with
the `PHRASEBOOK_DB` env var. Point multiple instances at the same path to share
data (WAL handles a few concurrent users with occasional writes).

## How to test
```bash
pip install -r requirements-dev.txt   # first time only
python -m pytest                       # all tests with coverage
python -m pytest tests/unit/           # unit tests only
python -m pytest tests/integration/    # integration tests
```
Coverage is enforced on the logic layers (`core` + `db`) at **80% minimum**;
the build fails below it. The GUI is smoke-tested via pytest-qt but excluded
from the coverage gate (thin Qt wiring, tested through integration instead).
On Linux/CI set `QT_QPA_PLATFORM=offscreen` so Qt runs headless.

## Testing requirements (ALWAYS follow these)

Non-negotiable for every development task:

1. **New function = new test.** Every new function/method in `core` or `db`
   gets at least one happy-path test and one edge/error test.
2. **Bug fix = regression test first.** Reproduce with a failing test, confirm
   it fails, fix, confirm it passes. Commit both together.
3. **No new code without running the full suite.** Run `python -m pytest`
   before every commit. Never commit red.
4. **Test file mirrors source file.** `src/core/coloring.py` →
   `tests/unit/core/test_coloring.py`.
5. **Test behavior, not implementation.** Assert on return values and side
   effects, not internal names or call order.
6. **Name tests as sentences.** `test_negative_length_raises`.
7. **Keep logic out of the GUI.** New business rules go in `core` with unit
   tests — never inline in a Qt callback.

## Project structure
```
hello-world/
├── src/
│   ├── main.py            # entry point — wires layers, launches Qt
│   ├── core/              # business logic (pure) + its own CLAUDE.md
│   ├── db/                # persistence + repository + its own CLAUDE.md
│   └── gui/               # PySide6 widgets + its own CLAUDE.md
├── tests/
│   ├── conftest.py        # shared fixtures (in-memory repo)
│   ├── unit/core/         # mirror of src/core
│   ├── unit/db/           # mirror of src/db
│   ├── integration/       # core + db together
│   └── gui/               # pytest-qt smoke tests
├── docs/
│   ├── architecture.md    # component map, layer rules, data flow
│   └── decisions/         # ADRs (NNN-short-title.md)
├── requirements.txt       # runtime deps (PySide6)
├── requirements-dev.txt   # + pytest, pytest-cov, pytest-qt
├── pyproject.toml         # pytest + coverage config
└── .claude/
    ├── PLAN.md            # milestones and task checklist
    └── STATUS.md          # current state — update before ending a session
```

## Session startup checklist
1. `CLAUDE.md` (this file)
2. The `CLAUDE.md` of whichever layer you're working in (`src/<layer>/CLAUDE.md`)
3. `docs/architecture.md`
4. `.claude/PLAN.md`
5. `.claude/STATUS.md`
6. `git log --oneline -10`

## Working effectively in this repo
- **Focus on one layer per session.** Tell Claude which layer you're in and
  have it read that layer's `CLAUDE.md` first.
- **Respect the dependency direction.** Cross-layer data shapes are documented
  in `docs/architecture.md`; don't change them casually.

## Adding an ADR
When a significant technical decision is made, add `docs/decisions/NNN-short-title.md`
following the existing pattern and add a row to the Dependencies table in
`docs/architecture.md`.

## Conventions
- Commit after each meaningful unit of work
- Update `.claude/STATUS.md` before ending a session
- Check off completed items in `.claude/PLAN.md` as work finishes
