from browser.browser_manager import BrowserManager
from browser.actions import TraTicketActions
from browser.dom_watcher import DomWatcher
from browser.page_loader import PageLoader
from db.ticket_log_repo import TicketLogRepository
from datetime import datetime

TRA_TICKET_URL = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"


class TicketService:
    """
    訂票 Use Case（支援排程送出）
    - prepare_booking：立即開 Selenium + 填資料
    - submit_booking：在排程時間按下送出
    """

    def __init__(self):
        self.browser = BrowserManager()
        self.driver = None
        self.actions = None

        # ===== 保留訂票狀態（給 submit 用）=====
        self._prepared = False
        self._booking_context = {}

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
    # Phase 1: Prepare booking
    # =========================
    def prepare_booking(
        self,
        *,
        employee_id: str,
        id_number: str,
        from_station: str,
        to_station: str,
        date: str,
        train_nos: list[str],
        ticket_count: int,
        one_way: bool = True,
    ):
        """
        1. 立刻開啟 Selenium
        2. 填完所有資料
        3. 停在「確認送出前」
        """

        if not train_nos:
            raise ValueError("未提供車次")

        if not self.driver:
            self.start_browser()

        # 日期格式轉換：YYYY-MM-DD → YYYY/MM/DD
        dt = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = dt.strftime("%Y/%m/%d")

        # ===== 填表 =====
        self.actions.fill_id_number(id_number)
        self.actions.fill_stations(from_station, to_station)
        self.actions.select_ticket_count(ticket_count)
        self.actions.fill_date(formatted_date)

        used_train_nos = []
        for index, train_no in enumerate(train_nos):
            if not train_no or index >= 3:
                continue
            self.actions.fill_train_no(train_no, index=index)
            used_train_nos.append(train_no)

        if not used_train_nos:
            raise ValueError("至少需提供一個有效車次")

        # ===== 儲存狀態給 submit 使用 =====
        self._booking_context = {
            "employee_id": employee_id,
            "travel_date": formatted_date,
            "from_station": from_station,
            "to_station": to_station,
            "train_nos": used_train_nos,
            "ticket_count": ticket_count,
        }
        self._prepared = True

    # =========================
    # Phase 2: Submit booking
    # =========================
    def submit_booking(self):
        """
        在排程時間執行：
        - 按下 Selenium 的送出鍵
        - 寫入成功 / 失敗紀錄
        """

        if not self._prepared:
            raise RuntimeError("尚未執行 prepare_booking")

        ctx = self._booking_context

        try:
            # ===== 真正送出 =====
            self.actions.click_submit()

            # ===== 成功紀錄 =====
            for train_no in ctx["train_nos"]:
                TicketLogRepository.insert(
                    employee_id=ctx["employee_id"],
                    travel_date=ctx["travel_date"],
                    start_station=ctx["from_station"],
                    end_station=ctx["to_station"],
                    train_no=train_no,
                    ticket_qty=ctx["ticket_count"],
                    status="SUCCESS",
                    message="訂票已送出"
                )

        except Exception as e:
            # ===== 失敗紀錄 =====
            for train_no in ctx["train_nos"]:
                TicketLogRepository.insert(
                    employee_id=ctx["employee_id"],
                    travel_date=ctx["travel_date"],
                    start_station=ctx["from_station"],
                    end_station=ctx["to_station"],
                    train_no=train_no,
                    ticket_qty=ctx["ticket_count"],
                    status="FAILED",
                    message=str(e)
                )
            raise

        finally:
            # 避免重複送出
            self._prepared = False

# from browser.browser_manager import BrowserManager
# from browser.actions import TraTicketActions
# from browser.dom_watcher import DomWatcher
# from browser.page_loader import PageLoader
# from db.ticket_log_repo import TicketLogRepository
# from datetime import datetime

# TRA_TICKET_URL = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"


# class TicketService:
#     """
#     訂票 Use Case
#     - 負責 Selenium 操作
#     - 不關心 UI
#     """

#     def __init__(self):
#         self.browser = BrowserManager()
#         self.driver = None
#         self.actions = None

#     # =========================
#     # Browser lifecycle
#     # =========================
#     def start_browser(self):
#         if self.driver:
#             return

#         self.driver = self.browser.start()

#         loader = PageLoader(self.driver)
#         loader.load(TRA_TICKET_URL)

#         watcher = DomWatcher(self.driver)
#         self.actions = TraTicketActions(self.driver, watcher)

#     # =========================
#     # Main use case
#     # =========================
#     def book_ticket(
#         self,
#         *,
#         employee_id: str,
#         id_number: str,
#         from_station: str,
#         to_station: str,
#         date: str,
#         train_nos: list[str],
#         ticket_count: int,
#         one_way: bool = True,
#         auto_submit: bool = True,
#     ):
#         """
#         訂票流程主入口（含成功 / 失敗紀錄）
#         """

#         if not self.driver:
#             self.start_browser()

#         if not train_nos:
#             raise ValueError("未提供車次")

#         # 日期格式轉換：YYYY-MM-DD → YYYY/MM/DD
#         def format_date(date_str: str) -> str:
#             dt = datetime.strptime(date_str, "%Y-%m-%d")
#             return dt.strftime("%Y/%m/%d")

#         formatted_date = format_date(date)

#         try:
#             # ===== 基本表單 =====
#             self.actions.fill_id_number(id_number)
#             self.actions.fill_stations(from_station, to_station)
#             self.actions.select_ticket_count(ticket_count)
#             self.actions.fill_date(formatted_date)

#             # ===== 車次（最多三個）=====
#             used_train_nos = []
#             for index, train_no in enumerate(train_nos):
#                 if not train_no or index >= 3:
#                     continue
#                 self.actions.fill_train_no(train_no, index=index)
#                 used_train_nos.append(train_no)

#             # ===== 送出 =====
#             if auto_submit:
#                 self.actions.click_submit()

#             # ===== 成功紀錄 =====
#             for train_no in used_train_nos:
#                 TicketLogRepository.insert(
#                     employee_id=employee_id,
#                     travel_date=formatted_date,
#                     start_station=from_station,
#                     end_station=to_station,
#                     train_no=train_no,
#                     ticket_qty=ticket_count,
#                     status="SUCCESS",
#                     message="訂票已送出"
#                 )

#             return True

#         except Exception as e:
#             # ===== 失敗紀錄 =====
#             for train_no in train_nos[:3]:
#                 TicketLogRepository.insert(
#                     employee_id=employee_id,
#                     travel_date=formatted_date,
#                     start_station=from_station,
#                     end_station=to_station,
#                     train_no=train_no,
#                     ticket_qty=ticket_count,
#                     status="FAILED",
#                     message=str(e)
#                 )

#             raise  # 讓上層（UI / scheduler）知道失敗
