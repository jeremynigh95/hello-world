# Project Plan

## Milestones

### Phase 1 — Foundation
- [x] Create initial program
- [x] Set up CLAUDE.md, PLAN.md, STATUS.md for session continuity
- [x] Initialize git repository and push to GitHub

### Phase 2 — Testing & CI
- [x] Add pytest + coverage enforcement (80% minimum)
- [x] Add CI via GitHub Actions
- [x] Add ADR-002 for pytest decision

### Phase 3 — Layered Phrasebook app
- [x] Decide stack: PySide6 + SQLite + repository (ADR-003, 004, 005)
- [x] Build `db/` layer: connection (WAL), schema + seed, repository interface + SQLite impl
- [x] Build `core/` layer: char counts, color banding, suggestion ranking
- [x] Build `gui/` layer: search + completer, Select/Append/Save/Clear, live counts/colors
- [x] Wire entry point `src/main.py`, prime DB with "hello world" / "bye world"
- [x] Tests: unit (core, db), integration, pytest-qt GUI smoke tests
- [x] Per-layer CLAUDE.md files + architecture doc + ADRs
- [x] Update CI for PySide6 / headless Qt

### Phase 4 — Polish (future)
- [ ] Live cross-instance refresh (poll/watch the DB) so other instances'
      writes appear without re-focusing the search box
- [ ] True inline "ghost text" autocomplete in the search box
- [ ] Enforce the layer dependency rule automatically (import-linter in CI)
- [ ] Add numbered migrations once the schema needs to change
- [ ] Package as a distributable app (PyInstaller) if desired

## Notes
- Add new tasks here as the project grows
- Check off items as they are completed
