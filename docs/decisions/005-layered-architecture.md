# ADR-005: Layered Architecture with One-Way Dependencies

**Date:** 2026-06-07
**Status:** Accepted

## Context
This project is intentionally structured more richly than the app requires, to
practice patterns that scale to larger systems. The central risk in a GUI +
DB app is business logic leaking into the UI or the SQL, where it becomes
untestable and entangled with frameworks.

## Decision
Split the code into three layers — `gui`, `core`, `db` — with dependencies
flowing in **one direction only: gui → core → db**.

- `core` is pure Python (no Qt, no SQL, no I/O) and imports neither sibling.
- `db` exposes a `PhraseRepository` interface; it imports neither sibling.
- `gui` depends on `core` and on the `PhraseRepository` abstraction.

## Reasons
- **Testability.** Pure `core` and an in-memory `db` are tested in milliseconds
  without a display or files. Logic never hides in a Qt callback.
- **Replaceability.** The GUI framework or the database can change without
  touching business rules.
- **Comprehension.** Each layer has a single responsibility and its own
  `CLAUDE.md`, so a session can focus on one layer at a time.

## Alternatives Considered
| Option | Why rejected |
|---|---|
| Single module / no layers | Simplest for a tiny app, but defeats the learning goal and makes logic untestable in isolation. |
| MVC/MVVM with a presenter layer | Valuable at larger scale; more ceremony than this app warrants today. Can be added later between gui and core. |

## Consequences
- A layer may only import from layers below it; reviews enforce this.
- Cross-layer contracts (`Phrase`, hex colors, `PhraseRepository`) are
  documented in `docs/architecture.md` and changed deliberately.
- Business rules go in `core` with unit tests — never inline in the GUI.
- Future option: add `import-linter` to enforce the dependency rule in CI.
