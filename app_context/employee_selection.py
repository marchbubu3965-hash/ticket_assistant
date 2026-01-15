class EmployeeSelectionContext:
    """
    全域員工選取狀態（Context / Pub-Sub）

    - 儲存目前選取的 employee（不關心型別）
    - 通知所有訂閱者
    """

    def __init__(self):
        self._employee = None
        self._subscribers = []

    def set(self, employee):
        self._employee = employee
        for callback in self._subscribers:
            callback(employee)

    def get(self):
        return self._employee

    def subscribe(self, callback):
        if callback not in self._subscribers:
            self._subscribers.append(callback)
