---
layout: default
title:  ms_mySQL.py
parent: Apache Druid Services
grand_parent: Apache Druid
last_modified_date: 2024-02-28 21:56:23
tags: DB_servers Druid
---

# ms_mySQL.py
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 背景

- [ms_mySQL.py](druid_service/ms_mySQL.py)使用 `pymssql` 连接到 MSSQL 数据库伺服器，执行查询并将结果存储到一个 Pandas DataFrame 中，最后将 DataFrame 写入 CSV 文件。
- 由於實數欄位只有一個，整數或字串又大多為重複，並沒有太過複雜，可以適度再縮減（詳[code_name.py](druid_service/code_name.md)）。

## 程式說明

以下是代码中主要部分的解释：

### 程式輸入

- `server`: 資料庫伺服器地址。
- `user`: 資料庫使用者名稱。
- `password`: 資料庫密碼。
- `database`: 資料庫名稱。
- `fname`: 輸出的 CSV 檔案名稱。

### 程式處理邏輯

1. **連接到 MSSQL 資料庫**:
    - 使用 `pymssql` 模組建立與 MSSQL 資料庫的連接。
    - 雖然有網友提議使用microsoft提供的`pyjdbc`，可以直接讀取中文碼，但嘗試了centos 7、ubuntu、16~19版，都沒有成功。

2. **執行 SQL 查詢**:
    - 使用 `cursor.execute` 執行 SQL 查詢語句，這裡執行了 `SELECT * FROM dbo.Dlist`。

3. **獲取查詢結果**:
    - 使用 `cursor.fetchall()` 獲取 SQL 查詢結果的數據。

4. **獲取表格結構**:
    - 使用 `cursor.execute` 執行 `EXEC sp_columns 'Dlist'` 查詢表格結構信息。

5. **整理查詢結果和表格結構**:
    - 將查詢結果和表格結構整理成一個字典 `dd`，其中鍵為列名，值為該列的所有數據。

6. **轉換成 DataFrame**:
    - 使用 `pandas.DataFrame` 將整理好的字典轉換為 DataFrame。

7. **寫出 CSV 檔案**:
    - 使用 `to_csv` 方法將 DataFrame 寫入 CSV 檔案。

### 程式輸出

- CSV 檔案 (`df0_111.csv`) 包含查詢結果。
- 大檔的問題：雖然轉存CSV檔並沒有縮小檔案的規模，但由於實數欄位只有一個，整數或字串又大多為重複，並沒有太過複雜，可以適度再縮減（詳[code_name.py](druid_service/code_name.md)）。


總體而言，這段程式([ms_mySQL.py](druid_service/ms_mySQL.py))的目的是將 MSSQL 資料庫中表格 `Dlist` 的內容讀取並寫入 CSV 檔案。