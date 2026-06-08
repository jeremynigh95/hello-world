"""Schema definition and first-run seeding.

For a project this size a single idempotent ``initialize`` is enough. When
the schema starts evolving, replace this with numbered migration files
(see docs/decisions/003) — the structure is ready for that.
"""

import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS phrases (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL UNIQUE
);
"""

# The app ships primed with these two phrases.
SEED_PHRASES = ["hello world", "bye world"]


def initialize(conn: sqlite3.Connection) -> None:
    """Create tables if needed and seed an empty database. Idempotent."""
    conn.executescript(SCHEMA)
    count = conn.execute("SELECT COUNT(*) AS n FROM phrases").fetchone()["n"]
    if count == 0:
        conn.executemany(
            "INSERT INTO phrases (text) VALUES (?)",
            [(phrase,) for phrase in SEED_PHRASES],
        )
    conn.commit()
