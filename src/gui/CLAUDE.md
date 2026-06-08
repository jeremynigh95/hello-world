# gui/ — PySide6 widgets

## What this layer owns
The window and its wiring (`main_window.MainWindow`): search box + completer,
Select/Append/Save/Clear controls, and the labels that show counts and colors.

## Hard rules
- **No business logic.** Character counts come from `core.text_stats`, colors
  from `core.coloring`, suggestion ranking from `core.suggestions`. If you're
  about to write `if len(text) ...` or pick a color here, stop — that rule
  belongs in `core`, with a unit test.
- **Talk to data through `PhraseRepository`.** The window is handed a
  repository; it never imports `sqlite_repository` or touches SQL.
- **Convert at the boundary.** Core returns hex strings; the GUI wraps them in
  `QColor` / stylesheets. That conversion is the only "translation" allowed here.

## Why
Qt code is the hardest to test and the most likely to change (layout tweaks,
widget swaps). Keeping it free of rules means UI churn never risks the logic,
and the logic stays testable without a display.

## Testing
Smoke-tested with pytest-qt in `tests/gui/` (skipped if PySide6 isn't
installed). These confirm the wiring delegates correctly — select/append/save
reaches the repository, counts update, clear resets. They are **not** in the
coverage gate; the rules they exercise are covered by `core` unit tests. Run
headless with `QT_QPA_PLATFORM=offscreen`.
