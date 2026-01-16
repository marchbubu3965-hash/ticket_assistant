from browser.browser_manager import BrowserManager
from browser.actions import TraTicketActions
from browser.dom_watcher import DomWatcher


class TicketService:
    """
    訂票 Use Case（只關心訂票流程，不關心 UI）
    """

    def __init__(self):
        self.browser = BrowserManager()
        self.driver = None
        self.actions = None

    # =========================
    # Browser lifecycle
    # =========================
    def start_browser(self):
        if self.driver:
            return

        self.driver = self.browser.start()
        watcher = DomWatcher(self.driver)
        self.actions = TraTicketActions(self.driver, watcher)

    # =========================
    # Public Use Case Entry
    # =========================
    def book_ticket(
        self,
        *,
        id_number: str,
        from_station: str,
        to_station: str,
        date: str,
        train_nos: list[str],
        ticket_count: int,
        one_way: bool,
    ):
        """
        訂票完整流程（Controller 只應呼叫此方法）
        """

        if not self.driver:
            self.start_browser()

        if not train_nos:
            raise ValueError("未提供車次")

        # 行程類型
        self.actions.select_trip_type(one_way=one_way)

        # 使用「依車次訂票」
        self.actions.select_booking_by_train_no()

        # 共用欄位
        self.actions.fill_id_number(id_number)
        self.actions.fill_stations(from_station, to_station)
        self.actions.fill_date(date)
        self.actions.select_ticket_count(ticket_count)

        # 逐一嘗試車次
        for train_no in train_nos:
            self.actions.fill_train_no(train_no)
            self.actions.click_submit()

            # TODO（可擴充）
            # if self.actions.is_booking_success():
            #     break
