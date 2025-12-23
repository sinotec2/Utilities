---
layout: default
title: cntr_kml_py
nav_order: 99
has_children: true
parent: Marking Languages
last_modified_date: 2025-11-23T11:24:36
tags: md
---
# cntr_kml_py

## `cntr_kml` – 中英混合說明手冊

### 1. 功能說明  
`cntr_kml` 將一組 2‑D 網格資料（`grid_z2`）畫成等值線，並輸出為 Google Earth 可讀取的 **KML** 檔。  
- 等值線的個數由參數 `N` 控制（預設 10 步）。  
- 標準化顏色表 (10 色)，如果你想改色或使用更細緻的色階，只需要改 `col` 之後的 10 種 HEX 色碼即可。  
- 程式已考量“邊界閉合”問題：若等值線段未自動結合至地圖邊境，會自動在合適位置填補點，使極圈完整。  

> **主要特點**  
> - 直接使用 `legacycontour`（舊版 matplotlib 封裝）做等值線追蹤。  
> - 產出的 KML 已經帶有 `LineStyle` 和 `PolyStyle`，可以在 Google Earth 中自行調整寬度、顏色等。  

---

### 2. 參數說明  

| 參數 | 類型 | 說明 | 範例 |
|------|------|------|------|
| `grid_z2` | `np.ndarray` (2‑D) | 高程／溫度／降雨等儀器資料，行數 = `lat.shape[0]`，列數 = `lon.shape[0]` | `np.random.rand(100,90)` |
| `lon` | `np.ndarray` (1‑D) | 排列於資料行，形如 0~360 或 -180~180 的水平座標 | `np.linspace(-180,180,90)` |
| `lat` | `np.ndarray` (1‑D) | 排列於資料列，形如 -90~90 的垂直座標 | `np.linspace(-90,90,100)` |
| `fname` | `str` | 輸出 KML 檔名（不含副檔名），若路徑中帶斷線則只用最後一段 | `"myMap"` 或 `"/tmp/region1"` |

> **備註**  
> - 若 `lon`、`lat` 與 `grid_z2` 經維度不匹配，程式會在執行前投機 `IndexError`。  
> - 輸出檔名 `fname` 需有寫入權限，否則 `IOError`。  

---

### 3. 回傳值  
- `int`：函式執行完成後始終回傳 `0`。並不會把 KML 內容作為回傳值（KML 由檔案系統寫出）。

---

### 4. 所需模組 / 依賴  

| 模組 | 版本建議 | 下載 / 安裝方式 |
|------|----------|-----------------|
| `numpy` | ≥ 1.18 | `pip install numpy` |
| `legacycontour` | 只需安裝其原始版本（原 matplotlib 2.x 版本的 `cntr` 介面） | `pip install legacycontour` |
| `os` | 內建 | 無需安裝 |
| `sys` | 內建 | 無需安裝 |

> **注意**  
> - `legacycontour._cntr` 是一個 compiled module，必須有與其相容的 C/C++ 編譯環境或已編好的 wheel。  
> - 若你不想安裝 `legacycontour`，可以自行改寫 `cntr.Cntr` 部分，改用 `matplotlib.contour` 或 `scipy.ndimage` 的等值線演算法，但必須重新調整傳回值結構。  

---

### 5. 計算流程（高階流程圖）

```
┌─────────────────────────────┐
│ 1. 讀取輸入參數            │
├─────────────────────────────┤
│ 2. 建立等值線梯度  levels │
│    - max值 → mxgrd          │
│    - np.linspace(0,mxgrd,N) │
│    - 取 1 重要數字舍入      │
├─────────────────────────────┤
│ 3. 設定顏色表 col          │
│    - 10 HEX 颜色 → RGB      │
│    - 轉為 KML 色碼格式      │
├─────────────────────────────┤
│ 4. 建立 KML 基本結構 (head1)│
├─────────────────────────────┤
│ 5. 迭代每個 level          │
│    │
│    +--- 透過 cntr.Cntr(lon,lat,grid_z2)
│        .trace(level, level, 0) → (nlist)
│    │
│    +--- 取每個 segment（兩半）
│    │
│    +--- 逐點寫入 coordinates
│    │
│    +--- 檢查是否需要加閉合點（ewsn）─> 觸發特殊邊界填補
│    │
│    +--- 加上 tail2 → 完成 Placemark
├─────────────────────────────┤
│ 6. 結束寫入 KML 結構       │
│    (</Document></kml>)      │
└─────────────────────────────┘
```

---

### 6. 程式內部細節說明  

| 步驟 | 說明 | 重要變數 |
|------|------|-----------|
| **创建颜色表** |  
   - `col`：`'#00FF0A #3FFF0A … #FA000A'` → 10 個 HEX 16進色碼。  
   - `aa`：顏色前綴針對 KML 需要的 α 參數（`28` 代表 40% 透明度，若想更透明改成 `4d` 代表 75%）。  
   - `col` 後面進一步轉成 KML 色碼：擺了 `bb, gg, rr` 的順序，把 R,G,B 反轉（RGB → BGR）再接 α，產生 KML 色碼。 | `aa, bb, gg, rr, col` |
| **等值線追蹤** | `c = cntr.Cntr(lon, lat, grid_z2)` 之後，`c.trace(level, level, 0)` 會回傳 (nlist1, nlist2, nlist3,…)，每個 list 的長度為場域等值線的數目。  
   - `nlist[:len(nlist)//2]` 取前半部，代表 “有效”的封閉等值線段。 | `nlist, segs` |
| **檢測與補點** | 中段程式碼 `if leng0 > leng and leng0 / leng > 5:` 用來判測等值線段是否有「長度遠大於其他段」（即可能開口），如果是就根據邊界 (`e,w,s,n`) 為此段頭尾增加補點 (`ewsn` array)。  
   - `ews` （East/West/​South/​North）對應一個 4×2 的 bool 矩陣。 | `ewsn, e, w, s, n` |
| **KML 格式構造** |  
   - `head1` 設定標頭與文件名。  
   - `st_head` 會將每種等值線的 `Style id="levelX"` 加入；裡面的 `<LineStyle>` 與 `<PolyStyle>` 會使用上述 `col`。  
   - `head2` 是每條多邊形內部的起始。  
   - `tail2` 關閉多邊形。 | `head1, st_head, st_med, st_tail, head2, tail2` |
| **輸出檔案** | `with open(fname + '.kml', 'w') as f:` 逐行寫入到 `line` 資料，最後產生 `xxx.kml`。 | `line, fname` |

---

### 7. 使用示範  

```python
import numpy as np
from your_module import cntr_kml   # 假設此程式碼放在 your_module.py

# 產生示例資料
lon = np.linspace(-180, 180, 200)           # 200 列
lat = np.linspace(-90, 90, 150)             # 150 列
lon_grid, lat_grid = np.meshgrid(lon, lat)  # 2‑D 坐標矩陣可選
# 生成「山形」偽資料
grid_z2 = 5000*np.exp(-((lon_grid)/120)**2 - (lat_grid/60)**2)

# 呼叫函式
cntr_kml(grid_z2, lon, lat, 'my_conformal_map')
# 會產生 my_conformal_map.kml
```

> **小技巧**  
> 1. 若想改等值線數目，只變 `N` 即可。  
> 2. 若想改等值線顏色自行改 `col` 或 `aa`（透明度）。  
> 3. 若想保留多點封閉區域，請在 `tail2` 與 `head2` 之間改 `Polygon` 為 `LineString` 以避免將資點誤寫成多邊形。  

---

### 8. 常見錯誤與排錯  

| 錯誤訊息                                            | 可能原因                         | 問題排查 & 解法                                    |     |
| ----------------------------------------------- | ---------------------------- | -------------------------------------------- | --- |
| `legacycontour._cntr` not found                 | 未安裝 `legacycontour` 或安裝版本不相容 | `pip install legacycontour`，或確認系統 C/C++ 編譯環境 |     |
| `ValueError: could not convert string to float` | `grid_z2` 含空值（NaN, inf）      | 在呼叫前使用 `np.nan_to_num(grid_z2)`              |     |
| `IndexError: list index out of range`           | `N` 大於 `levels` 之長度          | 確認 `N` 係數 <= 10 或對 `levels` 做修正              |     |
| `PermissionError: [Errno 13] Permission denied` | 無寫檔權限                        | 重新設定輸出路徑或以 `sudo` 執行                         |     |
| `OSError: [Errno 36] File name too long`        | `fname` 輸入的路徑太長              | 只使用最後一段檔名或切短路徑                               |     |

---

### 9. 進階提醒  

1. **Python 版本**：此程式使用 `numpy`，可支援 Python 3.8+，但如果你在舊版（<3.8）下執行，可能需要調整 `range` 與 `print` 的語法。  
2. **KML 版本**：此程式產生的 KML 為 Earth 的 `2.2` 版，足以在 Google Earth 4.0+ 以上正確顯示。  
3. **多邊形封閉**：若等值線必須在座標外迴圈時，`legacycontour` 可能不返回正確的多邊形封閉順序。你可自行呼叫 `shapely` 的 `Polygon(buffer)` 做細節修正。  

---

### 10. 小結

- **核心功能**：將 2‑D 網格資料轉成 Google Earth 可看見的等值線 KML。  
- **最快捷**：只要 `np.ndarray`、`lon`、`lat`、`fname` 就能執行。  
- **擴充性**：顏色表、等值線個數、透明度、線寬都可以在 code‐block 內簡易改動。  
- **依賴**：`numpy`、`legacycontour`（含 `cntr` wrap ），其餘為內建模組。  

先將 `legacycontour` 安裝好後，直接呼叫上述程式即可得到一份完整的 KML，方便在 Google Earth 或其他 GIS 軟體檢視。祝你玩得開心 🚀  
```python
def cntr_kml(grid_z2, lon, lat, fname):
  import numpy as np
  import legacycontour._cntr as cntr
  last=fname
  if '/' in fname:last=fname.split('/')[-1]
  # levels size,>10 too thick, <5 too thin
  N = 10
  mxgrd=np.max(grid_z2)
  levels = np.linspace(0, mxgrd, N)
  col = '#00FF0A #3FFF0A #7FFF0A #BFFF0A #FFFF0A #FECC0A #FD990A #FC660A #FB330A #FA000A'.replace('#', '').split()
  if len(col) != N: print ('color scale not right, please redo from http://www.zonums.com/online/color_ramp/')
  aa = '28'  # ''28'~ 40%, '4d' about 75%
  rr, gg, bb = ([i[j:j + 2] for i in col] for j in [0, 2, 4])
  col = [aa + b + g + r for b, g, r in zip(bb, gg, rr)]

  # round the values of levels to 1 significant number at least, -2 at least 2 digits
  i = int(np.log10(levels[1])) - 1
  levels = [round(lev, -i) for lev in levels]

  #the Cntr method is valid only in previous version of matplotlib
  c = cntr.Cntr(lon, lat, grid_z2)
  # the tolerance to determine points are connected to the boundaries
  tol = 1E-3
  col0 = '4d6ecdcf'
  col_line0 = 'cc2d3939'


  #writing the KML, see the KML official website
  head1 = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://earth.google.com/kml/2.2"><Document><name><![CDATA[' + last + ']]></name>'
  st_head = ''
  st_med = '</color><width>1</width></LineStyle><PolyStyle><color>'
  st_tail = '</color></PolyStyle></Style>'
  for i in range(N):
    st_head += '<Style id="level' + str(i) + '"><LineStyle><color>' + col[i] + st_med + col[i] + st_tail
  head2 = '</styleUrl><Polygon><outerBoundaryIs><LinearRing><tessellate>1</tessellate><coordinates>'
  tail2 = '</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>'
  line = [head1 + st_head]
  # repeat for the level lines
  e, w, s, n = np.max(lon), np.min(lon), np.min(lat), np.max(lat)
  for level in levels[:]:
    nlist = c.trace(level, level, 0)
    segs = nlist[:len(nlist) // 2]
    i = levels.index(level)
    for seg in segs:
      line.append('<Placemark><name>level:' + str(level) + '</name><styleUrl>#level' + str(i) + head2)
      leng = -9999
      for j in range(len(seg[:, 0])):
        line.append(str(seg[j, 0]) + ',' + str(seg[j, 1]) + ',0 ')
        if j > 0:
          leng = max(leng, np.sqrt((seg[j, 0] - seg[j - 1, 0]) ** 2 + (seg[j, 1] - seg[j - 1, 1]) ** 2))
      leng0 = np.sqrt((seg[j, 0] - seg[0, 0]) ** 2 + (seg[j, 1] - seg[0, 1]) ** 2)
      ewsn = np.zeros(shape=(4, 2))
      j = -1
      # end points not closed, add coner point(s) to close the polygons.
      if leng0 > leng and leng0 / leng > 5:
        if abs(seg[j, 0] - e) < tol: ewsn[0, 1] = 1
        if abs(seg[0, 0] - e) < tol: ewsn[0, 0] = 1
        if abs(seg[j, 0] - w) < tol: ewsn[1, 1] = 1
        if abs(seg[0, 0] - w) < tol: ewsn[1, 0] = 1
        if abs(seg[j, 1] - s) < tol: ewsn[2, 1] = 1
        if abs(seg[0, 1] - s) < tol: ewsn[2, 0] = 1
        if abs(seg[j, 1] - n) < tol: ewsn[3, 1] = 1
        if abs(seg[0, 1] - n) < tol: ewsn[3, 0] = 1
        if sum(ewsn[1, :] + ewsn[2, :]) == 2: line.append(str(np.min(lon)) + ',' + str(np.min(lat)) + ',0 ')
        if sum(ewsn[1, :] + ewsn[3, :]) == 2: line.append(str(np.min(lon)) + ',' + str(np.max(lat)) + ',0 ')
        if sum(ewsn[0, :] + ewsn[3, :]) == 2: line.append(str(np.max(lon)) + ',' + str(np.max(lat)) + ',0 ')
        if sum(ewsn[0, :] + ewsn[2, :]) == 2: line.append(str(np.max(lon)) + ',' + str(np.min(lat)) + ',0 ')
      # TODO: when contour pass half of the domain,must add two edge points.
      line.append(tail2)
  line.append('</Document></kml>')
  with open(fname + '.kml', 'w') as f:
    [f.write(i) for i in line]
  return 0
```