"""Database layer. Owns persistence and nothing else.

Exposes a ``PhraseRepository`` interface so the rest of the app depends
on the abstraction, not on SQLite. Swap ``SqlitePhraseRepository`` for a
Postgres one later and no other layer changes.
"""
