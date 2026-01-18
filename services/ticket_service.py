from browser.browser_manager import BrowserManager
from browser.actions import TraTicketActions
from browser.dom_watcher import DomWatcher
from browser.page_loader import PageLoader
from datetime import datetime

TRA_TICKET_URL = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"

class TicketService:
    """
    訂票 Use Case
    - 負責 Selenium 操作
    - 不關心 UI
    - 不關心 Employee 物件
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

        loader = PageLoader(self.driver)
        loader.load(TRA_TICKET_URL)

        watcher = DomWatcher(self.driver)
        self.actions = TraTicketActions(self.driver, watcher)

    # =========================
    # Main use case
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
        one_way: bool = True,
        auto_submit: bool = True,
    ):
        """
        訂票流程主入口
        """
        if not self.driver:
            self.start_browser()

        if not train_nos:
            raise ValueError("未提供車次")
        def format_date(date_str: str) -> str:
            # 嘗試解析常見格式，再輸出 YYYY/MM/DD
            dt = datetime.strptime(date_str, "%Y-%m-%d")  # 如果輸入是 2026-01-28
            return dt.strftime("%Y/%m/%d")
        # ===== 基本表單 =====
        # self.actions.select_trip_type(one_way=one_way)
        # self.actions.select_booking_by_train_no()

        self.actions.fill_id_number(id_number)
        self.actions.fill_stations(from_station, to_station)
        self.actions.select_ticket_count(ticket_count)
        formatted_date = format_date(date)
        self.actions.fill_date(formatted_date)
        

        # 填寫多車次（最多三個）
        for index, train_no in enumerate(train_nos):
            if not train_no:
                continue
            if index >= 3:
                break
            self.actions.fill_train_no(train_no, index=index)

        # ===== 是否真的送出 =====
        if auto_submit:
            self.actions.click_submit()

    

