from domain.employee import Employee
from repository.employee_repository import EmployeeRepository
from core.exceptions import NotFoundError, ValidationError


class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

    # ---------- Use Cases ----------

    def hire_employee(self, emp_id: str, name: str, department: str) -> Employee:
        """
        新增員工（入職）
        """
        if not emp_id or not name:
            raise ValidationError("emp_id and name are required")

        if self.repo.exists(emp_id):
            raise ValidationError(f"Employee {emp_id} already exists")

        employee = Employee(
            emp_id=emp_id,
            name=name,
            department=department,
        )

        self.repo.add(employee)
        return employee

    def get_employee(self, emp_id: str) -> Employee:
        """
        查詢單一員工
        """
        employee = self.repo.get(emp_id)
        if employee is None:
            raise NotFoundError(f"Employee {emp_id} not found")
        return employee

    def list_employees(self, active_only: bool = False) -> list[Employee]:
        """
        查詢員工清單
        """
        employees = self.repo.list_all()
        if active_only:
            employees = [e for e in employees if e.is_active]
        return employees

    def deactivate_employee(self, emp_id: str) -> Employee:
        """
        員工離職 / 停用
        """
        employee = self.get_employee(emp_id)

        if not employee.is_active:
            raise ValidationError(f"Employee {emp_id} is already inactive")

        updated = employee.deactivate()
        self.repo.update(updated)
        return updated
