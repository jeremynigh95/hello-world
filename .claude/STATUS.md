# Status

**Last updated:** 2026-06-23

## Current state
Phase 3 complete. The layered Phrasebook app is built, tested, and documented.
All 34 tests pass; core + db at 100% coverage (gate is 80%).

## Known behavior / limitations
- Cross-instance freshness: each window refreshes its phrase list from the DB
  on startup, after a local save, and when the search box gains focus. So
  another instance's saved phrases appear when you click into the search box
  to start a new search. They do NOT appear live while a window sits idle with
  the search box already focused — acceptable for "few users, occasional
  writes". A polling/live-refresh option is noted in PLAN Phase 4.

## Layer state
- **db/**: complete — WAL connection, schema + seed, `PhraseRepository` +
  `SqlitePhraseRepository`. Fully unit-tested.
- **core/**: complete — `char_count`, `color_for_length` (10-char bands),
  `prefix_matches` / `best_match`. ~100% covered.
- **gui/**: complete — `MainWindow` with search/completer, Select/Append/
  Save/Clear, live counts and colors. pytest-qt smoke tests pass.

## Just finished
- Duplicate-save feedback: Save on an already-stored phrase used to silently
  no-op (DB `UNIQUE` + `ON CONFLICT DO NOTHING`) and clear the form, so it
  looked like a duplicate was accepted. Added `PhraseRepository.exists(text)`
  (exact match) and made the GUI show "'<phrase>' is already saved." instead of
  swallowing the Save. Duplicate rule is **exact match only** (case/spacing
  variants remain distinct, by design). Regression + unit tests added
  (test_saving_existing_phrase_is_blocked_with_feedback, test_exists_*).
- Fixed stale-search bug: a window now re-reads the DB when its search box
  gains focus, so phrases saved by another instance become searchable without
  the local window having to save first. Regression test added
  (test_search_reflects_phrases_saved_by_another_instance).
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
