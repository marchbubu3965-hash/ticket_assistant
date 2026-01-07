from repository.employee_repository import EmployeeRepository
from domain.employee import Employee


def main():
    repo = EmployeeRepository()

    repo.clear_all()

    emp = Employee(
        emp_id="E001",
        name="王小明",
        department="資訊室",
        title="工程師"
    )

    repo.add(emp)

    loaded = repo.get_by_id("E001")
    assert loaded is not None
    assert loaded.name == "王小明"

    print("Employee Repository smoke test OK")


if __name__ == "__main__":
    main()
