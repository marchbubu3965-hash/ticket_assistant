from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from browser.page_loader import PageLoader


class BrowserManager:
    """
    Responsible for managing the browser lifecycle.

    Responsibilities:
    - Create and manage WebDriver instance
    - Open default entry page when required

    This class does NOT handle page logic or DOM interaction.
    """

    # 台鐵訂票系統預設入口
    DEFAULT_ENTRY_URL = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"

    def __init__(self, headless: bool = False):
        self.headless = headless
        self._driver = None

    def start(self, open_default_page: bool = True):
        """
        Start a Chrome browser instance.

        :param open_default_page: Whether to navigate to default entry URL after startup.
        :return: WebDriver
        """
        if self._driver is not None:
            return self._driver

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")

        self._driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        if open_default_page:
            loader = PageLoader(self._driver)
            loader.load(self.DEFAULT_ENTRY_URL)

        return self._driver

    def get_driver(self):
        """
        Return the active WebDriver instance.
        Raises an error if browser has not been started.
        """
        if self._driver is None:
            raise RuntimeError("Browser has not been started. Call start() first.")
        return self._driver

    def stop(self):
        """
        Properly close the browser and release resources.
        """
        if self._driver is not None:
            self._driver.quit()
            self._driver = None


if __name__ == "__main__":
    """
    Standalone test for BrowserManager.
    """

    browser_manager = BrowserManager(headless=False)

    try:
        driver = browser_manager.start(open_default_page=True)
        print("BrowserManager test passed: browser started and default page loaded.")
    except Exception as e:
        print("BrowserManager test failed:", e)
    finally:
        browser_manager.stop()

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager


# class BrowserManager:
#     """
#     Responsible for managing the browser lifecycle.
#     This class does NOT handle page logic or DOM interaction.
#     """

#     def __init__(self, headless: bool = False):
#         self.headless = headless
#         self._driver = None

#     def start(self):
#         """
#         Start a Chrome browser instance.
#         """
#         if self._driver is not None:
#             return self._driver

#         options = webdriver.ChromeOptions()
#         options.add_argument("--start-maximized")

#         if self.headless:
#             options.add_argument("--headless=new")
#             options.add_argument("--disable-gpu")

#         self._driver = webdriver.Chrome(
#             service=Service(ChromeDriverManager().install()),
#             options=options
#         )

#         return self._driver

#     def get_driver(self):
#         """
#         Return the active WebDriver instance.
#         Raises an error if browser has not been started.
#         """
#         if self._driver is None:
#             raise RuntimeError("Browser has not been started. Call start() first.")
#         return self._driver

#     def stop(self):
#         """
#         Properly close the browser and release resources.
#         """
#         if self._driver is not None:
#             self._driver.quit()
#             self._driver = None


# if __name__ == "__main__":
#     """
#     Standalone test for BrowserManager.
#     """

#     from browser.page_loader import PageLoader

#     TEST_URL = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"

#     browser_manager = BrowserManager(headless=False)

#     try:
#         driver = browser_manager.start()
#         loader = PageLoader(driver)
#         loader.load(TEST_URL)
#         print("BrowserManager test passed: browser started and page loaded.")
#     except Exception as e:
#         print("BrowserManager test failed:", e)
#     finally:
#         browser_manager.stop()
