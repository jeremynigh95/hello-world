"""Application entry point. Wires the layers together and launches Qt.

Run with:  python src/main.py
The database path defaults to ``phrases.db`` in the working directory;
override with the PHRASEBOOK_DB environment variable. Point several
instances at the same path to share data (WAL handles concurrency).
"""

import os
import sys

from db.connection import connect
from db.schema import initialize
from db.sqlite_repository import SqlitePhraseRepository


def build_repository(db_path: str) -> SqlitePhraseRepository:
    """Open the database, ensure schema + seed data, return a repository."""
    conn = connect(db_path)
    initialize(conn)
    return SqlitePhraseRepository(conn)


def main() -> int:
    from PySide6.QtWidgets import QApplication

    from gui.main_window import MainWindow

    db_path = os.environ.get("PHRASEBOOK_DB", "phrases.db")
    app = QApplication(sys.argv)
    repository = build_repository(db_path)
    window = MainWindow(repository)
    window.show()
    return app.exec()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
