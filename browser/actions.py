from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from browser.element_locator import TraTicketQueryLocators
import time


class TraTicketActions:
    """
    台鐵訂票頁面操作行為封裝
    """

    def __init__(self, driver, watcher):
        self.driver = driver
        self.watcher = watcher

    # =========================
    # 行程類型
    # =========================
    def select_trip_type(self, one_way: bool = True):
        locator = (
            TraTicketQueryLocators.TRIP_TYPE_ONE_WAY
            if one_way
            else TraTicketQueryLocators.TRIP_TYPE_ROUND_TRIP
        )
        by, value = locator
        element = self.watcher.wait_for_clickable(by, value)
        self.driver.execute_script("arguments[0].click();", element)

    # =========================
    # 訂票方式：依車次
    # =========================
    def select_booking_by_train_no(self):
        by, value = TraTicketQueryLocators.BOOKING_BY_TRAIN_NO
        element = self.watcher.wait_for_clickable(by, value)
        self.driver.execute_script("arguments[0].click();", element)

    # =========================
    # 身分證字號
    # =========================
    def fill_id_number(self, id_number: str):
        by, value = TraTicketQueryLocators.ID_NUMBER_INPUT
        element = self.watcher.wait_for_visible(by, value)
        element.clear()
        element.send_keys(id_number)

    # =========================
    # 起站 / 迄站（autocomplete）
    # =========================
    def fill_stations(self, from_station: str, to_station: str):
        # 起站
        by, value = TraTicketQueryLocators.FROM_STATION_INPUT
        from_input = self.watcher.wait_for_visible(by, value)
        from_input.clear()
        from_input.send_keys(from_station)

        # 給 autocomplete JS 反應時間
        time.sleep(0.5)

        # 迄站
        by, value = TraTicketQueryLocators.TO_STATION_INPUT
        to_input = self.watcher.wait_for_visible(by, value)
        to_input.clear()
        to_input.send_keys(to_station)

        time.sleep(0.5)

    # =========================
    # 票數（select 或 input，依你 locator）
    # =========================
    def select_ticket_count(self, count: int):
        by, value = TraTicketQueryLocators.TICKET_COUNT_SELECT
        element = self.watcher.wait_for_presence(by, value)

        tag_name = element.tag_name.lower()
        if tag_name == "select":
            Select(element).select_by_value(str(count))
        else:
            element.clear()
            element.send_keys(str(count))

    # =========================
    # 日期（⚠️ 台鐵 datepicker 一定要用 JS）
    # =========================
    def fill_date(self, date_str: str):
        by, value = TraTicketQueryLocators.DATE_INPUT
        element = self.watcher.wait_for_presence(by, value)

        self.driver.execute_script(
            "arguments[0].value = arguments[1];", element, date_str
        )

        # 觸發 change 事件，避免被 JS 覆寫
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('change'));", element
        )

        time.sleep(0.3)

    # =========================
    # 車次
    # =========================
    def fill_train_no(self, train_no: str):
        by, value = TraTicketQueryLocators.TRAIN_NO_INPUT
        element = self.watcher.wait_for_presence(by, value)

        self.driver.execute_script(
            "arguments[0].value = arguments[1];",
            element,
            train_no
        )

        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('change'));",
            element
        )

    # def fill_train_no(self, train_no: str):
    #     by, value = TraTicketQueryLocators.TRAIN_NO_INPUT
    #     element = self.watcher.wait_for_visible(by, value)
    #     element.clear()
    #     element.send_keys(train_no)

    # =========================
    # 座位偏好（目前可不呼叫）
    # =========================
    def select_seat_preference(self, pref_value: str):
        by, value = TraTicketQueryLocators.SEAT_PREFERENCE_SELECT
        element = self.watcher.wait_for_presence(by, value)
        Select(element).select_by_value(pref_value)

    # =========================
    # 送出（smoke test 先不呼叫）
    # =========================
    def click_submit(self):
        by, value = TraTicketQueryLocators.SUBMIT_BUTTON
        element = self.watcher.wait_for_clickable(by, value)
        self.driver.execute_script("arguments[0].click();", element)



# from selenium.webdriver.support.ui import Select
# from browser.element_locator import TraTicketQueryLocators
# from selenium.webdriver.common.by import By
# import time

# class TraTicketActions:
#     """
#     台鐵訂票頁面操作行為封裝
#     """

#     def __init__(self, driver, watcher):
#         self.driver = driver
#         self.watcher = watcher

#     # =========================
#     # 行程類型
#     # =========================
#     def select_trip_type(self, one_way: bool = True):
#         locator = (
#             TraTicketQueryLocators.TRIP_TYPE_ONE_WAY
#             if one_way
#             else TraTicketQueryLocators.TRIP_TYPE_ROUND_TRIP
#         )
#         by, value = locator
#         element = self.watcher.wait_for_clickable(by, value)
#         self.driver.execute_script("arguments[0].click();", element)

#     # =========================
#     # 訂票方式：依車次
#     # =========================
#     def select_booking_by_train_no(self):
#         by, value = TraTicketQueryLocators.BOOKING_BY_TRAIN_NO
#         element = self.watcher.wait_for_clickable(by, value)
#         self.driver.execute_script("arguments[0].click();", element)

#     # =========================
#     # 票數
#     # =========================
#     def select_ticket_count(self, count: int):
#         by, value = TraTicketQueryLocators.TICKET_COUNT_SELECT
#         element = self.watcher.wait_for_presence(by, value)
#         Select(element).select_by_value(str(count))

#     # =========================
#     # 日期（⚠️ 台鐵一定要用 JS）
#     # =========================
#     def fill_date(self, date_str: str):
#         by, value = TraTicketQueryLocators.DATE_INPUT
#         element = self.watcher.wait_for_presence(by, value)

#         self.driver.execute_script(
#             "arguments[0].value = arguments[1];", element, date_str
#         )

#     # =========================
#     # 車次
#     # =========================
#     def fill_train_no(self, train_no: str):
#         by, value = TraTicketQueryLocators.TRAIN_NO_INPUT
#         element = self.watcher.wait_for_visible(by, value)
#         element.clear()
#         element.send_keys(train_no)

#     # =========================
#     # 座位偏好
#     # =========================
#     def select_seat_preference(self, pref_value: str):
#         by, value = TraTicketQueryLocators.SEAT_PREFERENCE_SELECT
#         element = self.watcher.wait_for_presence(by, value)
#         Select(element).select_by_value(pref_value)

#     # =========================
#     # 送出（目前 smoke test 不會呼叫）
#     # =========================
#     def click_submit(self):
#         by, value = TraTicketQueryLocators.SUBMIT_BUTTON
#         element = self.watcher.wait_for_clickable(by, value)
#         self.driver.execute_script("arguments[0].click();", element)


#     def fill_id_number(self, id_number: str):
#         by, value = TraTicketQueryLocators.ID_NUMBER_INPUT
#         element = self.watcher.wait_for_visible(by, value)
#         element.clear()
#         element.send_keys(id_number)

#     def fill_stations(self, from_station: str, to_station: str):
#         # 起站
#         by, value = TraTicketQueryLocators.FROM_STATION_INPUT
#         from_input = self.watcher.wait_for_visible(by, value)
#         from_input.clear()
#         from_input.send_keys(from_station)

#         # 小停一下，避免 autocomplete JS 吃不到值
#         time.sleep(0.3)

#         # 迄站
#         by, value = TraTicketQueryLocators.TO_STATION_INPUT
#         to_input = self.watcher.wait_for_visible(by, value)
#         to_input.clear()
#         to_input.send_keys(to_station)

