import geopandas as gpd
from rtree import index
import sys
from shapely.wkt import loads


# Assuming you have two GeoDataFrames, one with points and one with polygons
points_gdf = gpd.read_file(sys.argv[1])

# Convert the geometry columns from string to Shapely objects
if 'geometry' not in points_gdf.columns: sys.exit('no geometries found')
if 'addr:floor' not in points_gdf.columns: sys.exit('no floors found')
points_gdf = points_gdf.loc[points_gdf['addr:floor']>1].reset_index(drop=True)
del points_gdf['addr:floor']
points_gdf['geometry'] = points_gdf['geometry'].apply(loads)
points_gdf['addr:full']=[i[:i.index('號')+1] for i in points_gdf['addr:full']]
points_gdf = points_gdf.drop_duplicates().reset_index(drop=True)
points_gdf.to_csv(sys.argv[1].replace('.csv','_drp.csv'),index=False)