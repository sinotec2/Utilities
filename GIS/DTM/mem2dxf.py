import numpy as np
import matplotlib
matplotlib.use('Agg')  # 使用 Agg 后端
import matplotlib.pyplot as plt
import tempfile as tf
from io import BytesIO
import ezdxf
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment

# Create a new DXF document.

def rd_mem(shape):
  fnames=['lat','lon','data']
  d = []
  for f in fnames:
    filename = f+'.dat'
    d.append(np.memmap(filename, dtype='float32', mode='r', shape=shape))
  return d

def dxf(swLL,neLL):
  with open('params.txt','r') as f:
    line=[i.strip('\n') for i in f][0]
  x0,y0,nx,ny,dx,dy=(float(i) for i in line.split())
  nx,ny=int(nx),int(ny)
  shape=(ny, nx)
  lat,lon,data=rd_mem(shape)
  data = np.where(data < 0, 0, data)
  idx=np.where((lat>=swLL[0])&(lat<=neLL[0])&(lon>=swLL[1])&(lon<=neLL[1]))
  if len(idx[0])==0:
    return 'LL not right!',list(swLL)+list(neLL)
  x=[x0+dx*i for i in range(nx)]
  y=[y0+dy*i for i in range(ny)]
  xg, yg = np.meshgrid(x, y)
  bounds=[np.min(xg[idx[0],idx[1]]),np.max(xg[idx[0],idx[1]]),np.min(yg[idx[0],idx[1]]),np.max(yg[idx[0],idx[1]])]
  ib=[x.index(bounds[0]),x.index(bounds[1]),y.index(bounds[2]),y.index(bounds[3])]
  cmin=data[ib[2]:ib[3]+1,ib[0]:ib[1]+1].min()
  cmax=data[ib[2]:ib[3]+1,ib[0]:ib[1]+1].max()
  doc = ezdxf.new(dxfversion="R2010")
  clrs={5:colors.RED,1:colors.BLUE}
  for intv in [5,1]:
    N=int((cmax-cmin)//5)
    if N == 0 :continue
    levels = np.linspace(cmin, cmax, N)
    fig, ax = plt.subplots()
    cs=ax.contour(x[ib[0]:ib[1]+1],y[ib[2]:ib[3]+1],data[ib[2]:ib[3]+1,ib[0]:ib[1]+1],levels=levels)
    N=len(cs.collections[:])
    if N==0:continue
    doc.layers.add("TEXTLAYER"+str(intv), color=clrs[intv])
    msp = doc.modelspace()
    for l in range(N):
      lines = cs.collections[l].get_paths()
      for line in lines:
        verts = line.vertices
        xv = verts[:, 0]
        yv = verts[:, 1]
        if len(xv)<=1:continue
        points=[p for p in zip(xv,yv)]
        for i in range(len(points)-1):
          msp.add_line(points[i], points[i+1], dxfattribs={"color": clrs[intv]})
      msp.add_text(
        levels[l],
        dxfattribs={
        "layer": "TEXTLAYER"
         }).set_placement(points[-1], align=TextEntityAlignment.CENTER)
  ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')
  fname='terr_'+ran+'.dxf'
  output = BytesIO()
  doc.write(output, fmt='bin')
  output.seek(0)  # 重置指针位置
  doc.saveas('./dxfs/'+fname)
  return fname,output
