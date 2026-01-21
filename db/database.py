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
