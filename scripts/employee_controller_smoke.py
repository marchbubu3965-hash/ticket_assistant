from core.controller import EmployeeController


def main():
    controller = EmployeeController()

    emp = controller.hire_employee("E004", "張小美", "Finance")
    print(emp)

    emp = controller.deactivate_employee("E004")
    print("Active:", emp.is_active)


if __name__ == "__main__":
    main()
