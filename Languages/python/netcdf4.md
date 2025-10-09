netCDF格式

NetCDF[^80] (Common Data Form)
的發展雖然以美國大氣科學研究性之資料應用為開始，然而其自我說明及相容性等優點，歷經十數年的發展，已經擴散到許多國家、應用在舉凡出現大型陣列資料庫性質之不同領域中，其在國內的發展值得進一步觀察。目前已經出到netCDF
4.3.22 (2014/5/27)

netCDF簡介

netCDF之背景

Unidata為美國國家科學委員會資助之計畫，其服務之對象為美國之大學及研究所，經由協助其電腦與網路之應用，將大氣及其他資料作最佳的運用，以增進研究與教學之效益。為顯示及計算這些資料，各研究單位可能原有其系統，Unidata則作為一基礎之資料界面，各單位於其上發展個別的軟體並進行存取管理等作業，而在底層資料的格式上有所統一。

最早共通資料格式(Common Data
Form)的用意，是在Unidata計畫中不同的應用項目下，提供一種可以通用的資料存取方式，資料的形狀包括單點的觀測值、時間序列、規則排列的網格、以及人造衛星或雷達之影像檔案。其自行說明表頭的理念是參照NASA
Goddart國家太空資料中心在1987年所發表的論文。而隨著陸續的發展，現已發展到第3.4版。

NetCDF軟體的功能，在於提供C、Fortran、C++、Perl、java或其他語言I/O的程式庫，以讓程式發展者可以讀寫資料檔案，其本身具有說明的能力、並且可以跨越平台和機器的限制。每一個netCDF檔案可以含括多維度的、具有名稱的變數，包括長短的整數、單倍與雙倍精度的實數、字元等，且每一個變數都有其自我介紹的資料，包括量度的單位、全名及意義等文字說明，在此摘要性的檔頭之後，才是真正的資料本身。

NetCDF與一般資料庫管理系統的比較

由於一般資料庫管理系統之套裝軟體(如ms-ACCESS或Excel)，對於大氣等陣列式的大型資料無法有效的處理，理由有幾：

資料密度問題

既有的套裝軟體並不將多維度的陣列，當作處理時單一的基本資料元素，若將多維度的陣列，以關連性相連，會將原本非常有用的資料，變得一無是處，對於提供特定維度條件下摘要性的資訊，也無能為力。遑論其他存取、修改、計算、乃至繪圖等功能。

對於大型陣列資料而言之，這些套裝軟體的處理能力也較低，諸如衛星資料、全球之長期氣象資料、以及模式所輸出的四階多變數資料等。

不必要的統計

一般套裝軟體所提供的功能，如報表的格式化、資料鍵入更新之界面、稽核與不必要的統計，對處理大型陣列之資料，是多餘且不必要的。

### netCDF在國內外應用的情形

由於netCDF使用暱名資料傳輸的方式，因此並不容易統計實際使用者的個數。然而由netCDFgroup的郵件清單上，已經有分散在15個國家的500個地址，其中有好幾個單位已經採用netCDF當作其標準的科學資料格式。由下載時所留下的電子郵件地址來看，自從1997年5月以來，已經有超過55個國家，2,000個單位的使用者，由網路下載netCDF軟體。使用的機器由最複雜的超級電腦到一般的個人電腦。

由經常支援回答問題的機構中約有25個，其中與環境或空氣污染較有關係的單位有：

- **[The Models-3 Project]{.underline}**, being cooperatively pursued by
the EPA's Atmospheric Research Laboratory and by North Carolina
Supercomputing Center

**[NOAA's]{.underline}** Climate Diagnostics Center (CDC),

The Southern Regional Climate Center (**[A NOAA/NWS]{.underline}**
funded center)

NOAA's Forecast System Laboratory

The Computer Planning Committee of NOAA's Pacific Marine Environmental
Laboratory (P**[MEL]{.underline}**)

The **[TAO]{.underline}** Project Office, at PMEL

The global ocean modeling group at **[Los Alamos National
Laboratory]{.underline}** (LANL),

Lamont-Doherty Earth Observatory of Columbia University

The **[Generic Mapping Tool]{.underline}**s (GMT), a unix -based set of
tools for data manipulation and display using PostScript,

A group in the Atmospheric Chemistry Division at **[NCAR]{.underline}**
(the National Center for Atmospheric Research) that deals with UARS
(Upper Atmospheric Research Satellite) data

**[NCAR's]{.underline}** Research Data Program for data archived and
used in the **[Zebra display]{.underline}** and analysis system.

The Cooperative Program for Operation Meteorology, Education, and
Training (**[COMET]{.underline}**), a program of UCAR

The Earth Scan Lab, an HRPT ground station at Coastal Studies Institute

The **[Woods Hole Field Center of the U.S.G.S]{.underline}**. Marine and
Coastal Geology Program

At the Woods Hole Oceanographic Institution

The **[Oregon State University]{.underline}** Oceanographic Research
Vessel WECOMA

The **[Arkansas Red-Basin River Forecast]{.underline}** Center

The CSIRO Division of Atmospheric Research in Australia

**[CIRES]{.underline}** (Cooperative Institute for Research in the
Environmental Sciences)

我國目前引進此一格式之單位很多，經網路上搜尋結果，至少台大大氣系已引入美國netCDF格式之氣象資料，並張貼有關netCDF之網站消息與討論。

### python-netCDF4系統

netCDF經常被使用在大氣科學領域的分析[^81]及繪圖[^82]，除了讀取應用之外，如何改寫、新創檔案亦非常重要。

netCDF的讀取及轉換

netCDF的數據、維度與其他屬性資料均整合在Dataset的模組之中，以下範例為m3
IO/API檔案轉換成pandas dataframe的格式，方便在python中進行各項操作。

```python
/home/SMOKE4.5/data/run_teds9_13/output/merge% cat ncf2df.py
import netCDF4
from pandas import *
def ncf2df(fname):
	nc = netCDF4.Dataset(fname)
	cols=list(nc.variables) #note 1
	d={}
	for c in cols:
		if c=='TFLAG':continue #note 2
		a=list(nc.variables[c]) #note 3
		for i in xrange(3):
			if len(a)==1: #note 4
				a=[x for x in a[0]]
			else:
				break
		a=[x[0] for x in a]
		d.update({c: a})
	return DataFrame(d)
```

note1:nc檔案的**variables.keys()**就是變數名稱，因此就是DataFrame的**columns**。Note2:其中若有**time**或者是**TFLAG**可能是無資訊的序號，沒有必要留存。**nc.variables[c]**可能是有好幾個維度的陣列，要逐一的拆解成一維的序列，方便成為資料表的形態，這是note3\~4在做的事情，通常可以由**nc.dimension**得知，如一般m3檔案的維度：

```python
In [5]: a.dimensions
Out[5]:
OrderedDict([(u'TSTEP', <netCDF4.Dimension at 0x2b6fe004b910>),
(u'DATE-TIME', <netCDF4.Dimension at 0x2b6ffece8cd0>),
(u'LAY', <netCDF4.Dimension at 0x2b6ffece8c80>),
(u'VAR', <netCDF4.Dimension at 0x2b6ffece8c30>),
(u'ROW', <netCDF4.Dimension at 0x2b6ffece8be0>),
(u'COL', <netCDF4.Dimension at 0x2b6ffece8b40>)])
```

變數的屬性存在個別變數的**collections.OrderedDict**之中，如：
```python
In [9]: for c in cols:
\...: print nc.variables[c]
\...:
<type 'netCDF4.Variable'>
int32 **TFLAG**(TSTEP, VAR, DATE-TIME)
units: <YYYYDDD,HHMMSS>
long_name: TFLAG
var_desc: Timestep-valid flags: (1) YYYYDDD or (2) HHMMSS
unlimited dimensions: TSTEP
current shape = (1, 16, 2)
filling off

In [14]: for c in cols:
\...: print nc.variables[c].**long_name**,nc.variables[c].**shape**
\...:
TFLAG (1, 16, 2)
ISTACK (1, 1, 1459, 1)
LATITUDE (1, 1, 1459, 1)
LONGITUDE (1, 1, 1459, 1)
STKDM (1, 1, 1459, 1)
STKHT (1, 1, 1459, 1)
STKTK (1, 1, 1459, 1)
STKVE (1, 1, 1459, 1)
STKFLW (1, 1, 1459, 1)
STKCNT (1, 1, 1459, 1)
ROW (1, 1, 1459, 1)
COL (1, 1, 1459, 1)
XLOCA (1, 1, 1459, 1)
```

 不同維度的內容分開存檔：

```python
fname='M-A0064-084.nc'
nc = netCDF4.Dataset(fname)
cols=list(nc.variables) #note 1
for ishp in [1,2,3]:
	d={}
	for c in cols:
		shp=nc.variables[c].shape
		if len(shp) !=ishp:continue
		a=list(nc.variables[c]) #note 3
		for i in range(3):
			if len(a)==1: #note 4
				a=[x for x in a[0]]
			else:
				break
		a=np.array(a[:])
	d.update({c: a.flatten()})
	df=DataFrame(d)
	df.to_csv(fname+str(ishp)+'.csv')
```

netCDF的修改與創檔

netCDF檔案有2個必要的元素，維度及變數，前者是矩陣的架構，後者則是矩陣的實質內容。二者的創檔指令皆為**creact**：

```python
In [19]: f=Dataset("ppso2PnG.nc","**w**")

\...: f.createDimension("y",381)

\...: f.createDimension("x",536)

\...: **xx**=f.createVariable("x","f4",("x",))

\...: yy=f.createVariable("y","f4",("y",))

\...: f.variables['x'][:]=x

\...: f.variables['y'][:]=y

\...: xx.long_name='x'; xx.units='degree
east';yy.long_name='y';yy.units='degree north'

\...: **zz**=f.createVariable('SO2_PnG',"f4",("y","x",))

\...: f.variables['SO2_PnG'][:,:]=za

\...: zz.long_name='emission for PowerPlant '

\...: zz.units='ton per year'

\...: f.close()
```

檔案開啟方式

此處Dataset實體必須以'w'或者'r+'方式開啟，否則一般netCDF的檔案的變數名稱、維度及長度等都是不容改變的。

維度設定方式

範例中.createDimension("y",**381**)的2個引數前者為維度名稱，後者則是大小，如果要讓netCDF可以增減筆數，則以**None**取代數字即可。如此在維度處就會出現「unlimited」，一般以時間維度最長使用此一形式，以變讓檔案可以增加內容。

變數設定方式

在.createVariable的指定過程中，xx及yy分別是東西及南北軸向的名稱，本身是1維的序列，在檔案內的名稱分別是x及y，在python中命名為xx,yy是有別於python內既有的序列，同時也方便賦予適當的屬性內容。

f4是單精度實數，雙精度為f8，同時若為整數、字串、判別等也需逐一給定[^83]。

第3個引數則連結到前述的維度，每個維度之後都要加一個,。

變數給定方式

接下來則給定數據予各個變數，可以(必須)用批次方式給定。因為若是循矩陣的維度逐一修改，會呼叫非常多次Dataset模組，花費太多時間，因此，必須先另行產生同樣大小的矩陣，一次填入Dataset中，如此才能提升程式的效率。

由於給定過程適用回溯給定(範例中不論是命名為xx,yy,zz，有關xx,yy,zz的任何改變都會回溯到f的實體)，因此程式設計時要注意各個變數的實體內容是什麼，如果不希望程式有回溯的可能，最好要將netCDF的實體轉變成別種型態(type)的實體，才不致於出錯。過程中如果有不確定變數的實體是什麼，可以用type()指令了解。

### 檔案關閉及儲存

最後則以**.close()**關閉並儲存nc檔案。關閉後即不能再更動內容。

## 範例：REAS排放[^84]資料文字檔轉nc檔

由於學術科研領域有關nc檔案的應用軟體非常豐富(如NCO[^85]及GMT[^86])，若獨立研發將重複浪費，因此將檔案轉成nc格式將有諸多好處，以下範例即為REAS排放量數據txt檔案轉成nc格式之工具：

```python
kuang@master /nas1/camxruns/2018/emis/REAS2.1
$ cat ./origins/txt2nc.py
from netCDF4 import Dataset
from pathlib import Path
fname='all_file.nam'
with open(fname) as ftext:
	fnames=[line.strip('\\n') for line in ftext]
coord_file = Path("./coord.txt")
try:
	my_abs_path = coord_file.resolve()
except FileNotFoundError:
	print 'generating nx,ny,x0,y0\...'
	# doesn't exist
	x0,y0=set(),set()
	for fname in fnames:
		# if stop==1:break
		with open(fname) as text_file:
			d=[line.strip('\\n').split() for line in text_file]
		f1=int(d[0][0])
		x0=set([d[l][0] for l in xrange(f1,len(d))])\|x0
		y0=set([d[l][1] for l in xrange(f1,len(d))])\|y0
		x0=[float(i) for i in x0];x0.sort()
		y0=[float(i) for i in y0];y0.sort()
		nx,ny=int((x0[-1]-x0[0])/0.25)+1,int((y0[-1]-y0[0])/0.25)+1
		x0=[x0[0]+0.25*float(i) for i in xrange(nx)]
		y0=[y0[0]+0.25*float(i) for i in xrange(ny)]
		with open('coord.txt','w') as ftext:
			ftext.write( "%s" % str(nx)+' '+str(ny)+'\\n')
			for i in xrange(nx):
				ftext.write( "%s" % str(x0[i])+' ')
				ftext.write( "%s" % '\\n')
				for i in xrange(ny):
					ftext.write( "%s" % str(y0[i])+' ')
else:
	print 'reading nx,ny,x0,y0\...'
# exists
with open('coord.txt','r') as ftext:
	d=[line.strip('\\n').split() for line in ftext]
nx,ny=int(d[0][0]),int(d[0][1])
x0=[float(d[1][i]) for i in xrange(nx)]
y0=[float(d[2][i]) for i in xrange(ny)]
stop=0
z_nam=['z'+str(i) for i in xrange(1,13)]
z=[]
for i in xrange(12):
	z.append([])
	for m in xrange(12):
		for j in xrange(ny):
			z[m].append(nx*[0.])
for fname in fnames:
	if stop==1:break
	with open(fname) as text_file:
		d=[line.strip('\\n').split() for line in text_file]
	print fname
	f1=int(d[0][0])
for l in xrange(**f1**,len(d)):

i=x0.index(float(d[l][0]))

j=y0.index(float(d[l][1]))

for m in xrange(12):

z[m][j][i]=float(d[l][m+2])

f=Dataset(fname+".nc","w")

f.createDimension("x",nx)

f.createDimension("y",ny)

x=f.createVariable("x","f4",("x",))

y=f.createVariable("y","f4",("y",))

z_n=[]

for i in xrange(12):

z_n.append(f.createVariable(z_nam[i],"f4",("y","x",)))

f.variables['x'][:]=x0

f.variables['y'][:]=y0

x.long_name='x'

x.units='degree east'

y.long_name='y'

y.units='degree north'

for m in xrange(12):

**f.variables[z_nam[m]][:,:]=z[m]**

z_n[m].long_name='emission for month of '+str(m+1)

z_n[m].units='Ton per year'

f.close()

# stop=1
```

範例中以底色做為區段分割以利說明：

第1段落

為模組宣告及檔案名稱之輸入。

第2段

主要的作用在產生足夠大的座標系統範圍。由於REAS並不是每一個污染物的範圍都一樣，如果沒有共同的範圍會發生組合上的困難，因此須先全部讀一遍，才能找出最大的範圍。

第3段

先是宣告一個3維的空白矩陣做為容器。然後逐一開啟REAS文字檔，並讀入每一行的內容。由於txt檔具有表頭，其行數記錄在表頭的第一個數字(f1)，這將做為重要的行數指標。

第4段

讀入3維的排放量數據z[m][j][i]，其順序是為配合GMT的習慣，以南北向先於東西向。各月份又先於水平向，以利批次輸出給Dataset。

第5段

即為前節所述的netCDF4創檔過程。由於GMT二維處理工具(此處擬用grdfilter進行正交系統的座標轉換)並不處理時間維度的問題，因此各個月份以變數形態分別儲存，屆時以ncks篩選特定月份的變數出來即可。

座標系統轉換

此處應用ncks及grdfilter進行d1及d2系統的轉換：

```bash
kuang@master /nas1/camxruns/2018/emis/REAS2.1
$ cat ./origins/d1234.cs
mon=9
LIM=(\\
98.0694874213/143.910512579/2.43777096217/44.7822290378 \\
112.572862612/129.407137388/15.8348876415/31.3851123585 \\
118.961254066/123.018745934/21.0182958805/26.2017041195 \\
119.786295683/122.193704317/21.7734648395/25.4465351605)
dx=(81 27 9 3)
dxh=(40.5 40.5 81 81)
x=(b b g g)
for f in $(cat all_file.nam);do
	ncks -v x,y,z$mon $f".nc" in.nc
	for d in 1 2;do
		n=$(( $d - 1 ))
		grdfilter in.nc -I${dx[$n]}"k" -R${LIM[$n]}
		-G$f"_d"$d".nc" -V -F$x${dxh[$n]} -D1
	done
	rm in.nc
done
```
		
LIM是以LCC投影中心點，向東西南北張開出nx/2*dx長度的經緯度範圍，先大略以地球周長計算，再以嘗試錯誤方式得到與d1\~d4相同的格點數，作法如下：

```python
peri=40075.02; peri_y=39941.
lonc,latc=120.99,23.61
lx,ly=81.63**.*360./peri,81.58.360./peri_y
print str(lonc-lx/2.)+'/'+str(lonc+lx/2.)+'/'+str(latc-ly/2.)+'/'+str(latc+ly/2.)
lx,ly=27.63./59.65.*360./peri,27.58./59.65.*360./peri_y
print str(lonc-lx/2.)+'/'+str(lonc+lx/2.)+'/'+str(latc-ly/2.)+'/'+str(latc+ly/2.)
lx,ly=9.63./59**.*47.*360./peri,9.58./59.65.*360./peri_y
print str(lonc-lx/2.)+'/'+str(lonc+lx/2.)+'/'+str(latc-ly/2.)+'/'+str(latc+ly/2.)
lx,ly=3.*6**3.5/59.83.*360./peri,3.58.5/59.137.*360./peri_y
print str(lonc-lx/2.)+'/'+str(lonc+lx/2.)+'/'+str(latc-ly/2.)+'/'+str(latc+ly/2.)
```

grdfilter的結果雖然說是新網格範圍內代表性較高的值(相較grdsample只是內插取樣)，然而其表達仍然以intensive quantity方式，而非extensive quantity，在總量上會有網格大小的比例差異，以d1而言(解析度約為0.72x0.73度)，其每一格的經緯度範圍與原有資料(0.25x0.25度)約有8\~10倍的比例差異。

```python
Delx,dely= 81.*360./peri, 81.*360./peri_y
delx*dely/(dxf*dyf)\~ 8.499
```
此值乃以赤道為基準，若在高緯度將會有嚴重的低估，應考量緯度的差異進行轉換。
