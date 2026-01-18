from selenium.webdriver.common.by import By

class TraTicketQueryLocators:
    """
    Element locators for TRA ticket booking query page.
    """

    # =========================
    # 身分識別
    # =========================
    ID_NUMBER_INPUT = (By.NAME, "pid")

    # =========================
    # 車站選擇
    # =========================
    FROM_STATION_INPUT = (By.NAME, "startStation")
    TO_STATION_INPUT = (By.NAME, "endStation")

    # =========================
    # 行程類型
    # =========================
    TRIP_TYPE_ONE_WAY = (By.XPATH, "//input[@type='radio' and @value='ONEWAY']")
    TRIP_TYPE_ROUND_TRIP = (By.XPATH, "//input[@type='radio' and @value='ROUNDTRIP']")

    # =========================
    # 訂票方式
    # =========================
    BOOKING_BY_TRAIN_NO = (By.XPATH, "//input[@type='radio' and contains(@value, 'TRAIN')]")

    # =========================
    # 票數
    # =========================
    TICKET_COUNT_SELECT = (By.ID, "normalQty")

    # =========================
    # 日期
    # =========================
    DATE_INPUT = (By.ID, "rideDate1")

    # =========================
    # 車次：依序取得三個 input
    # =========================
    @staticmethod
    def TRAIN_NO_INPUT_BY_INDEX(index: int):
        """
        index: 0, 1, 2 分別對應三個車次欄位
        """
        assert 0 <= index <= 2, "index must be 0, 1, or 2"
        return (By.ID, f"trainNoList{index+1}")

    # =========================
    # 座位偏好
    # =========================
    SEAT_PREFERENCE_SELECT = (By.NAME, "seatPref")

    # =========================
    # 送出訂票
    # =========================
    SUBMIT_BUTTON = (By.XPATH, "//input[@type='submit' and contains(@class, 'btn-3d') and @value='訂票']")
