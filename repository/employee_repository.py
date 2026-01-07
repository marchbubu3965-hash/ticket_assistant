
import sqlite3
from typing import List, Optional
from domain.employee import Employee
import os


class EmployeeRepository:
    def __init__(self, db_path: str = "data/app.db"):
        self.db_path = db_path
        self._init_db()


    def _get_conn(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        return sqlite3.connect(self.db_path)


    # def _get_conn(self):
    #     return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    emp_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    title TEXT,
                    is_active INTEGER NOT NULL
                )
            """)

    # ===== CRUD =====

    def add(self, employee: Employee):
        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO employees
                (emp_id, name, department, title, is_active)
                VALUES (?, ?, ?, ?, ?)
            """, (
                employee.emp_id,
                employee.name,
                employee.department,
                employee.title,
                int(employee.is_active)
            ))

    def get_by_id(self, emp_id: str) -> Optional[Employee]:
        with self._get_conn() as conn:
            cur = conn.execute(
                "SELECT emp_id, name, department, title, is_active FROM employees WHERE emp_id = ?",
                (emp_id,)
            )
            row = cur.fetchone()
            if not row:
                return None

            return Employee(
                emp_id=row[0],
                name=row[1],
                department=row[2],
                title=row[3],
                is_active=bool(row[4])
            )

    def list_all(self) -> List[Employee]:
        with self._get_conn() as conn:
            cur = conn.execute(
                "SELECT emp_id, name, department, title, is_active FROM employees"
            )
            return [
                Employee(
                    emp_id=r[0],
                    name=r[1],
                    department=r[2],
                    title=r[3],
                    is_active=bool(r[4])
                )
                for r in cur.fetchall()
            ]

    def deactivate(self, emp_id: str):
        with self._get_conn() as conn:
            conn.execute(
                "UPDATE employees SET is_active = 0 WHERE emp_id = ?",
                (emp_id,)
            )


    def clear_all(self):
        with self._get_conn() as conn:
            conn.execute("DELETE FROM employees")
            conn.commit()


# from typing import Dict, List, Optional
# from domain.employee import Employee


# class EmployeeRepository:
#     """
#     員工資料存取層（目前為 In-Memory，之後可換 DB）
#     """

#     def __init__(self):
#         self._employees: Dict[str, Employee] = {}

#     def add(self, employee: Employee) -> None:
#         if employee.employee_id in self._employees:
#             raise ValueError(f"Employee {employee.employee_id} already exists")
#         self._employees[employee.employee_id] = employee

#     def get(self, employee_id: str) -> Optional[Employee]:
#         return self._employees.get(employee_id)

#     def list_all(self, include_inactive: bool = False) -> List[Employee]:
#         if include_inactive:
#             return list(self._employees.values())
#         return [e for e in self._employees.values() if e.is_active]

#     def deactivate(self, employee_id: str) -> None:
#         employee = self.get(employee_id)
#         if not employee:
#             raise ValueError(f"Employee {employee_id} not found")
#         employee.deactivate()

#     def activate(self, employee_id: str) -> None:
#         employee = self.get(employee_id)
#         if not employee:
#             raise ValueError(f"Employee {employee_id} not found")
#         employee.activate()
