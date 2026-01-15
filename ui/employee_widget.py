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
from app_context.employee_selection import EmployeeSelectionContext


class EmployeeWidget(QWidget):
    """
    員工管理畫面
    - 顯示員工清單
    - 提供 CRUD 操作入口
    - 與訂票系統同步選擇員工
    """

    def __init__(
        self,
        employee_controller=None,
        employee_selection: EmployeeSelectionContext | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.controller = employee_controller
        self.employee_selection = employee_selection

        if self.employee_selection:
            self.employee_selection.subscribe(
                self._on_external_employee_selected
            )

        self._init_ui()
        self.refresh()

    # =========================
    # UI
    # =========================
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
        self.toggle_active_button = QPushButton("停用")

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
        self.employee_list.currentItemChanged.connect(
            self._on_selection_changed
        )
        self.employee_list.itemDoubleClicked.connect(
            self._on_item_double_clicked
        )


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
            text = f"{emp.emp_id} | {emp.name} | {emp.department} | {status}"

            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, emp)
            self.employee_list.addItem(item)

        self.toggle_active_button.setEnabled(False)

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
    # Selection Sync
    # =========================
    def _on_selection_changed(self):
        emp = self._get_selected_employee()
        if not emp:
            self.toggle_active_button.setEnabled(False)
            return

        self.toggle_active_button.setEnabled(True)
        self.toggle_active_button.setText(
            "停用" if emp.is_active else "啟用"
        )

        # ⭐ 同步給訂票系統
        if self.employee_selection:
            self.employee_selection.set(emp)

    def _on_item_double_clicked(self, item):
        emp = item.data(Qt.UserRole)
        if not emp:
            return

        # ⭐ 再次設定（保證同步）
        if self.employee_selection:
            self.employee_selection.set(emp)

        # ⭐ 通知：這是「確認選擇」
        self._emit_confirm_selection()


    def _on_external_employee_selected(self, employee):
        """由訂票頁選擇員工 → 員工清單自動反白"""
        if not employee:
            return

        for i in range(self.employee_list.count()):
            item = self.employee_list.item(i)
            emp = item.data(Qt.UserRole)
            if emp and emp.emp_id == employee.emp_id:
                self.employee_list.setCurrentRow(i)
                break

    # =========================
    # CRUD
    # =========================
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


    def _emit_confirm_selection(self):
        """
        Hook method: 由外部（MainWindow）決定要做什麼
        """
        if hasattr(self, "on_employee_confirmed"):
            self.on_employee_confirmed()
