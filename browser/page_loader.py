from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class PageLoadError(RuntimeError):
    """Raised when target page fails to load correctly."""


class PageLoader:
    """
    Responsible for loading a page and determining when it is ready for interaction.

    Responsibilities:
    - Navigate to target URL
    - Verify page identity
    - Ensure page is ready for user interaction

    This class does NOT manage browser lifecycle.
    """

    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.timeout = timeout

    def load(self, url: str) -> None:
        """
        Navigate to the given URL and wait until the page is ready.
        """
        self.driver.get(url)
        self._wait_until_ready()

    def _wait_until_ready(self) -> None:
        """
        Wait until the TRA booking page is fully loaded and interactive.

        Ready conditions:
        1. Correct page identity (URL & title)
        2. Presence of submit button ("訂票")
        """
        try:
            wait = WebDriverWait(self.driver, self.timeout)

            # 1️⃣ 確認仍在台鐵訂票系統頁面
            wait.until(lambda d: "railway.gov.tw" in d.current_url)

            # 2️⃣ 確認訂票按鈕存在（主要互動元素）
            wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//input[@type='submit' and @value='訂票']"
                    )
                )
            )

        except TimeoutException as e:
            raise PageLoadError(
                f"TRA booking page failed to load within {self.timeout} seconds. "
                f"Current URL: {self.driver.current_url}"
            ) from e


if __name__ == "__main__":
    """
    Standalone test for PageLoader.
    This block is for development verification only.
    """

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    TEST_URL = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        loader = PageLoader(driver)
        loader.load(TEST_URL)
        print("PageLoader test passed: page is ready.")
    except Exception as e:
        print("PageLoader test failed:", e)
    finally:
        driver.quit()

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


# class PageLoader:
#     """
#     Responsible for loading a page and determining when it is ready for interaction.
#     This class does NOT manage browser lifecycle.
#     """

#     def __init__(self, driver, timeout: int = 15):
#         self.driver = driver
#         self.timeout = timeout

#     def load(self, url: str) -> None:
#         """
#         Navigate to the given URL and wait until the page is ready.
#         """
#         self.driver.get(url)
#         self._wait_until_ready()

#     def _wait_until_ready(self) -> None:
#         """
#         Wait until the TRA booking page is fully loaded and interactive.

#         Ready condition:
#         - Presence of the submit button:
#           <input type="submit" class="btn btn-3d" value="訂票">
#         """
#         WebDriverWait(self.driver, self.timeout).until(
#             EC.presence_of_element_located(
#                 (
#                     By.XPATH,
#                     "//input[@type='submit' and contains(@class, 'btn-3d') and @value='訂票']"
#                 )
#             )
#         )


# if __name__ == "__main__":
#     """
#     Standalone test for PageLoader.
#     This block is for development verification only.
#     """

#     from selenium import webdriver
#     from selenium.webdriver.chrome.service import Service
#     from webdriver_manager.chrome import ChromeDriverManager

#     TEST_URL = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"

#     options = webdriver.ChromeOptions()
#     options.add_argument("--start-maximized")

#     driver = webdriver.Chrome(
#         service=Service(ChromeDriverManager().install()),
#         options=options
#     )

#     try:
#         loader = PageLoader(driver)
#         loader.load(TEST_URL)
#         print("PageLoader test passed: page is ready.")
#     except Exception as e:
#         print("PageLoader test failed:", e)
#     finally:
#         driver.quit()
