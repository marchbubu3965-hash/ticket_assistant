import sqlite3
from pathlib import Path
from typing import Optional

from domain.employee import Employee


class EmployeeRepository:
    """
    Employee Repository
    - 負責 Employee 的資料存取
    - 僅接受 / 回傳 Employee domain object
    """

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = Path(__file__).resolve().parents[1]
            data_dir = base_dir / "data"
            data_dir.mkdir(exist_ok=True)
            self.db_path = data_dir / "employees.db"
        else:
            self.db_path = Path(db_path)

        self._init_db()

    # =========================
    # DB bootstrap
    # =========================

    def _get_conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """
        初始化資料表（若不存在）
        """
        with self._get_conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS employees (
                    emp_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    id_number TEXT NOT NULL,
                    is_active INTEGER NOT NULL,
                    hired_date TEXT
                )
                """
            )

    # =========================
    # CRUD operations
    # =========================

    def add(self, employee: Employee) -> None:
        """
        新增員工
        """
        try:
            with self._get_conn() as conn:
                conn.execute(
                    """
                    INSERT INTO employees (
                        emp_id,
                        name,
                        department,
                        id_number,
                        is_active,
                        hired_date
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        employee.emp_id,
                        employee.name,
                        employee.department,
                        employee.id_number,
                        int(employee.is_active),
                        employee.hired_date.isoformat()
                        if employee.hired_date
                        else None,
                    ),
                )
        except sqlite3.IntegrityError as e:
            raise ValueError(
                f"Employee with emp_id '{employee.emp_id}' already exists"
            ) from e

    def get(self, emp_id: str) -> Optional[Employee]:
        """
        依 emp_id 取得 Employee
        """
        with self._get_conn() as conn:
            row = conn.execute(
                """
                SELECT
                    emp_id,
                    name,
                    department,
                    id_number,
                    is_active,
                    hired_date
                FROM employees
                WHERE emp_id = ?
                """,
                (emp_id,),
            ).fetchone()

        if row is None:
            return None

        return Employee(
            emp_id=row[0],
            name=row[1],
            department=row[2],
            id_number=row[3],
            is_active=bool(row[4]),
            hired_date=None,
        )

    def list_all(self) -> list[Employee]:
        """
        取得全部員工
        """
        with self._get_conn() as conn:
            rows = conn.execute(
                """
                SELECT
                    emp_id,
                    name,
                    department,
                    id_number,
                    is_active,
                    hired_date
                FROM employees
                ORDER BY emp_id
                """
            ).fetchall()

        return [
            Employee(
                emp_id=r[0],
                name=r[1],
                department=r[2],
                id_number=r[3],
                is_active=bool(r[4]),
                hired_date=None,
            )
            for r in rows
        ]

    def update(self, employee: Employee) -> None:
        """
        更新既有員工（以 emp_id 為 key）
        """
        with self._get_conn() as conn:
            cur = conn.execute(
                """
                UPDATE employees
                SET
                    name = ?,
                    department = ?,
                    id_number = ?,
                    is_active = ?,
                    hired_date = ?
                WHERE emp_id = ?
                """,
                (
                    employee.name,
                    employee.department,
                    employee.id_number,
                    int(employee.is_active),
                    employee.hired_date.isoformat()
                    if employee.hired_date
                    else None,
                    employee.emp_id,
                ),
            )

            if cur.rowcount == 0:
                raise ValueError(
                    f"Employee with emp_id '{employee.emp_id}' does not exist"
                )

    def delete(self, emp_id: str) -> None:
        """
        刪除員工（實體刪除）
        """
        with self._get_conn() as conn:
            conn.execute(
                "DELETE FROM employees WHERE emp_id = ?",
                (emp_id,),
            )

    def exists(self, emp_id: str) -> bool:
        with self._get_conn() as conn:
            cur = conn.execute(
                "SELECT 1 FROM employees WHERE emp_id = ? LIMIT 1",
                (emp_id,)
            )
            return cur.fetchone() is not None
