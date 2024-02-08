---
layout: default
title:  使用Kerberos進行身分驗證
parent: Apache Druid
grand_parent: DB_servers
grand_parent: OLAP
last_modified_date: 2024-01-31 19:49:51
tags: DB_servers Druid
---

# # Apache Druid 安裝Kerberos驗證系統
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

- 這項Apache Druid 擴展插件可使用 Kerberos 對 Druid 程序進行驗證。
- 此擴充功能新增了一個驗證器，用於使用簡單且受保護的[GSSAPI](#gasapi)協商機制[SPNEGO](#spnego)來保護 HTTP 端點。確保包含 druid-kerberos在擴充功能載入清單中。

## 建立

```java
druid.auth.authenticatorChain=["MyKerberosAuthenticator"]
druid.auth.authenticator.MyKerberosAuthenticator.type=kerberos
```

- 若要使用 Kerberos 驗證器，請將帶有類型的驗證器新增kerberos至authenticatorChain。
- 上面的範例使用名稱“MyKerberosAuthenticator”作為身份驗證器。

### 指派

- 命名身份驗證器的配置:透過以下形式的屬性進行指派

```java
druid.auth.authenticator.<authenticatorName>.<authenticatorProperty>
```

本文檔其餘部分的設定範例將使用「kerberos」作為所配置的身份驗證器的名稱。

### 插件特質

特質項目	|可能的值|描述|預設|必需項目
|-|-|-|-|-
druid.auth.authenticator.kerberos.serverPrincipal|HTTP/_HOST@EXAMPLE.COM	druid 程序使用的 SPNEGO 服務主體	空的	是的
druid.auth.authenticator.kerberos.serverKeytab	/etc/security/keytabs/spnego.service.keytab	druid 程序使用的 SPNEgo 服務金鑰表	空的	是的
druid.auth.authenticator.kerberos.authToLocal	RULE:[1:$1@$0](druid@EXAMPLE.COM)s/.*/druid DEFAULT	它允許您設定將主體名稱對應到本機使用者名稱的一般規則。如果正在翻譯的主體名稱沒有明確映射，則將使用它。	預設	不
druid.auth.authenticator.kerberos.cookieSignatureSecret	secretString	用於簽署身分驗證 cookie 的秘密。如果您有多個 druid 節點在同一台機器上使用不同的連接埠運行，建議明確設定它，因為 Cookie 規範不保證連接埠隔離。	隨機值	不
druid.auth.authenticator.kerberos.authorizerName	取決於可用的授權者	請求應發送至的授權者	空的	是的

- 請注意，druid 程序使用的 SPNego 主體必須以 HTTP 開頭（由RFC-4559指定），且格式必須為「HTTP/_HOST@REALM」。特殊字串_HOST將自動替換為config的值druid.host

### 排除路徑

```java
druid.auth.authenticator.kerberos.excludedPaths
```

- 在舊版本中，Kerberos 身份驗證器有一個excludedPaths屬性，允許使用者指定應跳過身份驗證檢查的路徑清單。
- 此屬性已從 Kerberos 驗證器中刪除，因為路徑排除功能現在會透過設定在所有驗證器/授權器之間進行處理druid.auth.unsecuredPaths，如主驗證文件中所述。

## 本地帳密之授權與簡化

### 意義

"Auth to local" 是指在身份驗證（Authentication）過程中，使用本地（Local）的帳號和密碼進行身份驗證。這可能在系統或應用程式的設定中被使用。

例如，當使用者嘗試登入某個系統或應用程式時，系統可能會優先使用本地的帳號和密碼進行驗證，而不是依賴外部的身份驗證提供者（例如 LDAP、Active Directory 等）。

這樣的做法通常在一些狀況下使用，例如當系統需要一些本地權限或資源，而不希望依賴外部身份驗證時。然而，對於整體的安全性而言，要謹慎使用 "Auth to local" 的設定，因為這可能使得身份驗證的管理複雜化，也可能增加安全風險。

### 語法

```java
druid.auth.authenticator.kerberos.authToLocal允許您設定將主體名稱對應到本機使用者名稱的一般規則。映射規則的語法是RULE:\[n:string](regexp)s/pattern/replacement/g。整數n表示目標主體應該有多少個元件。如果匹配，則將從 string 形成一個字串，將主體的領域替換為 $0，將主體的第 n 個元件替換為 $neg（如果主體是 druid/admin），則會得到\[2:$2$1suffix]字串admindruidsuffix。如果該字串與正規表示式匹配，則將對該字串執行s// [ g] 取代命令。可選的 g 將導致替換在字串中全域進行，而不是僅替換字串中的第一個匹配項。如果需要，可以透過換行符號連接多個規則並將其指定為字串。
```

## 增加大型 SPNEGO 協商的http檔頭

- 在 Active Directory 環境中，授權標頭中的 SPNEGO 令牌包含 PAC（特權存取憑證）訊息，其中包括使用者的所有安全性群組。
- 在某些情況下，當使用者隸屬於許多安全群組時，標頭的成長將會超出了 druid 預設可以處理的範圍。
- 在這種情況下，可以透過設定`druid.server.http.maxRequestHeaderSize`（預設8KiB）和druid.router.http.maxRequestBufferSize（預設8KiB）來增加druid可以處理的最大請求標頭大小。

## Kerberos 升級功能之配置

- 使用Kerberos插件，Druid 內部的過程彼此之間將會透過一種升級、強化的 HTTP 客戶端進行通信。
- 在這種情境下，"escalated" 的意思可能是指經過提升、強化、或升級，表明這個 HTTP 客戶端可能具有一些特殊權限、安全性提升，或者其他升級的特性。
- 簡而言之，Druid 內部的模組之間通過 HTTP 客戶端相互溝通，而這個客戶端可能有一些特殊屬性或權限，使其能夠在內部過程之間進行更強化的通信。
- Druid 是使用升級後的內部程序來與http 用戶端相互通訊。
- 啟用 Kerberos 的升級 HTTP 用戶端可以透過以下屬性進行設定

財產	範例值	描述	預設	必需的
druid.escalator.type	kerberos	用於內部進程通訊的 Escalator 用戶端類型。	不適用	是的
druid.escalator.internalClientPrincipal	druid@EXAMPLE.COM	主要用戶名，用於內部進程通信	不適用	是的
druid.escalator.internalClientKeytab	/etc/security/keytabs/druid.keytab	用於內部進程通訊的密鑰表檔案的路徑	不適用	是的
druid.escalator.authorizerName	MyBasicAuthorizer	請求應發送至的授權者。	不適用	是的

## 啟動kerberos驗證後Druid HTTP 各端點的存取

- 需要透過curl存取druid HTTP端點，用戶需要先使用kinit以下命令登入

```bash
kinit -k -t <path_to_keytab_file> user@REALM.COM
```

- 登入成功後使用klist指令驗證登入是否成功
- 現在您可以使用curl命令存取druid HTTP端點，如下所示:

```bash 
curl --negotiate -u:anyUser -b ~/cookies.txt -c ~/cookies.txt -X POST -H'Content-Type: application/json' <HTTP_END_POINT>
```

- 例如，要將查詢從文件傳送query.json到 Druid Broker，請使用此命令:

```bash
curl --negotiate -u:anyUser -b ~/cookies.txt -c ~/cookies.txt -X POST -H'Content-Type: application/json'  http://broker-host:port/druid/v2/?pretty -d @query.json
```

注意：
- 以上命令將使用 SPNEgo 協商機制首次對使用者進行身份驗證，並將身份驗證 cookie 儲存在檔案中。
- 對於後續請求，cookie 將用於身份驗證。

## 從網頁

- 要從瀏覽器存取 Coordinator/Overlord 控制台，您需要將瀏覽器配置為 SPNego 身份驗證，如下所示 -

Safari - 無需配置。
Firefox - 開啟 Firefox 並依照下列步驟操作 -
前往about:config並蒐索network.negotiate-auth.trusted-uris.
雙擊並添加以下值："http://druid-coordinator-hostname:ui-port"和"http://druid-overlord-hostname:port"
Google Chrome - 從命令列執行以下命令 -
google-chrome --auth-server-whitelist="druid-coordinator-hostname" --auth-negotiate-delegate-whitelist="druid-coordinator-hostname"
google-chrome --auth-server-whitelist="druid-overlord-hostname" --auth-negotiate-delegate-whitelist="druid-overlord-hostname"
IE瀏覽器 -
配置受信任的網站以包括"druid-coordinator-hostname"和"druid-overlord-hostname"
允許 UI 網站協商。
發送查詢

許多 HTTP 用戶端程式庫（例如 Apache Commons HttpComponents ）已經支援執行 SPNEGO 驗證。您可以使用任何可用的 HTTP 用戶端程式庫與 druid 叢集進行通訊。


## Terminology

### SSSPI

GSSAPI（Generic Security Services Application Program Interface）是一種通用的安全服務應用程式介面。它是一個標準的應用程式編程界面，用於在不同的應用程式和協議之間提供通用的安全服務。GSSAPI 的目標是提供一種標準的方式，使應用程式能夠進行安全通信，而無需深入了解底層的安全機制。

GSSAPI 的主要特點包括：

1. **通用性：** GSSAPI 設計成通用的 API，允許應用程式使用相同的代碼與不同的安全機制進行交互。

2. **安全機制獨立性：** GSSAPI 可以與多種不同的安全機制（例如Kerberos、NTLM等）一起使用，使應用程式無需直接處理底層安全協議的細節。

3. **單點登入：** GSSAPI 支援單點登入（Single Sign-On），這使得一次認證可以被用於多個不同的應用程式和服務。

4. **跨平台性：** GSSAPI 的標準化有助於實現跨平台的安全通信，無論是在不同的操作系統還是編程語言中。

5. **支援加密和數位簽名：** GSSAPI 提供了加密、數位簽名等安全功能，確保通信的機密性和完整性。

GSSAPI 常用於支援安全的網路應用程式，例如客戶端-服務器應用程式、電子郵件和網際網路協議等，以確保在不安全的網路環境中進行通信時的安全性。

### SPNEGO

SPNEGO（Simple and Protected GSSAPI Negotiation Mechanism）是一種機制，用於在 GSSAPI 的框架下進行身份驗證協商。它主要用於網際網路應用程式中，允許客戶端和伺服器使用 GSSAPI 進行安全通信。

主要特點包括：

1. **單一登入：** SPNEGO 提供了單一登入功能，允許使用者只需一次身份驗證，就可以訪問多個相互信任的應用程式或伺服器。

2. **支援多種安全機制：** SPNEGO 可以協商多種支援的 GSSAPI 安全機制，例如 Kerberos、NTLM、Digest-MD5 等，以應對不同應用程式和環境的需求。

3. **GSSAPI 結合：** SPNEGO 是基於 GSSAPI 的，因此它利用 GSSAPI 的通用性和安全機制獨立性，允許不同的應用程式和平台之間實現安全通信。

4. **標準化：** SPNEGO 是一個標準的協商機制，有助於確保在不同系統和應用程式之間實現一致的單一登入體驗。

5. **安全性：** 通過使用 GSSAPI 的安全機制，SPNEGO 確保通信的機密性和完整性，以及身份驗證的可靠性。

SPNEGO 主要應用於支援單一登入的 Web 應用程式，使得使用者能夠方便地訪問多個相互信任的應用程式，同時保護通信的安全性。

### NTLM

NTLM（NT LAN Manager）雖然在過去被廣泛使用，但由於其安全性漏洞，現代環境中不再被視為最安全的身份驗證協議之一。以下是使用 NTLM 時應該考慮的一些建議安全檢查：

1. **避免單獨使用：** 不建議單獨使用 NTLM 作為主要的身份驗證協議。現代 Windows 環境更傾向於使用 Kerberos 協議，因為它提供更高的安全性。

2. **升級到最新版本：** 如果仍然需要使用 NTLM，確保所有系統和應用程式的版本都是最新的，以防止已知的漏洞。

3. **強化密碼策略：** 如果 NTLM 配置需要使用密碼，確保應用強化的密碼策略，包括長度、複雜性和定期更換。

4. **監控日誌：** 監控 NTLM 相關的事件日誌，以便追蹤可能的攻擊或濫用。特別注意登入失敗和異常活動。

5. **限制遠端訪問：** 如果不需要，盡量限制 NTLM 的遠端訪問。避免在不安全的網路上使用 NTLM。

6. **檢查安全性更新：** 確保已安裝操作系統和相關應用程式的最新安全性更新，以修補已知的 NTLM 漏洞。

7. **考慮其他身份驗證方式：** 如果可能，考慮使用更現代且安全的身份驗證方式，如 OAuth、OpenID Connect 或其他單一登入（SSO）解決方案。

8. **備份和還原：** 建立 NTLM 設定的備份，以便在需要時能夠快速還原到安全的配置。

總的來說，使用 NTLM 時應該謹慎，並且在可能的情況下遷移到更安全的身份驗證協議。
