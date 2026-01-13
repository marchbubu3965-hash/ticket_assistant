from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QListWidget,
    QStackedWidget,
    QHBoxLayout
)

from repository.employee_repository import EmployeeRepository
from services.employee_service import EmployeeService
from controller.employee_controller import EmployeeController

from ui.employee_panel import EmployeePanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ticket Assistant")
        self.resize(1100, 700)

        self._init_dependencies()
        self._init_ui()

    def _init_dependencies(self):
        repo = EmployeeRepository()
        service = EmployeeService(repo)
        self.employee_controller = EmployeeController(service)

    def _init_ui(self):
        root = QWidget()
        layout = QHBoxLayout(root)

        # -------- Sidebar --------
        self.sidebar = QListWidget()
        self.sidebar.addItem("員工管理")
        self.sidebar.setFixedWidth(180)

        # -------- Pages --------
        self.pages = QStackedWidget()

        self.employee_panel = EmployeePanel(self.employee_controller)
        self.pages.addWidget(self.employee_panel)

        # -------- Wiring --------
        self.sidebar.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages)

        self.setCentralWidget(root)


# from PySide6.QtWidgets import (
#     QMainWindow,
#     QWidget,
#     QVBoxLayout,
#     QHBoxLayout,
#     QPushButton,
#     QLabel,
#     QMessageBox,
# )
# from PySide6.QtCore import Qt
# from ui.employee_widget import EmployeeWidget
# from controller.employee_controller import EmployeeController
# from services.employee_service import EmployeeService
# from repository.employee_repository import EmployeeRepository


# class MainWindow(QMainWindow):
#     """
#     主視窗（Application Shell）

#     負責：
#     - 建立主要 UI Layout
#     - 作為各功能畫面的入口（Facade）
#     - 將 UI 操作轉交給 Controller
#     """

#     def __init__(self):
#         super().__init__()

#         repo = EmployeeRepository()
#         service = EmployeeService(repo)
#         controller = EmployeeController(service)

#         self.setWindowTitle("Ticket Assistant")
#         self.setMinimumSize(800, 600)
#         self.employee_widget = EmployeeWidget(controller)
#         self.setCentralWidget(self.employee_widget)


#         self._init_ui()

#     def _init_ui(self):
#         """
#         初始化 UI 結構
#         """
#         central_widget = QWidget(self)
#         self.setCentralWidget(central_widget)

#         main_layout = QVBoxLayout()
#         central_widget.setLayout(main_layout)

#         # ===== Header =====
#         header_label = QLabel("Ticket Assistant 管理系統")
#         header_label.setAlignment(Qt.AlignCenter)
#         header_label.setStyleSheet(
#             """
#             QLabel {
#                 font-size: 20px;
#                 font-weight: bold;
#                 padding: 16px;
#             }
#             """
#         )
#         main_layout.addWidget(header_label)

#         # ===== 功能按鈕區 =====
#         button_layout = QHBoxLayout()

#         self.employee_button = QPushButton("員工管理")
#         self.ticket_button = QPushButton("票務處理")
#         self.exit_button = QPushButton("離開系統")

#         button_layout.addWidget(self.employee_button)
#         button_layout.addWidget(self.ticket_button)
#         button_layout.addStretch()
#         button_layout.addWidget(self.exit_button)

#         main_layout.addLayout(button_layout)

#         # ===== 內容顯示區（Placeholder）=====
#         self.content_label = QLabel(
#             "請選擇上方功能模組\n\n"
#             "此區域將顯示對應的管理畫面"
#         )
#         self.content_label.setAlignment(Qt.AlignCenter)
#         self.content_label.setStyleSheet(
#             """
#             QLabel {
#                 border: 1px dashed #999;
#                 padding: 40px;
#                 margin: 20px;
#             }
#             """
#         )

#         main_layout.addWidget(self.content_label, stretch=1)

#         # ===== Signal 綁定 =====
#         self._bind_signals()

#     def _bind_signals(self):
#         """
#         綁定 UI 事件
#         """
#         self.employee_button.clicked.connect(self._on_employee_clicked)
#         self.ticket_button.clicked.connect(self._on_ticket_clicked)
#         self.exit_button.clicked.connect(self.close)

#     # =========================
#     # Event Handlers
#     # =========================

#     def _on_employee_clicked(self):
#         self.setCentralWidget(self.employee_widget)
#         self.employee_widget.refresh()


#     def _on_ticket_clicked(self):
#         """
#         票務處理入口
#         """
#         self.content_label.setText(
#             "【票務處理】\n\n"
#             "此畫面將顯示：\n"
#             "- 開立案件\n"
#             "- 狀態追蹤\n"
#             "- 處理紀錄"
#         )

#     # =========================
#     # 視窗關閉確認（良好 UX）
#     # =========================

#     def closeEvent(self, event):
#         reply = QMessageBox.question(
#             self,
#             "確認離開",
#             "確定要離開系統嗎？",
#             QMessageBox.Yes | QMessageBox.No,
#             QMessageBox.No,
#         )

#         if reply == QMessageBox.Yes:
#             event.accept()
#         else:
#             event.ignore()
