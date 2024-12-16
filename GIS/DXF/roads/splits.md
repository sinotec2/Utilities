---
layout: default
title: 按照經緯度切割高架道路
grand_parent: DXF
parent: roads
last_modified_date: 2024-12-10 20:32:50
tags: GIS DXF
---

# 按照經緯度切割高架道路

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

- 內政部檔案除了高速公路之外，其他快速道路或重要路段，是採行按照縣市進行分類。共計8個檔案。但實務上有可能會在縣市邊界上，還需要讀取鄰近縣市的檔案，過程常常會發生不流暢的作業方式。
- 讀取OSM檔案時，我們用過按照經緯度執行`osmconvert`來轉換OSM與KML檔案。解析度用0.5/0.1度2個層次。因為使用第三方程式工具，需要在`bash`上執行。
- 此處要處理的是`csv`檔案的切割，還是用python還是比較方便。

## 相關程式說明

### 按經緯度切割

```python
import geopandas as gpd
import pandas as pd
import os
from shapely.wkt import loads
from shapely.geometry import Polygon


# Load the 3D LineString data from the CSV file
gdf = pd.read_csv('line3D.csv')
gdf['geometry'] = gdf['geometry'].apply(loads)
gdf = gpd.GeoDataFrame(gdf, geometry='geometry', crs="EPSG:3857")

# Set the starting coordinates and the resolution
start_lon = 119.2
start_lat = 21.5
resolution = 0.5
overlap = 0.1

# Calculate the grid boundaries
min_lon, min_lat, max_lon, max_lat = gdf.total_bounds


# Create the output directory if it doesn't exist
output_dir = 'splits'
os.makedirs(output_dir, exist_ok=True)
grid_info = []


# Iterate through the grid and split the data
for lon in range(int((max_lon - min_lon) / resolution) + 1):
    for lat in range(int((max_lat - min_lat) / resolution) + 1):
        x1 = min_lon + lon * resolution - overlap
        x2 = min_lon + (lon + 1) * resolution + overlap
        y1 = min_lat + lat * resolution - overlap
        y2 = min_lat + (lat + 1) * resolution + overlap

        # Filter the data based on the grid boundaries
        dd={'geometry': [Polygon([(x1, y1), (x1, y2), (x2, y2), (x2, y1), (x1, y1)])]}
        bounds_df=pd.DataFrame(dd)
        bounds_gdf = gpd.GeoDataFrame(bounds_df, geometry=bounds_df['geometry'], crs="EPSG:3857")
        grid_gdf = gpd.overlay(gdf, bounds_gdf, how='intersection')

        # Save the filtered data to a new file
        output_file = os.path.join(output_dir, f'grid_{lon}_{lat}.csv')
        grid_gdf.to_csv(output_file,index=False)
        print(f'Saved file: {output_file}')

        grid_info.append({
            'file_name': f'grid_{lon}_{lat}.csv',
            'min_lon': x1,
            'min_lat': y1,
            'max_lon': x2,
            'max_lat': y2
        })

# Save the grid information to a CSV file
grid_info_df = pd.DataFrame(grid_info)
grid_info_df.to_csv('grid_info.csv', index=False)
```

### 切割結果之調用

- [line2dxf.py中的open_grid_files副程式]()
- 會需要[split1.py]()之中另存的範圍座標值與檔案名稱的綁定數據組。

```python
def open_grid_files(bounds_gdf):
    """
    Open the grid files that intersect with the given bounding box, and return the one with the smallest length.

    Args:
    bounds_gdf (GeoDataFrame): The GeoDataFrame containing the bounding box.

    Returns:
    GeoDataFrame or None: The GeoDataFrame with the smallest length data, or None if no matching files are found.
    """
    # Load the grid information from the CSV file
    root_dir = '/nas2/kuang/MyPrograms/CADNA-A/112roads'
    file_name = f"{root_dir}/grid_info.csv"
    grid_info_df = pd.read_csv(file_name)
    grid_info_df['geometry'] = [f"POLYGON(({i} {j},{k} {j},{k} {l}, {i} {l}, {i} {j}))" for i, j, k, l in zip(grid_info_df.min_lon, grid_info_df.min_lat, grid_info_df.max_lon, grid_info_df.max_lat)]
    grid_info_gdf = gpd.GeoDataFrame(grid_info_df, geometry=grid_info_df['geometry'].apply(loads), crs="EPSG:3857")

    # Find the grid files that are fully contained within the given bounding box
    covering_grids = grid_info_gdf[bounds_gdf.geometry[0].within(grid_info_gdf.geometry)]

    # Open the corresponding grid files
    grid_gdfs = []
    for _, row in covering_grids.iterrows():
        file_name = row['file_name']
        file_path = os.path.join(f"{root_dir}/splits", file_name)
        grid_gdfs.append(pd.read_csv(file_path))

    if grid_gdfs:
        return min(grid_gdfs, key=lambda x: len(x))
    else:
        sys.exit('wrong bounds_gdf:', bounds_gdf)
```

### 