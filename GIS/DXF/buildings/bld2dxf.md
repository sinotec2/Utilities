---
layout: default
title:  bld2dxf
grand_parent: DXF
parent: buildings
last_modified_date: 2024-12-08 16:24:44
tags: GIS DXF
---

# 建築物DXF檔之讀寫

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

- 整體工作流程如圖所示，區分為3大區塊

  ![alt text](./pngs/image-1.png)

### 檢視工具

- 利用ezdxf模組解讀、輸出建築物的3維平面
- 座標轉換
- 松山機場周邊建築物

![pngs/2024-12-08-16-19-16.png](pngs/2024-12-08-16-19-16.png)

- by [autodesk viewer ](https://viewer.autodesk.com/)

![pngs/2024-12-08-17-49-51.png](pngs/2024-12-08-17-49-51.png)

### 多邊形是否重新排序

### 如何快速轉換多邊形的座標

### 是否納入沒有高度的建築物


## 範圍切割

### building.csv切割

### 2D數據的應用

- 點Point如何轉成Polygon
- 高度設定的考量

## 高程數據的應用

### 地形高程的策略考量

- 因為是三維的模型，建築物的基地高程就變得很重要。還好已經有準備好的地形檔案可以快速引用。
- 策略面要考慮的是
  - 高程需不需要內插到多邊形的每一個點？這樣建築物會不會歪斜？這也會牽動到執行量與執行速率。
  - 如果不需要每一點，那建築物該取哪一點來代表它的位置？最低、最高、中心？平均高程？
  - 內插機制怎麼樣做到很快速又正確？

### 程式說明
  

### 幾何物件頂點的座標轉換

### 多邊形立體物件的輸出

### 串連道路資料庫

## ezdxf輸出函式的應用及程式說明

- `Vec3`物件
  - 一如在數值地形資料的輸出，如果只是輸出線形物件，後續程式仍然不能正確讀取DXF檔案，因為DXF的點都必須是3度空間完整定義([Vec3](https://ezdxf.readthedocs.io/en/stable/math/core.html#ezdxf.math.Vec3)物件)
- `3dface`
  - 使用`3dface`的必要性似乎是很直覺的，畢竟要輸出的是建築物的立方體，會需要上層、底層、各個立面的平面。
  - layer的高程設定卡了一陣子無法決定，如果建築物在山坡上，layer的高程究竟該取上、下層的高程？平均？答案是：都沒差別、在`polyliine3d`的個案中，直接把layer的高程設為0，徹底解決斷層的問題。
- `polyliine2d`物件
  - 會想重複提供多邊形邊框的描繪是查看範例檔案中有很多`LineString`物件，並沒有測試其必要性。
  - 在繪圖預覽過程中，有`polyliine2d`物件對不夠完整的`3dface`集合會有很大的幫助，建築物看起來會比較平整。
- 參考
  - [ezdxf官網說明](https://ezdxf.readthedocs.io/en/stable/index.html)
  - [等高線DXF輸出的經驗](../../DTM/mem2dxf.md)
  - [範例DXF檔案轉python碼](../roads/pys/w_source.py)
### 輸入

- **sliced_gdf**: 一個 GeoDataFrame，包含多邊形的幾何資訊及其相關屬性（如 `elevation` 和 `maxAltitude`）。
- **p, s, m**: 這些變數代表不同的索引集合，用於確定當前處理的幾何形狀類型。分別是多邊形、線段、與多個多邊形。

### 輸出

- **fname**: 生成的 DXF 檔案名稱。
- **output**: 包含生成的 DXF 檔案的二進位資料，方便後續操作或直接返回給使用者。

### 重要邏輯

1. **DXF 檔案創建**: 使用 `ezdxf` 庫創建新的 DXF 檔案，並設置模型空間。
2. **分層管理**: 根據每個多邊形的索引創建不同的圖層，並將多邊形的底部和頂部高度計算出來。
3. **多邊形處理**: 根據 `sliced_gdf` 中的幾何資料，將多邊形的外部點提取出來，並為每個多邊形生成上下平面及其立面。
   - 使用 `add_polyline2d` 和 `add_3dface` 方法將生成的點添加到模型空間中。
4. **立面生成**: 對於每個多邊形的邊，生成對應的立面，並將其添加到 DXF 檔案中。

### 較艱澀語法的解釋

- **Vec3**: 用於表示三維空間中的點，通常包含 x, y, z 三個座標。
- **add_polyline2d**: 用於將二維折線添加到模型空間中。
- **add_3dface**
  - 用於將**三維面**添加到模型空間中，通常用於構建立體幾何。
  - **三維面**的限制是一次只能有3點、至多4點、同一平面的點。因此當點數多於4點的建築物，就必須執行迴圈，同時也要注意每一點都必須有前後點作為**三維面**，否則會出現多邊形無法閉合的情況。
- MultiPolygon的處理：其函式`.geoms`的形態為個別多邊形所形成的序列，依序執行原來多邊形的任務即可。

### 改進建議

1. **錯誤處理**: 增加對於輸入資料有效性的檢查，避免因資料格式不正確而導致的執行錯誤。
2. **性能優化**: 對於大規模的多邊形數據，可以考慮使用多執行緒或異步處理來加速生成過程。
3. **功能擴展**: 可以考慮添加選項來支持不同的 DXF 版本，以滿足不同用戶的需求。

這段程式碼的主要目的是將地理數據轉換為 DXF 格式的三維模型，並能夠根據多邊形的特性生成相應的結構。

### 程式碼

```python
...
  doc = ezdxf.new(dxfversion="R2010")
  msp = doc.modelspace()
  align=TextEntityAlignment.CENTER
  ii=0
  for i in sliced_gdf.index:
    layer_name = f"Polygon_{ii}"
    layer = doc.layers.add(layer_name)
    bot=float(sliced_gdf.loc[i,'elevation'])
    Vbot=Vec3(0, 0, bot)
    top=bot+sliced_gdf.loc[i,'maxAltitude']
    if i in p.index or i in s.index:
      polygons=[sliced_gdf.loc[i,'geometry_twd97']]
    if i in m.index:
      polygons=[polygon for polygon in sliced_gdf.loc[i,'geometry_twd97'].geoms]
    for polygon in polygons:
      points=[j for j in polygon.exterior.coords] #reorder_polygon_points(polygon)
      #上下平面
      for hgt in [bot,top]:
        pnts=[Vec3(p[0],p[1],hgt) for p in points]
        npnts=len(pnts)
        msp.add_polyline2d(pnts, dxfattribs={ "layer": layer_name, 'elevation':Vbot  })
        if npnts <=4 and npnts in [3,4]:
          msp.add_3dface(pnts, dxfattribs={'layer': layer_name})
        else:
          rep=npnts//4
          for k in range(rep):
            for n in range(2*k, npnts, 4):
              nnd=min(n+4,npnts)
              if nnd-n not in [3,4]:continue
              msp.add_3dface(pnts[n:nnd], dxfattribs={'layer': layer_name})
      #立面
      for j in range(len(points)):
        pj = points[j]
        p1 = Vec3(pj[0],pj[1],bot)
        pn = points[(j + 1) % len(points)]
        p2 = Vec3(pn[0],pn[1],bot)
        p3 = Vec3(p2[0], p2[1], top)
        p4 = Vec3(p1[0], p1[1], top)
        pnts=[p1, p2, p3, p4]
        msp.add_polyline2d(pnts, dxfattribs={ "layer": layer_name, 'elevation': Vbot })
        msp.add_3dface(pnts, dxfattribs={'layer': layer_name})
    ii+=1

  ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')
  fname='bldn_'+ran+'.dxf'
  output=BytesIO()
  doc.write(output, fmt='bin')
  output.seek(0)  # 重置指针位置
  doc.saveas('./dxfs/'+fname)
  return fname,output
...
```

## 切割套件與應用

### app.py

- 這個程式繼承自[API伺服器的設計](../../DTM/app.md)，新增建築物資料庫的切割功能。
- 輸入bld2dxf模組
- 新增`bld(swLL, neLL)`之呼叫

### index.html

- 新增`SaveButtom_b` javascriple函式

### 檢查執行進度

- 因每次程式執行都會重新讀取資料庫、切割及座標轉換，因此會需要一些時間，可以進入瀏覽器`檢查`介面了解實際情況，是否正確運作。
- 可能無法正確執行的原因
  - 切割範圍的資訊位正確傳遞(檢視`saved bounds`)
  - 背景數據品質問題(訊息為`Network Response not OK`，請將**經緯度**範圍複製給研資部進一步追蹤除錯，TWD97值還需轉換。)
- 空白處按右鍵進入`檢查`

![pngs/2024-12-09-14-06-17.png](pngs/2024-12-09-14-06-17.png)
- 點選`console`(或紅色停止標誌-帶數字![pngs/2024-12-09-14-00-48.png](pngs/2024-12-09-14-00-48.png)) 

![pngs/2024-12-09-13-58-44.png](pngs/2024-12-09-13-58-44.png)

- `The file at blob ... is loaded`：是正確信息
  - 請檢視瀏覽器的`下載`介面。
  - 因為結果檔案是隨機碼，瀏覽器會認為是病毒拒絕直接下載，需進一步確認。

## 結果

- 中研院附近山坡與平地
- 範圍

![](./pngs/1733710208552.jpg)

- 地形

![](./pngs/terr_pxdm_ssw.png)

- 建築物群

![](./pngs/messageImage_1733719838403.jpg)

- 進入CADNA模式系統檢視

![](./pngs/1733720994018.jpg)

## 完整程式碼[bld2dxf.py](./pys/bld2dxf.py)

  {% include download.html content="建築物DXF檔之改寫[bld2dxf.py](./pys/bld2dxf.py)" %}