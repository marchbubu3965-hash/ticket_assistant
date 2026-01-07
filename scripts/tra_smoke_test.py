from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from browser.page_loader import PageLoader
from browser.dom_watcher import DomWatcher
from browser.actions import TraTicketActions
from browser.element_locator import TraTicketQueryLocators

import time

TRA_URL = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"


def assert_input_value(driver, by, value, expected, field_name: str):
    """
    驗證 input 欄位的 value 是否正確
    """
    element = driver.find_element(by, value)
    actual = element.get_attribute("value")
    assert actual == expected, (
        f"[ASSERT FAILED] {field_name} "
        f"expected='{expected}', actual='{actual}'"
    )
    print(f"[OK] {field_name} = {actual}")


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        # 1. 載入頁面
        loader = PageLoader(driver)
        loader.load(TRA_URL)

        # 2. DOM watcher
        watcher = DomWatcher(driver)

        # 3. Actions
        actions = TraTicketActions(driver, watcher)

        # ===== 測試資料（假資料）=====
        id_number = "A123456789"
        from_station = "1000-臺北"
        to_station = "6000-臺東"
        ride_date = "2026/01/20"
        train_no = "402"

        # =============================
        # 身分證
        # =============================
        time.sleep(1)
        actions.fill_id_number(id_number)
        assert_input_value(
            driver,
            *TraTicketQueryLocators.ID_NUMBER_INPUT,
            id_number,
            "身分證字號"
        )

        # =============================
        # 起站 / 迄站
        # =============================
        time.sleep(0.3)
        actions.fill_stations(
            from_station=from_station,
            to_station=to_station
        )

        assert_input_value(
            driver,
            *TraTicketQueryLocators.FROM_STATION_INPUT,
            from_station,
            "起站"
        )
        assert_input_value(
            driver,
            *TraTicketQueryLocators.TO_STATION_INPUT,
            to_station,
            "迄站"
        )

        # =============================
        # 訂票方式（依車次）
        # =============================
        time.sleep(0.3)
        actions.select_booking_by_train_no()

        # =============================
        # 日期
        # =============================
        time.sleep(0.3)
        actions.fill_date(ride_date)
        assert_input_value(
            driver,
            *TraTicketQueryLocators.DATE_INPUT,
            ride_date,
            "乘車日期"
        )

        # =============================
        # 車次
        # =============================
        time.sleep(0.3)
        actions.fill_train_no(train_no)
        assert_input_value(
            driver,
            *TraTicketQueryLocators.TRAIN_NO_INPUT,
            train_no,
            "車次"
        )

        print("\n✅ Smoke test completed. All asserts passed.")
        print("❗ Submit button NOT clicked.")

        # 停留讓你人工確認
        input("按 Enter 鍵關閉瀏覽器...")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
