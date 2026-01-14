from services.employee_service import EmployeeService
from domain.employee import Employee


class EmployeeController:
    """
    Employee Controller
    - 負責接收 UI 行為
    - 將請求轉交給 Service（Use Case）
    """

    def __init__(self, service: EmployeeService):
        self.service = service

    # -------------------------
    # Create
    # -------------------------
    def create(
        self,
        emp_id: str,
        name: str,
        id_number: str,
        department: str,
    ) -> Employee:
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
    # Update（基本資料）
    # -------------------------
    def update_info(
        self,
        emp_id: str,
        name: str,
        id_number: str,
        department: str,
    ) -> Employee:
        return self.service.update_employee_info(
            emp_id=emp_id,
            name=name,
            id_number=id_number,
            department=department,
        )

    # -------------------------
    # Update（狀態）
    # -------------------------
    def deactivate(self, emp_id: str) -> Employee:
        return self.service.deactivate_employee(emp_id)

    def activate(self, emp_id: str) -> Employee:
        return self.service.activate_employee(emp_id)
