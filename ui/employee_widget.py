from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QMessageBox,
)
from PySide6.QtCore import Qt
from ui.employee_add_dialog import EmployeeAddDialog



class EmployeeWidget(QWidget):
    """
    員工管理畫面

    職責：
    - 顯示員工清單
    - 提供新增 / 停用入口
    - 將操作轉交給 Controller
    """

    def __init__(self, employee_controller=None, parent=None):
        super().__init__(parent)
        self.controller = employee_controller

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # ===== Title =====
        title = QLabel("員工管理")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                font-weight: bold;
                padding: 12px;
            }
            """
        )
        layout.addWidget(title)

        # ===== 員工清單 =====
        self.employee_list = QListWidget()
        layout.addWidget(self.employee_list, stretch=1)

        # ===== 操作按鈕 =====
        button_layout = QHBoxLayout()

        self.refresh_button = QPushButton("重新整理")
        self.add_button = QPushButton("新增員工")
        self.deactivate_button = QPushButton("停用員工")

        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.deactivate_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # ===== Signals =====
        self.refresh_button.clicked.connect(self.refresh)
        self.add_button.clicked.connect(self._on_add_employee)
        self.deactivate_button.clicked.connect(self._on_deactivate_employee)

    # =========================
    # Public API
    # =========================

    def refresh(self):
        """
        從 Controller 重新載入員工清單
        """
        self.employee_list.clear()

        if not self.controller:
            self.employee_list.addItem("（尚未接上 Controller）")
            return

        employees = self.controller.list_employees()

        if not employees:
            self.employee_list.addItem("（目前沒有員工資料）")
            return

        for emp in employees:
            status = "在職" if emp.is_active else "停用"
            self.employee_list.addItem(
                f"{emp.emp_id} | {emp.name} | {emp.department} | {status}"
            )

    # =========================
    # Event Handlers
    # =========================

    def _on_add_employee(self):
        if not self.controller:
            QMessageBox.warning(self, "錯誤", "尚未接上 Controller")
            return

        dialog = EmployeeAddDialog(self)
        if not dialog.exec():
            return

        try:
            emp = self.controller.create(
                emp_id=dialog.emp_id,
                name=dialog.name,
                department=dialog.department
            )
            QMessageBox.information(
                self,
                "成功",
                f"已新增員工：{emp.name}"
            )
            self.refresh()

        except Exception as e:
            QMessageBox.critical(self, "錯誤", str(e))



    def _on_deactivate_employee(self):
        """
        停用選取的員工
        """
        item = self.employee_list.currentItem()
        if not item:
            QMessageBox.warning(self, "提醒", "請先選擇員工")
            return

        emp_id = item.text().split("|")[0].strip()

        try:
            self.controller.deactivate(emp_id)
            QMessageBox.information(
                self,
                "完成",
                f"員工 {emp_id} 已停用"
            )
            self.refresh()

        except Exception as e:
            QMessageBox.critical(self, "錯誤", str(e))
