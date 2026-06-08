"""The persistence contract the rest of the app depends on.

Core and GUI accept a ``PhraseRepository``; they never import the SQLite
implementation directly. This is the seam that keeps the database
swappable and lets tests substitute an in-memory version.
"""

from abc import ABC, abstractmethod

from .models import Phrase


class PhraseRepository(ABC):
    @abstractmethod
    def list_all(self) -> list[Phrase]:
        """Return every stored phrase, ordered by text."""

    @abstractmethod
    def find_by_prefix(self, prefix: str) -> list[Phrase]:
        """Return phrases whose text starts with ``prefix``."""

    @abstractmethod
    def add(self, text: str) -> Phrase:
        """Persist ``text`` and return it as a ``Phrase``.

        Idempotent: adding existing text returns the existing row.
        """
