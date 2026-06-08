# db/ — persistence

## What this layer owns
Storing and retrieving phrases, behind an interface:
- `models.Phrase` — the entity passed to other layers.
- `repository.PhraseRepository` — the abstract contract everyone depends on.
- `sqlite_repository.SqlitePhraseRepository` — the concrete SQLite implementation.
- `connection.connect` — connection factory (WAL mode for shared access).
- `schema.initialize` — schema creation + first-run seeding.

## Hard rules
- **Everyone depends on `PhraseRepository`, not on SQLite.** Core and GUI import
  the abstract class; only `main.py` and tests construct the concrete one.
- **No business logic here.** Retrieval (LIKE prefix queries) lives here;
  *ranking* the results ("which is closest") is core's job. Don't compute
  char counts or colors in SQL.
- **Return `Phrase` objects, never raw `sqlite3.Row`**, so callers never couple
  to the storage format.
- **Parameterize every query.** User input (e.g. search prefixes) must be
  escaped — see `_escape_like`. Never string-format SQL.

## Schema changes
Today `schema.initialize` is a single idempotent setup. When the schema starts
to evolve, switch to numbered migration files (see `docs/decisions/003`) — one
file per change, each reversible. Treat a schema change like an ADR.

## Testing
Tests use the in-memory `repo` fixture (`tests/conftest.py`) — a fresh seeded
database per test, no files, no cleanup. Mirror sources in
`tests/unit/db/test_<module>.py`. Cover prefix escaping, idempotent adds, and
empty-input errors, not just the happy path.
