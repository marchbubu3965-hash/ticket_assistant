import json
from datetime import datetime
from db.database import get_connection


class BookingRequestRepository:

    @staticmethod
    def insert(
        *,
        employee_id: str,
        id_number: str,
        from_station: str,
        to_station: str,
        trip_type: str,
        ticket_qty: int,
        travel_date: str,
        train_nos: list[str],
        is_scheduled: bool,
        scheduled_at,
        requested_at: datetime,
    ):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO booking_requests (
                employee_id,
                id_number,
                from_station,
                to_station,
                trip_type,
                ticket_qty,
                travel_date,
                train_nos,
                is_scheduled,
                scheduled_at,
                requested_at,
                request_source
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                employee_id,
                id_number,
                from_station,
                to_station,
                trip_type,
                ticket_qty,
                travel_date,
                json.dumps(train_nos, ensure_ascii=False),
                1 if is_scheduled else 0,
                scheduled_at,
                requested_at,
                "MANUAL",
            ),
        )

        conn.commit()
        return cursor.lastrowid
