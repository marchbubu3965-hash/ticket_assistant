from services.employee_service import EmployeeService
from domain.employee import Employee


class EmployeeController:
    def __init__(self, service: EmployeeService):
        self.service = service

    # -------------------------
    # Create
    # -------------------------
    def create(self, emp_id: str, name: str, id_number: str, department: str) -> Employee:
        return self.service.hire_employee(
            emp_id=emp_id,
            name=name,
            id_number=id_number,
            department=department,
        )

    # -------------------------
    # Read
    # -------------------------
    def list_all(self) -> list[Employee]:
        return self.service.list_employees()

    def get(self, emp_id: str) -> Employee:
        return self.service.get_employee(emp_id)

    # -------------------------
    # Update（狀態）
    # -------------------------
    def deactivate(self, emp_id: str) -> Employee:
        return self.service.deactivate_employee(emp_id)

    # 預留：未來編輯資料
    def update(self, emp_id: str, name: str, id_number: str, department: str) -> Employee:
        employee = self.get(emp_id)
        updated = Employee(
            emp_id=employee.emp_id,
            name=name,
            id_number=id_number,
            department=department,
            is_active=employee.is_active,
            hired_date=employee.hired_date,
        )
        return self.service.update_employee(updated)


    # -------------------------
    # Delete（如你要）
    # -------------------------
    def delete(self, emp_id: str) -> None:
        self.service.delete_employee(emp_id)

    def list_employees(self) -> list[Employee]:
        return self.list_all()