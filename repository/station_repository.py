import sqlite3
from pathlib import Path

class StationRepository:
    def __init__(self):
        db_path = Path(__file__).parent.parent / "data" / "stations.db"
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def search(self, keyword: str, limit: int = 10):
        cursor = self.conn.cursor()
        kw = f"%{keyword}%"

        cursor.execute(
            """
            SELECT code, name
            FROM stations
            WHERE code LIKE ? OR name LIKE ?
            ORDER BY code
            LIMIT ?
            """,
            (kw, kw, limit),
        )

        return [dict(row) for row in cursor.fetchall()]
