#kuang@DEVP /nas2/kuang/MyPrograms/CADNA-A/112roads
$ cat split1.py
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
