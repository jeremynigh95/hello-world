"""Text measurement helpers."""


def char_count(text: str) -> int:
    """Return the number of characters in ``text``.

    Empty string returns 0. This is deliberately a thin wrapper around
    ``len`` so the GUI never computes counts itself — the rule lives here.
    """
    return len(text)
