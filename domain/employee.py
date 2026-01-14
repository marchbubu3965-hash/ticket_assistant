from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional
import re


class InvalidEmployeeError(ValueError):
    """
    Employee Domain 驗證失敗時拋出的例外
    """
    pass


@dataclass(frozen=True)
class Employee:
    """
    Employee Domain Model

    原則：
    - 只描述「員工是什麼」
    - 不處理 IO / DB / UI
    - 所有欄位在此即為業務真相
    """

    emp_id: str
    name: str
    id_number: str
    department: str
    is_active: bool = True
    hired_date: Optional[date] = None

    def __post_init__(self):
        """
        Domain-level validation
        """
        self._validate_emp_id()
        self._validate_name()
        self._validate_id_number()
        self._validate_department()

    # =========================
    # Validation rules
    # =========================

    def _validate_emp_id(self):
        if not self.emp_id or not isinstance(self.emp_id, str):
            raise InvalidEmployeeError("emp_id must be a non-empty string")

        if len(self.emp_id) > 20:
            raise InvalidEmployeeError("emp_id length must be <= 20")

    def _validate_name(self):
        if not self.name or not isinstance(self.name, str):
            raise InvalidEmployeeError("name must be a non-empty string")

        if len(self.name) > 50:
            raise InvalidEmployeeError("name length must be <= 50")

    def _validate_department(self):
        if not self.department or not isinstance(self.department, str):
            raise InvalidEmployeeError("department must be a non-empty string")

        if len(self.department) > 50:
            raise InvalidEmployeeError("department length must be <= 50")
        
    def _validate_id_number(self):
        pattern = r"^[A-Z][12]\d{8}$"
        if not re.match(pattern, self.id_number):
            raise InvalidEmployeeError("身分證字號格式錯誤")

    # =========================
    # Domain behaviors
    # =========================

    def deactivate(self) -> Employee:
        """
        回傳一個「已停用」的新 Employee instance
        """
        if not self.is_active:
            return self

        return Employee(
            emp_id=self.emp_id,
            name=self.name,
            id_number=self.id_number,
            department=self.department,
            is_active=False,
            hired_date=self.hired_date,
        )

    def activate(self) -> Employee:
        """
        回傳一個「啟用中」的新 Employee instance
        """
        if self.is_active:
            return self

        return Employee(
            emp_id=self.emp_id,
            name=self.name,
            id_number=self.id_number,
            department=self.department,
            is_active=True,
            hired_date=self.hired_date,
        )
