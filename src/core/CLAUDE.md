# core/ — business logic

## What this layer owns
The rules that define app behavior, expressed as pure functions:
- `text_stats.char_count` — how a string's length is measured.
- `coloring.color_for_length` — the 10-character color banding rule.
- `suggestions.prefix_matches` / `best_match` — how autocomplete ranks
  candidates and picks the "closest" one.

## Hard rules
- **Pure Python only.** No `import` of Qt/PySide6, no `sqlite3`, no file or
  network I/O. If you need data, the caller passes it in as plain values.
- **No knowledge of callers.** This layer doesn't know a GUI or a database
  exists. It takes values and returns values.
- **Colors are hex strings.** Never return Qt `QColor`; the GUI converts.

## Why
This is the only layer that encodes *what the app means*. Keeping it pure
makes every rule unit-testable in microseconds with no fixtures, and lets the
GUI or database change without touching business logic.

## Testing
Every function here gets unit tests in `tests/unit/core/test_<module>.py`,
covering the happy path and at least one edge/error case. This layer should
sit at or near 100% coverage — there's no excuse for untested pure functions.
