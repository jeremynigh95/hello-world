# ADR-004: PySide6 (Qt) for the GUI

**Date:** 2026-06-07
**Status:** Accepted

## Context
The app needs a desktop GUI with a type-ahead search box: as the user types,
the closest stored phrase is suggested, with a dropdown of prefix matches they
can arrow through. We also want it to stay in Python to reuse the existing
pytest/coverage/CI setup.

## Decision
Use **PySide6** (the official Qt for Python bindings) for the desktop GUI.

## Reasons
- `QCompleter` + `QLineEdit` provide type-ahead and a prefix dropdown close to
  out-of-the-box, matching the core UX requirement.
- Qt's item models let us color each dropdown entry by length cleanly.
- Stays in Python — the `core` and `db` test suites, coverage gate, and CI all
  carry over unchanged; GUI gets pytest-qt on top.
- PySide6 is LGPL and officially maintained by the Qt Company.

## Alternatives Considered
| Option | Why rejected |
|---|---|
| Tkinter (stdlib) | No batteries-included completer; type-ahead + colored dropdown is manual and fiddly. |
| Web (FastAPI + browser) | Natural for multi-user, but adds a server + JS frontend; heavier than a shared-file desktop app needs. |
| PyQt6 | Functionally similar, but GPL/commercial licensing is less convenient than PySide6's LGPL. |

## Consequences
- Runtime dependency on PySide6 (`requirements.txt`); dev adds pytest-qt.
- GUI code stays a thin wiring layer — all rules live in `core` (see ADR-005).
- GUI tests run headless via `QT_QPA_PLATFORM=offscreen`; they are smoke tests,
  excluded from the coverage gate.
- Multi-user is achieved by running multiple instances against one shared
  SQLite file (see ADR-003), not via a server.
