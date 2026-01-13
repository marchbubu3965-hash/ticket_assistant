from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
)

from ui.employee_widget import EmployeeWidget
from ui.employee_add_dialog import EmployeeAddDialog
from controller.employee_controller import EmployeeController


class EmployeePanel(QWidget):
    def __init__(self, controller: EmployeeController):
        super().__init__()
        self.controller = controller
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # 員工清單 Widget
        self.employee_widget = EmployeeWidget(self.controller)

        # 新增按鈕
        add_btn = QPushButton("新增員工")
        add_btn.clicked.connect(self._on_add_employee)

        layout.addWidget(add_btn)
        layout.addWidget(self.employee_widget)

        # 初始化時先載入資料
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
                department=data["department"],
            )
            self.employee_widget.refresh()

        except Exception as e:
            QMessageBox.critical(self, "錯誤", str(e))




# from PyQt5.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout,
#     QLabel, QLineEdit, QPushButton, QMessageBox
# )

# from core.controller import EmployeeController
# from core.exceptions import ValidationError, NotFoundError


# class EmployeePanel(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#         self.controller = EmployeeController()
#         self._build_ui()

#     def _build_ui(self):
#         layout = QVBoxLayout()

#         self.emp_id_input = QLineEdit()
#         self.emp_id_input.setPlaceholderText("Employee ID")

#         self.name_input = QLineEdit()
#         self.name_input.setPlaceholderText("Name")

#         self.dept_input = QLineEdit()
#         self.dept_input.setPlaceholderText("Department")

#         layout.addWidget(QLabel("Employee ID"))
#         layout.addWidget(self.emp_id_input)
#         layout.addWidget(QLabel("Name"))
#         layout.addWidget(self.name_input)
#         layout.addWidget(QLabel("Department"))
#         layout.addWidget(self.dept_input)

#         btn_layout = QHBoxLayout()

#         hire_btn = QPushButton("Hire")
#         hire_btn.clicked.connect(self.hire_employee)

#         deactivate_btn = QPushButton("Deactivate")
#         deactivate_btn.clicked.connect(self.deactivate_employee)

#         get_btn = QPushButton("Get")
#         get_btn.clicked.connect(self.get_employee)

#         btn_layout.addWidget(hire_btn)
#         btn_layout.addWidget(deactivate_btn)
#         btn_layout.addWidget(get_btn)

#         layout.addLayout(btn_layout)
#         self.setLayout(layout)

#     def hire_employee(self):
#         try:
#             emp = self.controller.hire_employee(
#                 self.emp_id_input.text(),
#                 self.name_input.text(),
#                 self.dept_input.text()
#             )
#             QMessageBox.information(self, "Success", f"Hired: {emp}")
#         except ValidationError as e:
#             QMessageBox.warning(self, "Error", str(e))

#     def deactivate_employee(self):
#         try:
#             emp = self.controller.deactivate_employee(
#                 self.emp_id_input.text()
#             )
#             QMessageBox.information(self, "Success", f"Deactivated: {emp.emp_id}")
#         except NotFoundError as e:
#             QMessageBox.warning(self, "Error", str(e))

#     def get_employee(self):
#         try:
#             emp = self.controller.get_employee(
#                 self.emp_id_input.text()
#             )
#             QMessageBox.information(
#                 self,
#                 "Employee",
#                 f"{emp}\nActive: {emp.is_active}"
#             )
#         except NotFoundError as e:
#             QMessageBox.warning(self, "Error", str(e))
