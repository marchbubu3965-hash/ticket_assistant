# Ticket Assistant（訂票輔助系統）

## 專案簡介
Ticket Assistant 是一套以 **Python + PySide6** 開發的桌面應用程式，  
用於協助內部人員進行火車訂票作業的**流程管理、排程與紀錄保存**。

本系統重點不在「搶票成功率」，而在於：
- 將訂票流程結構化
- 明確區分 UI、業務邏輯與資料存取
- 確保每一筆訂票請求都可追蹤、可回溯

---

## 主要功能

- 員工資料管理（含身分證驗證）
- 起訖站選擇（站碼＋中文名稱）
- 多車次訂票設定
- 支援「立即訂票」與「排程訂票」
- 完整訂票請求紀錄（非訂票結果）
- SQLite 本地資料庫，啟動時自動初始化
- 可打包為單一執行檔（PyInstaller）

---

## 系統架構說明

本專案採用明確的分層設計：

UI (PySide6)
└─ Controller（TicketController）
└─ Service（TicketService）
└─ Repository（SQLite）
└─ Domain Model（Employee）


### 各層責任劃分

- **UI**
  - 使用者互動
  - 表單輸入、資料呈現
- **Controller**
  - UI 與業務邏輯的橋接
  - 參數驗證
  - 排程控制（Qt Event Loop）
- **Service**
  - 實際訂票流程（Selenium）
  - 不處理資料庫
- **Repository**
  - 專責 SQLite 存取
  - 自動建立資料表
- **Domain**
  - 純業務規則（如 Employee 驗證）
  - 不依賴 UI / DB

---

## 使用技術

- Python 3.10+
- PySide6（Qt for Python）
- SQLite3
- Selenium（訂票流程自動化）
- PyInstaller（打包成執行檔）

---

## 專案結構

ticket-assistant/
│
├─ main.py # 程式進入點
├─ ui/ # UI 元件
├─ controller/ # Controller
├─ services/ # 業務流程
├─ repository/ # DB 存取
├─ domain/ # Domain Models
├─ db/ # DB 初始化與連線
├─ data/ # SQLite / 站點資料
└─ requirements.txt


---

## 資料庫設計（重點）

### employee
- emp_id（員工編號）
- name（姓名）
- id_number（身分證）
- department
- is_active

### ticket_request_log
- employee_id
- start_station / end_station
- ticket_count
- travel_date
- is_scheduled
- scheduled_at
- requested_at

> 所有資料表皆在程式啟動時自動初始化，避免部署環境差異問題。

---

## 執行方式（開發模式）

```bash
pip install -r requirements.txt
python main.py



##打包成執行檔（macOS)
pyinstaller \
  --name TicketAssistant \
  --onefile \
  --windowed \
  --add-data "data:./data" \
  --add-data "ui:./ui" \
  --add-data "repository:./repository" \
  --add-data "services:./services" \
  --add-data "domain:./domain" \
  --add-data "db:./db" \
  main.py
