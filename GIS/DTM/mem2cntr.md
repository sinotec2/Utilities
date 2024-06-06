---
layout: default
title:  DTM等值線圖的產生
parent: DTM and Relatives
grand_parent: GIS Relatives
last_modified_date: 2024-06-06 20:17:23
tags: dtm GIS
---

# DTM等值線圖的產生
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

- 等高線dxf圖檔事實上是`matplotlib.pyplot.contour`過程的中間產物，由每條折線上的逐點座標所組成，一般程式設計者是不會需要知道每條等高線上的詳細座標的。
- 除了最終成果的控制目的之外，視覺化驗證也是本項工作一個很重要的理由。
- 處理好的龐大矩陣，也需要藉由本程式來測試看看讀取、篩選過程的工作效率到底怎樣、是否還需要進一步優化。
- 這支程式有函式及獨立運作等2個版本。
  - 函式型態，可以在API伺服器者、或其他程式場合呼叫
  - 獨立運作，雖然需要手動輸入圖框邊界座標，但還算是一個滿方便順手的工具。

## 程式說明

這段程式碼讀取存儲在 `.dat` 文件中的經緯度和數據，並根據給定的地理界限生成等高線圖，最終保存為 PNG 文件。它使用了 `matplotlib` 庫來繪製圖形，並使用 `tempfile` 來生成臨時文件名。以下是代碼的詳細解釋：

### 匯入必要的庫

- `numpy` 用於數據處理。
- `matplotlib` 用於繪圖。
- `tempfile` 和 `BytesIO` 用於處理臨時文件和內存中的文件。

### 讀取數據文件

- `rd_mem` 函數讀取經緯度和DTM數據的 `.dat` 文件，返回一個包含這3項數據的序列。
- 使用[記憶體映射](https://numpy.org/doc/stable/reference/generated/numpy.memmap.html)的方式讀取
  - 定義矩陣形狀與讀取檔案同一個指令完成
  - 副程式無法執行`exec()`指令，GPT建議使用`dict`或`list`方式依序讀取、回應呼叫的程式。

### 生成等高線圖

- 雖然等高線圖不是本次專案的目標，但是因為DXF檔案檢視不易，DTM數據量又很大，需要有效率的工具來進行過程驗證。
- `cntr` 函數根據圖框給定的地理邊界 `swLL`（西南角）和 `neLL`（東北角），在數據中以`np.where()`篩選符合條件的經緯度索引(`idx`)。
- 如果沒有找到符合條件的數據，返回錯誤信息。
- 根據找到的經緯度索引、計算繪圖的直角座標(TWD97)範圍、以及等高線圖的級別（9個層級共10條等高線）。
- 使用 `matplotlib` 繪製等高線圖，並保存為 PNG 文件。

### 程式碼

以下是完整的代碼：

```python
# 匯入必要的庫
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 使用 Agg 后端
import matplotlib.pyplot as plt
import tempfile as tf
from io import BytesIO

# 讀取數據文件
def rd_mem(shape):
    fnames = ['lat', 'lon', 'data']
    d = []
    for f in fnames:
        filename = f + '.dat'
        d.append(np.memmap(filename, dtype='float32', mode='r', shape=shape))
    return d

# 生成(swLL, neLL)範圍的等高線圖
def cntr(swLL, neLL):

    # 讀取GeoTiff檔案的基本參數、用在產生網格點的TWD97座標
    with open('params.txt', 'r') as f:
        line = [i.strip('\n') for i in f][0]
    x0, y0, nx, ny, dx, dy = (float(i) for i in line.split())
    nx, ny = int(nx), int(ny)
    shape = (ny, nx)

    # 讀取全島緯度、精度、以及高程等3項矩陣
    lat, lon, data = rd_mem(shape)

    # 負值歸0，避免拉大最低、最高值的區間
    data = np.where(data < 0, 0, data)

    # 利用經緯度進行範圍切割：共有4個條件都必須符合。
    idx = np.where((lat >= swLL[0]) & (lat <= neLL[0]) & (lon >= swLL[1]) & (lon <= neLL[1]))

    # 'LL not right!'是關鍵字，app.py中會檢核。
    if len(idx[0]) == 0:
        return 'LL not right!', list(swLL) + list(neLL)
    
    # TWD97座標值：
    ## 1維
    x = [x0 + dx * i for i in range(nx)]
    y = [y0 + dy * i for i in range(ny)]
    ## 2維（y,x）
    xg, yg = np.meshgrid(x, y)

    # 取4個方向的TWD97座標極值，用於標定位置
    bounds = [np.min(xg[idx[0], idx[1]]), np.max(xg[idx[0], idx[1]]), np.min(yg[idx[0], idx[1]]), np.max(yg[idx[0], idx[1]])]
    
    # 起訖點的索引
    ib = [x.index(bounds[0]), x.index(bounds[1]), y.index(bounds[2]), y.index(bounds[3])]

    # 範圍內地形的極值、用於計算間距(固定10層)
    cmin = data[ib[2]:ib[3]+1, ib[0]:ib[1]+1].min()
    cmax = data[ib[2]:ib[3]+1, ib[0]:ib[1]+1].max()
    levels = np.linspace(cmin, cmax, 10)
    
    # 新的圖面(使用Agg避免顯示器干擾)
    fig, ax = plt.subplots()

    ## 繪圖
    ax.contour(x[ib[0]:ib[1]+1], y[ib[2]:ib[3]+1], data[ib[2]:ib[3]+1, ib[0]:ib[1]+1], levels=levels)
    
    ## 存檔、輸出到BytesIO供前後端API傳輸
    ran = tf.NamedTemporaryFile().name.replace('/', '').replace('tmp', '')
    fname = 'terr_' + ran + '.png'
    output = BytesIO()
    fig.savefig(output, format='png')
    output.seek(0)  # 重置指针位置
    fig.savefig('./pngs/' + fname, format='png')
    
    return fname, output
```

這段代碼的關鍵步驟包括：
- 讀取地理數據。
- 查找給定界限內的數據。
- 繪製等高線圖並保存為 PNG 文件。

## 程式下載

- 副程式版本{% include download.html content="[mem2cntr.py](./mem2cntr.py)" %}，供API呼叫、自動回復。
- 獨立程式版本{% include download.html content="[mem2ccontour.py](./mem2ccontour.py)" %}，獨立手動運作。

## 圖檔結果比較

|![](https://github.com/sinotec2/Utilities/blob/main/GIS/DTM/pngs/2024-06-06-10-27-25.png?raw=true)|![](https://github.com/sinotec2/Utilities/blob/main/GIS/DTM/pngs/2024-06-06-12-01-09.png?raw=true)|
|:-:|:-:|
|mapbox切割範圍|matplotlib等高線圖|
