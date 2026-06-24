"""SQLite implementation of :class:`PhraseRepository`."""

import sqlite3

from .models import Phrase
from .repository import PhraseRepository


def _escape_like(text: str) -> str:
    """Escape LIKE wildcards so user input is treated literally."""
    return text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


class SqlitePhraseRepository(PhraseRepository):
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def list_all(self) -> list[Phrase]:
        rows = self._conn.execute(
            "SELECT id, text FROM phrases ORDER BY text"
        ).fetchall()
        return [Phrase(row["id"], row["text"]) for row in rows]

    def find_by_prefix(self, prefix: str) -> list[Phrase]:
        pattern = _escape_like(prefix) + "%"
        rows = self._conn.execute(
            "SELECT id, text FROM phrases WHERE text LIKE ? ESCAPE '\\' ORDER BY text",
            (pattern,),
        ).fetchall()
        return [Phrase(row["id"], row["text"]) for row in rows]

    def exists(self, text: str) -> bool:
        row = self._conn.execute(
            "SELECT 1 FROM phrases WHERE text = ? LIMIT 1", (text,)
        ).fetchone()
        return row is not None

    def add(self, text: str) -> Phrase:
        if not text:
            raise ValueError("phrase text must not be empty")
        self._conn.execute(
            "INSERT INTO phrases (text) VALUES (?) ON CONFLICT(text) DO NOTHING",
            (text,),
        )
        self._conn.commit()
        row = self._conn.execute(
            "SELECT id, text FROM phrases WHERE text = ?", (text,)
        ).fetchone()
        return Phrase(row["id"], row["text"])
