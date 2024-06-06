---
layout: default
title:  DXF檔之讀寫
parent: GIS Relatives
last_modified_date: 2024-05-09 10:42:16
tags: GIS DXF
---

# DXF檔之讀寫

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

- DXF 是什麼檔案？(Adobe)
 - DXF 是Drawing Exchange Format 或Drawing Interchange Format(意譯皆為繪圖交換格式) 的縮寫，屬於向量檔案類型。
 - 許多工程師、設計師和建築師都會在產品設計階段，使用DXF 檔案格式作2D 及3D 繪圖。
 - DXF是AutoCAD DXF（Drawing Interchange Format或者Drawing Exchange Format）的簡稱，它是Autodesk公司開發的用於AutoCAD與其它軟體之間進行CAD數據交換的CAD數據文件格式。

### 緣起(wiki)

- DXF於1982年12月作為AutoCAD 1.0的一部分首次面世，用於從未公開的AutoCAD內部文件格式DWG的一種精確表示。目前Autodesk在它的網站上公布有從1994年11月發布的AutoCAD Release 13到2006年3月發布的AutoCAD 2007的DXF規範。
- 從1988年10月發布的AutoCAD Release 10開始DXF同時支持ASCII與二進位格式數據。早期的版本只支持ASCII格式。
- 隨著AutoCAD功能越來越強大，支持的對象類型越來越複雜，DXF的作用也日漸減弱。包括ACIS實體與區域在內的一些對象類型都沒有介紹。其它一些對象類型，包括AutoCAD 2006的動態塊以及所有AutoCAD vertical-market版本特有的對象，都只有部分的介紹，而且開發人員無法根據這些信息進行全面的支持。
- 幾乎所有的商用軟體開發商，包括所有的Autodesk的競爭對手都選擇DWG作為與AutoCAD進行數據交換的主要格式，他們使用的函數庫是Open Design Alliance這個非營利性業界協會對DWG文件格式進行逆向工程得到的。

### 文件結構(wiki)

ASCII格式的DXF可以用文本編輯器進行查看。DXF文件的基本組成如下所示：

1. HEADER部分：圖的總體信息。每個參數都有一個變量名和相應的值
2. CLASSES部分
  - 包括應用程式定義的類的信息，這些實例將顯示在BLOCKS、ENTITIES以及OBJECTS部分。
  - 通常不包括用於充分用於與其它應用程式交互的信息。
3. TABLES部分：這部分包括命名條目的定義(9項)。
  - Application ID（APPID）表
  - Block Recod（BLOCK_RECORD）表
  - Dimension Style（DIMSTYPE）表
  - Layer（LAYER）表
  - Linetype（LTYPE）表
  - Text style（STYLE）表
  - User Coordinate System（UCS）表
  - View（VIEW）表
  - Viewport configuration（VPORT）表
4. BLOCKS部分-這部分包括Block Definition實體用於定義每個Block的組成。
5. ENTITIES部分-這部分是繪圖實體，包括Block References在內。
6. OBJECTS部分-包括非圖形對象的數據，供AutoLISP以及ObjectARX應用程式所使用。
7. THUMBNAILIMAGE部分-包括DXF文件的預覽圖。
8. END OF FILE

## 讀寫方式

- pypi：[ezdxf](https://pypi.org/project/ezdxf/)

```python
import ezdxf
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment

# Create a new DXF document.
doc = ezdxf.new(dxfversion="R2010")

# Create new table entries (layers, linetypes, text styles, ...).
doc.layers.add("TEXTLAYER", color=colors.RED)

# DXF entities (LINE, TEXT, ...) reside in a layout (modelspace, 
# paperspace layout or block definition).  
msp = doc.modelspace()

# Add entities to a layout by factory methods: layout.add_...() 
msp.add_line((0, 0), (10, 0), dxfattribs={"color": colors.YELLOW})
msp.add_text(
    "Test", 
    dxfattribs={
        "layer": "TEXTLAYER"
    }).set_placement((0, 0.2), align=TextEntityAlignment.CENTER)

# Save the DXF document.
doc.saveas("test.dxf")
```