from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
)
from PySide6.QtCore import Qt

from ui.employee_add_dialog import EmployeeAddDialog
from ui.employee_edit_dialog import EmployeeEditDialog


class EmployeeWidget(QWidget):
    """
    員工管理畫面
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
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                padding: 12px;
            }
        """)
        layout.addWidget(title)

        # ===== 員工清單 =====
        self.employee_list = QListWidget()
        layout.addWidget(self.employee_list, stretch=1)

        # ===== 操作按鈕 =====
        button_layout = QHBoxLayout()

        self.refresh_button = QPushButton("重新整理")
        self.add_button = QPushButton("新增")
        self.edit_button = QPushButton("編輯")
        self.toggle_active_button = QPushButton("停用")  # 動態切換

        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.toggle_active_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # ===== Signals =====
        self.refresh_button.clicked.connect(self.refresh)
        self.add_button.clicked.connect(self._on_add_employee)
        self.edit_button.clicked.connect(self._on_edit_employee)
        self.toggle_active_button.clicked.connect(self._on_toggle_active)
        self.employee_list.currentItemChanged.connect(self._on_selection_changed)

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
            item_text = f"{emp.emp_id} | {emp.name} | {emp.department} | {status}"

            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, emp)
            self.employee_list.addItem(item)

        self.toggle_active_button.setEnabled(False)

        # 選中第一筆
        if self.employee_list.count() > 0:
            self.employee_list.setCurrentRow(0)

    # =========================
    # Helpers
    # =========================
    def _get_selected_employee(self):
        item = self.employee_list.currentItem()
        if not item:
            return None
        return item.data(Qt.UserRole)

    # =========================
    # Event Handlers
    # =========================
    def _on_selection_changed(self):
        emp = self._get_selected_employee()
        if not emp:
            self.toggle_active_button.setEnabled(False)
            return

        self.toggle_active_button.setEnabled(True)
        self.toggle_active_button.setText("停用" if emp.is_active else "啟用")

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
        emp = self._get_selected_employee()
        if not emp:
            QMessageBox.warning(self, "提醒", "請先選擇員工")
            return

        try:
            dialog = EmployeeEditDialog(emp, self)
            if not dialog.exec():
                return

            data = dialog.get_data()
            self.controller.update_info(
                emp_id=emp.emp_id,
                name=data["name"],
                id_number=data["id_number"],
                department=data["department"],
            )

            QMessageBox.information(self, "成功", "員工資料已更新")
            self.refresh()

        except Exception as e:
            QMessageBox.critical(self, "錯誤", str(e))

    def _on_toggle_active(self):
        emp = self._get_selected_employee()
        if not emp:
            return

        try:
            if emp.is_active:
                self.controller.deactivate(emp.emp_id)
                QMessageBox.information(self, "完成", "員工已停用")
            else:
                self.controller.activate(emp.emp_id)
                QMessageBox.information(self, "完成", "員工已啟用")

            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, "錯誤", str(e))
