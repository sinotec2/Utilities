---
layout: default
title:  ezdxf的座標系統
parent: DTM and Relatives
grand_parent: GIS Relatives
last_modified_date: 2024-06-05 09:17:56
nav_order: 99
tags: ezdxf GIS ocr
---

# ezdxf的座標系統

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

- [使用手冊]((https://ezdxf.readthedocs.io/en/stable/concepts/coordinates.html))
  - object coordinate system (OCS)
  - User coordinate system (UCS)
- [Tutorial](https://ezdxf.readthedocs.io/en/stable/tutorials/ocs_usage.html)

item|num
-|-
`[e for e in doc.modelspace()]`|3858
`[e for e in msp if e.dxf.layer=='98112']`|301
`len([e for e in msp if e.dxf.layer=='98112' and e.dxftype()=='POLYLINE'])`|277(其餘為`e.dxftype()`為`'TEXT'`)
`set([i.plain_text() for i in txt.plain_text()`|26~97共17個不連續值
`set([i.plain_text() for i in [e for e in msp if e.dxf.layer=='98111' and e.dxftype()=='TEXT']])`|20~95每隔5之整數字元、分散在65條`POLYLINE`
`[i for i in e.points()][:5]`|`[Vec3(313858.7020155214, 2771736.841981305, 86.0),...]` ('TEXT'沒有`points()`)
`e.dxf.elevation`|`Vec3(0.0, 0.0, 86.0)`
`e.get_mode()`|`'AcDb2dPolyline'`


### WCS to OCS

```python
def wcs_to_ocs(point):
    px, py, pz = Vec3(point)  # point in WCS
    x = px * Ax.x + py * Ax.y + pz * Ax.z
    y = px * Ay.x + py * Ay.y + pz * Ay.z
    z = px * Az.x + py * Az.y + pz * Az.z
    return Vec3(x, y, z)
```

### OCS to WCS

```python
Wx = wcs_to_ocs((1, 0, 0))
Wy = wcs_to_ocs((0, 1, 0))
Wz = wcs_to_ocs((0, 0, 1))

def ocs_to_wcs(point):
    px, py, pz = Vec3(point)  # point in OCS
    x = px * Wx.x + py * Wx.y + pz * Wx.z
    y = px * Wy.x + py * Wy.y + pz * Wy.z
    z = px * Wz.x + py * Wz.y + pz * Wz.z
    return Vec3(x, y, z)
```

### e.ocs()

```python
['from_wcs',
 'points_from_wcs',
 'points_to_wcs',
 'render_axis',
 'to_wcs',
 'transform',
 'ux',
 'uy',
 'uz']
```

## Tutorial for OCS/UCS Usage

### Placing 2D Circle in 3D Space

```python
import ezdxf
from ezdxf.math import OCS

doc = ezdxf.new('R2010')
msp = doc.modelspace()

# For this example the OCS is rotated around x-axis about 45 degree
# OCS z-axis: x=0, y=1, z=1
# extrusion vector must not normalized here
ocs = OCS((0, 1, 1))
msp.add_circle(
    # You can place the 2D circle in 3D space
    # but you have to convert WCS into OCS
    center=ocs.from_wcs((0, 2, 2)),
    # center in OCS: (0.0, 0.0, 2.82842712474619)
    radius=1,
    dxfattribs={
        # here the extrusion vector should be normalized,
        # which is granted by using the ocs.uz
        'extrusion': ocs.uz,
        'color': 1,
    })
# mark center point of circle in WCS
msp.add_point((0, 2, 2), dxfattribs={'color': 1})
```

## 3D Polyline

- [Using UCS to Place 3D Polyline](https://ezdxf.readthedocs.io/en/stable/tutorials/ucs_transform.html#using-ucs-to-place-3d-polyline)

```python
# using an UCS simplifies 3D operations, but UCS definition can happen later
# calculating corner points in local (UCS) coordinates without Vec3 class
angle = math.radians(360 / 5)
corners_ucs = [(math.cos(angle * n), math.sin(angle * n), 0) for n in range(5)]

# let's do some transformations by UCS
transformation_ucs = UCS().rotate_local_z(math.radians(15))  # 1. rotation around z-axis
transformation_ucs.shift((0, .333, .333))  # 2. translation (inplace)
corners_ucs = list(transformation_ucs.points_to_wcs(corners_ucs))

location_ucs = UCS(origin=(0, 2, 2)).rotate_local_x(math.radians(-45))
msp.add_polyline3d(
    points=corners_ucs,
    close=True,
    dxfattribs={
        'color': 1,
    }
).transform(location_ucs.matrix)

# Add lines from the center of the POLYLINE to the corners
center_ucs = transformation_ucs.to_wcs((0, 0, 0))
for corner in corners_ucs:
    msp.add_line(
        center_ucs, corner, dxfattribs={'color': 1}
    ).transform(location_ucs.matrix)
```

### add_line


```bash
add_line(start: UVec, end: UVec, dxfattribs=None)→ Line¶
Add a Line entity from start to end.

Parameters:
start – 2D/3D point in WCS
end – 2D/3D point in WCS
dxfattribs – additional DXF attributes
```

```python
points=[p for p in zip(xv,yv)]
M=len(points)
for i in range(M-1):
  msp.add_line(points[i], points[i+1], dxfattribs={"color": clrs[intv]})
```

### add_polyline2d

```bash
add_polyline2d(points: Iterable[UVec], format: str | None = None, *, close: bool = False, dxfattribs=None)→ Polyline¶
Add a 2D Polyline entity.

Parameters:
points – iterable of 2D points in WCS(OCS)
close – True for a closed polyline
format – user defined point format like add_lwpolyline(), default is None
dxfattribs – additional DXF attributes
```

### add_polyline3d

3d points in [wcs(World coordinate system )](https://ezdxf.readthedocs.io/en/stable/concepts/coordinates.html#wcs)  

```bash
add_polyline3d(points: Iterable[UVec], *, close: bool = False, dxfattribs=None)→ Polyline¶
Add a 3D Polyline entity.

Parameters:
points – iterable of 3D points in WCS
close – True for a closed polyline
dxfattribs – additional DXF attributes
```



### polyline.points()

```bash
points()→ Iterator[Vec3]¶
Returns iterable of all polyline vertices as (x, y, z) tuples, not as Vertex objects.
```

## Tutorial for the Geo Add-on

- [Tutorial for the Geo Add-on](https://ezdxf.readthedocs.io/en/stable/tutorials/geo.html)
- [Geo Interface](https://ezdxf.readthedocs.io/en/stable/addons/geo.html#geo-intended-usage)

313600.000, 2771200.000 25.0476184564796,121.630312241047
314600,2772200 25.0566038304452, 121.640269221663,
