# ADR-003: SQLite Behind a Repository Interface

**Date:** 2026-06-07
**Status:** Accepted

## Context
The app needs persistent storage that a few instances can share, with only
occasional writes and no authentication. We also want the freedom to change
the storage engine later without rewriting the app.

## Decision
Use **SQLite in WAL mode** as the database, accessed exclusively through a
`PhraseRepository` abstract interface. The concrete `SqlitePhraseRepository`
is constructed only in `main.py` and in tests.

## Reasons
- SQLite is serverless — a single file, no daemon to run or configure.
- WAL (write-ahead logging) allows multiple readers plus one writer
  concurrently, which fits "a few users, occasional writes" exactly.
- The repository interface decouples the app from SQLite. Upper layers depend
  on the abstraction, so swapping in Postgres later touches one file.
- The interface also makes tests trivial: an in-memory SQLite repo is a
  fast, isolated substitute (no mocking framework needed).

## Alternatives Considered
| Option | Why rejected (for now) |
|---|---|
| PostgreSQL | Real multi-writer concurrency, but needs a server; overkill for occasional writes and no auth. Still the documented upgrade path. |
| Raw SQLite calls in the GUI | Couples UI to storage; untestable without a real DB; violates the layer rule. |
| Flat file / JSON | No concurrent access story; no query/prefix support. |

## Consequences
- All persistence goes through `PhraseRepository`; no SQL outside `db/`.
- Multiple app instances share data by pointing at the same file path.
- Schema today is a single idempotent `initialize`. When it evolves, move to
  numbered migration files (one per change, reversible).
- Swapping databases later means writing one new repository implementation.
