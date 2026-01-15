from browser.browser_manager import BrowserManager
from browser.actions import TraTicketActions
from browser.dom_watcher import DomWatcher


class TicketService:
    """
    訂票 Use Case（不關心 UI）
    """

    def __init__(self):
        self.browser = BrowserManager()
        self.driver = None
        self.actions = None

    def start_browser(self):
        self.driver = self.browser.start()
        watcher = DomWatcher(self.driver)
        self.actions = TraTicketActions(self.driver, watcher)

    def fill_ticket_form(
        self,
        id_number: str,
        from_station: str,
        to_station: str,
        date: str,
        train_no: str,
        ticket_count: int,
    ):
        if not self.actions:
            raise RuntimeError("Browser not started")

        self.actions.select_trip_type(one_way=True)
        self.actions.select_booking_by_train_no()
        self.actions.fill_id_number(id_number)
        self.actions.fill_stations(from_station, to_station)
        self.actions.fill_date(date)
        self.actions.fill_train_no(train_no)
        self.actions.select_ticket_count(ticket_count)

    def submit(self):
        self.actions.click_submit()
