---
layout: default
title:  KML之座標個數
parent: KML and GML
grand_parent: GIS Relatives
last_modified_date: 2024-12-04 11:22:35
tags: KML GIS
---

# KML之座標個數
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

- 這個GPT建議的小程式對計算KML檔案的大小很有用，這是因為leaflet或其他顯示界面對KML檔案的大小具有敏感性。
- 當然這題的解決方案是提供具有縮放效果的地圖伺服器，如mapbox，但如果只是為了預覽，實在沒有必要大費周章，寫一個瘦身程式會比較方便。
- 瘦身程式的目標：將座標的組數控制在1萬筆以下，對leaflet是OK的。如果要使用google map，可能會需要更低。

## 程式碼

```python
import sys

def count_coordinates(kml_file):
    import xml.etree.ElementTree as ET
    tree = ET.parse(kml_file)
    root = tree.getroot()
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    coordinates_count = 0
    for coordinates in root.findall('.//kml:coordinates', ns):
        coords = coordinates.text.strip().split()
        coordinates_count += len(coords)
    
    return coordinates_count

# 使用示例
kml_file_path = sys,argv[1]
print(count_coordinates(kml_file_path))
```
