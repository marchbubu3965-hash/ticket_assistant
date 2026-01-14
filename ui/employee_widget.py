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
from ui.employee_edit_dialog import EmployeeEditDialog



class EmployeeWidget(QWidget):
    """
    員工管理畫面

    職責：
    - 顯示員工清單
    - 提供 CRUD 操作入口
    - 將行為轉交給 Controller
    """

    def __init__(self, employee_controller=None, parent=None):
        super().__init__(parent)
        self.controller = employee_controller
        self._init_ui()
        self.refresh()


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
        self.add_button = QPushButton("新增")
        self.edit_button = QPushButton("編輯")
        self.deactivate_button = QPushButton("停用")

        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.deactivate_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # ===== Signals =====
        self.refresh_button.clicked.connect(self.refresh)
        self.add_button.clicked.connect(self._on_add_employee)
        self.edit_button.clicked.connect(self._on_edit_employee)
        self.deactivate_button.clicked.connect(self._on_deactivate_employee)

    # =========================
    # Public API
    # =========================

    def refresh(self):
        self.employee_list.clear()

        if not self.controller:
            self.employee_list.addItem("（尚未接上 Controller）")
            return

        employees = self.controller.list_all()

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

    def _get_selected_emp_id(self) -> str | None:
        item = self.employee_list.currentItem()
        if not item:
            return None
        return item.text().split("|")[0].strip()

    def _on_add_employee(self):
        dialog = EmployeeAddDialog(self)
        if not dialog.exec():
            return

        data = dialog.get_data()

        try:
            self.controller.create(
                emp_id=data["emp_id"],
                name=data["name"],
                id_number=data["id_number"],
                department=data["department"],
            )
            QMessageBox.information(self, "成功", "員工已新增")
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, "錯誤", str(e))

    def _on_edit_employee(self):
        emp_id = self._get_selected_emp_id()
        if not emp_id:
            QMessageBox.warning(self, "提醒", "請先選擇員工")
            return

        try:
            employee = self.controller.get(emp_id)

            dialog = EmployeeEditDialog(employee, self)
            if not dialog.exec():
                return

            data = dialog.get_data()

            self.controller.update(
                emp_id=data["emp_id"],
                name=data["name"],
                id_number=data["id_number"],
                department=data["department"],
            )

            QMessageBox.information(self, "成功", "員工資料已更新")
            self.refresh()

        except Exception as e:
            QMessageBox.critical(self, "錯誤", str(e))


    def _on_deactivate_employee(self):
        emp_id = self._get_selected_emp_id()
        if not emp_id:
            QMessageBox.warning(self, "提醒", "請先選擇員工")
            return

        try:
            self.controller.deactivate(emp_id)
            QMessageBox.information(self, "完成", f"員工 {emp_id} 已停用")
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, "錯誤", str(e))
