

# Apache Druid 安裝Kerberos驗證系統

## 背景

- 這項Apache Druid 擴展插件可使用 Kerberos 對 Druid 程序進行驗證。
- 此擴充功能新增了一個驗證器，用於使用簡單且受保護的[GSSAPI][gasapi]協商機制SPNEGO來保護 HTTP 端點。確保包含 druid-kerberos在擴充功能載入清單中。


## 建立


druid.auth.authenticatorChain=["MyKerberosAuthenticator"]

druid.auth.authenticator.MyKerberosAuthenticator.type=kerberos


- 若要使用 Kerberos 驗證器，請將帶有類型的驗證器新增kerberos至authenticatorChain。
- 上面的範例使用名稱“MyKerberosAuthenticator”作為身份驗證器。

- 命名身份驗證器的配置:透過以下形式的屬性進行指派


druid.auth.authenticator.<authenticatorName>.<authenticatorProperty>


本文檔其餘部分的設定範例將使用「kerberos」作為所配置的身份驗證器的名稱。


財產	可能的值	描述	預設	必需的
druid.auth.authenticator.kerberos.serverPrincipal	HTTP/_HOST@EXAMPLE.COM	druid 程序使用的 SPNEGO 服務主體	空的	是的
druid.auth.authenticator.kerberos.serverKeytab	/etc/security/keytabs/spnego.service.keytab	druid 程序使用的 SPNEgo 服務金鑰表	空的	是的
druid.auth.authenticator.kerberos.authToLocal	RULE:[1:$1@$0](druid@EXAMPLE.COM)s/.*/druid DEFAULT	它允許您設定將主體名稱對應到本機使用者名稱的一般規則。如果正在翻譯的主體名稱沒有明確映射，則將使用它。	預設	不
druid.auth.authenticator.kerberos.cookieSignatureSecret	secretString	用於簽署身分驗證 cookie 的秘密。如果您有多個 druid 節點在同一台機器上使用不同的連接埠運行，建議明確設定它，因為 Cookie 規範不保證連接埠隔離。	隨機值	不
druid.auth.authenticator.kerberos.authorizerName	取決於可用的授權者	請求應發送至的授權者	空的	是的
請注意，druid 程序使用的 SPNego 主體必須以 HTTP 開頭（由RFC-4559指定），且格式必須為「HTTP/_HOST@REALM」。特殊字串_HOST將自動替換為config的值druid.host

druid.auth.authenticator.kerberos.excludedPaths

在舊版本中，Kerberos 身份驗證器有一個excludedPaths屬性，允許使用者指定應跳過身份驗證檢查的路徑清單。此屬性已從 Kerberos 驗證器中刪除，因為路徑排除功能現在會透過設定在所有驗證器/授權器之間進行處理druid.auth.unsecuredPaths，如主驗證文件中所述。

授權本地

druid.auth.authenticator.kerberos.authToLocal允許您設定將主體名稱對應到本機使用者名稱的一般規則。映射規則的語法是RULE:\[n:string](regexp)s/pattern/replacement/g。整數n表示目標主體應該有多少個元件。如果匹配，則將從 string 形成一個字串，將主體的領域替換為 $0，將主體的第 n 個元件替換為 $neg（如果主體是 druid/admin），則會得到\[2:$2$1suffix]字串admindruidsuffix。如果該字串與正規表示式匹配，則將對該字串執行s// [ g] 取代命令。可選的 g 將導致替換在字串中全域進行，而不是僅替換字串中的第一個匹配項。如果需要，可以透過換行符號連接多個規則並將其指定為字串。

增加大型 SPNEGO 協

在 Active Directory 環境中，授權標頭中的 SPNEGO 令牌包含 PAC（特權存取憑證）訊息，其中包括使用者的所有安全性群組。在某些情況下，當使用者屬於許多安全群組時，標頭的成長超出了 druid 預設可以處理的範圍。druid.server.http.maxRequestHeaderSize在這種情況下，可以透過設定（預設8KiB）和druid.router.http.maxRequestBufferSize（預設8KiB）來增加druid可以處理的最大請求標頭大小。

配置 Kerberos 升級

Druid 內部程序使用升級的 http 用戶端相互通訊。啟用 Kerberos 的升級 HTTP 用戶端可以透過以下屬性進行設定 -

財產	範例值	描述	預設	必需的
druid.escalator.type	kerberos	用於內部進程通訊的 Escalator 用戶端類型。	不適用	是的
druid.escalator.internalClientPrincipal	druid@EXAMPLE.COM	主要用戶名，用於內部進程通信	不適用	是的
druid.escalator.internalClientKeytab	/etc/security/keytabs/druid.keytab	用於內部進程通訊的密鑰表檔案的路徑	不適用	是的
druid.escalator.authorizerName	MyBasicAuthorizer	請求應發送至的授權者。	不適用	是的
kerberos 安全性時存取 Druid HTTP 端點

要透過curl存取druid HTTP端點，用戶需要先使用kinit以下命令登入 -

kinit -k -t <path_to_keytab_file> user@REALM.COM


登入成功後使用klist指令驗證登入是否成功

現在您可以使用curl命令存取druid HTTP端點，如下所示 -

curl --negotiate -u:anyUser -b ~/cookies.txt -c ~/cookies.txt -X POST -H'Content-Type: application/json' <HTTP_END_POINT>


例如，要將查詢從文件傳送query.json到 Druid Broker，請使用此命令 -

curl --negotiate -u:anyUser -b ~/cookies.txt -c ~/cookies.txt -X POST -H'Content-Type: application/json'  http://broker-host:port/druid/v2/?pretty -d @query.json


注意：以上命令將使用 SPNEgo 協商機制首次對使用者進行身份驗證，並將身份驗證 cookie 儲存在檔案中。對於後續請求，cookie 將用於身份驗證。

從網頁

要從瀏覽器存取 Coordinator/Overlord 控制台，您需要將瀏覽器配置為 SPNego 身份驗證，如下所示 -

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
