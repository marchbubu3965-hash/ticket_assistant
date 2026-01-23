from services.ticket_service import TicketService
from domain.employee import Employee
from datetime import datetime

from PySide6.QtCore import QTimer
from repository.ticket_request_repo import TicketRequestRepository


class TicketController:
    """
    UI → 訂票系統的橋接層
    """

    def __init__(self):
        self.service = TicketService()
        self._submit_timer: QTimer | None = None

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
        # =========================
        # 驗證
        # =========================
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

        train_nos = [n.strip() for n in train_nos if n and n.strip()]
        if not train_nos:
            raise ValueError("至少需提供一個車次")

        # =========================
        # 記錄 UI 訂票請求（存快照）
        # =========================
        try:
            TicketRequestRepository.insert(
                employee_id=employee.emp_id,
                employee_name=employee.name,
                employee_id_number=employee.id_number,
                start_station=from_station,
                end_station=to_station,
                trip_type="ONE_WAY" if one_way else "ROUND_TRIP",
                ticket_count=ticket_count,
                travel_date=date,
                train_nos=train_nos,
                is_scheduled=bool(schedule_at),
                scheduled_at=schedule_at,
            )
        except Exception as e:
            print(f"[TicketController] 無法寫入請求紀錄: {e}")

        # =========================
        # Phase 1：準備訂票
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
        # Phase 2：排程 / 立即送出
        # =========================
        if schedule_at:
            now = datetime.now()
            delay_ms = int((schedule_at - now).total_seconds() * 1000)

            if delay_ms <= 0:
                raise ValueError("排程時間必須晚於現在")

            self._submit_timer = QTimer()
            self._submit_timer.setSingleShot(True)
            self._submit_timer.timeout.connect(self.service.submit_booking)
            self._submit_timer.start(delay_ms)
        else:
            self.service.submit_booking()
