from core.suggestions import best_match, prefix_matches

CANDIDATES = ["hello world", "bye world", "hello there", "help"]


def test_prefix_matches_filters_by_prefix():
    # "help" is shortest; the two 11-char matches tie on length and fall
    # back to alphabetical order ("there" before "world").
    assert prefix_matches(CANDIDATES, "hel") == ["help", "hello there", "hello world"]


def test_prefix_matches_is_case_insensitive():
    assert prefix_matches(CANDIDATES, "HEL") == ["help", "hello there", "hello world"]


def test_prefix_matches_orders_shortest_first():
    result = prefix_matches(CANDIDATES, "hello ")
    assert result == ["hello there", "hello world"]


def test_prefix_matches_returns_empty_when_no_match():
    assert prefix_matches(CANDIDATES, "xyz") == []


def test_best_match_returns_closest():
    assert best_match(CANDIDATES, "b") == "bye world"


def test_best_match_empty_prefix_returns_none():
    assert best_match(CANDIDATES, "") is None


def test_best_match_no_match_returns_none():
    assert best_match(CANDIDATES, "zzz") is None
