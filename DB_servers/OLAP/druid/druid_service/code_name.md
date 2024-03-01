---
layout: default
title:  code_name.py
parent: Apache Druid
grand_parent: DB_servers
grand_parent: OLAP
last_modified_date: 2024-02-28 21:56:31
tags: DB_servers Druid
---

# code_name.py
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

- 環境部事業廢棄物資料庫為microsoft SQL檔案，經[轉檔成為 CSV檔案](./ms_mySQL.md)後，此處進一步加工。
- [code_name.py](./code_name.py)這支程式的主要功能包括找到代碼與名稱的對照表、調整列名、修正代碼、校正中文編碼，並將處理後的資料，經修剪、存留代碼與名稱、重新寫入 CSV 檔案、並儲存各個對照表。 以下是程式碼中各部分的詳細解釋：

## 程序輸入、輸出

### 輸入

- `fname`: 由microsoft SQL伺服器轉檔後的 CSV 檔名。

### 程式輸出

- 對應處理後的 CSV 檔案。
- 對應列名的對照表 CSV 檔案。

## 程式處理邏輯

### 「代碼」對應到「名稱」的字典

**讀取 CSV 檔案並產生代碼——名稱對照表**。2021年版本共有15組、2022年版本只有10組。

- 讀取 CSV 檔案 `df0`。
- 取得原始列名 `cols`。
- 找出以「名稱」結尾的列和以「管編」或「代碼」結尾的列，然後分別排序。
- 建立 `code_name` 字典，將「代碼」對應到「名稱」。

### 中文碼之修正

**修正代碼成為字符**:

- 將特定列中工業區代碼整數 99 替換為字串 '99 '。

**中文碼校正**:

- 對特定列進行中文編碼的校正。
- 偵測中文編碼，如果不是 'latin1' 編碼，則跳過。`if chardet.detect(a[0].encode())['encoding'] != 'latin1':continue`
- 使用 'latin1' 編碼將中文編碼轉換成 'big5'，並忽略錯誤。
- 校正範圍
  - `code_name` 字典中的值，「...名稱」
  - 沒有代碼的變數：`['縣市別','申報途徑','廢棄物種類(一般&有害)']`

### 一一輸出各組對照表

1. **寫出處理後的 CSV 檔案**:

- 將處理後的 DataFrame (`df0`) 覆蓋原始檔案。

2. **產生對照表**:

- 產生 `fnames` 列表，其中包含需要產生對照表的列名。
  - `fnames`來源：將`code_name` 字典中的值，「...名稱」貼到google translate所得之英文翻譯。

項次|中文|英文
-|-|-
1||BusinessOrganizationName
2||RecyclingOrganizationName
3||IndustrialAreaName
4||WasteName
5||FinalDisposalAgencyName
6||ChineseNameCleaningMethod
7||ClearOrganizationName
8||ProcessingOrganizationName
9||IndustryChineseName
10||ProcessChineseName

- 對每個列進行如下處理：
  - 選取指定列和對應的名稱列。
  - 移除缺失值，排序，移除重複值。
  - 將列名改為 `['key', 'value']`。
  - 寫出對照表到以列名為名稱的 CSV 檔案中。

1. 英文檔名、英文欄位名稱的理由：druid雖然可以解析，但不穩定。不利系統更新緩存。