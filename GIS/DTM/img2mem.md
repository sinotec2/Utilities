---
layout: default
title:  geotiff格式DTM之前處理
parent: DTM and Relatives
grand_parent: GIS Relatives
last_modified_date: 2024-06-06 20:17:23
tags: dtm GIS
---

# Geotiff格式DTM之前處理
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

### 前處理目標與必要性

- 直角座標數位[高程模型資訊](./dtm_info.md)格柵檔案的處理並不困難，但是因為格點數量龐大，座標轉換會花很多時間，如果每一次處理都要轉換，將會造成瓶頸。
- GeoTiff格式檔案並未儲存每個格點的經緯度或TWD97座標，後者還可以線型計算，前者則需轉換，計算過程需時較久，偏偏一般地圖裁切介面都是使用經緯度座標系統。

### 座標轉換的精確性

- 直角座標系統轉經緯度一般採取Lambert轉換，轉換的精準度與南北割線緯度(true latitude)有關，一般範例以10/40度為基準，轉換將會比實際略為偏南。
- 此處以臺灣本島的最南與最北端緯度代入，來降低轉換的誤差。

### 輸出檔案格式與讀寫的有效性

- 作為大型矩陣切割(過濾)的方式，可以用pandas.DataFrame篩選，也可以用`np.where`線性化篩選。然前者將會儲存成十數G的csv，而後者分開以二進位檔案儲存，將可大量壓縮暫存檔案的容量。
- 全島GeoTiff檔案經壓縮約為500MB、解開後地形檔、格點中心座標（lat、lon）三個2D陣列合計約為2GB。讀寫、篩選都較DataFrame有效率。

## 程式說明

這段程式碼使用 Python 中的 `rasterio` 和 `pyproj` 庫來處理地理空間數據，具體操作如下：

### 輸入與翻轉

1. **讀取 GeoTIFF 文件**：
    - 使用 `rasterio.open` 打開名為 `taiwan2018.tif` 的 GeoTIFF 文件。
    - 獲取影像的寬度、高度和波段數。

2. **讀取影像數據並翻轉**：
    - 使用 `img.read()[0,:,:]` 讀取第一個波段的數據，
    - 並使用 `np.flipud` 進行南北方向數據的翻轉（upside down）。

### 座標轉換

1. **獲取地理坐標及影像的變換參數**：
    - 使用 `img.xy(0,0)` 獲取影像左上角的地理坐標。
    - 獲取影像的變換參數 `transform`，其中包括像元大小 `dx` 和 `dy`（取絕對值）。
    - 計算影像的南北座標y值範圍。

2. **計算影像像元的地理坐標**：
    - 創建 x 和 y 座標的 numpy 陣列。
    - 將 x 和 y 座標中心化。
    - 使用 `np.meshgrid` 創建2維網格點每一點中心的TWD97座標值。

3. **定義投影和轉換地理坐標**：
    - 設置投影參數（這裡使用了 Lambert Conformal Conic 投影）。
    - 使用 `pnyc` 將網格點轉換為經緯度。

### 儲存檔案

1. 將地理資訊參數（包括原點坐標、影像尺寸和像元大小）保存到 `params.txt` 文件。
2. **將數據保存到文件**：
    - 將影像數據、經度和緯度數據保存為 `.dat` 文件。

## 程式碼附加說明

- 以下是完整的代碼與代碼分段說明：

### 輸入與基本設定

```python
import rasterio
import numpy as np
from pyproj import Proj

# 打開 GeoTIFF 文件
fname = 'taiwan2018.tif'
img = rasterio.open(fname)

# 獲取影像寬度、高度和波段數
nx, ny, nz = img.width, img.height, img.count
```

### 翻轉南北方向

- GeoTiff

```python
# 讀取影像數據並翻轉
data = np.flipud(img.read()[0,:,:])

# 獲取影像左上角的地理坐標
x0, y0 = img.xy(0, 0)

# 獲取影像的變換參數
transform = img.transform
dx, dy = transform.a, abs(transform.e)

# 計算影像的 y 座標範圍
y0 = y0 - dy * ny

# 創建 x 和 y 座標的 numpy 陣列
x = np.array([x0 + dx * i for i in range(nx)])
y = np.array([y0 + dy * i for i in range(ny)])

# 將 x 和 y 座標中心化
xcent, ycent = x[nx // 2], y[ny // 2]
x -= xcent
y -= ycent

# 使用 np.meshgrid 創建網格點
xg, yg = np.meshgrid(x, y)
```

### 座標轉換

```python
# 定義投影參數
Longitude_Pole, Latitude_Pole = img.lnglat()
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=21.8, lat_2=25.4,
            lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)

# 將網格點轉換為經緯度
lon, lat = pnyc(xg, yg, inverse=True)
```

### 儲存2維陣列

- 直角座標之數值，雖會被運用在後續等高線的計算，但屬線性計算，速度很快，因此就不儲存了。
- 按照GPT建議，以[記憶體映射](https://numpy.org/doc/stable/reference/generated/numpy.memmap.html)方式之二進位檔案存取最有效率。
- 儲存方式，先將陣列記憶體與檔案連在一起。直接將數據上傳到記憶體，就會儲存到檔案了，沒有（不需要）`write`指令。

```python
# 定義數據形狀
shape = (ny, nx)

# 保存數據到 .dat 文件
fnames = ['data', 'lon', 'lat']
arrays = [data, lon, lat]
for f in range(3):
    filename = fnames[f] + '.dat'
    memmap_array = np.memmap(filename, dtype='float32', mode='w+', shape=shape)
    memmap_array[:] = arrays[f][:,:]

# 保存參數到 params.txt 文件
params_str = f"{x0} {y0} {nx} {ny} {dx} {dy}\n"
with open('params.txt', 'w+') as f:
    f.write(params_str)
```

這段代碼將讀取 GeoTIFF 文件中的數據，將其轉換為經緯度，並將結果保存為 .dat 文件和一個參數文件。您可以根據需要進一步處理或可視化這些數據。

## 程式下載

{% include download.html content="[img2mem.py](./img2mem.py)" %}