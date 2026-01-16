import sqlite3
from pathlib import Path

class RecentStationRepository:
    def __init__(self):
        db_path = Path(__file__).parent.parent / "data" / "stations.db"
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_table()

    def _init_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recent_stations (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            used_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()

    def record(self, code, name):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO recent_stations (code, name, used_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (code, name))
        self.conn.commit()

    def list_recent(self, limit=5):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT code, name
        FROM recent_stations
        ORDER BY used_at DESC
        LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
