---
layout: default
title: OSM檔案的拆分
grand_parent: DXF
parent: buildings
last_modified_date: 2024-12-14 17:11:55
tags: GIS DXF
---

# OSM檔案的拆分

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

- 整體建築物資料庫的整理、整併、與切割應用的工作流程如圖所示。
- 大致上整體工作區分為3大區塊。OSM資料庫的拆分屬[join_pnt_bld.py](./join.md)的前處理。

  ![alt text](./pngs/image-1.png)

- 任務說明如下：
  - 拆分taiwan.osm
  - 過濾建築物標籤
  - 區分多邊形與節點
  - 從地址中可以辨識所在縣市之篩選
  - 整合節點與多邊形

### 全台OSM數據的拆分策略

-任務說明
  - OSM檔案是個ASCII檔，按順序區分為節點(`node`)、道路(`way`含`LineString`及`Polygon`，`MuitiPolygon`)，與關聯(`relation`)等3個段落。何以可以寫成這樣不理解，猜測應該是資料庫輸出的結果。
  - 因為道路與關聯是用節點標籤來表示，如果在同一個程式內來處理檔案，會造成記憶體不足的衝擊，必須先行拆分。
- 拆分的官方建議：使用online服務（`overpass`）、QGIS、使用`osmconvert`或`ogr2ogr`等命令列工具(參考[GIS StackExchang](https://gis.stackexchange.com/questions/121652/obtaining-osm-data-within-bounds)的討論)。QGIS個人就不建議了，（猜）記憶體也會被卡死。
- 任務策略檢討說明如下
  - 0方案：不區分直接進行空間切割。好處是不必太多的前處理。壞處是必須將節點全部載入記憶體，才會讀取道路，這超過記憶體容量、且無法同步運作。不論速度與容量，似乎都不太合理。
  - 1方案：將OSM按照各個維度區分另存備用。
- 區分的維度
  - OSM數據的所有維度包括：段落、行政區、空間、與建立的時間
  - 按照段落區分：這個想法應該是比較正統、容易作業化。要資料庫容器分別儲存節點、道路及關聯的定義方式，再以資料庫程式進行關聯計算，擷取所要範圍的幾何物件。
  - 按照縣市區分：並不是所有的元件都有完整的地址，道路、relation就沒有太多的屬性信息，用縣市區分不能貫徹。
  - 按照經緯度（解析度0.5/0.1度）區分：對節點與多邊形有其可行性。

### OSM幾何物件的拆解

- 切割後的物件區分：[osm2csv_points.py](./pys/osm2csv_points.py)、 [osm2csv_buildings.py](./pys/osm2csv_buildings.py)，
- 節點會有較完整的訊息，分別按照經緯度順序編號儲存、只儲存具有`building`屬性內容的節點。
- 整併節點座標後的道路（含建物），

## [osm2csv_points.py](./pys/osm2csv_points.py)程式說明

這段程式碼的功能是從 OSM (OpenStreetMap) 檔案中提取含有完整地址的節點，並將其轉換為 CSV 格式的檔案，具體步驟如下：

### 程式結構

- 匯入必要的庫: 使用 geopandas 處理地理數據，osmium 處理 OSM 檔案，shapely 處理幾何圖形。
- 定義 OSMHandler 類別: 繼承自 osmium.SimpleHandler，用於解析 OSM 数据。
- 節點處理: 在 node 方法中，僅處理包含 “addr:full” 標籤的有效節點，並將其經緯度和標籤儲存到 self.nodes 字典中。
- 應用文件: 使用提供的 OSM 檔案名來解析數據。
- 檢查節點: 如果找不到任何節點，則退出程式。
- 創建 GeoDataFrame: 將節點數據轉換為 GeoDataFrame，並設置坐標系。
- 刪除不必要的欄位: 如果存在 ‘addr:floor’ 欄位，則將其刪除。
- 處理地址: 對於包含 “號” 的地址，修剪出完整地址。
- 去重: 刪除重複的地址，並重設索引。
- 輸出 CSV: 將結果儲存為 CSV 檔案，檔名由原 OSM 檔名轉換而來。
整體來說，此程式碼能有效地從 OSM 數據中提取地理信息並導出為可用的 CSV 格式。

### 輸入

- **OSM 檔案**: 程式接受一個 OSM 格式的檔案作為輸入，該檔案包含了 OpenStreetMap 中的地理資料，包括節點、路徑和關係等數據。
- **依賴庫**: 需要安裝 `geopandas`, `osmium`, 和 `shapely` 等 Python 庫以確保程式正常運行。

### 輸出

- **CSV 檔案**: 程式會將提取的節點數據轉換並儲存為 CSV 格式的檔案，檔名會以原 OSM 檔名為基礎進行改名，後綴為 `.pnt.csv`。

### 重要邏輯

1. **OSMHandler 類別**
   - 繼承自 `osmium.SimpleHandler`，用於處理 OSM 數據。
   - **node() 方法**: 當遇到節點時，檢查其位置是否有效，然後提取其標籤並儲存於字典中。
2. **資料篩選**: 篩選出具有完整地址的節點，並將地址格式化。
   - 透過檢查 `addr:full` 標籤來確認節點是否包含地址信息。
   - 使用字符串操作來修剪地址，去掉多餘的部分，並刪除包含 "addr:floor" 的列。
3. **去重與重設索引**: 在輸出之前，程式碼會刪除重複的地址並重設數據框的索引，以確保最終輸出的數據整潔。

### 較艱澀語法的解釋

- **`osmium.SimpleHandler`**: 是一個 OSM 數據處理的基類，提供了簡單的接口來處理 OSM 數據的各種元素（如節點、路徑等）。
- **`location.valid()`**: 檢查節點是否有有效的地理位置，這是提取地址數據的前提。
- **字典推導式**: `{tag.k: tag.v for tag in n.tags}` 用於快速生成一個字典，將標籤的鍵和值配對，簡化了傳統的迴圈方式。

### 改進建議

1. **錯誤處理**: 增加對檔案讀取和寫入過程中的錯誤處理，以提高程式的穩定性。
2. **進度顯示**: 如果處理的 OSM 檔案非常大，可以考慮增加進度條或日誌輸出，以便用戶了解處理進度。
3. **參數化**: 可以將檔案路徑和輸出格式作為命令行參數來提高靈活性，使用者可以更方便地處理不同的 OSM 檔案。
4. **更全面的數據處理**: 除了地址外，還可以考慮提取其他有用的標籤數據，並進行更深入的數據分析和視覺化。

這些改進可以使得程式更具彈性和易用性，並提升使用者體驗。

### 下載程式碼  [osm2csv_point.py](./pys/osm2csv_points.py)

{% include download.html content="建築物DXF檔之改寫[osm2csv_point.py](./pys/osm2csv_points.py)" %}

### 改進建議

1. **錯誤處理**：增加對檔案讀取和轉換過程中的錯誤處理，以防止因為格式不正確或檔案不存在而導致程序崩潰。
2. **增強輸出**：可考慮將結果存儲為 `GeoPackage` 或 `shapefile` 格式，保留地理信息。
3. **性能優化**：對於大型數據集，可以考慮使用平行處理來加快查詢速度。
4. **使用函數封裝邏輯**：將主要邏輯分為多個函數，這樣可以提高程式的可讀性和可維護性。
5. **引入日誌功能**：增加日誌功能以記錄程式運行狀態和錯誤，便於後續調試。

## 程式說明：osm2csv_buildings.py

### 輸入

- **OSM 檔案**: 程式接受一個 OSM 格式的檔案作為輸入，該檔案包含了 OpenStreetMap 中的地理資料，包括節點、路徑和關係等數據。
- **依賴庫**: 需要安裝 `geopandas`, `osmium`, 和 `shapely` 等 Python 庫以確保程式正常運行。

### 輸出

- **CSV 檔案**: 程式會將提取的節點數據轉換並儲存為 CSV 格式的檔案，檔名會以原 OSM 檔名為基礎進行改名，後綴為 `.pnt.csv`。

### 重要邏輯

1. **OSMHandler 類別**
   - 繼承自 `osmium.SimpleHandler`，用於處理 OSM 數據。
   - **node() 方法**: 當遇到節點時，檢查其位置是否有效，然後提取其標籤並儲存於字典中。
2. **資料篩選**: 篩選出具有完整地址的節點，並將地址格式化。
   - 透過檢查 `addr:full` 標籤來確認節點是否包含地址信息。
   - 使用字符串操作來修剪地址，去掉多餘的部分，並刪除包含 "addr:floor" 的列。
3. **去重與重設索引**: 在輸出之前，程式碼會刪除重複的地址並重設數據框的索引，以確保最終輸出的數據整潔。

### 較艱澀語法的解釋

- **`osmium.SimpleHandler`**: 是一個 OSM 數據處理的基類，提供了簡單的接口來處理 OSM 數據的各種元素（如節點、路徑等）。
- **`location.valid()`**: 檢查節點是否有有效的地理位置，這是提取地址數據的前提。
- **字典推導式**: `{tag.k: tag.v for tag in n.tags}` 用於快速生成一個字典，將標籤的鍵和值配對，簡化了傳統的迴圈方式。

### 改進建議

1. **錯誤處理**: 增加對檔案讀取和寫入過程中的錯誤處理，以提高程式的穩定性。
2. **進度顯示**: 如果處理的 OSM 檔案非常大，可以考慮增加進度條或日誌輸出，以便用戶了解處理進度。
3. **參數化**: 可以將檔案路徑和輸出格式作為命令行參數來提高靈活性，使用者可以更方便地處理不同的 OSM 檔案。
4. **更全面的數據處理**: 除了地址外，還可以考慮提取其他有用的標籤數據，並進行更深入的數據分析和視覺化。

這些改進可以使得程式更具彈性和易用性，並提升使用者體驗。

### 下載程式碼  [osm2csv_point.py](./pys/osm2csv_points.py)

{% include download.html content="建築物DXF檔之改寫[osm2csv_point.py](./pys/osm2csv_points.py)" %}

### 改進建議

1. **錯誤處理**：增加對檔案讀取和轉換過程中的錯誤處理，以防止因為格式不正確或檔案不存在而導致程序崩潰。
2. **增強輸出**：可考慮將結果存儲為 `GeoPackage` 或 `shapefile` 格式，保留地理信息。
3. **性能優化**：對於大型數據集，可以考慮使用平行處理來加快查詢速度。
4. **使用函數封裝邏輯**：將主要邏輯分為多個函數，這樣可以提高程式的可讀性和可維護性。
5. **引入日誌功能**：增加日誌功能以記錄程式運行狀態和錯誤，便於後續調試。

- 道路含多邊形、如何區分
  - 讀取套件不會自行判定是否為封閉曲線
