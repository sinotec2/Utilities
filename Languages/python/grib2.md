---
layout: default
title: grib2
parent: python
grand_parent: Languages
last_modified_date: 2024-01-02 13:33:58
tags: UML
---

# GRIB格式之讀取分析

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

## GRIB格式之讀取分析


Grib格式是美國、歐洲、及我國氣象官方公開檔案通用的格式，應用套件很多，包括直讀的grads、繪圖軟體meteoInfo等、ncl_stable等轉換程式，python也有相對應的套件，介紹如下。

unresp(grib2)

Create3DDAT.py的安裝與修改

Python環境之設定（內設為3.6版）

conda env create -f environment.yml

Centos 6執行安裝並無困難，也可順利執行

Mac上執行有困難

Gcc/gfortran/c++等無法安裝指定的版本

將yml檔案內相對應的指標去掉，雖可通過，但執行仍然有誤，swig無法import

```bash
ModuleNotFoundError: No module named '_gribapi_swig'
```
解決方式：將環境套件整體升級到py37之**gribby**


`conda create -n gribby -c conda-forge python-**eccodes**`

-   (Grib2 with python 3.7)

-   [[https://stackoverflow.com/questions/39787578/importerror-when-using-python-anaconda-package-grib-api]{.underline}](https://stackoverflow.com/questions/39787578/importerror-when-using-python-anaconda-package-grib-api) 
              [\
    ]{.underline}

    模擬範圍之選取

    濃度場的模擬範圍、輸出入檔的目錄位置、高度氣壓座標

```python
193,200c197,206
< latMinCP = 11.7  # Min lat of CALPUFF grid
< latMaxCP = 12.2  # Max lat of CALPUFF grid
< lonMinCP = 273.2  # Min lon of CALPUFF grid
< lonMaxCP = 274.1  # Max lon of CALPUFF grid
< inDir = '../NAM_data/raw/'+date  # Directory containing GRIB
files
< nfiles = 17 #Number of GRIB files (files are 3 hourly, so 48 hours
is 17 files including hours 0 and 48)
< outFile = '../NAM_data/processed/met_'+date+'.dat' #Output
file path
< levsIncl =
[1000,950,925,900,850,800,700,600,500,400,300,250,200,150,100,75,50,30,20,10,7,5,2]
#pressure levels to include in output
\-\--
> latMinCP = 21.4    # Min lat of CALPUFF grid
> latMaxCP = 25.7   # Max lat of CALPUFF grid
> lonMinCP = 119.4   # Min lon of CALPUFF grid
> lonMaxCP = 122.4   # Max lon of CALPUFF grid
> inDir = 
'/home/kuang/MyPrograms/UNRESPForecastingSystem/CWB_data/raw/'+date 
# Directory containing GRIB files
> nfiles = 15 #Number of GRIB files (files are 6 hourly, so 84 hours
is 15 files including hours 0 and 48)

> outFile
='/home/kuang/MyPrograms/UNRESPForecastingSystem/CWB_data/processed/met_'+date+'.dat'
#Output file path
> if os.path.isfile(outFile):
>     sys.exit('exist outFile: '+outFile)
> levsIncl = [1000,925,850,700,500,400,300,250,200,150,100]
#pressure levels to include in output
```

座標系統的調整轉換（經緯度twd97 VS LCP）

原程式是以gribapi模組中的grib_get_array來解讀格點經緯度與格點數，解讀的對象是任意的2維變數(如海平面氣壓PRMSL)

求取不同經緯度：適用在以經緯度為座標軸的等度數網格系統

然在小範圍模擬一般是以等距離、正交之直角座標系統，其座標點的經緯度將會是2個2維陣列

由於格點位置及格點數並無會每一次不一樣，由固定的一個檔來提供似乎比較單純合理。(修改程式gribapi似更複雜)

```python
< lats = gribapi.grib_get_array(gidPRMSL,'distinctLatitudes')
< lons = gribapi.grib_get_array(gidPRMSL,'distinctLongitudes')
< Ni = gribapi.grib_get(gidPRMSL,'Ni')
< Nj = gribapi.grib_get(gidPRMSL,'Nj')
---
> ishp=2
>
CSV='/home/kuang/MyPrograms/UNRESPForecastingSystem/data/M-A0064nc2.csv'
> df=read_csv(CSV)
> #lats =
gribapi.grib_get_array(gidPRMSL,'distinctygrid')#Latitudes')
> #lons = gribapi.grib_get_array(gidPRMSL,'distinctLongitudes')
> lats = np.array(list(df.gridlat_0))
> lons = np.array(list(df.gridlon_0))
> Ni = 1158
> Nj = 673
```
 

- 濃度場模擬範圍在氣象場中相對位置與切割

    -   原來的網格是等間距經緯度系統，因此其取網格是1維線性切割、四角經緯度為其向量中之某一值

    -   直角座標4角經緯度，為所有點中，最接近該4點位置的點座標中得知。


```python
< for i in range(len(lats)-1):
if lats[i+1] >= latMinCP:
 **iLatMinGRIB**=i
 break
for i in range(len(lats)-1):
if lats[i+1] > latMaxCP:
 **iLatMaxGRIB**=i+1
 break
for i in range(len(lons)-1):
if lons[i+1] >= lonMinCP:
 **iLonMinGRIB**=i
 break
for i in range(len(lons)-1):
if lons[i+1] > lonMaxCP:
 **iLonMaxGRIB**=i+1
 break
\-\--

> XY=np.array([twd97.fromwgs84(i,j) for i,j in
zip(lats,lons)],dtype=int)
> twd97X,twd97Y=(XY[:,i] for i in [0,1])
> XminCP,YminCP=(int(i) for i in
twd97.fromwgs84(latMinCP,lonMinCP))
> XmaxCP,YmaxCP=(int(i) for i in twd97.fromwgs84(latMaxCP,lonMaxCP))
> DIST =(twd97X-XminCP)**2+(twd97Y-YminCP)**2
> minD=min(DIST)
> ji=list(DIST).index(minD)
> **ijLLMinGRIB** = ji
> **iLatMinGRIB** = int(ji/Ni)
> **iLonMinGRIB** = ji - Ni * iLatMinGRIB
> DIST =(twd97X-XmaxCP)**2+(twd97Y-YmaxCP)**2
> minD=min(DIST)
> ji=list(DIST).index(minD)
> **ijLLMaxGRIB** = ji
> **iLatMaxGRIB** = int(ji/Ni)
> **iLonMaxGRIB** = ji - Ni * iLatMaxGRIB
-   格點座標值由1維增加為(實質)2維
			78,81c80,83
RXMIN = lons[iLonMinGRIB]  # W-most E longitude
RXMAX = lons[iLonMaxGRIB]  # E-most E longitude
RYMIN = lats[iLatMinGRIB]  # S-most N latitude
RYMAX = lats[iLatMaxGRIB]  # N-most N latitude
\-\--
> RXMIN = lons[ijLLMinGRIB]  # W-most E longitude
> RXMAX = lons[ijLLMaxGRIB]  # E-most E longitude
> RYMIN = lats[ijLLMinGRIB]  # S-most N latitude
> RYMAX = lats[ijLLMaxGRIB]  # N-most N latitude
97c99
 XLATDOT = lats[iLatMinGRIB+j]  # N latitude of grid point

\-\--

> XLATDOT = lats[ijLLMinGRIB+j*Ni]  # N latitude of grid
point

100c102
	 XLONGDOT = lons[iLonMinGRIB+i]  # E longitude of grid
point
\-\--
>	 XLONGDOT = lons[ijLLMinGRIB+i]  # E longitude of grid
point
```



```python
-   檔案名稱系統
    -   舊檔名系統是逐3小時。修改為6小時間隔之˙檔名系統。
 filePrefix = 'nam.t00z.afwaca'
 fileSuffix = '.tm00.grib2'
\-\--
> filePrefix = 'M-A0064-0'
> fileSuffix = '.grb2'
209c215
  filenames.append(filePrefix+'{:02d}'.format(i3**)+fileSuffix)

\-\--

>   
 filenames.append(filePrefix+'{:02d}'.format((i)6**)+fileSuffix)

ecwmf(grib1)
```

## note
grib1檔案雖然目前已經不多了，但ecmwf似乎沒有要進版的意思。由於ecmwf的檔案並非等間距，無法直接轉成nc
檔案進一步處理。此處使用**eccode**指令，先將grib1檔案轉成ASCII檔，經切割時間之後，再逐一進行空間的切割，內插到直角座標系統上進行繪圖。
