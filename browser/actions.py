from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from browser.element_locator import TraTicketQueryLocators
import time

class TraTicketActions:
    """
    台鐵訂票頁面操作行為封裝（⚠️ 必須模擬人類輸入節奏）
    """

    def __init__(self, driver, watcher):
        self.driver = driver
        self.watcher = watcher

    # =========================
    # 共用：人類輸入
    # =========================
    def _human_input(self, element, text: str, delay: float = 0.15):
        time.sleep(1)
        element.clear()
        time.sleep(delay)

        for ch in text:
            element.send_keys(ch)
            time.sleep(delay)

        element.send_keys(Keys.TAB)
        time.sleep(delay)

    # =========================
    # 行程類型
    # =========================
    def select_trip_type(self, one_way: bool = True):
        locator = TraTicketQueryLocators.TRIP_TYPE_ONE_WAY if one_way else TraTicketQueryLocators.TRIP_TYPE_ROUND_TRIP
        by, value = locator
        element = self.watcher.wait_for_clickable(by, value)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(0.3)

    # =========================
    # 訂票方式：依車次
    # =========================
    def select_booking_by_train_no(self):
        by, value = TraTicketQueryLocators.BOOKING_BY_TRAIN_NO
        element = self.watcher.wait_for_clickable(by, value)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(1)  # 等待表單更新

    # =========================
    # 身分證字號
    # =========================
    def fill_id_number(self, id_number: str):
        by, value = TraTicketQueryLocators.ID_NUMBER_INPUT
        element = self.watcher.wait_for_visible(by, value)
        self._human_input(element, id_number)

    # =========================
    # 起站 / 迄站
    # =========================
    def fill_stations(self, from_station: str, to_station: str):
        by, value = TraTicketQueryLocators.FROM_STATION_INPUT
        from_input = self.watcher.wait_for_visible(by, value)
        self._human_input(from_input, from_station, delay=0.1)
        time.sleep(0.5)

        by, value = TraTicketQueryLocators.TO_STATION_INPUT
        to_input = self.watcher.wait_for_visible(by, value)
        self._human_input(to_input, to_station, delay=0.1)
        time.sleep(0.5)

    # =========================
    # 票數
    # =========================
    def select_ticket_count(self, count: int):
        by, value = TraTicketQueryLocators.TICKET_COUNT_SELECT
        element = self.watcher.wait_for_visible(by, value)
        element.clear()
        time.sleep(0.2)
        element.send_keys(str(count))
        element.send_keys(Keys.TAB)
        time.sleep(0.3)

    # =========================
    # 日期
    # =========================
    def fill_date(self, date_str: str):
        by, value = TraTicketQueryLocators.DATE_INPUT
        element = self.watcher.wait_for_visible(by, value)
        self.driver.execute_script("arguments[0].value = arguments[1];", element, date_str)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", element)
        time.sleep(1)

    # =========================
    # 車次
    # =========================
    def fill_train_no(self, train_no: str, index: int = 0):
        by, value = TraTicketQueryLocators.TRAIN_NO_INPUT_BY_INDEX(index)
        element = self.watcher.wait_for_visible(by, value)
        self._human_input(element, train_no, delay=0.12)

    # =========================
    # 送出
    # =========================
    def click_submit(self):
        by, value = TraTicketQueryLocators.SUBMIT_BUTTON
        element = self.watcher.wait_for_clickable(by, value)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(1)
