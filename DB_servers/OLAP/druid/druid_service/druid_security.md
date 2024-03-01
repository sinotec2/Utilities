---
layout: default
title:  Druid安全設定
parent: Apache Druid
grand_parent: DB_servers
grand_parent: OLAP
last_modified_date: 2024-02-12 14:15:31
tags: DB_servers Druid
---

# Apache Druid 之安全設定
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

- 文件來源：[Security overview](https://druid.apache.org/docs/latest/operations/security-overview/)

## 安全概述

本文檔概述了 Apache Druid 安全功能、設定說明以及一些保護 Druid 的最佳實務。

預設情況下，Druid 中的安全功能是停用的，這簡化了初始部署體驗。但是，必須在生產部署中配置安全功能。這些功能包括 TLS、身份驗證和授權。

## 最佳實務建議

### Druid 叢集安全設定

- 以非特權 Unix 使用者身分執行 Druid。不要以 root 使用者身分執行 Druid。
  - Druid 管理員與執行 Druid 的 Unix 使用者帳戶具有相同的作業系統權限。請參閱身份驗證和授權模型。
  - 如果Druid進程在作業系統root使用者帳戶下運行，那麼Druid管理員可以讀取或寫入root帳戶有權存取的所有文件，包括敏感文件，例如/etc/passwd.
- 對於生產環境、和其他可以存取不可信網路的環境條件，啟用 Druid 叢集的身份驗證。
  - 啟用授權，並且在未啟用授權的情況下不要公開 Web 控制台(web console)。
  - 如果未啟用授權，則任何有權存取 Web 控制台的使用者都具有與執行 Web 控制台程序的作業系統使用者相同的權限。
- 授予使用者執行其功能所需的最低權限。
  - 例如，對只需要查詢資料的使用者，不要允許寫入資料來源或檢視狀態。
- 不要在設定規格中為生產系統提供純文字密碼。
  - 例如，敏感屬性不應在consumerProperties(位於`./quickstart/tutorial/wikipedia-kafka-supervisor.json`)中予以揭露。
  - 有關詳細信息，請參閱環境變數動態配置提供者。
- 停用 JavaScript，如JavaScript 指南安全性部分所述。

### Druid 網路運作的建議

- 啟用 TLS 以加密叢集內的通訊。
- 使用 API 通道可以：
  - 限制來自不受信任網路的訪問
  - 建立使用者允許列表，已過濾真正需要存取特定 API 的人
  - 實施帳戶鎖定和限制功能。
- 如果可能，請使用防火牆和其他網路層過濾，僅公開您的用例特別需要的 Druid 服務和連接埠。
  - 例如，僅將 Broker 連接埠公開給執行查詢的下游應用程式。
  - 您可以限制對特定 IP 位址或網段的訪問，以進一步加強和增強安全性。

### 適用於 Druid 授權認證模型的建議

- 僅向受信任的使用者授予DATASOURCE WRITE權限。
  - Druid 的信任模型會假設這些使用者與執行 Web 控制台程序的作業 系統使用者具有相同的權限。
  - 此外，具有WRITE權限的使用者可以更改資料來源，並且可以存取可能影響數據攝取和主管更新任務的API POST動作。
  - 僅授予高度信任的使用者`STATE READ`、`STATE WRITE`、`CONFIG WRITE`和`DATASOURCE WRITE`的權限。
  - 這些權限允許使用者代表 Druid 伺服器進程存取資源，無論資料來源為何。
- 如果您的 Druid 用戶端應用程式允許不太受信任的使用者控制數據攝取任務的輸入來源或某個數據傾瀉火管(Firehose)，請驗證該使用者的 URL。這些未經檢查的 URL 可能指向內部網路或本機檔案系統中的其他位置和資源而造成災難。

## 啟用 TLS

啟用 TLS 會對外部用戶端與 Druid 叢集之間的流量以及叢集內服務之間的流量進行加密。

### 產生金鑰

- 在 Druid 中啟用 TLS 之前，請產生 KeyStore 和 truststore
  - 當一個 Druid 進程（例如 Broker）聯繫另一個 Druid 進程（例如 Historical）時，第一個服務是第二個服務（被視為伺服器）的客戶端。
  - 用戶端使用包含用戶端信任的憑證的 trustStore。例如，經紀人。
  - 伺服器使用包含私鑰和憑證鏈的 KeyStore，用於安全地識別自身。
- 以下範例示範如何使用 Java keytool 為伺服器產生 KeyStore，然後建立一個 trustStore 以信任用戶端的金鑰：

1. 使用 Java 指令產生 ：`keytool -keystore keystore.jks -alias druid -genkey -keyalg RSA`

2. 匯出公共憑證：`keytool -export -alias druid -keystore keystore.jks -rfc -file public.cert`

3. 建立信任庫：`keytool -import -file public.cert -alias druid -keystore truststore.jks`

-  使用 Jetty 作為其嵌入式 Web 伺服器。請參閱Jetty 文件中的設定 SSL/TLS 金鑰庫 。
- 警告：不要在生產環境中使用自簽名憑證。相反，依靠您當前的公鑰基礎設施來產生和分發可信任金鑰。

### 更新 Druid TLS

- 編輯common.runtime.properties所有節點上的所有 Druid 服務。
- 新增或更新以下 TLS 選項。完成後重新啟動叢集。

```bash  
# Turn on TLS globally
druid.enableTlsPort=true

# Disable non-TLS communicatoins
druid.enablePlaintextPort=false

# For Druid processes acting as a client
# Load simple-client-sslcontext to enable client side TLS
# Add the following to extension load list
druid.extensions.loadList=[......., "simple-client-sslcontext"]

# Setup client side TLS
druid.client.https.protocol=TLSv1.2
druid.client.https.trustStoreType=jks
druid.client.https.trustStorePath=truststore.jks # replace with correct trustStore file
druid.client.https.trustStorePassword=secret123  # replace with your own password

# Setup server side TLS
druid.server.https.keyStoreType=jks
druid.server.https.keyStorePath=my-keystore.jks # replace with correct keyStore file
druid.server.https.keyStorePassword=secret123 # replace with your own password
druid.server.https.certAlias=druid
```

- 有關更多信息，請參閱TLS 支援和簡單 SSLContext 提供者模組。

### 身份驗證和授權

您可以設定身份驗證和授權來控制對 Druid API 的存取。然後配置使用者、角色和權限，如下部分所述。common.runtime.properties在叢集中所有 Druid 伺服器上的檔案中進行設定變更。

在 Druid 的操作上下文中，身份驗證器控制驗證使用者身份的方式。授權者使用使用者角色將經過身份驗證的使用者與允許他們存取的資料來源相關聯。您可以針對每個資料來源設定最細粒度的權限。

下圖描述了請求通過身份驗證過程的過程：

![Druid安全檢查流程](https://druid.apache.org/assets/images/security-model-1-52af921005928cc8df8fa854071ac883.png)

## 啟用身份驗證器

- 要在 Druid 中對請求進行身份驗證，您需要設定一個身份驗證器。
  - HTTP 基本驗證、LDAP 和 Kerberos 都有驗證器之擴充外掛。
  - 以下將引導您完成啟用基本驗證的範例設定步驟：
- 將外掛檔名`indruid-basic-security`加入通用設定檔`common.runtime.properties`中的外掛清單`druid.extensions.loadList`中。
  - 如要快速入門安裝，可以參考位於`conf/druid/cluster/_common`目錄下屬性檔案`common.runtime.properties`中的建議。(參考[屬性檔範例說明](./common.runtime.properties.md))

```python
druid.extensions.loadList=["druid-basic-security", "druid-histogram", "druid-datasketches", "druid-kafka-indexing-service"]
```

在同一 `common.runtime.properties` 檔案中設定基本的驗證器、授權器和`Escalator`設定。 `Escalator` 定義了 `Druid` 進程如何相互驗證。

範例配置：

```python
# Druid basic security
druid.auth.authenticatorChain=["MyBasicMetadataAuthenticator"]
druid.auth.authenticator.MyBasicMetadataAuthenticator.type=basic

# Default password for 'admin' user, should be changed for production.
druid.auth.authenticator.MyBasicMetadataAuthenticator.initialAdminPassword=password1

# Default password for internal 'druid_system' user, should be changed for production.
druid.auth.authenticator.MyBasicMetadataAuthenticator.initialInternalClientPassword=password2

# Uses the metadata store for storing users.
# You can use the authentication API to create new users and grant permissions
druid.auth.authenticator.MyBasicMetadataAuthenticator.credentialsValidator.type=metadata

# If true and if the request credential doesn't exist in this credentials store,
# the request will proceed to next Authenticator in the chain.
druid.auth.authenticator.MyBasicMetadataAuthenticator.skipOnFailure=false

druid.auth.authenticator.MyBasicMetadataAuthenticator.authorizerName=MyBasicMetadataAuthorizer

# Escalator
druid.escalator.type=basic
druid.escalator.internalClientUsername=druid_system
druid.escalator.internalClientPassword=password2
druid.escalator.authorizerName=MyBasicMetadataAuthorizer

druid.auth.authorizers=["MyBasicMetadataAuthorizer"]

druid.auth.authorizer.MyBasicMetadataAuthorizer.type=basic
```

- 重新啟動叢集。
- 請參閱以下主題以獲取更多資訊：

身份驗證和授權，以了解有關身份驗證器、自動扶梯和授權器的更多資訊。
基本安全性，以了解有關上述範例中使用的擴充功能的更多資訊。
Kerberos用於 Kerberos 驗證。
使用者認證和授權，以了解權限的詳細資訊。
SQL 權限用於 SQL 系統表的權限。
Pythondruidapi庫作為 Druid 教程的一部分提供，用於設定使用者和角色以學習安全性的工作原理。

## 啟用使用者角色權限

啟用基本驗證擴充功能後，您可以透過 `Druid Coordinator` 端點(8081、8281)新增使用者、角色和權限user。請注意，您不能直接向單一使用者指派權限。他們必須透過該使用者所歸屬的角色來分配權限。

下圖描述了授權模型以及使用者、角色、權限和資源之間的關係。

![](https://druid.apache.org/assets/images/security-model-2-983fc88399981fc0d7e5119e928b45e3.png)

### 德魯伊安全模型

以下步驟示範了範例設定流程：

- 資訊
  - 對於非 TLS 連接，預設協調器 API 連接埠為 8081；對於安全連接，預設協調器 API 連接埠為 8281。
  - 透過向 發出 POST 請求來建立使用者druid-ext/basic-security/authentication/db/MyBasicMetadataAuthenticator/users/<USERNAME>。替換<USERNAME>為您嘗試建立的新使用者名稱。例如：

```bash
curl -u admin:password1 -XPOST https://my-coordinator-ip:8281/druid-ext/basic-security/authentication/db/MyBasicMetadataAuthenticator/users/myname
```

- 資訊
  - 如果啟用了 TLS，請務必相應地調整curl 命令。例如，如果您的 Druid 伺服器使用自簽名證書，您可以選擇包含insecurecurl 選項以放棄對curl 命令進行證書檢查。
  - 透過向 發出 POST 請求來新增使用者憑證druid-ext/basic-security/authentication/db/MyBasicMetadataAuthenticator/users/<USERNAME>/credentials。例如：

```bash
curl -u admin:password1 -H'Content-Type: application/json' -XPOST https://my-coordinator-ip:8281/druid-ext/basic-security/authentication/db/MyBasicMetadataAuthenticator/users/myname/credentials --data-raw '{"password": "my_password"}'
```

  - 對於您建立的每個身分驗證者用戶，透過向 發出 POST 請求來建立對應的授權者使用者druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/users/<USERNAME>。例如：

```bash
curl -u admin:password1 -XPOST https://my-coordinator-ip:8281/druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/users/myname
```

建立授權者角色以透過向 發出 POST 請求來控制權限druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/roles/<ROLENAME>。例如：

```bash
curl -u admin:password1 -XPOST https://my-coordinator-ip:8281/druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/roles/myrole
```

透過向 發出 POST 請求來為使用者指派角色druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/users/<USERNAME>/roles/<ROLENAME>。例如：

```bash
curl -u admin:password1 -XPOST https://my-coordinator-ip:8281/druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/users/myname/roles/myrole | jq
```

最後，為角色附加權限以控制他們如何與 Druid 進行互動druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/roles/<ROLENAME>/permissions。例如：

```bash
curl -u admin:password1 -H'Content-Type: application/json' -XPOST --data-binary @perms.json https://my-coordinator-ip:8281/druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/roles/myrole/permissions
```

的有效負載perms.json應採用以下形式(注意格式)：

```json
[
   {
     "resource": {
       "type": "DATASOURCE",
       "name": "<PATTERN>"
     },
     "action": "READ"
   },
   {
     "resource": {
       "type": "STATE",
       "name": "STATE"
     },
     "action": "READ"
   }
]
```

- 完整的管理者，有這下列7種讀寫的權限
  - `CONFIG`、`QUERY_CONTEXT`、`SYSTEM_TABLE`、`EXTERNAL`、`DATASOURCE`、`STATE`、`VIEW`


```json
[
  {
    "resource":{
        "name":".*",
        "type":"CONFIG"
      },
    "action":"READ"
  },
  {
    "resource":{
        "name":".*",
        "type":"CONFIG"
        },
      "action":"WRITE"
  },
  {
    "resource":{
        "name":".*",
        "type":"QUERY_CONTEXT"
        },
      "action":"READ"
  },
  {
    "resource":{
        "name":".*",
        "type":"QUERY_CONTEXT"
        },
      "action":"WRITE"
  },
  {
    "resource":{
        "name":".*",
        "type":"SYSTEM_TABLE"
      },
      "action":"READ"
  },
  {
    "resource":{
        "name":".*",
        "type":"SYSTEM_TABLE"
        },
      "action":"WRITE"
  },
  {
    "resource":{
        "name":".*",
        "type":"EXTERNAL"
        },
      "action":"READ"
  },
  {
    "resource":{
        "name":".*",
        "type":"EXTERNAL"
        },
      "action":"WRITE"
  },
  {
    "resource":{
        "name":".*",
        "type":"DATASOURCE"
        },
      "action":"READ"
  },
  {
    "resource":{
        "name":".*",
        "type":"DATASOURCE"
        },
      "action":"WRITE"
  },
  {
    "resource":{
        "name":".*",
        "type":"STATE"
        },
      "action":"READ"
  },
  {
    "resource":{
        "name":".*",
        "type":"STATE"
        },
      "action":"WRITE"
  },
  {
    "resource":{
        "name":".*",
        "type":"VIEW"
        },
      "action":"READ"
  },
  {
    "resource":{
        "name":".*",
        "type":"VIEW"
        },
      "action":"WRITE"
  },
]
```

- 資訊
  - 注意：Druid 將資源名稱（`name`）視為正規表示式（regex）。您可以使用特定資料來源名稱或正規表示式一次授予多個資料來源的權限。

### 配置 LDAP

作為使用基本元資料驗證器的替代方法，您可以使用 LDAP 對使用者進行身份驗證。有關為 LDAP 和 LDAPS 配置 Druid 的信息，請參閱配置[LDAP 身份驗證]()。

### Druid安全信任

在 Druid 的信任模型中，使用者可以有不同的授權等級：

- 具有資源寫入權限的使用者可以執行 druid 進程可以執行的任何操作。
- 經過身份驗證的唯讀使用者可以針對他們**有權存取**的資源執行查詢。
- 沒有任何權限的經過身份驗證的使用者可以執行**不需要存取資源**的查詢(已經分析好的圖表)。

此外，Druid 按照以下原則運行：

- 從最內層開始：
  - Druid 進程對**本機檔案**具有與執行該進程的啟動使用者，具有相同的存取權限。
  - Druid 攝取系統可以建立新的程序來執行任務。這些任務繼承其父進程的使用者。這意味著任何有權提交攝取任務的使用者，都可以使用攝取任務權限來讀取或寫入Druid程序有權存取的任何本機檔案或外部資源。
  - 注意：僅將權限授予`DATASOURCE WRITE`受信任的用戶，因為他們可以控制 Druid 進程。
- 集群內：
  - Druid 內設是在一個隔離的、受保護的網路上運行，且能保證網路中每個可存取的 IP 都不會受到駭客的控制。當您實施 Druid 時，請注意設定系統防火牆的設定和其他安全措施，以保護入站和出站連線。Druid 假設叢集內的內部網路流量是加密的，包括 API 呼叫和資料傳輸。預設加密的實作方式是使用 TLS。
  - Druid 假設元資料儲存和 ZooKeeper 節點等輔助服務，也不受到任何駭客的控制。
- 叢集到深度儲存：
  - Druid 不對深度儲存的安全性做出假設。它遵循系統的本機安全策略來對深度儲存進行身份驗證和授權。
  - Druid 不會對深度儲存的檔案進行加密。相反，它依賴儲存系統的本機加密功能來確保與所有儲存類型的加密方案的兼容性。
- 叢集到客戶端：
  - Druid 根據配置的身份驗證器、向客戶端進行身份驗證。
  - Druid 僅在授權者授予權限時執行操作。預設配置是allowAll authorizer.

### 報告安全

- Apache Druid 團隊非常重視安全性。
- 如果您在 Druid 中發現潛在的安全性問題，例如繞過前面所述的安全機制的方法，請將此問題回報給security@apache.org。這是一個私人郵件清單。請針對您報告的每個漏洞發送一封純文字電子郵件。

### 漏洞

漏洞處理流程總結如下：
- 回報者私下將漏洞回報給security@apache.org
- 回報者得到的回覆稱，Druid團隊已收到舉報，並將調查該問題。
- Druid 專案安全團隊私下與回報者合作解決漏洞。
- Druid 團隊透過創建受漏洞影響的軟體包的新版本來提供修復。
- Druid 團隊公開宣布了該漏洞並描述如何應用修復。
- 提交者應該閱讀該過程的更詳細的描述。安全漏洞的回報者也可能會發現它很有用。
  