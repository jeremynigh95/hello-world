from core.text_stats import char_count


def test_char_count_counts_characters():
    assert char_count("hello") == 5


def test_char_count_empty_string_is_zero():
    assert char_count("") == 0


def test_char_count_includes_spaces():
    assert char_count("hello world") == 11
