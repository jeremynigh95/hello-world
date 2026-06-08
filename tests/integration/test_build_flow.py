"""Integration: core ranking + db persistence working together.

Exercises the same path the GUI drives, minus Qt: search -> pick closest
-> append -> save -> verify persisted, with core computing stats/colors.
"""

from core.coloring import color_for_length
from core.suggestions import best_match
from core.text_stats import char_count


def test_build_and_save_flow(repo):
    candidates = [p.text for p in repo.list_all()]

    suggestion = best_match(candidates, "hel")
    assert suggestion == "hello world"

    new_text = suggestion + " again"
    assert char_count(new_text) == len(new_text)
    assert color_for_length(char_count(new_text)).startswith("#")

    saved = repo.add(new_text)
    assert saved.text == new_text
    assert new_text in [p.text for p in repo.list_all()]


def test_appended_phrase_is_searchable_after_save(repo):
    repo.add("bye world forever")
    matches = [p.text for p in repo.find_by_prefix("bye world")]
    assert "bye world forever" in matches
