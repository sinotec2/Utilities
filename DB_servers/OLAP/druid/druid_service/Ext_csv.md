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

```sql
REPLACE INTO "all_yr" OVERWRITE ALL
WITH "ext" AS (
  SELECT *
  FROM TABLE(
    EXTERN(
      '{"type":"local","baseDir":"/nas2/sespub/epa/pys/","filter":"all_yr.csv"}',
      '{"type":"csv","findColumnsFromHeader":true}'
    )
  ) EXTEND ("ymdh" VARCHAR, "SO2" DOUBLE, "CO" DOUBLE, "O3" DOUBLE, "PM10" DOUBLE, "NOx" DOUBLE, "NO" DOUBLE, "NO2" DOUBLE, "THC" DOUBLE, "NMHC" DOUBLE, "WIND_SPEED" DOUBLE, "WIND_DIREC" BIGINT, "AMB_TEMP" DOUBLE, "RAINFALL" DOUBLE,"CH4" DOUBLE, "PM2.5" DOUBLE, "stn" BIGINT)
)
SELECT
  TIME_PARSE("ymdh", 'yyyy-MM-dd HH:mm:ss', 'yyyy-MM-dd HH:mm:ss') AS "__time", 
  "SO2",
  "CO",
  "O3",
  "PM10",
  "NOx",
  "NO",
  "NO2",
  "THC",
  "NMHC",
  "WIND_SPEED",
  "WIND_DIREC",
  "CH4",
  "PM2.5",
  "stn"
FROM "ext"
PARTITIONED BY MONTH
```