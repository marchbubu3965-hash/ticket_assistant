from services.employee_service import EmployeeService
from repository.employee_repository import EmployeeRepository
from core.exceptions import ValidationError, NotFoundError


class EmployeeController:
    """
    Employee 用例層 / Facade
    UI 或 script 只與此類別互動
    """

    def __init__(self):
        repo = EmployeeRepository()
        self.service = EmployeeService(repo)

    # === 用例 1：新增員工 ===
    def hire_employee(self, emp_id: str, name: str, department: str):
        try:
            return self.service.hire_employee(emp_id, name, department)
        except ValidationError as e:
            # 之後 UI 可以直接顯示這個訊息
            raise e

    # === 用例 2：停用員工 ===
    def deactivate_employee(self, emp_id: str):
        try:
            return self.service.deactivate_employee(emp_id)
        except NotFoundError as e:
            raise e

    # === 用例 3：查詢員工 ===
    def get_employee(self, emp_id: str):
        try:
            return self.service.get_employee(emp_id)
        except NotFoundError as e:
            raise e
