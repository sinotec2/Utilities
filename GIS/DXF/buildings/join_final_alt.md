---
layout: default
title:  join_final_alt.py
grand_parent: DXF
parent: buildings
last_modified_date: 2024-12-08 16:24:44
tags: GIS DXF
---

# OSM建築物與內政部資訊的整併（join_final_alt.py）

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

- 建築物資料庫的整理、整併、與切割應用的工作流程如圖所示。
- 大致上整體工作區分為3大區塊，`join_pnt_bld.py`的範圍與功能，為最終整併成`3Dbuildings.csv`的重要程序。

  ![alt text](./pngs/image-1.png)

### 程式說明

[](./pys/)程式使用