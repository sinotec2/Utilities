---
layout: default
title:  Druid查詢範例
parent: Apache Druid
grand_parent: DB_servers
grand_parent: OLAP
last_modified_date: 2024-01-29 12:57:32
tags: DB_servers Druid
---

# Druid查詢範例
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

## 快速啟動

### apache druid伺服器

- 打開Druid伺服器介面
- 目前尚未設定帳密系統。注意不要更動到資料庫(僅執行查詢功能)。

> http://200.200.32.195:8888/

- 按下查詢(Query)

![](2024-01-29-13-19-28.png)

- 左方出現**資料表**(如`df0_clean`及`wikipedia`)、與資料表的各個欄位。有3種前綴：
1. **A** 為文字屬性
2. **123** 為整數
3. **1.0** 為實數

- 點擊欄位後，可進行簡易樞紐分析(會與**程式碼輸入板**連動)
1. 顯示(Show)：如無其他條件，則為計數(count)。 如有其他條件，則會增添至被選項目 
2. 篩選(Filter)：文字、整數、實數(all)
3. 群組(Group by)：文字、整數
4. 聚合(Aggregate)：計數(文字)、大小、加總、平均、近似分位數(整、實數)、最新(all)
5. 複製(Copy)：複製欄位名稱到剪貼簿，以便在**程式碼輸入板**內編輯使用

![](2024-01-30-09-07-50.png)

- 中間上方為**程式碼輸入板**
   1. 按下`+`開啟新的tab，
   2. 貼上SQL程式碼、或執行欄位右鍵選項
   3. 按下`Run`即可跑出結果。

![](2024-01-29-13-22-55.png)

- 可以用自然語言在GPT上詢問
- 按下右方下載按鍵，將結果另存新檔。

### 計數

1. 在**程式碼輸入板**上方點擊`+`，出現空白輸入板、等候輸入查詢程式指令
2. 點擊`事業機構管編`欄位名稱，出現選項
3. 點擊顯示(Show)：會在**程式碼輸入板**出現程式碼
4. 程式碼中的 `1`、`2`即為`SELECT`被選項目之順位、以1起算。

```sql
SELECT
  "事業機構管編",
  COUNT(*) AS "Count"
FROM "df0_clean"
GROUP BY 1
ORDER BY 2 DESC
```

![](2024-01-30-09-41-35.png)

- 檢視程式碼、孰悉其意義、以利自然語言對話。
- 點擊`Run`，即在下方結果看板出現**事業機構管編**群組的計數
- 按看板下方的`< >`鍵，可翻看結果

![](2024-01-30-10-09-47.png)

## 查詢範例

### 群組加總

> 加總資料表df0_clean中"申報途徑"各種樣態的"申報量"，加總結果取到小數點以下2位，按照加總結果大小反向排序

```sql
SELECT
  "申報途徑",
  ROUND(SUM("申報量"), 2) AS "總申報量"
FROM
  "df0_clean"
GROUP BY
  "申報途徑"
ORDER BY
  "總申報量" DESC
```

- 注意：druid不接受一般SQL語言之結尾標示(分號`;`)。

### 過濾、群組、加總

> 我想了解資料表df0_clean中、"事業機構管編"為'L02**473'、各項"廢棄物代碼"的"申報量"加總結果，加總結果取到小數點以下2位，按照加總結果大小反向排序

```sql
SELECT
  廢棄物代碼,
  SUM(申報量) AS sum_申報量
FROM df0_clean
WHERE 事業機構管編 = 'L02**473'
GROUP BY 廢棄物代碼
ORDER BY sum_申報量 DESC
```

- druid沒有外卡(wild card `*`之設定)

### 3個維度的樞紐分析

- `SELECT`項目
  1. `事業機構管編`：維度1
  2. `申報途徑`：維度2
  3. `sum_申報量`：維度3

```sql
SELECT
  "事業機構管編", "申報途徑",
  round(SUM("申報量"),2) AS "sum_申報量"
FROM "df0_clean"
GROUP BY 1,2
ORDER BY 3 DESC
```

- 注意：不指定排序方式即維正向排序，如`ORDER BY 1`。