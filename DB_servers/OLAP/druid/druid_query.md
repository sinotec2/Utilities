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

## 背景

### apache druid伺服器

1. 打開Druid伺服器介面
2. 目前尚未設定帳密系統。注意不要更動到資料庫(僅執行查詢功能)。

> http://200.200.32.195:8888/

3. 按下查詢(Query)

![](2024-01-29-13-19-28.png)

4. 左方出現資料表各個欄位
   1. A為文字屬性(可群組、可篩選)
   2. 123為整數(可群組、可篩選)
   3. 1.0 為實數(注意不要進行群組化)

![](2024-01-29-13-22-55.png)

5. 中間上方為程式碼
   1. 可以用自然語言在GPT上詢問
   2. 提示：我會給你一段自然語言，請給我SQL程式碼。
   3. 按下`+`開啟新的tab，貼上SQL程式碼，按下`Run`即可跑出結果。
6. 按下右方下載按鍵，將結果另存新檔。

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
  "總申報量" DESC;
```

### 過濾、群組、加總

> 我想了解資料表df0_clean中、"事業機構管編"為'L0200473'、各項"廢棄物代碼"的"申報量"加總結果，加總結果取到小數點以下2位，按照加總結果大小反向排序

```sql
SELECT
  廢棄物代碼,
  SUM(申報量) AS sum_申報量
FROM df0_clean
WHERE 事業機構管編 = 'L0200473'
GROUP BY 廢棄物代碼
ORDER BY sum_申報量 DESC
```
