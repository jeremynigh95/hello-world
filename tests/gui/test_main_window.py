"""GUI smoke tests via pytest-qt.

Skipped automatically if PySide6 / pytest-qt aren't installed, so the
core+db suite (the coverage-gated logic) never depends on a display.
These verify the wiring delegates correctly — not the business rules,
which are covered by the core unit tests.
"""

import pytest

pytest.importorskip("PySide6")
pytest.importorskip("pytestqt")

from PySide6.QtCore import QEvent  # noqa: E402
from PySide6.QtGui import QFocusEvent  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from gui.main_window import MainWindow  # noqa: E402
from main import build_repository  # noqa: E402


def _completer_texts(window):
    model = window.completer.model()
    return [model.item(row).text() for row in range(model.rowCount())]


def test_search_reflects_phrases_saved_by_another_instance(qtbot, tmp_path):
    # Two instances sharing one database file (the multi-user scenario).
    db_path = str(tmp_path / "shared.db")
    repo_here = build_repository(db_path)
    repo_other = build_repository(db_path)
    window = MainWindow(repo_here)
    qtbot.addWidget(window)

    assert "hello world over here" not in _completer_texts(window)

    # The other instance saves a new phrase.
    repo_other.add("hello world over here")

    # The user clicks into the search box to start a new search.
    QApplication.sendEvent(window.search, QFocusEvent(QEvent.Type.FocusIn))

    # It should now be searchable here, without this window having saved.
    assert "hello world over here" in _completer_texts(window)


def test_select_append_save_adds_phrase(qtbot, repo):
    window = MainWindow(repo)
    qtbot.addWidget(window)

    window._on_selected("hello world")
    window.append_edit.setText("!!!")
    window._on_save()

    assert "hello world!!!" in [p.text for p in repo.list_all()]


def test_saving_existing_phrase_is_blocked_with_feedback(qtbot, repo):
    window = MainWindow(repo)
    qtbot.addWidget(window)

    before = len(repo.list_all())
    window._on_selected("hello world")  # already seeded; no append
    window._on_save()

    # No new row created, and the user is told it already exists.
    assert len(repo.list_all()) == before
    assert "hello world" in window.status_label.text()
    assert "already" in window.status_label.text().lower()


def test_counts_update_on_select(qtbot, repo):
    window = MainWindow(repo)
    qtbot.addWidget(window)

    window._on_selected("hello world")

    assert "11 chars" in window.counts_label.text()


def test_clear_resets_state(qtbot, repo):
    window = MainWindow(repo)
    qtbot.addWidget(window)

    window._on_selected("hello world")
    window._on_clear()

    assert window._selected == ""
    assert not window.save_btn.isEnabled()
    assert not window.append_edit.isEnabled()
