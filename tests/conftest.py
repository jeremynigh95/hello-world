"""Shared pytest fixtures available to all tests."""

import pytest

from db.connection import connect
from db.schema import initialize
from db.sqlite_repository import SqlitePhraseRepository


@pytest.fixture
def repo():
    """An in-memory repository seeded with the default phrases.

    In-memory means each test gets a clean database with no file I/O and
    no cleanup — fast and fully isolated.
    """
    conn = connect(":memory:")
    initialize(conn)
    return SqlitePhraseRepository(conn)
