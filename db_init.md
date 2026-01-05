# Database Initialization Flow

> 本文件定義本地 SQLite 資料庫的建立、載入與生命週期管理方式。
> 目標為確保資料一致性、可維護性，以及與 UI / 流程狀態機的清楚分離。

---

## Initialization Timing

### Application Startup

```text
APP_START
  ↓
CHECK_DB_EXISTS
  ├── Yes → LOAD_DB
  └── No  → CREATE_DB → APPLY_SCHEMA → LOAD_DB
```

* 資料庫僅於應用程式啟動時初始化一次
* 初始化流程不可由 UI 任意觸發

---

## Database Location Policy

* 預設路徑（範例）：

```text
data/app.db
```

* 規則：

  * 僅限本機存取
  * 不支援網路同步
  * 不納入 Git 版控

---

## Schema Application Strategy

### First Run Only

* 僅在資料庫不存在時：

  * 建立資料庫檔案
  * 套用完整 schema（見 `db_schema.md`）

### Subsequent Runs

* 不重新套用 schema
* 不進行自動 migration

---

## Schema Version Handling

* Schema 版本由應用程式版本隱含管理
* 不維護獨立 schema_version table
* 若 schema 變更：

  * 建立新資料庫檔案
  * 由使用者自行重新輸入資料

---

## Data Integrity Rules

* 所有寫入操作必須：

  * 使用交易（transaction）
  * 成功才 commit，否則 rollback

* 禁止：

  * UI 直接操作 SQL
  * 未驗證資料寫入 DB

---

## Security Constraints

* 不允許：

  * 將完整身分證字號寫入 DB
  * 將身分證字號寫入 log

* 僅允許：

  * hash 與末四碼進入資料庫

---

## Failure Handling

### Database File Corrupted

* 行為：

  * 停止應用程式啟動
  * 顯示錯誤提示
  * 不嘗試自動修復

### Schema Mismatch

* 行為：

  * 視為不支援版本
  * 要求重新建立資料庫

---

## Logging Policy

* 僅記錄：

  * 初始化成功 / 失敗
  * DB 檔案路徑

* 不記錄：

  * SQL 明文
  * 任何身分相關欄位內容

---

## Summary

* DB 初始化流程僅發生於啟動階段
* Schema 套用具備一次性與不可逆性
* 明確區分 DB、UI、流程控制責任

本文件作為資料層設計依據，後續所有實作須遵循此規範。
