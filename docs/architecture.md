# Architecture

## Overview
Phrasebook is a single-process PySide6 desktop app that lets a user build new
phrases from existing ones and save them to a shared SQLite database. The code
is split into three layers with a strict one-way dependency rule, so each layer
can be understood, tested, and replaced in isolation.

## Component Map
```
┌──────────────────────────────────────────────────────────┐
│                        Phrasebook                          │
│                                                            │
│   ┌─────────────────┐                                      │
│   │   gui/          │  PySide6 widgets, completer,         │
│   │   MainWindow    │  Select/Append/Save/Clear            │
│   └───────┬─────────┘                                      │
│           │ calls (counts, colors, ranking)                │
│           ▼                                                 │
│   ┌─────────────────┐                                      │
│   │   core/         │  char_count, color_for_length,       │
│   │  (pure logic)   │  prefix_matches, best_match          │
│   └───────┬─────────┘                                      │
│           │ receives Phrase values                         │
│           ▼                                                 │
│   ┌─────────────────┐                                      │
│   │   db/           │  PhraseRepository (interface)        │
│   │  repository     │  SqlitePhraseRepository (SQLite/WAL) │
│   └───────┬─────────┘                                      │
│           ▼                                                 │
│      phrases.db  (SQLite file, shareable across instances) │
└──────────────────────────────────────────────────────────┘
```

## The dependency rule
Dependencies flow in one direction only: **gui → core → db**.

| Layer | May import | Must NOT import |
|---|---|---|
| `gui` | `core`, `db` (the `PhraseRepository` interface) | — |
| `core` | nothing in this app (pure Python) | `gui`, `db`, Qt, sqlite3 |
| `db` | nothing in this app | `gui`, `core` |

`core` is the center of gravity: it has no dependencies and everything testable
depends on it. This is enforced by convention and code review (see ADR-005).

## Layers

### gui/ (PySide6)
The outer shell. Wires widgets to actions and renders state. Holds no business
rules — it asks `core` for counts/colors/rankings and a `PhraseRepository` for
data. Hardest to test, most likely to churn, so deliberately kept thin.

### core/ (pure logic)
The meaning of the app: how length is measured, how length maps to a color
band (every 10 chars), how autocomplete candidates are ranked and the closest
chosen. Pure functions, no I/O — unit-tested at ~100%.

### db/ (persistence)
Stores and retrieves `Phrase` entities behind the `PhraseRepository` interface.
SQLite with WAL mode supports a few concurrent instances with occasional
writes. Retrieval lives here; ranking does not.

## Cross-layer contracts
These shapes pass between layers and shouldn't change without a deliberate decision:
- **`Phrase`** (`db.models`): `{ id: int | None, text: str }`. The currency
  between `db` and the upper layers.
- **Color**: a hex string (e.g. `"#00008B"`) returned by `core.coloring`. The
  GUI converts to `QColor`. `core` never returns Qt types.
- **`PhraseRepository`**: `list_all()`, `find_by_prefix(prefix)`, `add(text)`.
  The only way upper layers touch storage.

## Data Flow (build-and-save)
1. User types in the search box → GUI calls `repo.find_by_prefix` / uses the
   completer model built from `repo.list_all`.
2. `core.suggestions.best_match` picks the closest phrase to surface.
3. User selects a phrase and appends text → GUI calls `core.text_stats.char_count`
   and `core.coloring.color_for_length` to update labels live.
4. User clicks Save → GUI calls `repo.add(new_text)`; the completer model is
   rebuilt so the new phrase is immediately searchable.

## External Dependencies
| Dependency | Purpose | Decision |
|---|---|---|
| Python 3.12 | Runtime | [ADR-001](decisions/001-python-as-primary-language.md) |
| pytest + pytest-cov | Testing & coverage gate | [ADR-002](decisions/002-pytest-for-testing.md) |
| SQLite (+ repository pattern) | Persistence | [ADR-003](decisions/003-sqlite-with-repository-pattern.md) |
| PySide6 (Qt) | Desktop GUI | [ADR-004](decisions/004-pyside6-for-gui.md) |
| Layered architecture | Structure & dependency rule | [ADR-005](decisions/005-layered-architecture.md) |

## Future Considerations
- Swap `SqlitePhraseRepository` for a Postgres implementation if true
  concurrent multi-writer access is needed — no other layer changes.
- Replace `schema.initialize` with numbered migrations once the schema evolves.
- Add an automated check (import-linter) to enforce the dependency rule in CI.
