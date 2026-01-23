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
from controller.ticket_controller import TicketController

from ui.employee_panel import EmployeePanel
from ui.ticket_panel import TicketPanel
from ui.ticket_request_log_panel import TicketRequestLogPanel

from app_context.employee_selection import EmployeeSelectionContext
from repository.station_repository import StationRepository
from controller.station_controller import StationController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ticket Assistant")
        self.resize(1100, 700)

        self._init_dependencies()
        self._init_ui()

    # =========================
    # Dependencies
    # =========================
    def _init_dependencies(self):
        # ---- Employee ----
        repo = EmployeeRepository()
        service = EmployeeService(repo)
        self.employee_controller = EmployeeController(service)

        # ---- Ticket ----
        self.ticket_controller = TicketController()

        # ---- Shared Context ----
        self.employee_selection = EmployeeSelectionContext()
        station_repo = StationRepository()
        self.station_controller = StationController(station_repo)

    # =========================
    # UI
    # =========================
    def _init_ui(self):
        root = QWidget()
        layout = QHBoxLayout(root)

        # -------- Sidebar --------
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(180)
        self.sidebar.addItem("員工管理")
        self.sidebar.addItem("台鐵訂票")
        self.sidebar.addItem("訂票請求紀錄")

        # -------- Pages --------
        self.pages = QStackedWidget()

        self.employee_panel = EmployeePanel(
            controller=self.employee_controller,
            employee_selection=self.employee_selection,
        )
        self.employee_panel.on_employee_confirmed = self._go_to_ticket_page

        self.ticket_panel = TicketPanel(
            ticket_controller=self.ticket_controller,
            station_controller=self.station_controller,
            employee_selection=self.employee_selection,
        )

        self.ticket_request_log_panel = TicketRequestLogPanel()

        self.pages.addWidget(self.employee_panel)            # index 0
        self.pages.addWidget(self.ticket_panel)              # index 1
        self.pages.addWidget(self.ticket_request_log_panel)  # index 2

        # -------- Wiring --------
        self.sidebar.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages)
        self.setCentralWidget(root)

    def _go_to_ticket_page(self):
        """
        使用者雙擊員工 → 切換到訂票頁
        """
        self.pages.setCurrentIndex(1)
        self.sidebar.setCurrentRow(1)
