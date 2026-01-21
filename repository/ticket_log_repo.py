# repository/ticket_log_repo.py
from datetime import datetime
from db.database import get_connection  # 確認你有這個模組

class TicketLogRepository:
    """
    台鐵訂票紀錄資料存取
    """

    @staticmethod
    def insert(
        employee_id: str,
        travel_date: str,
        start_station: str,
        end_station: str,
        train_no: str,
        ticket_qty: int,
        status: str,
        message: str = ""
    ):
        """
        新增一筆訂票紀錄
        """
        conn = get_connection()
        cursor = conn.cursor()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
        INSERT INTO ticket_order_log (
            employee_id, order_time, travel_date,
            start_station, end_station,
            train_no, ticket_qty,
            status, message, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            employee_id, now, travel_date,
            start_station, end_station,
            train_no, ticket_qty,
            status, message, now
        ))

        conn.commit()
        conn.close()
