# Phrasebook

A small PySide6 desktop app for building phrases from existing ones — and a
deliberately over-structured sandbox for practicing layered architecture and
Claude Code workflows.

Type to search stored phrases (the closest is suggested as you type), pick one,
append text to build a new phrase, watch the character count and a length-based
color update live, then save it back to a shared SQLite database. Ships primed
with "hello world" and "bye world".

## Architecture
Three layers with dependencies flowing one way — **gui → core → db**:

- `src/gui/` — PySide6 widgets (wiring only, no business rules)
- `src/core/` — pure business logic: counts, color banding, suggestion ranking
- `src/db/` — SQLite (WAL) behind a swappable `PhraseRepository` interface

See [docs/architecture.md](docs/architecture.md) and the per-layer `CLAUDE.md`
files. Design decisions are recorded in [docs/decisions/](docs/decisions/).

## Run
```bash
pip install -r requirements.txt
python src/main.py
```
The database defaults to `phrases.db` in the working directory; override with
the `PHRASEBOOK_DB` environment variable. Point several instances at the same
path to share data (WAL handles a few concurrent users with occasional writes).

## Test
```bash
pip install -r requirements-dev.txt
python -m pytest
```
Coverage is enforced on the logic layers (`core` + `db`) at 80% minimum. On
Linux/CI run headless with `QT_QPA_PLATFORM=offscreen`.
