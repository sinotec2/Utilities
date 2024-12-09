import geopandas as gpd
from rtree import index
import sys
from shapely.wkt import loads


# Assuming you have two GeoDataFrames, one with points and one with polygons
points_gdf = gpd.read_file(sys.argv[1])
polygons_gdf = gpd.read_file(sys.argv[2])

# Convert the geometry columns from string to Shapely objects
points_gdf['geometry'] = points_gdf['geometry'].apply(loads)
polygons_gdf['geometry'] = polygons_gdf['geometry'].apply(loads)

# Create an Rtree index for the polygons
idx = index.Index()
for i, geometry in enumerate(polygons_gdf.geometry):
    idx.insert(i, geometry.bounds)

# Query the Rtree index to find which points are within which polygons
points_in_polygons = []
for i, point in enumerate(points_gdf.geometry):
    possible_matches = list(idx.intersection(point.bounds))
    for j in possible_matches:
        if polygons_gdf.geometry[j].contains(point):
            points_in_polygons.append((i, j))

# Create a new GeoDataFrame with the matched points and polygons
result_gdf = gpd.GeoDataFrame({
    'point_idx': [p[0] for p in points_in_polygons],
    'polygon_idx': [p[1] for p in points_in_polygons],
    'geometry_pnt': [points_gdf.geometry[p[0]] for p in points_in_polygons],
    'geometry_png': [polygons_gdf.geometry[p[1]] for p in points_in_polygons]
})
#result_gdf for checking
result_gdf.to_csv(sys.argv[1]+sys.argv[2],index=False)

pgn_pnt={i:j for i,j in zip(result_gdf.polygon_idx,result_gdf.point_idx)}
s_polygon_idx=list(set(result_gdf.polygon_idx))
final=gpd.GeoDataFrame({'geometry':[polygons_gdf.geometry[i] for i in s_polygon_idx]})
final['addr:full']=[points_gdf.loc[pgn_pnt[i],'addr:full'] for i in s_polygon_idx]
final.to_csv('final'+sys.argv[1]+sys.argv[2],index=False)
