import rasterio
import numpy as np
from pyproj import Proj

fname='taiwan2018.tif'
img = rasterio.open(fname)
nx,ny,nz=img.width,img.height,img.count
data=np.flipud(img.read()[0,:,:])
x0,y0=img.xy(0,0) #center xy
transform=img.transform
dx,dy=transform.a,abs(transform.e)
y0=y0-dy*ny
x=np.array([x0+dx*i for i in range(nx)])
y=np.array([y0+dy*i for i in range(ny)])
xcent,ycent=x[nx//2],y[ny//2]
x-=xcent
y-=ycent
xg, yg = np.meshgrid(x, y)
Longitude_Pole,Latitude_Pole=img.lnglat()
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=21.8, lat_2=25.4,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
lon,lat=pnyc(xg, yg, inverse=True)
shape=(ny, nx)
fnames=['data','lon','lat']
arrays=[data,lon,lat]
for f in range(3):
  filename = fnames[f]+'.dat'
  memmap_array = np.memmap(filename, dtype='float32', mode='w+', shape=shape)
  memmap_array[:] = arrays[f][:,:]
params_str = f"{x0} {y0} {nx} {ny} {dx} {dy}\n"
with open('params.txt','w+') as f:
  f.write(params_str)
