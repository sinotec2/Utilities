---
layout: default
title:  CADNA整合地圖服務系統應用
parent: leaflet
grand_parent: Graphics
date:  2024-06-04
last_modified_date: 2024-06-04 14:04:00
tags: CMAQ leaflet graphics
---

# CADNA整合地圖服務系統應用
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

### 專業領域需求

- 彈性判斷需擷取的空間範圍
- 檔案格式、解析度

为实现从地图上选取矩形范围并输出该范围的数值地形文件，同时支持多个用户的LDAP身份管理，可以考虑以下开源方案的组合系统：

### 前端部分

1. **Leaflet**:
   - Leaflet 是一个开源的 JavaScript 库，用于在网页上显示交互式地图。
   - 通过插件支持绘图工具，可以让用户在地图上选择矩形范围。
   
   示例代码：
   ```html
   <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
   <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
   <script src="https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.js"></script>
   <link rel="stylesheet" href="https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.css" />

   <div id="map" style="width: 600px; height: 400px;"></div>

   <script>
     var map = L.map('map').setView([51.505, -0.09], 13);
     L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
       attribution: '© OpenStreetMap contributors'
     }).addTo(map);

     var drawnItems = new L.FeatureGroup();
     map.addLayer(drawnItems);

     var drawControl = new L.Control.Draw({
       edit: {
         featureGroup: drawnItems
       }
     });
     map.addControl(drawControl);

     map.on(L.Draw.Event.CREATED, function (event) {
       var layer = event.layer;
       drawnItems.addLayer(layer);
       var bounds = layer.getBounds();
       console.log(bounds); // Send bounds to backend
     });
   </script>
   ```

### 后端部分

2. **Django**:
   - Django 是一个高效的 Python Web 框架，可以处理用户身份验证和后台逻辑。
   - 可以使用 Django Rest Framework (DRF) 来创建 REST API，供前端使用。
   
3. **GeoDjango**:
   - GeoDjango 是 Django 的扩展，支持地理空间数据处理。
   - 可以与 PostGIS 一起使用来存储和处理地理数据。

4. **PostGIS**:
   - PostGIS 是 PostgreSQL 的地理空间扩展，用于存储和查询地理空间数据。
   - 适合存储和处理地形数据。

示例代码：
```python
# models.py
from django.contrib.gis.db import models

class Terrain(models.Model):
    name = models.CharField(max_length=100)
    location = models.PolygonField()

# views.py
from django.shortcuts import render
from rest_framework import viewsets
from .models import Terrain
from .serializers import TerrainSerializer

class TerrainViewSet(viewsets.ModelViewSet):
    queryset = Terrain.objects.all()
    serializer_class = TerrainSerializer

# serializers.py
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Terrain

class TerrainSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Terrain
        fields = '__all__'
        geo_field = 'location'

# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TerrainViewSet

router = DefaultRouter()
router.register(r'terrain', TerrainViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

### 用户身份管理部分

5. **LDAP**:
   - 使用 OpenLDAP 作为 LDAP 服务器，管理用户身份验证和授权。
   
6. **django-auth-ldap**:
   - Django 的扩展，可以与 LDAP 集成，支持用户身份验证。
   
配置示例：
```python
# settings.py
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_LDAP_SERVER_URI = "ldap://your-ldap-server.com"
AUTH_LDAP_BIND_DN = "cn=admin,dc=example,dc=com"
AUTH_LDAP_BIND_PASSWORD = "yourpassword"
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "ou=users,dc=example,dc=com",
    ldap.SCOPE_SUBTREE,
    "(uid=%(user)s)",
)

# Optionally configure group search and member membership
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    "ou=groups,dc=example,dc=com",
    ldap.SCOPE_SUBTREE,
    "(objectClass=groupOfNames)"
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()
AUTH_LDAP_REQUIRE_GROUP = "cn=required_group,ou=groups,dc=example,dc=com"
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=active_group,ou=groups,dc=example,dc=com",
    "is_staff": "cn=staff_group,ou=groups,dc=example,dc=com",
    "is_superuser": "cn=superuser_group,ou=groups,dc=example,dc=com",
}
```

### 综合方案

以上组件组合起来，可以实现用户通过前端选取地图上的矩形范围，后端接收请求并处理生成地形文件，并且通过 LDAP 进行用户身份验证管理的功能。

### 具体实现步骤

1. **部署 OpenLDAP** 进行用户身份验证管理。
2. **搭建 Django 和 GeoDjango** 后端，处理用户请求和地理数据存储。
3. **设置 PostgreSQL 和 PostGIS** 数据库，存储和查询地理空间数据。
4. **前端使用 Leaflet** 实现地图交互功能，让用户选取矩形范围。
5. **使用 Django Rest Framework** 创建 API，前端将选取的范围发送到后端。
6. **集成 LDAP**，通过 `django-auth-ldap` 实现用户身份验证。
7. **配置 Nginx 或 Apache**，进行负载均衡和反向代理。

这套方案可以满足您的需求，支持多用户并发操作，并具备良好的扩展性。

