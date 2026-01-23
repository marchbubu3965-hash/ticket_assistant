import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "ticket.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # UI 請求紀錄（只記 UI）
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ticket_request_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT NOT NULL,
        id_number TEXT NOT NULL,

        start_station TEXT NOT NULL,
        end_station TEXT NOT NULL,

        trip_type TEXT NOT NULL,               -- ONE_WAY / ROUND_TRIP
        ticket_count INTEGER NOT NULL,

        travel_date TEXT NOT NULL,
        train_nos TEXT NOT NULL,               -- comma-separated

        is_scheduled INTEGER NOT NULL,          -- 0 / 1
        scheduled_at TEXT,                      -- nullable

        requested_at TEXT NOT NULL              -- UI click time
    )
    """)

    # =========================
    # 訂票結果紀錄（你原本的）
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ticket_order_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        order_time TEXT,
        travel_date TEXT,
        start_station TEXT,
        end_station TEXT,
        train_no TEXT,
        ticket_qty INTEGER,
        status TEXT,
        message TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()
