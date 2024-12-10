#(pyn_env)
#kuang@DEVP /nas2/kuang/MyPrograms/CADNA-A
#$ cat line2dxf.py
import pandas as pd
import geopandas as gpd
from shapely.wkt import loads
from shapely.geometry import Point, Polygon, LineString, MultiLineString
import os
import sys
from pyproj import Proj
from bld2dxf import cut_data, grid_prep, query_p

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

def create_line_segments(sw_ll, ne_ll):
    """
    Create the bounding box from the given southwest and northeast coordinates, and read and transform the line segment data from the grid files.

    Args:
    sw_ll (tuple): The southwest corner coordinates (latitude, longitude).
    ne_ll (tuple): The northeast corner coordinates (latitude, longitude).

    Returns:
    list: A list of GeoDataFrames containing the transformed line segment data.
    """
    # Create the bounding box
    south, west = sw_ll[0], sw_ll[1]
    north, east = ne_ll[0], ne_ll[1]
    dd = {'geometry': [f'POLYGON(({west} {south}, {west} {north}, {east} {north}, {east} {south}, {west} {south}))']}
    bounds_df = pd.DataFrame(dd)
    bounds_gdf = gpd.GeoDataFrame(bounds_df, geometry=bounds_df['geometry'].apply(loads), crs="EPSG:3857")
    bbox_center = Point((west + east) / 2, (south + north) / 2)
    #locate the nearest gridpoint to transfer twd97 coordinates and terrain elevation
    grid_df=cut_data (sw_ll,ne_ll)
    pnts_tw,pnts_ll,data_arr,ll_tree=grid_prep (grid_df)
    # Create a Proj object for coordinate transformation
    point_tw=query_p(bbox_center,pnts_tw,pnts_ll,ll_tree)
    pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40, lat_0=bbox_center.y, lon_0=bbox_center.x, x_0=point_tw.x, y_0=point_tw.y)

    # Read and transform the line segment data
    linestr_gdf = open_grid_files(bounds_gdf)
    if isinstance(linestr_gdf, str):
        return linestr_gdf
    linestr_gdf['geometry'] = linestr_gdf['geometry'].apply(loads)
    linestr_gdf = gpd.GeoDataFrame(linestr_gdf, geometry='geometry', crs="EPSG:3857")
    p=[]
    for geom in ['LineString', 'MultiLineString']:
        gdf_tmp = linestr_gdf.loc[linestr_gdf.geometry.map(lambda x: x.geom_type == geom)]
        pi=gpd.overlay(gdf_tmp, bounds_gdf, how='intersection')
        if len(pi)>0:
            p.append(pi)
    sliced_gdf = pd.concat(p, ignore_index=True)
    if len(sliced_gdf)==0:
        return 'no line found'
    sliced_gdf = gpd.GeoDataFrame(sliced_gdf, geometry='geometry', crs=linestr_gdf.crs)

    # Transform the line segment coordinates
    p=sliced_gdf.loc[sliced_gdf.geometry.map(lambda x: x.geom_type=='LineString')]
    if len(p)>0:
        plg=list(p.geometry)
        sliced_gdf.loc[p.index,'geometry_twd97']=[query_l(geom,pnyc) for geom in plg]
    m=sliced_gdf.loc[sliced_gdf.geometry.map(lambda x: x.geom_type=='MultiLineString')]
    if len(m)>0:
        mplg=list(m.geometry)
        sliced_gdf.loc[m.index,'geometry_twd97']=[query_ml(geom,pnyc) for geom in mplg]

    return sliced_gdf

def query_l(polylin_ll, pnyc):
    """
    Transform the LineString geometry from latitude/longitude to TWD97 projection coordinates.

    Args:
    polylin_ll (LineString): The LineString geometry to be transformed.
    pnyc (Proj): The Proj object for coordinate transformation.

    Returns:
    LineString: The transformed LineString geometry.
    """
    lon_new = [coord[0] for coord in polylin_ll.coords]
    lat_new = [coord[1] for coord in polylin_ll.coords]
    alt_new = [coord[2] for coord in polylin_ll.coords]
    twd97X, twd97Y = pnyc(lon_new, lat_new, inverse=False)
    return LineString([(x, y, z) for x, y, z in zip(twd97X, twd97Y, alt_new)])

def query_ml(polylin_ll, pnyc):
    polylin_twd=[]
    for polylin in polylin_ll.geoms:
        polylin_twd.append(query_l(polylin,pnyc))
    return MultiLineString(polylin_twd)
