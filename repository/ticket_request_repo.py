from datetime import datetime
from db.database import get_connection


class TicketRequestRepository:
    TABLE_NAME = "ticket_request_log"

    # =========================
    # Table init
    # =========================
    @staticmethod
    def ensure_table():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TicketRequestRepository.TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            -- 員工快照（避免跨 DB JOIN）
            employee_id TEXT NOT NULL,
            employee_name TEXT NOT NULL,
            employee_id_number TEXT NOT NULL,

            -- 訂票資訊
            start_station TEXT NOT NULL,
            end_station TEXT NOT NULL,
            trip_type TEXT NOT NULL,
            ticket_count INTEGER NOT NULL,
            travel_date TEXT NOT NULL,
            train_nos TEXT NOT NULL,

            -- 排程
            is_scheduled INTEGER NOT NULL,
            scheduled_at TEXT,

            -- 時間
            requested_at TEXT NOT NULL
        )
        """)

        conn.commit()
        conn.close()

    # =========================
    # Insert
    # =========================
    @staticmethod
    def insert(
        *,
        employee_id: str,
        employee_name: str,
        employee_id_number: str,
        start_station: str,
        end_station: str,
        trip_type: str,
        ticket_count: int,
        travel_date: str,
        train_nos: list[str],
        is_scheduled: bool,
        scheduled_at: datetime | None,
    ):
        TicketRequestRepository.ensure_table()

        clean_train_nos = [no for no in train_nos if no]
        train_nos_str = ",".join(clean_train_nos)

        requested_at = datetime.now().isoformat()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f"""
        INSERT INTO {TicketRequestRepository.TABLE_NAME} (
            employee_id,
            employee_name,
            employee_id_number,
            start_station,
            end_station,
            trip_type,
            ticket_count,
            travel_date,
            train_nos,
            is_scheduled,
            scheduled_at,
            requested_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            employee_id,
            employee_name,
            employee_id_number,
            start_station,
            end_station,
            trip_type,
            ticket_count,
            travel_date,
            train_nos_str,
            1 if is_scheduled else 0,
            scheduled_at.isoformat() if scheduled_at else None,
            requested_at,
        ))

        conn.commit()
        conn.close()

    # =========================
    # Fetch (for UI)
    # =========================
    @staticmethod
    def fetch_all(limit: int = 100):
        TicketRequestRepository.ensure_table()
        conn = get_connection()
        cursor = conn.cursor()

        # 修改後的 SQL 查詢，確保順序與 TableModel 對齊
        # index 0: 員工 (ID-姓名)
        # index 1: 身分證
        # index 2: 起站
        # index 3: 迄站
        # index 4: 張數
        # index 5: 乘車日期
        # index 6: 排程 (is_scheduled)
        # index 7: 預計時間 (scheduled_at)
        # index 8: 申請時間 (requested_at)
        cursor.execute(f"""
        SELECT
            employee_id || '-' || employee_name,
            employee_id_number,
            start_station,
            end_station,
            ticket_count,
            travel_date,
            is_scheduled,
            scheduled_at,
            requested_at
        FROM {TicketRequestRepository.TABLE_NAME}
        ORDER BY requested_at DESC
        LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        conn.close()
        return rows
    
# from datetime import datetime
# from db.database import get_connection


# class TicketRequestRepository:
#     TABLE_NAME = "ticket_request_log"

#     # =========================
#     # Table init
#     # =========================
#     @staticmethod
#     def ensure_table():
#         conn = get_connection()
#         cursor = conn.cursor()

#         cursor.execute(f"""
#         CREATE TABLE IF NOT EXISTS {TicketRequestRepository.TABLE_NAME} (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,

#             -- 員工快照（避免跨 DB JOIN）
#             employee_id TEXT NOT NULL,
#             employee_name TEXT NOT NULL,
#             employee_id_number TEXT NOT NULL,

#             -- 訂票資訊
#             start_station TEXT NOT NULL,
#             end_station TEXT NOT NULL,
#             trip_type TEXT NOT NULL,
#             ticket_count INTEGER NOT NULL,
#             travel_date TEXT NOT NULL,
#             train_nos TEXT NOT NULL,

#             -- 排程
#             is_scheduled INTEGER NOT NULL,
#             scheduled_at TEXT,

#             -- 時間
#             requested_at TEXT NOT NULL
#         )
#         """)

#         conn.commit()
#         conn.close()

#     # =========================
#     # Insert
#     # =========================
#     @staticmethod
#     def insert(
#         *,
#         employee_id: str,
#         employee_name: str,
#         employee_id_number: str,
#         start_station: str,
#         end_station: str,
#         trip_type: str,
#         ticket_count: int,
#         travel_date: str,
#         train_nos: list[str],
#         is_scheduled: bool,
#         scheduled_at: datetime | None,
#     ):
#         TicketRequestRepository.ensure_table()

#         clean_train_nos = [no for no in train_nos if no]
#         train_nos_str = ",".join(clean_train_nos)

#         requested_at = datetime.now().isoformat()

#         conn = get_connection()
#         cursor = conn.cursor()

#         cursor.execute(f"""
#         INSERT INTO {TicketRequestRepository.TABLE_NAME} (
#             employee_id,
#             employee_name,
#             employee_id_number,
#             start_station,
#             end_station,
#             trip_type,
#             ticket_count,
#             travel_date,
#             train_nos,
#             is_scheduled,
#             scheduled_at,
#             requested_at
#         )
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, (
#             employee_id,
#             employee_name,
#             employee_id_number,
#             start_station,
#             end_station,
#             trip_type,
#             ticket_count,
#             travel_date,
#             train_nos_str,
#             1 if is_scheduled else 0,
#             scheduled_at.isoformat() if scheduled_at else None,
#             requested_at,
#         ))

#         conn.commit()
#         conn.close()

#     # =========================
#     # Fetch (for UI)
#     # =========================
#     @staticmethod
#     def fetch_all(limit: int = 100):
#         TicketRequestRepository.ensure_table()
#         conn = get_connection()
#         cursor = conn.cursor()

#         cursor.execute(f"""
#         SELECT
#             employee_id,
#             employee_name,
#             employee_id_number,
#             start_station,
#             end_station,
#             ticket_count,
#             travel_date,
#             is_scheduled,
#             requested_at
#         FROM {TicketRequestRepository.TABLE_NAME}
#         ORDER BY requested_at DESC
#         LIMIT ?
#         """, (limit,))

#         rows = cursor.fetchall()
#         conn.close()
#         return rows

