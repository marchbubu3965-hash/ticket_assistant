from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableView,
    QPushButton,
)
from repository.ticket_request_repo import TicketRequestRepository
from ui.models.ticket_request_table_model import TicketRequestTableModel


class TicketRequestLogPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self.refresh()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("訂票請求紀錄")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.table = QTableView()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setEditTriggers(QTableView.NoEditTriggers)
        layout.addWidget(self.table)

        self.refresh_btn = QPushButton("重新整理")
        self.refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(self.refresh_btn)

    def refresh(self):
        """
        讀取最近 100 筆訂票請求紀錄，並顯示員工姓名、身分證、
        起迄站（含代碼和文字）、張數、乘車日期、排程、申請時間
        """
        # 確保資料表存在
        TicketRequestRepository.ensure_table()
        rows = TicketRequestRepository.fetch_all()

        model = TicketRequestTableModel(rows)
        self.table.setModel(model)
        self.table.resizeColumnsToContents()
