kuang@DEVP /nas2/kuang/MyPrograms/CADNA-A
$ cat bld2dxf.py
import numpy as np
import tempfile as tf
from io import BytesIO
import ezdxf
from ezdxf import colors
from ezdxf.math import Vec3
from ezdxf.enums import TextEntityAlignment, MTextLineAlignment
import pandas as pd
import geopandas as gpd
import sys, json
from shapely.wkt import loads
from shapely.geometry import Point, Polygon, MultiPolygon
from scipy.spatial import cKDTree

from pyproj import Proj

# Create a new DXF document.

def rd_mem(shape):
  fnames=['lat','lon','data']
  d = []
  for f in fnames:
    filename = f+'.dat'
    d.append(np.memmap(filename, dtype='float32', mode='r', shape=shape))
  return d

def cut_data (swLL,neLL):
  #load terrain data
  with open('params.txt','r') as f:
    line=[i.strip('\n') for i in f][0]
  x0,y0,nx,ny,dx,dy=(float(i) for i in line.split())
  nx,ny=int(nx),int(ny)
  shape=(ny, nx)
  lat,lon,data=rd_mem(shape)
  data = np.where(data < 0, 0, data)
  x=[x0+dx*i for i in range(nx)]
  y=[y0+dy*i for i in range(ny)]
  xg, yg = np.meshgrid(x, y)

  idx=np.where((lat>=swLL[0])&(lat<=neLL[0])&(lon>=swLL[1])&(lon<=neLL[1]))
  if len(idx[0])==0:
    return 'LL not right!',list(swLL)+list(neLL)
  bounds=[np.min(xg[idx[0],idx[1]]),np.max(xg[idx[0],idx[1]]),np.min(yg[idx[0],idx[1]]),np.max(yg[idx[0],idx[1]])]
  dd={'twd97X':xg[idx[0],idx[1]],'twd97Y':yg[idx[0],idx[1]],'lat':lat[idx[0],idx[1]],'lon':lon[idx[0],idx[1]],'data':data[idx[0],idx[1]]}
  grid_df=pd.DataFrame(dd)
  ib=[x.index(bounds[0]),x.index(bounds[1]),y.index(bounds[2]),y.index(bounds[3])]
  return grid_df

def grid_prep (grid_df):
  lon_arr = grid_df['lon'].values
  lat_arr = grid_df['lat'].values
  twd97X_arr = grid_df['twd97X'].values
  twd97Y_arr = grid_df['twd97Y'].values
  pnts_tw=[Point([i,j]) for i,j in zip(twd97X_arr,twd97Y_arr)]
  pnts_ll=[Point([i,j]) for i,j in zip(lon_arr,lat_arr)]
  data_arr = grid_df['data'].values
  ll_coords = np.column_stack((lon_arr, lat_arr))
  ll_tree = cKDTree(ll_coords)
  return pnts_tw,pnts_ll,data_arr,ll_tree

def query_p(point,pnts_tw,pnts_ll,ll_tree):
  lat_new=[coord[1] for coord in point.coords]
  lon_new=[coord[0] for coord in point.coords]
  query_coords = np.column_stack((lon_new, lat_new))
  _, indices = ll_tree.query(query_coords, k=1)
  return pnts_tw[indices[0]]

def query_g(polygon_ll,pnyc):
  lon_new=np.array([coord[0] for coord in polygon_ll.exterior.coords])
  lat_new=np.array([coord[1] for coord in polygon_ll.exterior.coords])
  twd97X,twd97Y=pnyc(lon_new, lat_new, inverse=False)
  return Polygon([(x, y) for x, y in zip(twd97X, twd97Y)])

def query_g2(point,pnyc):
  f=6/2
  x,y=pnyc(point.x, point.y, inverse=False)
  return Polygon([(x-f, y-f),(x+f, y-f),(x+f, y+f),(x-f, y+f),])

def query_mp(polygon_ll,pnyc):
  polygon_twd=[]
  for polygon in polygon_ll.geoms:
    polygon_twd.append(query_g(polygon,pnyc))
  return MultiPolygon(polygon_twd)

def query_e(points,data_arr,ll_tree):
  coords = np.array([list(p.coords) for p in points])
  _, indices = ll_tree.query(coords, k=1)
  return [data_arr[indices[i]][0] for i in range(len(points))]

def reorder_polygon_points(polygon):
    """
    接受一個 Polygon 對象,返回一個按照西南端開始,逆時針順序排列的點序列,並最後回到起始點。
    """
    # 獲取多邊形的外部環
    exterior = np.array(polygon.exterior.coords)

    # 計算每個點相對於多邊形西南端的角度
    angles = np.arctan2(exterior[:, 1] - exterior[0, 1], exterior[:, 0] - exterior[0, 0])

    # 根據角度排序點的序列
    sorted_indices = np.argsort(angles)

    # 返回排序後的點序列,包括起始點
    return [exterior[i] for i in sorted_indices]  + [exterior[sorted_indices[0]]]

# drop duplicate
def drop_dup(sliced_gdf):
  mean_ll_series = sliced_gdf.geometry.copy()
  unique_centroids = mean_ll_series.unique()
  unique_gdf = gpd.GeoDataFrame(geometry=unique_centroids, crs=sliced_gdf.crs)
  sliced_gdf = gpd.sjoin(sliced_gdf, unique_gdf, how='inner', predicate='intersects')
  sliced_gdf = sliced_gdf.drop_duplicates(subset='geometry')
  return sliced_gdf

def bld(swLL,neLL):
  # cutting domain
  south,west=swLL[0],swLL[1]
  north,east=neLL[0],neLL[1]
  dd={'geometry': [f'POLYGON(({west} {south}, {west} {north}, {east} {north}, {east} {south}, {west} {south}))']}
  bounds_df=pd.DataFrame(dd)
  bounds_gdf = gpd.GeoDataFrame(bounds_df, geometry=bounds_df['geometry'].apply(loads), crs="EPSG:3857")
  bbox_center = Point((west + east) / 2, (south + north) / 2)

  #read the 3d buildings
  roots='/nas2/kuang/MyPrograms/CADNA-A/OSM'
  dim=['3D','2D']
  for d in dim[:]:
    fname=f"{roots}/building{d}.csv"
    polygons_gdf = pd.read_csv(fname)
    polygons_gdf['geometry'] = polygons_gdf['geometry'].apply(loads)
    polygons_gdf = gpd.GeoDataFrame(polygons_gdf, geometry='geometry', crs="EPSG:3857")
    p = []
    for i, geom in enumerate(['Point', 'Polygon', 'MultiPolygon']):
      gdf_tmp = polygons_gdf.loc[polygons_gdf.geometry.map(lambda x: x.geom_type == geom)]
      p.append(gpd.overlay(gdf_tmp, bounds_gdf, how='intersection'))
    sliced_gdf = pd.concat(p, ignore_index=True)
    if len(sliced_gdf)>=4:
      break
  if len(sliced_gdf)==0:
    return 'no buildings'
  sliced_gdf = gpd.GeoDataFrame(sliced_gdf, geometry='geometry', crs=polygons_gdf.crs)
  sliced_gdf['mean_ll']=sliced_gdf.geometry.centroid
  if 'maxAltitude' not in sliced_gdf.columns: sliced_gdf['maxAltitude'] = 5
  sliced_gdf['maxAltitude'] = sliced_gdf['maxAltitude'].fillna(5)

# drop duplicate
  # sliced_gdf=drop_dup(sliced_gdf)
  mean_ll_series = sliced_gdf.geometry.copy()
  unique_centroids = mean_ll_series.unique()
  unique_gdf = gpd.GeoDataFrame(geometry=unique_centroids, crs=sliced_gdf.crs)
  sliced_gdf = gpd.sjoin(sliced_gdf, unique_gdf, how='inner', predicate='intersects')
  sliced_gdf = sliced_gdf.drop_duplicates(subset='geometry')

  if len(sliced_gdf) > 500:
    sliced_gdf['distance'] = sliced_gdf.geometry.distance(bbox_center)
    sliced_gdf = sliced_gdf.sort_values('distance').head(500)
  grid_df=cut_data (swLL,neLL)
  pnts_tw,pnts_ll,data_arr,ll_tree=grid_prep (grid_df)

  #coord transformation
  sliced_gdf.maxAltitude=[float(i) for i in sliced_gdf.maxAltitude]
  sliced_gdf['geometry_twd97']=''
  point_tw=query_p(bbox_center,pnts_tw,pnts_ll,ll_tree)
  Xcent, Ycent = point_tw.x, point_tw.y
  pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
  lat_0=bbox_center.y, lon_0=bbox_center.x, x_0=Xcent, y_0=Ycent)
  sliced_gdf['elevation']=[float(i) for i in query_e(sliced_gdf.mean_ll,data_arr,ll_tree)]
  p=sliced_gdf.loc[sliced_gdf.geometry.map(lambda x: x.geom_type=='Polygon')]
  if len(p)>0:
    plg=list(p.geometry)
    sliced_gdf.loc[p.index,'geometry_twd97']=[query_g(i,pnyc) for i in plg]
  m=sliced_gdf.loc[sliced_gdf.geometry.map(lambda x: x.geom_type=='MultiPolygon')]
  if len(m)>0:
    mplg=list(m.geometry)
    sliced_gdf.loc[m.index,'geometry_twd97']=[query_mp(i,pnyc) for i in mplg]
  s=sliced_gdf.loc[sliced_gdf.geometry.map(lambda x: x.geom_type=='Point')]
  if len(s)>0:
    points=list(s.geometry)
    sliced_gdf.loc[s.index,'geometry_twd97']=[query_g2(i,pnyc) for i in points]

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
