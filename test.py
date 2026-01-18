from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 1. 設定 Chrome 選項
chrome_options = Options()
# 讓瀏覽器在程式執行完後保持開啟
chrome_options.add_experimental_option("detach", True)

# 2. 啟動瀏覽器
driver = webdriver.Chrome(options=chrome_options)

try:
    # 3. 前往台鐵訂票網址
    url = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"
    driver.get(url)

    # 設定顯性等待，確保網頁元件已載入
    wait = WebDriverWait(driver, 10)

    # 4. 輸入身分證字號 (pid)
    time.sleep(1)
    pid_input = wait.until(EC.presence_of_element_located((By.ID, "pid")))
    pid_input.clear()
    pid_input.send_keys("G121920255")
    print("✅ 已填寫身分證字號")

    # 5. 輸入車次號碼 (trainNoList1)
    # 注意：該網頁可能有多個車次輸入框，這裡根據您的需求鎖定 ID 為 trainNoList1 的欄位
    time.sleep(1)
    train_no_input = wait.until(EC.presence_of_element_located((By.ID, "trainNoList1")))
    train_no_input.clear()
    train_no_input.send_keys("1003")
    print("✅ 已填寫車次號碼：1003")


    time.sleep(1)
    qty_input = wait.until(EC.presence_of_element_located((By.ID, "normalQty")))
    qty_input.clear()  # 清除原本的 1
    qty_input.send_keys("3")
    print("✅ 已將訂購數量修改為：3")

    print("\n🚀 程式已完成自動填寫，您可以開始後續操作。")
    print("📢 提示：若要結束程式並關閉瀏覽器，請在「終端機(Terminal)」按下 Enter 鍵。")

    # 6. 停留在該網頁，直到使用者在終端機按下 Enter
    input("\n[按下 Enter 鍵以關閉瀏覽器並結束程式...]")

except Exception as e:
    print(f"❌ 發生錯誤: {e}")

finally:
    # 關閉瀏覽器
    driver.quit()
    print("👋 程式已結束。")