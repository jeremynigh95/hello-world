"""GUI smoke tests via pytest-qt.

Skipped automatically if PySide6 / pytest-qt aren't installed, so the
core+db suite (the coverage-gated logic) never depends on a display.
These verify the wiring delegates correctly — not the business rules,
which are covered by the core unit tests.
"""

import pytest

pytest.importorskip("PySide6")
pytest.importorskip("pytestqt")

from gui.main_window import MainWindow  # noqa: E402


def test_select_append_save_adds_phrase(qtbot, repo):
    window = MainWindow(repo)
    qtbot.addWidget(window)

    window._on_selected("hello world")
    window.append_edit.setText("!!!")
    window._on_save()

    assert "hello world!!!" in [p.text for p in repo.list_all()]


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
