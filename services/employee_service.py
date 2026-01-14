from domain.employee import Employee
from repository.employee_repository import EmployeeRepository
from core.exceptions import NotFoundError, ValidationError


class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

    def hire_employee(self, emp_id: str, name: str, id_number: str, department: str) -> Employee:
        if not emp_id or not name or not id_number:
            raise ValidationError("emp_id, name, id_number are required")

        if self.repo.exists(emp_id):
            raise ValidationError(f"Employee {emp_id} already exists")

        employee = Employee(
            emp_id=emp_id,
            name=name,
            id_number=id_number,
            department=department,
        )

        self.repo.add(employee)
        return employee

    def get_employee(self, emp_id: str) -> Employee:
        employee = self.repo.get(emp_id)
        if not employee:
            raise NotFoundError(f"Employee {emp_id} not found")
        return employee

    def list_employees(self, active_only: bool = False) -> list[Employee]:
        employees = self.repo.list_all()
        return [e for e in employees if e.is_active] if active_only else employees

    def update_employee_info(
        self,
        emp_id: str,
        name: str,
        id_number: str,
        department: str,
    ) -> Employee:
        employee = self.get_employee(emp_id)

        updated = Employee(
            emp_id=employee.emp_id,
            name=name,
            id_number=id_number,
            department=department,
            is_active=employee.is_active,
        )

        self.repo.update(updated)
        return updated

    def deactivate_employee(self, emp_id: str) -> Employee:
        employee = self.get_employee(emp_id)
        if not employee.is_active:
            raise ValidationError("Employee already inactive")

        updated = employee.deactivate()
        self.repo.update(updated)
        return updated

    def activate_employee(self, emp_id: str) -> Employee:
        employee = self.get_employee(emp_id)
        if employee.is_active:
            raise ValidationError("Employee already active")

        updated = employee.activate()
        self.repo.update(updated)
        return updated


