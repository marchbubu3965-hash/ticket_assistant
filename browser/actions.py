from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from browser.dom_watcher import DomWatcher
from browser.element_locator import TraTicketQueryLocators


class TraTicketActions:
    """
    Encapsulates user-like interactions on the TRA ticket query page.
    This class performs actions only; it does not manage flow or state.
    """

    def __init__(self, driver, watcher: DomWatcher):
        self.driver = driver
        self.watcher = watcher

    # =========================
    # 身分證字號
    # =========================
    def fill_id_number(self, id_number: str) -> None:
        by, value = TraTicketQueryLocators.ID_NUMBER_INPUT
        element = self.watcher.wait_for_visible(by, value)
        element.clear()
        element.send_keys(id_number)

    # =========================
    # 車站選擇
    # =========================
    def fill_stations(self, from_station: str, to_station: str) -> None:
        from_by, from_value = TraTicketQueryLocators.FROM_STATION_INPUT
        to_by, to_value = TraTicketQueryLocators.TO_STATION_INPUT

        from_input = self.watcher.wait_for_visible(from_by, from_value)
        from_input.clear()
        from_input.send_keys(from_station)
        from_input.send_keys(Keys.TAB)

        to_input = self.watcher.wait_for_visible(to_by, to_value)
        to_input.clear()
        to_input.send_keys(to_station)
        to_input.send_keys(Keys.TAB)

    # =========================
    # 行程類型
    # =========================
    def select_trip_type(self, one_way: bool = True) -> None:
        locator = (
            TraTicketQueryLocators.TRIP_TYPE_ONE_WAY
            if one_way
            else TraTicketQueryLocators.TRIP_TYPE_ROUND_TRIP
        )
        by, value = locator
        element = self.watcher.wait_for_clickable(by, value)
        element.click()

    # =========================
    # 訂票方式
    # =========================
    def select_booking_by_train_no(self) -> None:
        by, value = TraTicketQueryLocators.BOOKING_BY_TRAIN_NO
        element = self.watcher.wait_for_clickable(by, value)
        element.click()

    # =========================
    # 票數
    # =========================
    def select_ticket_count(self, count: int) -> None:
        if count < 1:
            raise ValueError("Ticket count must be at least 1")

        by, value = TraTicketQueryLocators.TICKET_COUNT_SELECT
        select_element = self.watcher.wait_for_visible(by, value)
        Select(select_element).select_by_value(str(count))

    # =========================
    # 日期
    # =========================
    def fill_date(self, ride_date: str) -> None:
        """
        ride_date format: YYYY/MM/DD
        """
        by, value = TraTicketQueryLocators.DATE_INPUT
        element = self.watcher.wait_for_visible(by, value)
        element.clear()
        element.send_keys(ride_date)
        element.send_keys(Keys.TAB)

    # =========================
    # 車次
    # =========================
    def fill_train_no(self, train_no: str) -> None:
        by, value = TraTicketQueryLocators.TRAIN_NO_INPUT
        element = self.watcher.wait_for_visible(by, value)
        element.clear()
        element.send_keys(train_no)

    # =========================
    # 座位偏好
    # =========================
    def select_seat_preference(self, preference_value: str) -> None:
        """
        preference_value depends on site options, e.g.:
        - ANY
        - WINDOW
        - AISLE
        """
        by, value = TraTicketQueryLocators.SEAT_PREFERENCE_SELECT
        select_element = self.watcher.wait_for_visible(by, value)
        Select(select_element).select_by_value(preference_value)

    # =========================
    # 送出訂票
    # =========================
    def submit_booking(self) -> None:
        by, value = TraTicketQueryLocators.SUBMIT_BUTTON
        element = self.watcher.wait_for_clickable(by, value)
        element.click()
