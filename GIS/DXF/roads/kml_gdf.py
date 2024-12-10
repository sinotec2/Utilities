import os
import geopandas as gpd
import pandas as pd
kml_dir ='.'
gdf_list = []

# Loop through all the KML files in the directory
for filename in os.listdir(kml_dir):
    if filename.endswith('.kml') and 'LINE' in filename:
        # Read the KML file into a GeoDataFrame
        gdf = gpd.read_file(os.path.join(kml_dir, filename), driver='KML')

        # Filter for LineString geometries
        gdf = gdf[gdf.geometry.geom_type == 'LineString']

        # Add the filename as a new column
        gdf['filename'] = filename

        # Append the GeoDataFrame to the list
        gdf_list.append(gdf)
all_gdf = pd.concat(gdf_list, ignore_index=True)
all_gdf.to_csv('line3D.csv', index=False)
