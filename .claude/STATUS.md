# Status

**Last updated:** 2026-06-07

## Current state
Phase 3 complete. The layered Phrasebook app is built, tested, and documented.
All 29 tests pass; core + db at 100% coverage (gate is 80%).

## Layer state
- **db/**: complete — WAL connection, schema + seed, `PhraseRepository` +
  `SqlitePhraseRepository`. Fully unit-tested.
- **core/**: complete — `char_count`, `color_for_length` (10-char bands),
  `prefix_matches` / `best_match`. ~100% covered.
- **gui/**: complete — `MainWindow` with search/completer, Select/Append/
  Save/Clear, live counts and colors. pytest-qt smoke tests pass.

## Just finished
- Restructured to `src/{gui,core,db}` with one-way dependencies (gui→core→db)
- Built all three layers + `src/main.py` entry point
- Seeded DB with "hello world" and "bye world"
- Added per-layer CLAUDE.md, rewrote architecture.md, added ADR-003/004/005
- Updated pyproject (pythonpath=src, coverage scoped to core+db), requirements
- Updated CI for PySide6 + headless Qt (offscreen)
- Removed obsolete hello.py / test_hello.py

## How to run / test
- Run: `python src/main.py` (DB path via `PHRASEBOOK_DB`, defaults to phrases.db)
- Test: `python -m pytest` (set `QT_QPA_PLATFORM=offscreen` on Linux/CI)

## Up next (Phase 4, optional)
- True inline ghost-text autocomplete in the search box
- Enforce the dependency rule in CI (import-linter)
- Numbered migrations when the schema first changes

## Blockers / decisions pending
- None

---
_Update this file before ending every session._
