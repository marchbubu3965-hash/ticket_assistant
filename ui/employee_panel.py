from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
)

from controller.employee_controller import EmployeeController
from app_context.employee_selection import EmployeeSelectionContext

from ui.employee_widget import EmployeeWidget
from ui.employee_add_dialog import EmployeeAddDialog


class EmployeePanel(QWidget):
    """
    員工管理主面板
    - 包含新增員工
    - 包含員工清單（EmployeeWidget）
    - 將員工選取狀態寫入 EmployeeSelectionContext
    """

    def __init__(
        self,
        controller: EmployeeController,
        employee_selection: EmployeeSelectionContext,
        parent=None,
    ):
        super().__init__(parent)
        self.controller = controller
        self.employee_selection = employee_selection
        self.on_employee_confirmed = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # ===== 新增員工按鈕 =====
        add_btn = QPushButton("新增員工")
        add_btn.clicked.connect(self._on_add_employee)

        # ===== 員工清單 Widget =====
        
        self.employee_widget = EmployeeWidget(
            employee_controller=self.controller,
            employee_selection=self.employee_selection,
            parent=self,
        )
        self.employee_widget.on_employee_confirmed = self._on_employee_confirmed

        layout.addWidget(add_btn)
        layout.addWidget(self.employee_widget)

        # 初始載入
        self.employee_widget.refresh()

    # =========================
    # Slots
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
            self.employee_widget.refresh()

        except Exception as e:
            QMessageBox.critical(self, "錯誤", str(e))

    def _on_employee_confirmed(self):
        """
        員工被雙擊確認
        交給 MainWindow（往上冒泡）
        """
        if hasattr(self, "on_employee_confirmed"):
            self.on_employee_confirmed()
