---
layout: default
title:  臺澎dtm切割介面
parent: DTM and Relatives
grand_parent: GIS Relatives
last_modified_date: 2024-06-06 20:17:23
nav_order: 1
tags: dtm GIS
---

# 臺澎dtm切割介面
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

### 資料之選擇

- 近年來內政部20m DTM([數位地形模式][wiki] [^1])數據並沒有顯著的更新（詳[dtm檔案收集情況](./dtm_info.md)），由於2020版本DTM在苗栗地區有顯著的缺值，因此使用2018年版本。
- 解析度：雖內政部也有1m解析度的DTM，但以噪音模式動輒10～100公頃範圍，將造成計算困難。全島之總體處理與儲存也有很大的挑戰。
- 此處選擇以20m解析度尚稱合理。

### DTM的前處理

- 最花時間的步驟為直角座標系統與經緯度系統的轉換，如果每次轉換將會造成速度瓶頸。
- 轉換後的儲存格式：按照GPT的建議，以[記憶體映射](https://numpy.org/doc/stable/reference/generated/numpy.memmap.html)的方式儲存最為有效，詳見[Geotiff格式DTM之前處理](./img2mem.md)。

### 系統架構策略考量

- 前台
  - 原生的[leaflet](https://leafletjs.com/)與html搭配是最穩定、功能齊全且易於發展的方案。
  - [streamlit](https://streamlit.io/)網頁設計雖然較為簡潔，但元件不多、與js、css等還是有很大的扞格。
  - 由於等高線是專案關切主題、而不是地面資訊，此處選擇[Mapbox](https://www.mapbox.com/)的圖磚，較[內政部圖磚](https://maps.nlsc.gov.tw/T09/mapshow.action?In_type=web)、[openTopoMap](https://opentopomap.org)等來得清晰簡潔、遮蔽較少，有較高的地圖品質（雖然尚未全面中文化）。
- API伺服器
  - 此處只有傳送邊界座標(`bounds`:東北、西南經緯度座標共4個數字)、以及切割後處理好的地形圖檔(`.png`或`.dxf`[後者詳](../DXF/DXF.md))，算是單純，不考慮複雜且功能完整的API伺服器。
  - GPT建議以[Flask](https://flask.palletsprojects.com/en/3.0.x/)來撰寫最簡潔穩定，且最受歡迎。
  - Flask伺服器可以同時營運html及多個API，程式架構單純。
- 資料庫
  - 因為是格柵資料，具有很高的系統性，不需要建立關聯或非關聯資料庫與查詢系統
  - 直接以格柵檔案進行存取最有效率
  - 如需更換DTM來源，所需的轉換作業也最單純。

## 前台畫面與應用

### 服務網址

- [devp.sinotech-eng.com:5000](http://devp.sinotech-eng.com:5000)

### 進入畫面與滑鼠內設功能

- 進入伺服器後，滑鼠默認自動進入矩形圖框切割功能、選取縮放(`fitBounds`)之後，會清除前次選取圖框、並再次進入切割狀態。
  - 此狀態下可接受滾輪放大縮小、但不能接受平移(pan)
  - 如果要移動地圖，需要按`esc`鍵、或點選垃圾桶`clear all`來停止切割功能。
- 畫面如下，說明如後。

![](https://github.com/sinotec2/Utilities/blob/main/GIS/DTM/pngs/2024-06-06-17-50-49.png?raw=true)

### 功能鍵說明

1. 矩形圖框切割功能：滑鼠雖然內設具有矩形圖框切割功能，但經取消(按`esc`鍵)後，如要繼續選取，可以點選黑色白底四方形鍵再次啟動切割功能。
2. 編輯圖框與清除選取
3. 將選取結果送交等高線繪製[API程式](./app.md)，圖檔可直接與地圖等高線定性比較([詳下](#案例比較))。
   - 點選此鍵前需先按`esc`鍵取消繼續切割。
   - 點選後系統將會在主機上產生等高線[matplotlib][mtb]圖檔，同時也在客戶端下載目錄儲存一份。檔名為`terr_隨機碼.png`。
   - 高度值：選取範圍內最低到最高共9個間隔。
4. 功能與3.幾乎一樣，但為每公尺的等高線`dxf`檔
   - 檔名為`terr_隨機碼.dxf`
   - 可以用線上dxf viewer來檢視，如[sharecad.org][cad]
5. 使用手冊
   - 公司內[vuepress](https://eng06.sinotech-eng.com/v2/search-pro/zh/Terr_Cut.html)
   - 公司外[github page](https://sinotec2.github.io/Utilities/GIS/DTM/TerrCutter/)

## 案例比較

- 個案位置：屏東縣來義鄉
- mapbox切割範圍（定稿為紅色框線）

  ![](https://github.com/sinotec2/Utilities/blob/main/GIS/DTM/pngs/2024-06-06-10-27-25.png?raw=true)

- matplotlib等高線圖：最低～最高10個等級

![](https://github.com/sinotec2/Utilities/blob/main/GIS/DTM/pngs/2024-06-06-12-01-09.png?raw=true)

- dxf檔案
  - viewer:使用[sharecad.org][cad]
  - 每一公尺一層

![](https://github.com/sinotec2/Utilities/blob/main/GIS/DTM/pngs/2024-06-06-16-06-34.png?raw=true)


[^1]: "數值高程模型（DEM）或數字地表模型（DSM）是一種3D電腦圖形表示，用於表現地形資料，代表地形或覆蓋物體，通常是指行星、月球或小行星的地形。"全球DEM"指的是一個離散的全球網格。DEM在地理資訊系統（GIS）中經常被使用，並且是數字製作的地形圖最常見的基礎。數字地形模型（DTM）特指地面表面，而DEM和DSM可能代表樹頂冠層或建築物屋頂。[wiki][wiki] "

[wiki]: https://zh.wikipedia.org/zh-tw/数字地面模型 "數值高程模型（DEM）或數字地表模型（DSM）是一種3D電腦圖形表示，用於表現地形資料，代表地形或覆蓋物體，通常是指行星、月球或小行星的地形。"全球DEM"指的是一個離散的全球網格。DEM在地理資訊系統（GIS）中經常被使用，並且是數字製作的地形圖最常見的基礎。數字地形模型（DTM）特指地面表面，而DEM和DSM可能代表樹頂冠層或建築物屋頂。 (wiki)"

[mtb]: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.contour.html "matplotlib.pyplot.contour(*args, data=None, **kwargs) Plot contour lines."
[cad]: https://sharecad.org/ "sharecad.org"

