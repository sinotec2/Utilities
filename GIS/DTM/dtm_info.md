---
layout: default
title:  dtm檔案收集情況
parent: DTM and Relatives
grand_parent: GIS Relatives
last_modified_date: 2024-06-05 09:17:56
tags: dtm GIS
---

# dtm檔案收集情況
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
## 背景

### 內政部2012

- 解析度：30m (28.88m)
- path `/home/QGIS/Data/dtm`
- filename: `twdtm_asterv2_30m-tm2_twd97.tif`
- same: `taiwan.tif`

```bash
$ tiffinfo twdtm_asterv2_30m-tm2_twd97.tif
TIFFReadDirectory: Warning, twdtm_asterv2_30m-tm2_twd97.tif: unknown field with tag 33550 (0x830e) encountered.
TIFFReadDirectory: Warning, twdtm_asterv2_30m-tm2_twd97.tif: unknown field with tag 33922 (0x8482) encountered.
TIFFReadDirectory: Warning, twdtm_asterv2_30m-tm2_twd97.tif: unknown field with tag 42112 (0xa480) encountered.
TIFFReadDirectory: Warning, twdtm_asterv2_30m-tm2_twd97.tif: unknown field with tag 42113 (0xa481) encountered.
TIFF Directory at offset 0x21559648 (559257160)
  Image Width: 14400 Image Length: 19224
  Tile Width: 128 Tile Length: 128
  Bits/Sample: 16
  Sample Format: signed integer
  Compression Scheme: None
  Photometric Interpretation: min-is-black
  Samples/Pixel: 1
  Planar Configuration: single image plane
  Tag 33550: 28.884201,28.884201,0.000000
  Tag 33922: 0.000000,0.000000,0.000000,42033.952431,2878094.424011,0.000000
  Tag 42112: <GDALMetadata>
  <Item name="PyramidResamplingType" domain="ESRI">NEAREST</Item>
  <Item name="STATISTICS_MINIMUM" sample="0">0</Item>
  <Item name="STATISTICS_MAXIMUM" sample="0">3893</Item>
  <Item name="STATISTICS_MEAN" sample="0">125.13239506028</Item>
  <Item name="STATISTICS_STDDEV" sample="0">438.65405799382</Item>
</GDALMetadata>

  Tag 42113: 32767
```

- `taiwan2.tiff`解析度與範圍都一樣，似乎為格式版本的差異(tif vs tiff)

```bash
kuang@master /home/QGIS/Data/dtm
$ tiffinfo taiwan2.tiff
TIFFReadDirectory: Warning, taiwan2.tiff: unknown field with tag 33550 (0x830e) encountered.
TIFFReadDirectory: Warning, taiwan2.tiff: unknown field with tag 33922 (0x8482) encountered.
TIFFReadDirectory: Warning, taiwan2.tiff: unknown field with tag 42113 (0xa481) encountered.
TIFF Directory at offset 0x210266e4 (553805540)
  Image Width: 14400 Image Length: 19224
  Bits/Sample: 16
  Sample Format: signed integer
  Compression Scheme: None
  Photometric Interpretation: min-is-black
  Samples/Pixel: 1
  Rows/Strip: 1
  Planar Configuration: single image plane
  Tag 33550: 28.884201,28.884201,0.000000
  Tag 33922: 0.000000,0.000000,0.000000,42033.952431,2878094.424011,0.000000
  Tag 42113: 32767
```

### 內政部2016

- 解析度：20m

```bash
kuang@master /home/QGIS/Data/dtm_20mTaiPenhu
$ tiffinfo dem_20m.tif
TIFFReadDirectory: Warning, dem_20m.tif: unknown field with tag 33550 (0x830e) encountered.
TIFFReadDirectory: Warning, dem_20m.tif: unknown field with tag 33922 (0x8482) encountered.
TIFFReadDirectory: Warning, dem_20m.tif: unknown field with tag 34735 (0x87af) encountered.
TIFFReadDirectory: Warning, dem_20m.tif: unknown field with tag 34736 (0x87b0) encountered.
TIFFReadDirectory: Warning, dem_20m.tif: unknown field with tag 34737 (0x87b1) encountered.
TIFFReadDirectory: Warning, dem_20m.tif: unknown field with tag 42113 (0xa481) encountered.
TIFF Directory at offset 0x1730edde (389082590)
  Image Width: 10175 Image Length: 19112
  Bits/Sample: 16
  Sample Format: signed integer
  Compression Scheme: None
  Photometric Interpretation: min-is-black
  Samples/Pixel: 1
  Rows/Strip: 1
  Planar Configuration: single image plane
  Tag 33550: 20.000000,20.000000,0.000000
  Tag 33922: 0.000000,0.000000,0.000000,148310.000000,2801730.000000,0.000000
  Tag 34735: 1,1,0,17,1024,0,1,1,1025,0,1,1,1026,34737,8,0,2048,0,1,4326,2049,34737,7,8,2054,0,1,9102,2057,34736,1,6,2059,34736,1,5,3072,0,1,32767,3074,0,1,32767,3075,0,1,1,3076,0,1,9001,3080,34736,1,1,3081,34736,1,0,3082,34736,1,3,3083,34736,1,4,3092,34736,1,2
  Tag 34736: 0.000000,121.000000,0.999900,250000.000000,0.000000,298.257224,6378137.000000
  Tag 34737: unnamed|WGS 84|
  Tag 42113: -32767
```

### 內政部2020

- 解析度：20m
```bash
kuang@master /home/QGIS/Data/dtm_20mTaiPenhu/2020台灣本島及離島(小琉球、龜山島、綠島及蘭嶼)
$ tiffinfo taiwan2020.tif
TIFFReadDirectory: Warning, taiwan2020.tif: unknown field with tag 33550 (0x830e) encountered.
TIFFReadDirectory: Warning, taiwan2020.tif: unknown field with tag 33922 (0x8482) encountered.
TIFFReadDirectory: Warning, taiwan2020.tif: unknown field with tag 34735 (0x87af) encountered.
TIFFReadDirectory: Warning, taiwan2020.tif: unknown field with tag 34736 (0x87b0) encountered.
TIFFReadDirectory: Warning, taiwan2020.tif: unknown field with tag 34737 (0x87b1) encountered.
TIFFReadDirectory: Warning, taiwan2020.tif: unknown field with tag 42113 (0xa481) encountered.
TIFF Directory at offset 0x2d1a9eb8 (756719288)
  Image Width: 10035 Image Length: 18852
  Bits/Sample: 32
  Sample Format: IEEE floating point
  Compression Scheme: None
  Photometric Interpretation: min-is-black
  Orientation: row 0 top, col 0 lhs
  Samples/Pixel: 1
  Rows/Strip: 1
  SMin Sample Value: -24.28
  SMax Sample Value: 3947.27
  Planar Configuration: single image plane
  Tag 33550: 20.000000,20.000000,1.000000
  Tag 33922: 0.000000,0.000000,0.000000,150980.000000,2799160.000000,0.000000
  Tag 34735: 1,1,0,31,1024,0,1,1,1025,0,1,2,1026,34737,13,0,2048,0,1,4326,2054,0,1,9102,2056,0,1,7030,2057,34736,1,0,2058,34736,1,1,2059,34736,1,2,3072,0,1,32767,3074,0,1,32767,3075,0,1,1,3076,0,1,9001,3078,34736,1,3,3079,34736,1,4,3080,34736,1,5,3081,34736,1,6,3082,34736,1,7,3083,34736,1,8,3084,34736,1,9,3085,34736,1,10,3086,34736,1,11,3087,34736,1,12,3088,34736,1,13,3089,34736,1,14,3090,34736,1,15,3091,34736,1,16,3092,34736,1,17,3094,34736,1,18,3095,34736,1,19,4099,0,1,9001
  Tag 34736: 6378137.000000,6356752.314245,298.257224,0.000000,0.000000,121.000000,0.000000,250000.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.999900,0.000000,0.000000
  Tag 34737: GCS_WGS_1984|
  Tag 42113: -32767
```