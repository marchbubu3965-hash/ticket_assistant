# domain/employee.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class Employee:
    emp_id: str
    name: str
    department: str
    title: Optional[str] = None
    is_active: bool = True



# from dataclasses import dataclass
# from datetime import datetime
# from typing import Optional


# @dataclass
# class Employee:
#     """
#     員工資料核心模型（Domain Model）
#     """
#     employee_id: str
#     name: str
#     department: str
#     title: str
#     is_active: bool = True
#     created_at: datetime = datetime.utcnow()
#     updated_at: Optional[datetime] = None

#     def deactivate(self):
#         self.is_active = False
#         self.updated_at = datetime.utcnow()

#     def activate(self):
#         self.is_active = True
#         self.updated_at = datetime.utcnow()
