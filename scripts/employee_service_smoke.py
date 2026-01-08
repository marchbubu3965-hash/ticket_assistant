from repository.employee_repository import EmployeeRepository
from services.employee_service import EmployeeService


def main():
    repo = EmployeeRepository("data/employee.db")
    service = EmployeeService(repo)

    emp = service.hire_employee("E003", "李小華", "HR")
    print(emp)

    emp = service.deactivate_employee("E003")
    print("Active:", emp.is_active)


if __name__ == "__main__":
    main()
