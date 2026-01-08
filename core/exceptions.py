# core/exceptions.py

class AppError(Exception):
    """所有應用層錯誤的基底類別"""
    pass


class ValidationError(AppError):
    """資料或業務規則驗證失敗"""
    pass


class NotFoundError(AppError):
    """找不到資源（例如 Employee 不存在）"""
    pass
