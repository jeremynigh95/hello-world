"""SQLite connection factory.

WAL (write-ahead logging) mode lets several app instances read the same
database file concurrently while one writes — exactly the "a few users,
occasional writes" profile this project targets. Point multiple instances
at the same file path and they share data with no server process.
"""

import sqlite3


def connect(db_path: str) -> sqlite3.Connection:
    """Open a connection with sensible defaults for shared access."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn
