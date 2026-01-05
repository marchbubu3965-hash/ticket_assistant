from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class DomWatcher:
    """
    負責監控與等待頁面 DOM 狀態的工具類別
    """

    def __init__(self, driver, timeout: int = 15):
        """
        :param driver: selenium webdriver instance
        :param timeout: 預設等待秒數
        """
        self.driver = driver
        self.timeout = timeout

    def wait_for_presence(self, by: By, value: str):
        """
        等待元素出現在 DOM 中（不保證可點擊）
        """
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def wait_for_visible(self, by: By, value: str):
        """
        等待元素出現在畫面中（可見）
        """
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located((by, value))
        )

    def wait_for_clickable(self, by: By, value: str):
        """
        等待元素可被點擊
        """
        return WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    def exists(self, by: By, value: str) -> bool:
        """
        檢查元素是否存在（不丟例外）
        """
        try:
            WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False
