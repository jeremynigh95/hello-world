import pytest


def test_seeded_with_default_phrases(repo):
    texts = {phrase.text for phrase in repo.list_all()}
    assert texts == {"hello world", "bye world"}


def test_list_all_is_ordered_by_text(repo):
    texts = [phrase.text for phrase in repo.list_all()]
    assert texts == sorted(texts)


def test_find_by_prefix_returns_matches(repo):
    results = repo.find_by_prefix("hello")
    assert [p.text for p in results] == ["hello world"]


def test_find_by_prefix_no_match_returns_empty(repo):
    assert repo.find_by_prefix("zzz") == []


def test_find_by_prefix_treats_wildcards_literally(repo):
    # "%" must not act as a SQL wildcard matching every row.
    assert repo.find_by_prefix("%") == []


def test_add_persists_new_phrase(repo):
    saved = repo.add("hello world again")
    assert saved.id is not None
    assert saved.text == "hello world again"
    assert any(p.text == "hello world again" for p in repo.list_all())


def test_add_is_idempotent_for_duplicates(repo):
    first = repo.add("hello world")  # already seeded
    again = repo.add("hello world")
    assert first.id == again.id
    assert sum(p.text == "hello world" for p in repo.list_all()) == 1


def test_add_empty_text_raises(repo):
    with pytest.raises(ValueError):
        repo.add("")
