# Database Schema

> 本資料庫設計用於半自動購票輔助工具（Human-in-the-loop），
> 僅作為身分資料參照與流程輔助，不儲存任何可直接使用之敏感個資。

---

## Database

* Engine: SQLite 3
* Scope: Local only (single-user desktop application)
* File example: `data/app.db`

---

## Table: employees

### Description

儲存員工基本識別資訊，用於購票流程中快速選擇與人工驗證。

---

### Columns

| Column Name  | Type     | Constraints                | Description                |
| ------------ | -------- | -------------------------- | -------------------------- |
| id           | INTEGER  | PRIMARY KEY, AUTOINCREMENT | Internal unique identifier |
| display_name | TEXT     | NOT NULL                   | 顯示名稱（姓名或代稱）                |
| id_hash      | TEXT     | NOT NULL, UNIQUE           | 身分證字號雜湊值（不可逆）              |
| id_last4     | TEXT     | NOT NULL                   | 身分證字號末四碼（僅供人工確認）           |
| note         | TEXT     | NULL                       | 備註（部門、梯次、說明）               |
| created_at   | DATETIME | NOT NULL                   | 建立時間                       |
| updated_at   | DATETIME | NOT NULL                   | 更新時間                       |

---

### Indexes

| Index Name            | Columns      | Purpose  |
| --------------------- | ------------ | -------- |
| idx_employees_name    | display_name | 快速搜尋顯示名稱 |
| idx_employees_id_hash | id_hash      | 驗證身分證一致性 |

---

### Security Considerations

* 不儲存完整身分證字號（raw value）
* 僅儲存不可逆雜湊值（hash）作為比對依據
* 身分證字號僅於執行期間存在於記憶體中
* 資料庫檔案不納入版本控制（git ignore）

---

## Table: booking_profiles (Optional)

> 此表為擴充用途，非必要，可於後續階段實作。

### Description

儲存常用訂票偏好設定，以加速人工操作流程。

---

### Columns

| Column Name | Type     | Constraints                | Description        |
| ----------- | -------- | -------------------------- | ------------------ |
| id          | INTEGER  | PRIMARY KEY, AUTOINCREMENT | Profile identifier |
| name        | TEXT     | NOT NULL                   | 設定檔名稱              |
| trip_type   | TEXT     | NOT NULL                   | 單程 / 去回            |
| seat_pref   | TEXT     | NULL                       | 座位偏好               |
| note        | TEXT     | NULL                       | 備註                 |
| created_at  | DATETIME | NOT NULL                   | 建立時間               |
| updated_at  | DATETIME | NOT NULL                   | 更新時間               |

---

## Relationship Overview

```text
employees
    │
    └── (future) booking_profiles
```

---

## Migration Policy

* Schema versioning 以應用程式版本控管
* 初期不導入自動 migration
* 若 schema 調整，建立新資料庫檔案

---

## Notes

* 本 schema 設計可直接延伸至其他多身分輸入型網站
* 若未來改為 client-server 架構，需重新評估加密與存取控制策略
