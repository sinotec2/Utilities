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

為實現從地圖上選取矩形範圍並輸出該範圍的數值地形文件，同時支援多個使用者的LDAP身分管理，可以考慮以下開源方案的組合系統：

### 前端部分

1. **Leaflet**:

- Leaflet 是一個開源的 JavaScript 函式庫，用於在網頁上顯示互動式地圖。
- 透過外掛程式支援繪圖工具，可以讓使用者在地圖上選擇矩形範圍。

 範例程式碼：

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

### 後端部分

2. **Django**:
 - Django 是一個高效的 Python Web 框架，可以處理使用者身份驗證和後台邏輯。
 - 可以使用 Django Rest Framework (DRF) 來建立 REST API，供前端使用。

3. **GeoDjango**:
 - GeoDjango 是 Django 的擴展，支援地理空間資料處理。
 - 可以與 PostGIS 一起使用來儲存和處理地理資料。

4. **PostGIS**:
 - PostGIS 是 PostgreSQL 的地理空間擴展，用於儲存和查詢地理空間資料。
 - 適合儲存和處理地形資料。

範例程式碼：

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
來自 django.urls import path, include
來自 rest_framework.routers import DefaultRouter
from .views import TerrainViewSet

router = DefaultRouter()
router.register(r'terrain', TerrainViewSet)

urlpatterns = [
 path('', include(router.urls)),
]
```

### 使用者身分管理部分

5. **LDAP**:
 - 使用 OpenLDAP 作為 LDAP 伺服器，管理使用者身份驗證和授權。

6. **django-auth-ldap**:
 - Django 的擴展，可與 LDAP 集成，支援使用者身份驗證。

設定範例：

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

### 綜合方案

以上元件組合起來，可以實現使用者透過前端選取地圖上的矩形範圍，後端接收請求並處理生成地形文件，並且透過 LDAP 進行使用者身份驗證管理的功能。

### 具體實作步驟

1. **部署 OpenLDAP** 進行使用者驗證管理。
2. **建立 Django 和 GeoDjango** 後端，處理使用者請求和地理資料儲存。
3. **設定 PostgreSQL 和 PostGIS** 資料庫，儲存和查詢地理空間資料。
4. **前端使用 Leaflet** 實作地圖互動功能，讓使用者選取矩形範圍。
5. **使用 Django Rest Framework** 建立 API，前端將選取的範圍傳送到後端。
6. **整合 LDAP**，透過 `django-auth-ldap` 實現使用者驗證。
7. **設定 Nginx 或 Apache**，進行負載平衡和反向代理。

這套方案可以滿足您的需求，支援多用戶並發操作，並具備良好的擴充性。
