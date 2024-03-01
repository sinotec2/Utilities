---
layout: default
title:  配置 LDAP 身份驗證
parent: Apache Druid
grand_parent: DB_servers
grand_parent: OLAP
last_modified_date: 2024-02-06 11:22:37
tags: DB_servers Druid
---

# 配置 LDAP 身份驗證
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

您可以使用輕量級目錄存取協定 (LDAP)來保護對 Apache Druid 的存取。本主題介紹如何使用 LDAP 和 LDAP over TLS (LDAPS) 設定 Druid 驗證和授權。此處範例將會顯示 Active Directory LDAP 系統的設定。

- 第一步是為 Druid 啟用 LDAP 身份驗證和授權。
- 然後，您將 LDAP 群組對應到 Druid 角色並為這些角色指派權限。
- 完成此配置後，您可以選擇啟用 LDAPS 以使 LDAP 流量保密且安全。

## 事前準備

在開始為 Druid 設定 LDAP 之前，請測試您的 LDAP 連線並執行示範性的搜尋。

### 檢查您的 LDAP

- 測試您的 LDAP 連線以驗證它是否適用於使用者憑證。
- 稍後在此過程中，您將 Druid 配置為 LDAP 身份驗證，並以該使用者作為綁定用戶（bindUser）.

- 以下範例旨在測試用戶的連線，用戶的DN=myuser@example.com。
  - 輸入您的 LDAP 伺服器 IP 位址。
  - 如果您的LDAP伺服器實例偵聽對象是除389之外的端口，請修改 LDAP 實例的連接埠號碼389。

```bash
ldapwhoami -vv -H ldap://ip_address:389  -D "myuser@example.com" -W
```

出現提示時輸入使用者的密碼並驗證指令是否成功。如果失敗，請檢查以下內容：

- 確保您的 LDAP 執行個體使用正確的連接埠。
- 檢查伺服器的網路防火牆是否阻止其他機器連接到 LDAP 連接埠。
- 查看您的 LDAP 實作詳細信息，以了解您是否需要在 LDAP 伺服器上專門允許 LDAP 用戶端。如果是這樣，請將 Druid Coordinator 伺服器新增至允許清單。

### 測試您的 LDAP

- LDAP 連線正常後，搜尋使用者。例如myuser。
- 下列指令也可在 Active Directory 系統中搜尋使用者。此sAMAccountName屬性特定於 Active Directory，包含經過驗證的使用者身分：

```bash
ldapsearch -x -W -H ldap://ip_address:389  -D "cn=admin,dc=example,dc=com" -b "dc=example,dc=com" "(sAMAccountName=myuser)" +
```

- `memberOf`結果中的屬性顯示使用者所屬的群組。
- 例如以下回應顯示該使用者乃是`mygroup`群組的成員：

```bash
memberOf: cn=mygroup,ou=groups,dc=example,dc=com
```

- 您可以在後續步驟中使用此資訊將 LDAP 群組對應到 Druid 角色。

### 重要資訊

- 透過LDAP，Druid 使用memberOf屬性來確定群組的成員資格。
- 如果您的 LDAP 伺服器實作不包含此屬性，則在將LDAP 群組對應到角色時，必須完成其他的附加步驟。

### 配置 Druid 進行 LDAP

若要將 Druid 設定為使用 LDAP 驗證，請依照下列步驟操作。有關設定檔的位置，請參閱設定參考。

1. 在 LDAP 系統中建立一個用戶，您將使用該用戶與 Druid 進行內部通訊並作為 LDAP 初始管理員用戶。有關詳細信息，請參閱安全概述。在下面的範例中，LDAP 使用者是internal@example.com。

2. 啟用`druid-basic-security`目錄中的外掛控制檔，名稱也是`common.runtime.properties`。

3. 在該`common.runtime.properties`文件中，為 LDAP 屬性新增以下行並將這些值替換為您自己的值。有關這些屬性的詳細信息，請參閱Druid 基本安全性。

```bash
druid.auth.authenticatorChain=["ldap"]
druid.auth.authenticator.ldap.type=basic
druid.auth.authenticator.ldap.enableCacheNotifications=true
druid.auth.authenticator.ldap.credentialsValidator.type=ldap
druid.auth.authenticator.ldap.credentialsValidator.url=ldap://ip_address:port
druid.auth.authenticator.ldap.credentialsValidator.bindUser=administrator@example.com
druid.auth.authenticator.ldap.credentialsValidator.bindPassword=adminpassword
druid.auth.authenticator.ldap.credentialsValidator.baseDn=dc=example,dc=com
druid.auth.authenticator.ldap.credentialsValidator.userSearch=(&(sAMAccountName=%s)(objectClass=user))
druid.auth.authenticator.ldap.credentialsValidator.userAttribute=sAMAccountName
druid.auth.authenticator.ldap.authorizerName=ldapauth
druid.escalator.type=basic
druid.escalator.internalClientUsername=internal@example.com
druid.escalator.internalClientPassword=internaluserpassword
druid.escalator.authorizerName=ldapauth
druid.auth.authorizers=["ldapauth"]
druid.auth.authorizer.ldapauth.type=basic
druid.auth.authorizer.ldapauth.initialAdminUser=internal@example.com
druid.auth.authorizer.ldapauth.initialAdminRole=admin
druid.auth.authorizer.ldapauth.roleProvider.type=ldap
```

### 配置說明

這些配置是用於 Druid 的身份驗證和授權的設定。以下是這些設定的解釋：

1. **`druid.escalator.type=basic`：**
   - 這個配置指定 Druid 使用Escalator類型函式。在這裡，它設置為 `basic`，表明 Druid 使用基本的身份驗證和授權機制。

2. **`druid.escalator.internalClientUsername=internal@example.com`：**
   - 這是 Druid 內部客戶端使用的用戶名，用於內部服務之間的通信。

3. **`druid.escalator.internalClientPassword=internaluserpassword`：**
   - 內部客戶端的密碼，用於內部服務之間的通信。

4. **`druid.escalator.authorizerName=ldapauth`：**
   - 這個配置指定 Druid 使用的授權器的名稱。在這裡，它設置為 `ldapauth`，表明 Druid 將使用 LDAP 身份驗證和授權。

5. **`druid.auth.authorizers=["ldapauth"]`：**
   - 此配置設定 Druid 使用的所有授權器的名稱列表。在這裡，僅指定了一個名稱 `ldapauth`。

6. **`druid.auth.authorizer.ldapauth.type=basic`：**
   - 這裡指定了 `ldapauth` 授權器的類型，設置為 `basic`。

7. **`druid.auth.authorizer.ldapauth.initialAdminUser=internal@example.com`：**
   - LDAP 授權器的初始管理員用戶名，此用戶在啟動時將具有管理權限。

8. **`druid.auth.authorizer.ldapauth.initialAdminRole=admin`：**
   - LDAP 授權器的初始管理員角色，此角色在啟動時將具有管理權限。

9. **`druid.auth.authorizer.ldapauth.roleProvider.type=ldap`：**
   - 此配置指定 Druid 使用的角色提供者的類型，這裡設置為 `ldap`，表明 Druid 使用 LDAP 作為角色提供者。

總的來說，這些配置表明 Druid 使用基本的身份驗證和 LDAP 作為授權機制。它設置了初始管理員的用戶名、角色和 LDAP 連接的一些相關設定。這些設定在 Druid 啟動時將被應用，並影響 Druid 的身份驗證和授權行為。

### 設定注意事項

請注意以下事項：

- bindUser：連接 LDAP 的使用者。這應該是您用於測試 LDAP 搜尋的相同使用者。
- userSearch ：您的 LDAP 搜尋語法。
- userAttribute ：用戶搜尋屬性。
- internal@example.com是您在步驟 1 中建立的 LDAP 使用者。在範例中，它既充當內部用戶端使用者又充當初始管理員使用者。

- 重要資訊提醒
  - 在上面的範例中，Druid Escalator和 LDAP 初始管理員使用者設定為相同使用者 - internal@example.com。
  - 如果Escalator設定為其他用戶，則必須按照步驟 4 和 5 建立群組對應並指派初始角色，然後叢集的其餘部分才能運作。

4. 將群組映射儲存到 JSON 檔案。範例文件groupmap.json如下所示：


```json
{
   "name": "mygroupmap",
   "groupPattern": "CN=mygroup,CN=Users,DC=example,DC=com",
   "roles": [
      "readRole"
   ]
}
```

在範例中，LDAP 群組mygroup對應到 Druid 角色readRole，映射名稱為mygroupmap。

使用 Druid API 建立群組對應並根據 JSON 檔案指派初始角色。groupmap.json以下範例使用curl 建立為LDAP 群組定義的對應mygroup：

```bash
curl -i -v  -H "Content-Type: application/json" -u internal -X POST -d @groupmap.json http://localhost:8081/druid-ext/basic-security/authorization/db/ldapauth/groupMappings/mygroupmap
```

檢查群組映射是否建立成功。以下範例請求列出了所有群組對應：

```bash
curl -i -v  -H "Content-Type: application/json" -u internal -X GET  http://localhost:8081/druid-ext/basic-security/authorization/db/ldapauth/groupMappings
```

## 將 LDAP 群組對應到 Druid
完成初始設定和映射後，您可以將更多 LDAP 群組對應到 Druid 角色。LDAP群組的成員可以存取對應Druid角色的權限。

### 創建德魯伊角色

- 若要建立 Druid 角色，您可以使用 Druid REST API 向協調器程序提交 POST 請求，也可以使用 Druid 控制台。
- 下面的範例用作localhost協調器主機和8081連接埠。根據部署的詳細資訊修改這些屬性。
- 建立名為readRole的角色的範例請求：

```bash
curl -i -v  -H "Content-Type: application/json" -u internal -X POST  http://localhost:8081/druid-ext/basic-security/authorization/db/ldapauth/roles/readRole 
```

- 檢查Druid是否成功創建角色。以下範例請求列出了所有角色：

```bash
curl -i -v  -H "Content-Type: application/json" -u internal -X GET  http://localhost:8081/druid-ext/basic-security/authorization/db/ldapauth/roles
```

### 為Druid新增權限

- 一旦您擁有了 Druid 角色，您就可以為其新增權限。以下範例新增對資料來源的唯讀存取權限wikipedia。
- 在名為perm.json的檔案中給予以下 ：

```json
[
    { "resource": { "name": "wikipedia", "type": "DATASOURCE" }, "action": "READ" },
    { "resource": { "name": ".*", "type": "STATE" }, "action": "READ" },
    { "resource": {"name": ".*", "type": "CONFIG"}, "action": "READ"}
]
```

以下請求將 JSON 檔案中的權限與readRole角色關聯：

```bash
curl -i -v  -H "Content-Type: application/json" -u internal -X POST -d@perm.json  http://localhost:8081/druid-ext/basic-security/authorization/db/ldapauth/roles/readRole/permissions
```

Druid 使用者需要STATE和CONFIG權限才能在 Druid 控制台中查看資料來源。如果您只想指派查詢權限，您可以僅套用READ檔案第一行的權限perm.json。

您也可以以正規表示式的形式提供資料來源名稱。例如，若要授予對以 開頭的所有資料來源的存取權限wiki，您可以將資料來源名稱指定為{ "name": "wiki.*" }。

建立群組
現在您可以將 LDAP 群組對應到 Druid 角色。以下範例請求建立一個名為 name 的對應mygroupmap。mygroup它假定目錄中存在名為 的群組。

```json
{
    "name": "mygroupmap",
    "groupPattern": "CN=mygroup,CN=Users,DC=example,DC=com",
    "roles": [
        "readRole"
    ]
}
```

以下範例請求配置映射-角色映射位於檔案中groupmap.json。有關範例文件的內容，請參閱為 LDAP 驗證設定 Druid 。

```bash
curl -i -v  -H "Content-Type: application/json" -u internal -X POST -d @groupmap.json http://localhost:8081/druid-ext/basic-security/authorization/db/ldapauth/groupMappings/mygroupmap
```

若要檢查群組對映是否已建立成功，下列請求會列出所有群組對應：

```bash
curl -i -v  -H "Content-Type: application/json" -u internal -X GET http://localhost:8081/druid-ext/basic-security/authorization/db/ldapauth/groupMappings
```

以下範例請求返回mygroupmap群組的詳細資訊：

```bash
curl -i -v  -H "Content-Type: application/json" -u internal -X GET http://localhost:8081/druid-ext/basic-security/authorization/db/ldapauth/groupMappings/mygroupmap
```

以下範例請求將角色新增queryRole至映射中mygroupmap：

curl -i -v  -H "Content-Type: application/json" -u internal -X POST http://localhost:8081/druid-ext/basic-security/authorization/db/ldapauth/groupMappings/mygroup/roles/queryrole


將 LDAP 使用者新增至 Druid 並指派
您只需在以下情況下完成此步驟：

您的 LDAP 使用者不屬於任何 LDAP 群組，或
您想要為使用者設定其他 Druid 角色，這些角色未對應到使用者所屬的 LDAP 群組。
將 LDAP 使用者新增myuser至 Druid 的範例請求：

```bash
curl -i -v  -H "Content-Type: application/json" -u internal -X POST http://localhost:8081/druid-ext/basic-security/authorization/db/ldapauth/users/myuser 
```

將使用者指派myuser給queryRole角色的範例請求：

```bash
curl -i -v  -H "Content-Type: application/json" -u internal -X POST http://localhost:8081/druid-ext/basic-security/authorization/db/ldapauth/users/myuser/roles/queryRole
```

啟用 LDAP over TLS (LDAPS 
在 Druid 中設定 LDAP 驗證後，您可以選擇使用傳輸層安全性 (TLS) （以前稱為安全通訊端層 (SSL) ）技術使 LDAP 流量保密且安全。

配置 LDAPS 在 Druid 和 LDAP 伺服器之間建立信任。

在開始在 Druid 中設定 LDAPS 之前，您必須設定 Druid 進行 LDAP 驗證。您還需要：

由公共憑證授權單位 (CA) 核發的憑證或由內部 CA 核發的自簽名憑證。
簽署 LDAP 伺服器憑證的 CA 的根憑證。如果您使用的是通用公共 CA，則憑證可能已位於 Java 信任庫中。否則您需要匯入 CA 的憑證。
為
完成以下步驟為 Druid 設定 LDAPS。有關設定檔的位置，請參閱設定參考。

將 LDAP 伺服器的 CA 或自簽名憑證匯入至新建立的 LDAP 信任儲存或由檔案druid.client.https.trustStorePath 中的屬性指定的信任儲存common.runtime.properties。

下面的範例說明了 HTTPS 用戶端和 LDAP 用戶端都使用一個金鑰儲存的選項，但如果您願意，也可以為 ldap 使用單獨的專用信任儲存。

```bash
keytool -import -trustcacerts -keystore path/to/cacerts -storepass truststorepassword -alias aliasName -file path/to/certificate.cer
```

替換path/to/cacerts為信任庫的路徑、truststorepassword信任庫密碼、aliasName金鑰庫的別名以及path/to/certificate.cer憑證的位置和名稱。例如：

```bash
keytool -import -trustcacerts -keystore /Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/security/cacerts -storepass mypassword -alias myAlias -file /etc/ssl/certs/my-certificate.cer
```

如果 Java 信任庫中尚不存在 CA 的根證書，請將其匯入：

```bash
keytool -importcert -keystore path/to/cacerts -storepass truststorepassword -alias aliasName -file path/to/certificate.cer
```

替換path/to/cacerts為信任庫的路徑、truststorepassword信任庫密碼、aliasName金鑰庫的別名以及path/to/certificate.cer憑證的位置和名稱。例如：

```bash
keytool -importcert -keystore /Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/security/cacerts -storepass mypassword -alias myAlias -file /etc/ssl/certs/my-certificate.cer
```

在您的common.runtime.properties檔案中，將以下行新增至 LDAP 設定部分，取代您自己的信任儲存路徑和密碼。請注意，指向信任儲存的屬性是druid.auth.basic.ssl.trustStorePath，而不是druid.client.https.trustStorePath。無論您是對 HTTPS 用戶端和 LDAP 使用相同的信任存儲，還是使用單獨的 LDAP 信任存儲，請確保正確的屬性指向導入 LDAP 憑證的信任存儲。

```bash
druid.auth.basic.ssl.trustStorePath=/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/security/cacerts
druid.auth.basic.ssl.protocol=TLS
druid.auth.basic.ssl.trustStorePassword=xxxxxx
```

有關這些屬性的詳細信息，請參閱Druid 基本安全性。

您可以選擇在common.runtime.properties檔案中配置其他 LDAPS 屬性。有關更多信息，請參閱Druid 基本安全性。

重啟德魯伊。

故障排除
以下是一些可幫助您解決 LDAP 和 LDAPS 問題的想法。

檢查協調器
如果您的 LDAP 連線不起作用，請檢查協調器日誌。有關詳細信息，請參閱日誌記錄。

檢查Druid扶梯
如果協調器正在工作，但叢集的其餘部分沒有工作，請檢查自動扶梯配置。有關詳細信息，請參閱配置參考。您也可以檢查其他服務日誌以了解為什麼服務無法從協調器取得授權詳細資訊。

檢查您的 LDAP 伺服器回應
如果使用者可以登入 Druid 控制台，但登陸頁面顯示 401 錯誤，請檢查您的 LDAP 伺服器回應時間。在擁有大量 LDAP 使用者的大型組織中，LDAP 回應可能會很慢，這可能會導致連線逾時。