from services.ticket_service import TicketService
from domain.employee import Employee
from datetime import datetime

from PySide6.QtCore import QTimer


class TicketController:
    """
    UI → 訂票系統的橋接層

    職責：
    - 接收 UI 表單資料
    - 驗證業務邏輯
    - 立即啟動 Selenium 並填表
    - 使用 Qt event loop 排程「單次送出」
    """

    def __init__(self):
        self.service = TicketService()

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
        schedule_at: datetime | None = None,
    ):
        # ===== 驗證 =====
        if not employee:
            raise ValueError("未選擇員工")

        if not employee.is_active:
            raise ValueError("該員工為停用狀態")

        if not employee.emp_id:
            raise ValueError("員工尚未建立 emp_id")

        if not employee.id_number:
            raise ValueError("員工未設定身分證字號")

        if not from_station or not to_station:
            raise ValueError("請選擇起訖站")

        if from_station == to_station:
            raise ValueError("起站與迄站不可相同")

        if ticket_count <= 0:
            raise ValueError("訂票數量需大於 0")

        train_nos = [n for n in train_nos if n]
        if not train_nos:
            raise ValueError("至少需提供一個車次")

        # =========================
        # Phase 1：立刻準備訂票
        # =========================
        self.service.prepare_booking(
            employee_id=employee.emp_id,
            id_number=employee.id_number,
            from_station=from_station,
            to_station=to_station,
            date=date,
            train_nos=train_nos,
            ticket_count=ticket_count,
            one_way=one_way,
        )

        # =========================
        # Phase 2：排程送出（主執行緒）
        # =========================
        if schedule_at:
            now = datetime.now()
            delay_ms = int((schedule_at - now).total_seconds() * 1000)

            if delay_ms <= 0:
                raise ValueError("排程時間必須晚於現在")

            QTimer.singleShot(
                delay_ms,
                self.service.submit_booking
            )

        else:
            # 立即送出
            self.service.submit_booking()



# from datetime import datetime
# from threading import Timer

# from services.ticket_service import TicketService
# from domain.employee import Employee


# class TicketController:
#     """
#     UI → 訂票系統的橋接層（Controller）

#     職責：
#     - 接收 UI 表單資料
#     - 執行業務層驗證
#     - 立即啟動 Selenium 並完成填表（prepare）
#     - 依指定時間「單次」送出訂票（submit）
#     """

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
#         schedule_at: datetime | None = None,
#     ):
#         """
#         UI「開始訂票」按鈕唯一入口

#         流程：
#         1. 驗證資料
#         2. 立即 prepare_booking（開 Selenium + 填資料）
#         3. 若有 schedule_at → 排程 submit_booking
#         4. 否則 → 立即 submit_booking
#         """

#         # =========================
#         # Phase 0：業務驗證
#         # =========================
#         self._validate_inputs(
#             employee=employee,
#             from_station=from_station,
#             to_station=to_station,
#             train_nos=train_nos,
#             ticket_count=ticket_count,
#         )

#         # 清洗車次資料
#         train_nos = [no.strip() for no in train_nos if no and no.strip()]

#         # =========================
#         # Phase 1：立即準備訂票
#         # =========================
#         service = TicketService()

#         service.prepare_booking(
#             employee_id=employee.emp_id,
#             id_number=employee.id_number,
#             from_station=from_station,
#             to_station=to_station,
#             date=date,
#             train_nos=train_nos,
#             ticket_count=ticket_count,
#             one_way=one_way,
#         )

#         # =========================
#         # Phase 2：排程 or 立即送出
#         # =========================
#         if schedule_at:
#             self._schedule_submit(
#                 service=service,
#                 schedule_at=schedule_at,
#             )
#         else:
#             service.submit_booking()

#     # =========================
#     # Internal helpers
#     # =========================
#     def _validate_inputs(
#         self,
#         *,
#         employee: Employee,
#         from_station: str,
#         to_station: str,
#         train_nos: list[str],
#         ticket_count: int,
#     ):
#         if not employee:
#             raise ValueError("未選擇員工")

#         if not employee.is_active:
#             raise ValueError("該員工為停用狀態")

#         if not employee.emp_id:
#             raise ValueError("員工尚未建立 emp_id")

#         if not employee.id_number:
#             raise ValueError("員工未設定身分證字號")

#         if not from_station or not to_station:
#             raise ValueError("請選擇起訖站")

#         if from_station == to_station:
#             raise ValueError("起站與迄站不可相同")

#         if ticket_count <= 0:
#             raise ValueError("訂票數量需大於 0")

#         if not train_nos or not any(train_nos):
#             raise ValueError("至少需提供一個車次")

#     def _schedule_submit(
#         self,
#         *,
#         service: TicketService,
#         schedule_at: datetime,
#     ):
#         now = datetime.now()
#         delay_seconds = (schedule_at - now).total_seconds()

#         if delay_seconds <= 0:
#             raise ValueError("排程時間必須晚於現在時間")

#         Timer(
#             delay_seconds,
#             service.submit_booking,
#         ).start()
