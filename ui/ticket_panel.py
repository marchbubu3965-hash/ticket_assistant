from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
)
from PySide6.QtCore import Qt


class TicketPanel(QWidget):
    """
    台鐵訂票面板
    - 顯示目前選取的員工
    - 與 EmployeeSelectionContext 同步
    - 作為後續訂票流程的入口
    """

    def __init__(
        self,
        ticket_controller,
        employee_controller,
        employee_selection,
        parent=None,
    ):
        super().__init__(parent)

        self.ticket_controller = ticket_controller
        self.employee_controller = employee_controller
        self.employee_selection = employee_selection

        # 訂閱員工選取變化
        self.employee_selection.subscribe(self._on_employee_changed)

        self._init_ui()

    # =========================
    # UI
    # =========================
    def _init_ui(self):
        layout = QVBoxLayout(self)

        # ===== 目前訂票人 =====
        self.current_employee_label = QLabel("目前訂票人：尚未選擇")
        self.current_employee_label.setAlignment(Qt.AlignLeft)
        self.current_employee_label.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        # ===== 身分證字號（自動帶入）=====
        self.id_number_input = QLineEdit()
        self.id_number_input.setPlaceholderText("身分證字號")
        self.id_number_input.setReadOnly(True)

        # ===== 選擇員工按鈕 =====
        self.select_employee_btn = QPushButton("從員工清單選擇")
        self.select_employee_btn.clicked.connect(self._open_employee_selection)

        layout.addWidget(self.current_employee_label)
        layout.addWidget(self.id_number_input)
        layout.addWidget(self.select_employee_btn)
        layout.addStretch()

    # =========================
    # Selection Sync
    # =========================
    def _on_employee_changed(self, employee):
        """
        當 EmployeeSelectionContext 發生變化時呼叫
        """
        if not employee:
            self.current_employee_label.setText("目前訂票人：尚未選擇")
            self.id_number_input.clear()
            return

        self.current_employee_label.setText(
            f"目前訂票人：{employee.emp_id} {employee.name}"
        )
        self.id_number_input.setText(employee.id_number)

    # =========================
    # Actions
    # =========================
    def _open_employee_selection(self):
        """
        目前設計：引導使用者回員工管理頁選擇
        （下一步可改為彈出 EmployeeSelectionDialog）
        """
        QMessageBox.information(
            self,
            "選擇員工",
            "請至「員工管理」頁面，點選員工即可帶入訂票系統。",
        )
