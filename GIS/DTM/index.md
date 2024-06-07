---
layout: default
title:  前端網頁的設計
parent: DTM and Relatives
grand_parent: GIS Relatives
last_modified_date: 2024-06-07 00:32:27
nav_order: 8
tags: dtm GIS
---

# 前端網頁的設計
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

- 整個專案的靈魂在於回饋使用者的地圖介面，高品質、高效率的介面是成敗關鍵。

### 目的

這個前端網頁的功能基本上是個地圖篩選器，藉由矩形圖框界定選取範圍、點選儲存icon來觸發[Flask](https://flask.palletsprojects.com/en/3.0.x/) API[程式](./app.md)，將圖檔返回儲存到使用者的下載區。

html圖面如下，內容詳[index.html](./index.html)，實例請造訪[devp.sinotech-eng.com:5000](http://devp.sinotech-eng.com:5000)。

![](./pngs/2024-06-06-17-50-49.png)

### 大略說明

這段 HTML 和 JavaScript 代碼創建了一個基於 Leaflet 的地圖應用，並且提供了五項交互功能，包括繪製矩形切割範圍、保存範圍內的數據作為 PNG 或 DXF 文件，以及打開作業手冊。以下是每個部分的簡要說明：

1. **HTML 基本結構**：
   - `<!DOCTYPE html>` 宣告文件類型。
   - `<html>` 和 `<head>` 包含標題和基本樣式設置。
   - 使用 `<meta>` 標籤設置兼容模式。
   - 引入 Leaflet、Leaflet Draw 和 Font Awesome 的樣式和腳本。

2. **樣式設置**：
   - 設置基本的樣式，包括 `.style1` 和 `.with-background`。

3. **地圖初始化**：
   - 使用 Leaflet 創建一個地圖，並設置初始視圖和圖層。

4. **繪圖控制**：
   - 初始化一個 `FeatureGroup` 來保存繪製的圖形。
   - 創建一個 `DrawControl` 來啟用繪製矩形的工具。

5. **自定義控制按鈕**：
   - 創建三個自定義按鈕，分別用於保存 PNG 文件、保存 DXF 文件和打開作業手冊。
   - 使用 `L.Control.extend` 創建自定義控制，並添加到地圖上。

6. **事件處理**：
   - 當繪製新的矩形時，清除之前的圖層，並將新的矩形添加到地圖上。
   - 當矩形繪製完成後，自動放大地圖以適應選取框範圍。

## Leaflet js設計

### 底圖的考量

- 由於等高線是專案關切主題、而不是其他地面資訊，因此不考慮[內政部圖磚](https://maps.nlsc.gov.tw/T09/mapshow.action?In_type=web)、[openStreetMap]()等，以避免等高線圖被文字遮蔽。
- 此處選擇[Mapbox](https://www.mapbox.com/)的圖磚，較、[openTopoMap](https://opentopomap.org)等來得清晰簡潔、遮蔽較少，有較高的地圖品質（雖然尚未全面中文化）。
-  

## API程式之觸發
