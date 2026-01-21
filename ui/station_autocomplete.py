from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
)
from PySide6.QtCore import Qt, Signal


class StationAutoComplete(QWidget):
    """
    起 / 迄站自動完成元件
    - SQLite 搜尋
    - 最近使用站點
    - 輸出格式：code-name（例：1000-台北）
    """

    stationSelected = Signal(dict)

    def __init__(self, controller, placeholder="", parent=None):
        super().__init__(parent)
        self.controller = controller
        self._init_ui(placeholder)

    # =========================
    # UI
    # =========================
    def _init_ui(self, placeholder):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)

        self.list = QListWidget()
        self.list.hide()
        self.list.setMaximumHeight(200)

        layout.addWidget(self.input)
        layout.addWidget(self.list)

        self.input.textChanged.connect(self._on_text_changed)
        self.list.itemClicked.connect(self._on_item_clicked)

    # =========================
    # Autocomplete logic
    # =========================
    def _on_text_changed(self, text: str):
        self.list.clear()

        # ===== 空白 → 最近使用 =====
        if not text.strip():
            recents = self.controller.get_recent()
            for st in recents:
                item = QListWidgetItem(
                    f"{st['code']}-{st['name']}（最近）"
                )
                item.setData(Qt.UserRole, st)
                self.list.addItem(item)

            self.list.setVisible(bool(recents))
            return

        # ===== 搜尋 =====
        results = self.controller.search(text)
        if not results:
            self.list.hide()
            return

        for st in results:
            item = QListWidgetItem(f"{st['code']}-{st['name']}")
            item.setData(Qt.UserRole, st)
            self.list.addItem(item)

        self.list.show()

    def _on_item_clicked(self, item: QListWidgetItem):
        station = item.data(Qt.UserRole)
        if not station:
            return

        # 填入輸入框
        self.input.setText(f"{station['code']}-{station['name']}")
        self.list.hide()

        # 通知外部（TicketPanel）
        self.stationSelected.emit(station)

        # ⭐ 記錄最近使用
        # self.controller.record_recent(station)

    # =========================
    # Public API
    # =========================
    def get_station_code(self):
        """
        回傳目前選取的站碼（只取 code）
        """
        text = self.input.text()
        return text.split("-", 1)[0] if "-" in text else None
