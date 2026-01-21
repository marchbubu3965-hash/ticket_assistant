from datetime import datetime
from db.database import get_connection

class TicketLogRepository:

    @staticmethod
    def insert(
        employee_id,
        travel_date,
        start_station,
        end_station,
        train_no,
        ticket_qty,
        status,
        message=""
    ):
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
