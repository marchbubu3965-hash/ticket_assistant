from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QFormLayout,
    QLineEdit,
    QLabel,
)


class EmployeeEditDialog(QDialog):
    """
    編輯員工 Dialog（Update）

    - emp_id：不可編輯
    - 其他欄位可編輯
    """

    def __init__(self, employee, parent=None):
        super().__init__(parent)
        self.employee = employee

        self.setWindowTitle("編輯員工資料")
        self.setModal(True)
        self.setMinimumWidth(360)

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        form = QFormLayout()

        # ===== emp_id（唯讀）=====
        self.emp_id_label = QLabel(self.employee.emp_id)
        form.addRow("員工編號：", self.emp_id_label)

        # ===== Editable fields =====
        self.name_input = QLineEdit(self.employee.name)
        self.department_input = QLineEdit(self.employee.department)
        self.id_number_input = QLineEdit(self.employee.id_number)

        form.addRow("姓名：", self.name_input)
        form.addRow("部門：", self.department_input)
        form.addRow("身分證字號：", self.id_number_input)

        layout.addLayout(form)

        # ===== Buttons =====
        btn_layout = QHBoxLayout()

        self.save_btn = QPushButton("儲存")
        self.cancel_btn = QPushButton("取消")

        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)

        self.save_btn.clicked.connect(self._on_accept)
        self.cancel_btn.clicked.connect(self.reject)

    def _on_accept(self):
        if not self.name_input.text().strip():
            self._error("姓名不可為空")
            return

        if not self.department_input.text().strip():
            self._error("部門不可為空")
            return

        if not self.id_number_input.text().strip():
            self._error("身分證字號不可為空")
            return

        self.accept()

    def _error(self, msg: str):
        QMessageBox.warning(self, "輸入錯誤", msg)

    def get_data(self) -> dict:
        return {
            "emp_id": self.employee.emp_id,
            "name": self.name_input.text().strip(),
            "department": self.department_input.text().strip(),
            "id_number": self.id_number_input.text().strip(),
        }
