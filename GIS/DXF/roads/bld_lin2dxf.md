---
layout: default
title:  建築物與道路整併輸出
grand_parent: DXF
parent: roads
last_modified_date: 2024-12-10 20:32:50
tags: GIS DXF
---

# 建築物與道路整併輸出（bld_line2dxf.py）

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

- 高架道路在噪音模擬作業中是很重要的噪音源，但是其幾何元件相對建築物來說還算單純，似乎沒有必要另外建立一個計算流程，附加在建築物的切割與輸出，會比較單純一些。
- 未來如果要再加入地區（平面）道路，元件內容項目可能會很多，建議再另外創建新的計算流程。

## 程式碼說明

- 呼叫`line2dxf.py`副程式，以得到高架道路的三維GeoPandaDataFrame，詳見[line2dxf.py]()說明。
- 內政部資料並沒有路寬，只有中心線的三維線段LineString/MuitiLineString，
- 輸出dxf時不必加地標的高程，但必須是`add_polyline3d`。
- MuitiLineString狀況：必須針對`polylin.geoms`進行迴圈、歷遍所有的線段。

```python
#原來bld2dxf.py內容
...
  sliced_gdf=create_line_segments(swLL,neLL)
  
  ii=0
  for i in sliced_gdf.index:
    layer_name = f"Polylin_{ii}"
    layer = doc.layers.add(layer_name)
    polylin=sliced_gdf.loc[i,'geometry_twd97']
    if polylin.geom_type=="LineString":
      pnts = [Vec3(p) for p in polylin.coords]
      msp.add_polyline3d(pnts, dxfattribs={ "layer": layer_name}) 
    elif polylin.geom_type=="MultiLineString":
      for lin in polylin.geoms:
        pnts = [Vec3(p) for p in lin.coords]
        msp.add_polyline3d(pnts, dxfattribs={ "layer": layer_name}) 
    ii+=1
    ...
# 輸出成檔案
```

