from services.ticket_service import TicketService
from domain.employee import Employee


class TicketController:
    """
    UI → 訂票系統的橋接層

    職責：
    - 接收 UI 表單資料
    - 執行業務驗證
    - 呼叫 TicketService 啟動 Selenium 訂票流程
    """

    def __init__(self):
        self.service = TicketService()

    # =========================
    # UI entry point
    # =========================
    def submit_ticket(
        self,
        *,
        employee: Employee,
        from_station: str,
        to_station: str,
        date: str,
        train_nos: list[str],
        ticket_count: int,
        one_way: bool,
    ):
        """
        UI「開始訂票」按鈕唯一入口
        """

        # ===== 業務驗證 =====
        if not employee:
            raise ValueError("未選擇員工")

        if not employee.is_active:
            raise ValueError("該員工為停用狀態")

        if not employee.id_number:
            raise ValueError("員工未設定身分證字號")

        if not from_station or not to_station:
            raise ValueError("請選擇起訖站")

        if from_station == to_station:
            raise ValueError("起站與迄站不可相同")

        if ticket_count <= 0:
            raise ValueError("訂票數量需大於 0")

        # 清理車次（移除空字串）
        train_nos = [no.strip() for no in train_nos if no and no.strip()]
        if not train_nos:
            raise ValueError("至少需提供一個車次")

        # ===== 呼叫 Selenium Use Case =====
        self.service.book_ticket(
            id_number=employee.id_number,
            from_station=from_station,
            to_station=to_station,
            date=date,
            train_nos=train_nos,
            ticket_count=ticket_count,
            one_way=one_way,
        )


# from services.ticket_service import TicketService
# from domain.employee import Employee


# class TicketController:
#     """
#     UI → 訂票系統的橋接層
#     """

#     def __init__(self):
#         self.service = TicketService()

#     # =========================
#     # UI entry point
#     # =========================
#     def submit_ticket(
#         self,
#         *,
#         employee: Employee,
#         from_station: str,
#         to_station: str,
#         date: str,
#         train_nos: list[str],
#         ticket_count: int,
#         one_way: bool,
#     ):
#         """
#         給 UI 呼叫的入口（submit 按鈕）
#         """
#         self.book_ticket_for_employee(
#             employee=employee,
#             from_station=from_station,
#             to_station=to_station,
#             date=date,
#             train_nos=train_nos,
#             ticket_count=ticket_count,
#             one_way=one_way,
#         )

#     # =========================
#     # Core use case
#     # =========================
#     def book_ticket_for_employee(
#         self,
#         *,
#         employee: Employee,
#         from_station: str,
#         to_station: str,
#         date: str,
#         train_nos: list[str],
#         ticket_count: int,
#         one_way: bool,
#     ):
#         """
#         真正的業務邏輯（可被測試、可被重用）
#         """

#         # ===== 業務驗證 =====
#         if not employee:
#             raise ValueError("未選擇員工")

#         if not employee.is_active:
#             raise ValueError("該員工為停用狀態")

#         if not employee.id_number:
#             raise ValueError("員工未設定身分證字號")

#         if from_station == to_station:
#             raise ValueError("起站與迄站不可相同")

#         if ticket_count <= 0:
#             raise ValueError("訂票數量需大於 0")

#         train_nos = [no for no in train_nos if no]
#         if not train_nos:
#             raise ValueError("至少需提供一個車次")

#         # ===== Selenium =====
#         self.service.book_ticket(
#             id_number=employee.id_number,
#             from_station=from_station,
#             to_station=to_station,
#             date=date,
#             train_nos=train_nos,
#             ticket_count=ticket_count,
#             one_way=one_way,
#         )
