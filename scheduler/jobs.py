from datetime import datetime
from controller.ticket_controller import TicketController
from domain.employee import Employee


def run_ticket_job(
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
    APScheduler 實際執行的工作（單次排程）
    使用 TicketController.submit_ticket()，以確保
    - 成功/失敗紀錄會寫入 SQLite
    - 排程邏輯一致
    """

    controller = TicketController()

    # 因為是排程，立即執行
    controller.submit_ticket(
        employee=employee,
        from_station=from_station,
        to_station=to_station,
        date=date,
        train_nos=train_nos,
        ticket_count=ticket_count,
        one_way=one_way,
        schedule_at=None,  # APScheduler 已經負責時間點
    )
