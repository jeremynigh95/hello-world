"""Domain entities passed between layers.

These are plain data carriers — no SQL, no Qt. The GUI and core receive
``Phrase`` objects and never touch raw database rows.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Phrase:
    """A stored phrase. ``id`` is None until it has been persisted."""

    id: int | None
    text: str
