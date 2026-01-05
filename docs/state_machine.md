# 台鐵購票流程狀態機（Human-in-the-loop）

> 本文件僅描述流程辨識與使用者操作輔助，不包含任何自動送出、付款或驗證碼處理。

---

## 流程入口

* URL: [https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query](https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query)

---

## 高階狀態流程

```text
INIT
 ↓
QUERY_PAGE
 ↓
FORM_INPUT_READY
 ↓
SEARCH_SUBMITTED
 ↓
RESULT_READY
 ↓
BOOKING_INTENT
 ↓
CONFIRM_PAGE (STOP)
```

> `CONFIRM_PAGE` 為終止狀態，系統僅提示，所有最終操作由使用者完成。

---

## 狀態定義（文字版）

### INIT

* 進入條件

  * 應用程式啟動
* 系統行為

  * 開啟瀏覽器
  * 導向購票查詢頁 URL
* 轉移條件

  * 偵測到查詢頁核心 DOM 出現 → `QUERY_PAGE`

---

### QUERY_PAGE

* 頁面特徵

  * 顯示身分證字號欄位
  * 顯示出發站 / 抵達站選擇元件
* 系統行為

  * 顯示狀態：`Query page loaded`
  * 提示使用者可開始填寫資料
* 轉移條件

  * 所有必要欄位 DOM 就緒 → `FORM_INPUT_READY`

---

### FORM_INPUT_READY

* 使用者操作（人工）

  * 輸入身分證字號
  * 選擇出發站
  * 選擇抵達站
  * 選擇行程類型（單程 / 去回）
  * 選擇訂票方式（依車次）
  * 選擇票數
  * 選擇搭乘日期
  * 輸入車次
  * 選擇座位偏好
* 系統行為

  * 顯示欄位完整度狀態（僅提示）
* 轉移條件

  * 使用者點擊「訂票」 → `SEARCH_SUBMITTED`

---

### SEARCH_SUBMITTED

* 頁面特徵

  * 查詢請求送出後，頁面進入載入狀態
* 系統行為

  * 顯示狀態：`Searching trains...`
  * 停止任何自動行為
* 轉移條件

  * 查詢結果 DOM 出現 → `RESULT_READY`

---

### RESULT_READY

* 頁面特徵

  * 顯示車次結果列表或訂票流程頁
* 系統行為

  * 顯示狀態：`Result list ready`
  * 提示使用者檢查結果
* 轉移條件

  * 使用者再次確認訂票意圖 → `BOOKING_INTENT`

---

### BOOKING_INTENT

* 頁面特徵

  * 顯示訂票確認相關資訊
* 系統行為

  * 顯示提示：`Please manually review and confirm booking`
* 轉移條件

  * 進入確認頁 DOM → `CONFIRM_PAGE`

---

### CONFIRM_PAGE（終止狀態）

* 頁面特徵

  * 出現最終訂票確認或驗證相關元素
* 系統行為

  * 顯示狀態：`Confirmation page reached`
  * 明確停止任何自動化流程

---

## 狀態機設計原則

* 僅以 DOM 狀態判斷流程位置
* 不記錄、不操作任何敏感資料
* 所有提交與確認均由使用者人工完成
* 系統僅提供狀態提示與流程引導

---

## 備註

* 若流程或 DOM 結構異動，僅需調整狀態判斷條件，不影響整體架構
* 本流程可作為其他多步驟網站的通用範本
