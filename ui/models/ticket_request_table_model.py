from PySide6.QtCore import QAbstractTableModel, Qt
from datetime import datetime

class TicketRequestTableModel(QAbstractTableModel):

    HEADERS = [
        "員工",
        "身分證",
        "起站",
        "迄站",
        "張數",
        "乘車日期",
        "排程",
        "申請時間",
    ]

    def __init__(self, rows: list):
        super().__init__()
        self._rows = rows 

    # =========================
    # Basic
    # =========================
    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self.HEADERS)

    # =========================
    # Data
    # =========================
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None

        row = self._rows[index.row()]
        col = index.column()

        if col == 0:  # 員工
            return row[0]

        elif col == 1:  # 身分證
            return row[1]

        elif col == 2:  # 起站
            return row[2]

        elif col == 3:  # 迄站
            return row[3]

        elif col == 4:  # 張數
            return row[4]

        elif col == 5:  # 乘車日期
            return row[5]

        elif col == 6:  # 排程
            return "是" if row[6] == 1 else "否"

        elif col == 7:  # 申請時間

            try:
                dt = datetime.fromisoformat(row[8])
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                return row[8] or ""

        return ""

    # =========================
    # Header
    # =========================
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.HEADERS[section]

        return section + 1
