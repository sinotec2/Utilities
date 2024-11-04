---
layout: default
title:  大型數據之讀取範例
parent: Apache Druid Services
grand_parent: Apache Druid
last_modified_date: 2024-11-03 12:21:53
tags: DB_servers Druid
---

# 大型數據之讀取範例
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

## 環境部空氣品質數據之讀取範例

### 時間標籤

- `ymdh`10碼整數，在轉換的時候會出現困難，還是以`VARCHAR`型態輸入druid比較保險。
- 也可以在`python`階段就將時間戳準備好，也可以不必，在druid sql階段轉換也行。
- 10碼`ymdh`轉時間戳：

```python
df.ymdh=[pd.Timestamp(
  year=int(datetime_str[:4]),
  month=int(datetime_str[4:6]),
  day=int(datetime_str[6:8]),
  hour=int(datetime_str[8:10])
  ) 
  for datetime_str in df.ymdh]
df.to_csv('all_yr.csv', date_format='%Y-%m-%d %H:%M:%S', index=False) #(此舉似乎沒有太大幫助)
```

### 刪除過多無效值的欄位

- THC/NMHC雖然只有部分測站有此測值，至少還有56%的有效值，因此設定超過8成以上都是無效值的欄位，予以刪除。

```python
In [28]: for c in df.columns:
    ...:     nan=df[c].isna().sum()
    ...:     if nan/n > 0.8:
    ...:         print(c)
    ...:         del df[c]
    ...:
SIGMA
WD_GLOBAL
DEW_POINT
SHELT_TEMP
PRESSURE
GLIB_RADIA
UBV_RADIA
NET_RADIA
PH_RAIN
RAIN_COND
RAIN_INT
UVB
UBA
```

- 結果檔頭

```python
In [33]: df.columns
Out[33]:
Index(['ymdh', 'SO2', 'CO', 'O3', 'PM10', 'NOx', 'NO', 'NO2', 'THC', 'NMHC',
       'WIND_SPEED', 'WIND_DIREC', 'AMB_TEMP', 'RAINFALL', 'CH4', 'PM2.5',
       'stn'],
      dtype='object')
```

### 讀取SQL

- 雖然風向和站碼都是整數，但是csv存成實數，如果SQL中讀成整數(`BIGINT`)會出現錯誤，**必須**維持`DOUBLE`。
- 時間戳的解析
  - str to timestamp：官網建議使用`TIME_FORMAT()`，實際上是不可行的，可能是版本的問題。**必須**使用`TIME_PARSE()`
  - bigint to timestamp：`MILLIS_TO_TIMESTAMP(“ymdh” * 1000) AS “__time”, `語法正確，但不能執行。
- 時間的切割(`PARTITION`)：似乎與儲存有關、與後續的granulate不同，druid內設最多5000個除存桶，所以不能太細(日、時皆不可行)。

```sql
REPLACE INTO "all_yr" OVERWRITE ALL
WITH "ext" AS (
  SELECT *
  FROM TABLE(
    EXTERN(
      '{"type":"local","baseDir":"/nas2/sespub/epa/pys/","filter":"all_yr.csv"}',
      '{"type":"csv","findColumnsFromHeader":true}'
    )
  ) EXTEND ("ymdh" VARCHAR, "SO2" DOUBLE, "CO" DOUBLE, "O3" DOUBLE, "PM10" DOUBLE, 
  "NOx" DOUBLE, "NO" DOUBLE, "NO2" DOUBLE, "THC" DOUBLE, "NMHC" DOUBLE, "WIND_SPEED" DOUBLE, "WIND_DIREC" DOUBLE, "AMB_TEMP" DOUBLE, "RAINFALL" DOUBLE, 
  "CH4" DOUBLE, "PM2.5" DOUBLE, "stn" DOUBLE)
)
SELECT
  TIME_PARSE("ymdh", 'yyyy-MM-dd HH:mm:ss', 'yyyy-MM-dd HH:mm:ss') AS "__time", 
  "SO2",  "CO",  "O3",  "PM10",  "NOx",  "NO",  "NO2",
  "THC",  "NMHC",  "WIND_SPEED",  "WIND_DIREC",
  "CH4",  "PM2.5",  "stn"
FROM "ext"
PARTITIONED BY MONTH
```

## AnythingLLM對話紀錄數據之讀取

- 這是每個月都要進行簡報的作業過程

```SQL
REPLACE INTO "avgWC_dpt" OVERWRITE ALL
WITH "ext" AS (
  SELECT *
  FROM TABLE(
    EXTERN(
      '{"type":"local","filter":"avgWC_dpt.csv","baseDir":"/nas2/kuang/MyPrograms/query_anything"}',
      '{"type":"csv","findColumnsFromHeader":true}'
    )
  ) EXTEND ("DeptName" VARCHAR, "avg_wc" DOUBLE)
)
SELECT
  "DeptName",
  "avg_wc"
FROM "ext"
PARTITIONED BY ALL
```
