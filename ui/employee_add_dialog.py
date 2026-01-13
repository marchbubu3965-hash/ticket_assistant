from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFormLayout,
)


class EmployeeAddDialog(QDialog):
    """
    新增 / 編輯員工 Dialog

    職責：
    - 收集員工資料
    - 基本欄位驗證
    - 不處理任何業務邏輯
    """

    def __init__(self, parent=None, employee=None):
        super().__init__(parent)
        self.employee = employee  # ⭐ 是否為編輯模式

        self.setWindowTitle("編輯員工" if employee else "新增員工")
        self.setModal(True)
        self.setMinimumWidth(360)

        self._init_ui()
        self._load_employee()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # ===== 表單 =====
        form = QFormLayout()

        self.emp_id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.department_input = QLineEdit()

        self.emp_id_input.setPlaceholderText("例如：E005")
        self.name_input.setPlaceholderText("例如：王小明")
        self.department_input.setPlaceholderText("例如：IT / HR / Finance")

        form.addRow("員工編號：", self.emp_id_input)
        form.addRow("姓名：", self.name_input)
        form.addRow("部門：", self.department_input)

        layout.addLayout(form)

        # ===== Buttons =====
        button_layout = QHBoxLayout()

        self.ok_button = QPushButton("確認")
        self.cancel_button = QPushButton("取消")

        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        # ===== Signals =====
        self.ok_button.clicked.connect(self._on_accept)
        self.cancel_button.clicked.connect(self.reject)

    def _load_employee(self):
        """
        若為編輯模式，預填資料並鎖定 emp_id
        """
        if not self.employee:
            return

        self.emp_id_input.setText(self.employee.emp_id)
        self.emp_id_input.setDisabled(True)

        self.name_input.setText(self.employee.name)
        self.department_input.setText(self.employee.department)

    # =========================
    # Event
    # =========================

    def _on_accept(self):
        if not self.emp_id_input.text().strip():
            self._error("請輸入員工編號")
            return

        if not self.name_input.text().strip():
            self._error("請輸入姓名")
            return

        if not self.department_input.text().strip():
            self._error("請輸入部門")
            return

        self.accept()

    def _error(self, message: str):
        QMessageBox.warning(self, "輸入錯誤", message)

    # =========================
    # Public API
    # =========================

    def get_data(self) -> dict:
        """
        回傳使用者輸入的資料
        """
        return {
            "emp_id": self.emp_id_input.text().strip(),
            "name": self.name_input.text().strip(),
            "department": self.department_input.text().strip(),
        }
