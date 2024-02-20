---
layout: default
title:  ArcGIS SDK
parent: GIS Relatives

last_modified_date: 2023-05-11 16:01:26
tags: GIS Voronoi Delaunay
---

# ArcGIS SDK
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

### GIS 資訊架構

地理信息系統（Geographic Information System，縮寫為GIS）的架構主要包括數據、軟體、硬體、人員和方法五個方面。以下是GIS的一般架構：

1. **數據：** GIS 的核心是地理數據，這些數據通常包括空間和非空間信息。空間信息是指地理位置和地理空間上的特徵，例如地圖、影像、地形數據等。非空間信息是與地理特徵相關聯的屬性數據，例如人口統計、土地使用、環境條件等。

2. **軟體：** GIS 軟體用於處理、分析、可視化和管理地理數據。它提供了用戶進行地理空間分析和視覺化的工具，以及數據庫管理、地理編輯和地理處理的功能。常見的GIS軟體包括ArcGIS、QGIS、MapInfo等。

3. **硬體：** GIS 硬體包括運行 GIS 軟體的計算機、數據存儲裝置、顯示器、印表機等。這些硬體設備需要足夠的性能和存儲能力，以應對處理大量地理數據的需求。

4. **人員：** GIS 系統需要具有地理信息相關專業知識的人員來設計、構建、維護和使用系統。這包括GIS分析師、數據庫管理員、地理信息科學家等。

5. **方法：** GIS 使用者需要採用一定的方法和流程來收集、處理和分析地理數據。這包括地理信息系統的設計、數據的獲取、地理分析和結果的呈現等步驟。

簡而言之，GIS 的架構是一個多層次的系統，整合了數據、軟體、硬體、人員和方法，以實現地理信息的有效管理、分析和應用。這種架構使得GIS能夠應對各種不同的應用場景，從城市規劃到自然資源管理，從環境監測到災害應對。

### 官網

- [Mapping APIs](https://developers.arcgis.com/documentation/mapping-apis-and-services/apis-and-sdks/)
  - [.NET](https://developers.arcgis.com/net/)
  - [JavaScript](https://developers.arcgis.com/javascript/latest/) 
  - [Esri Leaflet](https://developers.arcgis.com/esri-leaflet/)

### 免費額度

|項目|數量
|:-|:-:
Basemap tiles|2,000,000
Nearby and extent searches|500
Place attributes|100 
Address attributes|100
Details attributes|100 
Location attributes|100 
Geocodes (not stored)|20,000 
Routes|20,000 
Service areas|5,000 
Features (storage)|100 MB 
Tiles, files and attachments (storage)|100 MB 
Feature queries (bandwidth)|15 MB 
Feature edits (bandwidth)|5 MB 
Vector tiles (bandwidth)|25 MB 
Map tiles (bandwidth)|25 MB 
Tiles generated|25,000 
Community Support
US East Regional Hosting

## 安全性

- [Certificate authentication with PKI](https://developers.arcgis.com/net/wpf/sample-code/certificate-authentication-with-pki/)
- [ Use LDAP and PKI to secure access](https://developers.arcgis.com/net/wpf/sample-code/certificate-authentication-with-pki/)


## 使用 LDAP 和用戶端憑證驗證來保護存取

- 使用輕量級目錄存取協定 (LDAP) 對使用者進行驗證時，您可以使用基於公鑰基礎架構 (PKI) 的用戶端憑證驗證來保護對 ArcGIS Enterprise 組織的存取。
- 若要使用 LDAP 和 PKI，必須使用部署到 Java 應用程式伺服器的 [ArcGIS Web Adaptor]() (Java Platform) 設定用戶端憑證驗證。 您無法使用 ArcGIS Web Adaptor (IIS) 透過 LDAP 執行用戶端憑證驗證。 如果您尚未執行此操作，請透過入口網站安裝並設定 ArcGIS Web Adaptor (Java Platform)。

### 使用 LDAP 設定您的組織

- 預設情況下，ArcGIS Enterprise 組織對所有通訊強制使用 HTTPS。 如果您先前已將此選項變更為允許 HTTP 和 HTTPS 通信，則必須按照下列步驟將入口網站重新配置為僅使用 HTTPS 通訊。
- 將組織配置為使用 HTTPS 進行所有通信

### 完成以下步驟將組織設定為使用 HTTPS

- 以管理員身分登入組織網站。
- URL 的格式為 https://webadaptorhost.domain.com/webadaptorname/home。
- 點擊組織並點擊設定選項卡，然後點擊頁面左側的安全性。
- 啟用僅允許透過 HTTPS 存取入口網站。

### 更新您入口網站的身份存儲

接下來，更新入口網站的身份儲存以使用 LDAP 使用者和群組。
- 以組織管理員身分登入 ArcGIS Portal Directory。
- URL 的格式為 https://webadaptorhost.domain.com/webadaptorname/portaladmin。
- 按一下安全性 > 設定 > 更新身分儲存。

在使用者儲存配置（JSON 格式）文字方塊中，貼上您組織的 LDAP 使用者設定資訊（JSON 格式）。 或者，使用特定於您的組織的使用者資訊更新以下範例：

```json
{
  "type": "LDAP",
  "properties": {
    "userPassword": "secret",
    "isPasswordEncrypted": "false",
    "user": "uid=admin,ou=system",
    "userFullnameAttribute": "cn",
    "userGivenNameAttribute": "givenName",
    "userSurnameAttribute": "sn",
    "ldapURLForUsers": "ldaps://bar2:10636/ou=users,ou=ags,dc=example,dc=com",
    "userEmailAttribute": "mail",
    "usernameAttribute": "uid",
    "caseSensitive": "false",
    "userSearchAttribute": "dn"
  }
}
```

- 在大多數情況下，您只需變更 user、userPassword、ldapURLForUsers 和 userSearchAttribute 參數的值。 userSearchAttribute 是PKI 憑證的Subject 參數的值。 如果您的組織使用 PKI 憑證中的其他屬性（例如電子郵件），則必須更新 userSearchAttribute 參數以符合 PKI 憑證中的主題參數。 您的 LDAP 管理員需要提供 LDAP 的 URL。
- 在上面的範例中，LDAP URL 引用特定 OU 中的使用者 (ou=users)。 如果使用者存在於多個 OU 中，則 LDAP URL 可以指向更高層級的 OU，甚至根據需要指向根層級。 在這種情況下，URL 將如下所示：

"ldapURLForUsers": "ldaps://bar2:10636/dc=example,dc=com",

您用於使用者參數的帳戶需要具有查找組織中使用者的電子郵件地址和使用者名稱的權限。 儘管您以明文輸入密碼，但當您按一下「更新配置」（如下）時，密碼將會被加密。

如果您的 LDAP 配置為區分大小寫，請將 caseSensitive 參數設為 true。

如果要在入口網站中建立使用身分識別儲存體中現有 LDAP 群組的群組，請將組織的 LDAP 群組設定資訊（JSON 格式）貼上到群組儲存設定（JSON 格式）文字方塊中，如下所示。 或者，使用特定於您的組織的群組資訊更新以下範例。 如果您只想使用入口網站的內建群組，請刪除文字方塊中的所有資訊並跳過此步驟。

```json
{
  "type": "LDAP",
  "properties": {
    "userPassword": "secret",
    "isPasswordEncrypted": "false",
    "user": "uid=admin,ou=system",
    "ldapURLForUsers": "ldaps://bar2:10636/ou=users,ou=ags,dc=example,dc=com",
    "ldapURLForRoles": "ldaps://bar2:10636/dc=example,dc=com",
    "usernameAttribute": "uid",
    "caseSensitive": "false",
    "userSearchAttribute": "dn",
    "memberAttributeInRoles": "member",
    "rolenameAttribute":"cn"
  }
}
```

在大多數情況下，您只需變更 user、userPassword、ldapURLForUsers、ldapURLForGroups 和 userSearchAttribute 參數的值。 userSearchAttribute 是PKI 憑證的Subject 參數的值。 如果您的組織使用 PKI 憑證中的其他屬性（例如電子郵件），則必須更新 userSearchAttribute 參數以符合 PKI 憑證中的主題參數。 您的 LDAP 管理員需要提供 LDAP 的 URL。

在上面的範例中，LDAP URL 引用特定 OU 內的使用者 (ou=users)。 如果使用者存在於多個 OU 中，則 LDAP URL 可以指向更高層級的 OU，甚至根據需要指向根層級。 在這種情況下，URL 將如下所示：

"ldapURLForUsers": "ldaps://bar2:10636/dc=example,dc=com",

您用於使用者參數的帳戶需要具有查找組織中群組名稱的權限。 儘管您以明文輸入密碼，但當您按一下「更新配置」（如下）時，密碼將會被加密。

如果您的 LDAP 配置為區分大小寫，請將 caseSensitive 參數設為 true。

點擊更新配置以儲存您的變更。
如果您已配置高可用門戶，請重新啟動每個門戶電腦。 有關完整說明，請參閱停止和啟動入口網站。

### 新增組織特定的帳戶

預設情況下，組織特定的使用者可以存取 ArcGIS Enterprise 組織。 但是，他們只能查看已與組織中的每個人共享的項目。 這是因為組織特定的帳戶尚未新增並授予存取權限。

- 使用以下方法之一將帳戶新增至您的組織：
  - 單獨或批次（一次一個、從 .csv 檔案批次或從現有 Active Directory 群組）
  - 命令列實用程式
  - 自動地
- 建議您至少指定一個特定於組織的帳戶作為入口網站的管理員。 您可以透過在新增帳戶時選擇管理員角色來執行此操作。 當您有備用入口網站管理員帳戶時，您可以將初始管理員帳戶指派給使用者角色或刪除該帳戶。 有關詳細信息，請參閱關於初始管理員帳戶。

- 新增帳戶並完成以下步驟後，使用者就可以登入組織並存取內容。

設定 ArcGIS Web Adaptor 以使用用戶端憑證驗證

在您的組織中安裝並設定 ArcGIS Web Adaptor (Java Platform) 後，請在 Java 應用程式伺服器上設定 LDAP 領域，並為 ArcGIS Web Adaptor 設定基於 PKI 的用戶端憑證驗證。 有關說明，請諮詢您的系統管理員或查看 Java 應用程式伺服器的產品文件。

筆記：
為了使客戶端憑證驗證起作用，必須在 Java 應用程式伺服器中停用 TLS 1.3。

### 使用 LDAP 和用戶端憑證驗證組織存取

若要驗證您可以使用 LDAP 和用戶端憑證驗證存取門戶，請完成下列步驟：

開啟 ArcGIS Enterprise 入口網站。 URL 的格式為 https://webadaptorhost.domain.com/webadaptorname/home。URL 的格式為 https://organization.example.com/<context>/home。
驗證系統是否提示您輸入安全憑證並且可以存取網站。

### 阻止使用者建立自己的內建帳戶

您可以透過在組織設定中停用使用者建立內建帳戶的功能來阻止使用者建立自己的內建帳戶。