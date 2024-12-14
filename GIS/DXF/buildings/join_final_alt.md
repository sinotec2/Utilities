---
layout: default
title:  join_final_alt.py
grand_parent: DXF
parent: buildings
last_modified_date: 2024-12-08 16:24:44
tags: GIS DXF
---

# OSM建築物與內政部資訊的整併（join_final_alt.py）

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

- 建築物資料庫的整理、整併、與切割應用的工作流程如圖所示。
- 大致上整體工作區分為3大區塊，`join_pnt_bld.py`的範圍與功能，為最終整併成`buildings.csv`的重要程序。

  ![alt text](./pngs/image-1.png)

### 程式說明

這個程式使用 `geopandas`、`rtree` 和 `shapely` 來處理地理空間數據。它的主要功能是將點（points）與多邊形（polygons）進行空間查詢，找出哪些點位於哪些多邊形內，並將結果寫入 CSV 檔案。

### 輸入

程式接受兩個命令列參數，這兩個參數是 GeoDataFrame 檔案的路徑：
1
. 第一個檔案：包含節點的 GeoDataFrame。
2. 第二個檔案：包含多邊形的 GeoDataFrame。

### 輸出

程式將生成兩個 CSV 檔案：

1. 第一個檔案：包含匹配的點與多邊形的資料。這個索引的表格是用來檢核結果的正確性，並沒有後續應用的必要性。
2. 第二個檔案：包含最終的多邊形與對應的地址資料。命名原則：`final_pnt_bld.csv` (`'final'+sys.argv[1]+sys.argv[2]`)

### 重要邏輯

1. **讀取 GeoDataFrames**：
   使用 `gpd.read_file()` 讀取點和多邊形資料。
2. **幾何數據轉換**：
   將 GeoDataFrame 中的幾何列從字符串格式轉換為 Shapely 對象，以便進行空間運算。
3. **創建 Rtree 索引**：
   使用 `rtree` 包來創建一個 Rtree 索引，以加速空間查詢。
4. **查詢 Rtree 索引**：
   對每個點，查詢 Rtree 索引以找出可能的多邊形，然後檢查這些多邊形是否包含該點。
5. **生成結果 GeoDataFrame**：
   將匹配的點和多邊形的索引以及幾何資料存儲到一個新的 GeoDataFrame 中。
6. **寫入 CSV**：
   將結果 GeoDataFrame 輸出為 CSV 檔案。

### 艱澀語法的解釋

- `apply(loads)`：這行代碼將 `loads` 函數應用到幾何列的每一個元素，將其從 WKT（Well-Known Text）格式轉換為 Shapely 幾何對象，這樣可以進行空間運算。  
- `idx.insert(i, geometry.bounds)`：這行代碼將多邊形的邊界（bounds）插入到 Rtree 索引中，以便後續進行快速查詢。
- `idx.intersection(point.bounds)`：這行代碼查詢 Rtree 索引，返回與給定點邊界相交的所有多邊形的索引。

## TODO's

### 下載程式碼 [join_pnt_bld.py](./pys/join_pnt_bld.py)

{% include download.html content="建築物DXF檔之改寫[bld2dxf.py](./pys/join_pnt_bld.py)" %}

### 改進建議

1. **錯誤處理**：增加對檔案讀取和轉換過程中的錯誤處理，以防止因為格式不正確或檔案不存在而導致程序崩潰。
2. **增強輸出**：可考慮將結果存儲為 `GeoPackage` 或 `shapefile` 格式，保留地理信息。
3. **性能優化**：對於大型數據集，可以考慮使用平行處理來加快查詢速度。
4. **使用函數封裝邏輯**：將主要邏輯分為多個函數，這樣可以提高程式的可讀性和可維護性。
5. **引入日誌功能**：增加日誌功能以記錄程式運行狀態和錯誤，便於後續調試。
