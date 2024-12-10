---
layout: default
title:  內政部高架道路3維線段之讀取及處理
grand_parent: DXF
parent: roads
last_modified_date: 2024-12-10 20:32:50
tags: GIS DXF
---

# 內政部高架道路3維線段之讀取及處理

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

- 內政部檔案格式是KML。
- 雖然geopandas可以直接讀取KML，但是只能擷取第一層，其他層會略過，最後只能放棄，改用`xml.etree`來讀取，還是比較實際有效。

### 主程式

- 主程式管理目錄下所有`*LINE*.kml`，執行`read_kml_to_gdf`副程式。
- 屬性資料儲存後予以刪除，以備整合成為一個大檔`'line3D.csv'`。

```python
import geopandas as gpd
from shapely.wkt import loads
import xml.etree.ElementTree as ET
import os
import pandas as pd
from shapely.geometry import LineString

# Example usage
kml_dir ='.'
gdf_list = []

# Loop through all the KML files in the directory
for filename in os.listdir(kml_dir):
    if filename.endswith('.kml') and 'LINE' in filename:
      gdf = read_kml_to_gdf(filename)
      if len(gdf)==0:continue
      root=filename.replace('kml','')
      gdf.to_csv(root+'csv',index=False)
      for c in gdf.columns:
        if c!='geometry':del gdf[c]
      gdf_list.append(gdf)
if len(gdf_list)==0:sys.exit('fail')
all_gdf = pd.concat(gdf_list, ignore_index=True)
all_gdf.to_csv('line3D.csv', index=False)
```

### 副程式

- `read_kml_to_gdf`的任務就是將kml檔案的3維線段的座標值取出來，存成GeoPandas的數據表型態
- 其他屬性資料包括行政區名稱等，似乎也沒有特別的需求，並不會用到，此處還是將其讀取另存。

```python
def read_kml_to_gdf(kml_file):
    tree = ET.parse(kml_file)
    root = tree.getroot()
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    features = []
    for placemark in root.findall('.//kml:Placemark', ns):
        name = placemark.find('kml:name', ns).text
        geom_type = placemark.find('kml:LineString', ns) is not None
        if geom_type:
            coordinates = placemark.find('kml:LineString/kml:coordinates', ns).text.strip()
            coords = [tuple(map(float, coord.split(','))) for coord in coordinates.split()]
            geometry = LineString(coords)

            # Extract the extended data
            extended_data = placemark.find('kml:ExtendedData', ns)
            if extended_data is not None:
                schema_data = extended_data.find('kml:SchemaData', ns)
                if schema_data is not None:
                    attributes = {
                        elem.attrib['name']: elem.text
                        for elem in schema_data.findall('kml:SimpleData', ns)
                    }
            else:
                attributes = {}

            feature = {
                'name': name,
                'geometry': geometry,
                **attributes
            }
            features.append(feature)
        else:
            # Handle other geometry types if needed
            continue

    gdf = gpd.GeoDataFrame(features, geometry='geometry')
    return gdf
```