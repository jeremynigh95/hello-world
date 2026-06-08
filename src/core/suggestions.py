"""Autocomplete selection logic.

The repository handles *retrieval* (which rows match a prefix). This
module owns the *business ranking*: given candidate strings, which one is
the "closest" to auto-populate, and in what order to show the rest.
Keeping this here (not in SQL, not in the GUI) makes the rule testable.
"""


def prefix_matches(candidates: list[str], prefix: str) -> list[str]:
    """Return candidates starting with ``prefix`` (case-insensitive).

    Ordered shortest-first, then alphabetically — so the tightest match
    surfaces at the top of the dropdown.
    """
    lowered = prefix.lower()
    matches = [c for c in candidates if c.lower().startswith(lowered)]
    return sorted(matches, key=lambda c: (len(c), c.lower()))


def best_match(candidates: list[str], prefix: str) -> str | None:
    """Return the single closest suggestion for inline autocomplete.

    Returns ``None`` when the prefix is empty or nothing matches.
    """
    if not prefix:
        return None
    matches = prefix_matches(candidates, prefix)
    return matches[0] if matches else None
