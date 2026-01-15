from services.ticket_service import TicketService
from domain.employee import Employee


class TicketController:
    """
    UI → 訂票系統的橋接層
    """

    def __init__(self):
        self.service = TicketService()

    def start(self):
        self.service.start_browser()

    def book_ticket_for_employee(
        self,
        employee: Employee,
        from_station: str,
        to_station: str,
        date: str,
        train_no: str,
        ticket_count: int,
    ):
        if not employee.is_active:
            raise ValueError("該員工為停用狀態")

        self.service.fill_ticket_form(
            id_number=employee.id_number,
            from_station=from_station,
            to_station=to_station,
            date=date,
            train_no=train_no,
            ticket_count=ticket_count,
        )
