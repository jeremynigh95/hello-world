"""The main application window.

Flow: type to search -> closest phrase suggested (completer) -> Select ->
Append text -> live char counts and color update -> Save (new phrase) or
Clear (start over). All logic is delegated; this file is wiring only.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QCompleter,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.coloring import color_for_length
from core.text_stats import char_count
from db.repository import PhraseRepository


class MainWindow(QMainWindow):
    def __init__(self, repository: PhraseRepository, parent=None):
        super().__init__(parent)
        self._repo = repository
        self._selected = ""  # the base phrase the user picked
        self.setWindowTitle("Phrasebook")
        self._build_ui()
        self._reload_phrases()

    # -- construction -----------------------------------------------------
    def _build_ui(self) -> None:
        self.search = QLineEdit()
        self.search.setPlaceholderText("Type to search phrases…")

        self.completer = QCompleter(self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.activated[str].connect(self._on_selected)
        self.search.setCompleter(self.completer)

        self.select_btn = QPushButton("Select")
        self.select_btn.clicked.connect(lambda: self._on_selected(self.search.text()))

        self.selected_label = QLabel("Selected: (none)")

        self.append_edit = QLineEdit()
        self.append_edit.setPlaceholderText("Append text to build a new phrase…")
        self.append_edit.setEnabled(False)
        self.append_edit.textChanged.connect(self._refresh_preview)

        self.preview_label = QLabel("New: (none)")
        self.counts_label = QLabel("")

        self.save_btn = QPushButton("Save")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self._on_save)
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self._on_clear)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Search"))
        layout.addWidget(self.search)
        select_row = QHBoxLayout()
        select_row.addWidget(self.select_btn)
        select_row.addStretch()
        layout.addLayout(select_row)
        layout.addWidget(self.selected_label)
        layout.addWidget(QLabel("Append"))
        layout.addWidget(self.append_edit)
        layout.addWidget(self.preview_label)
        layout.addWidget(self.counts_label)
        button_row = QHBoxLayout()
        button_row.addWidget(self.save_btn)
        button_row.addWidget(self.clear_btn)
        layout.addLayout(button_row)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # -- data -------------------------------------------------------------
    def _reload_phrases(self) -> None:
        """Rebuild the completer model, coloring each item by its length."""
        model = QStandardItemModel(self)
        for phrase in self._repo.list_all():
            item = QStandardItem(phrase.text)
            item.setForeground(QColor(color_for_length(char_count(phrase.text))))
            model.appendRow(item)
        self.completer.setModel(model)

    # -- behavior ---------------------------------------------------------
    def _new_text(self) -> str:
        return self._selected + self.append_edit.text()

    def _on_selected(self, text: str) -> None:
        text = text.strip()
        if not text:
            return
        self._selected = text
        self.search.setText(text)
        color = color_for_length(char_count(text))
        self.selected_label.setText(f"Selected: {text}")
        self.selected_label.setStyleSheet(f"color: {color};")
        self.append_edit.setEnabled(True)
        self.save_btn.setEnabled(True)
        self._refresh_preview()

    def _refresh_preview(self) -> None:
        new_text = self._new_text()
        color = color_for_length(char_count(new_text))
        self.preview_label.setText(f"New: {new_text}")
        self.preview_label.setStyleSheet(f"color: {color};")
        self.counts_label.setText(
            f"Selected: {char_count(self._selected)} chars"
            f"    |    New: {char_count(new_text)} chars"
        )

    def _on_save(self) -> None:
        new_text = self._new_text().strip()
        if not new_text:
            return
        self._repo.add(new_text)
        self._reload_phrases()
        self._on_clear()

    def _on_clear(self) -> None:
        self._selected = ""
        self.search.clear()
        self.append_edit.clear()
        self.append_edit.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.selected_label.setText("Selected: (none)")
        self.selected_label.setStyleSheet("")
        self.preview_label.setText("New: (none)")
        self.preview_label.setStyleSheet("")
        self.counts_label.setText("")
