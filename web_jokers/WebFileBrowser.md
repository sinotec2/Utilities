---
layout: default
title: WebFileBrowser
parent: Web Jokers
nav_order: 99
last_modified_date: 2025-02-13 14:40:16
tags: web
---

#  Web File Browser
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

## config init

### Synopsis

Initialize a new database to use with File Browser. All of this options can be changed in the future with the command 'filebrowser config set'. The user related flags apply to the defaults when creating new users and you don't override the options.

`filebrowser config init [flags]`

### Options

Name|Shorthand|Usage
-|:-:|-
addre|a|address to listen on
auth.header||HTTP header for auth.method=proxy
auth.method||authentication type
baseurl|b|base url
branding.disableExternal||disable external links such as GitHub links
branding.files||path to directory with images and custom styles
branding.name||replace 'File Browser' by this name
cert|t|tls certificate
commands||a list of the commands a user can execute
help|h|help for init
key|k|tls key
locale||locale for users
lockPassword||lock password
log|l|log output
perm.admin||admin perm for users
perm.create||create perm for users
perm.delete||delete perm for users
perm.download||download perm for users
perm.execute||execute perm for users
perm.modify||modify perm for users
perm.rename||rename perm for users
perm.share||share perm for users
port|p|port to listen on
recaptcha.host||use another host for ReCAPTCHA. recaptcha.net might be useful in China
recaptcha.key||ReCaptcha site key
recaptcha.secret||ReCaptcha secret
root|r|root to prepend to relative paths
scope||scope for users
shell||shell command to which other commands should be appended
signup|s|allow users to signup
sorting.asc||sorting by ascending order
sorting.by||sorting mode (name, size or modified)
viewMode||view mode for users

### Inherited

Name|Shorthand|Usage
-|:-:|-
config|c|config file path
database|d|database path

## window 端口設定

### 開放端口

是的，Windows 系統作為網路伺服器時，通常需要開放特定的網路端口，才能讓外部用戶存取服務。例如：

	•	Web 伺服器（IIS、Apache、Nginx） → 需開放 80（HTTP）、443（HTTPS）
	•	遠端桌面（RDP） → 需開放 3389
	•	資料庫伺服器（MySQL、MSSQL） → 需開放 3306（MySQL） 或 1433（MSSQL）
	•	FTP 伺服器 → 需開放 21（FTP 控制端口）
	•	其他應用程式 → 依需求開放特定端口

### 防火牆設定

如何在 Windows 防火牆開放端口？

	1.	 打開「Windows Defender 防火牆」
	•	Win + R → 輸入 wf.msc → 按 Enter
	2.	 點擊「進階設定」（左側選單）
	3.	 選擇「輸入規則」 → 點擊 「新增規則」
	4.	 選擇「連接埠」 → 點擊「下一步」
	5.	 選擇「TCP 或 UDP」 → 輸入要開放的端口號，例如 80 或 443
	6.	 選擇「允許連線」 → 點擊「下一步」
	7.	 選擇適用的網路範圍（「私人」或「公用」）
	8.	 命名規則（例如「開放 HTTP 服務」） → 點擊「完成」

### 如何用 PowerShell 開放端口？

如果需要自動化開放端口，可以使用 PowerShell：

New-NetFirewallRule -DisplayName "開放80端口" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow

這樣就能允許 HTTP 服務（80 端口）從外部訪問 Windows 伺服器。

如果要刪除該規則，可執行：

Remove-NetFirewallRule -DisplayName "開放80端口"

### 其他考量

- 確認 Windows 防火牆沒有阻擋流量
- 若有防毒軟體，需檢查是否有額外的網路保護功能
- 如果 Windows 位於內部網路，還需要在企業防火牆或路由器上開放對應端口
- 使用 netstat -an 或 Get-NetTCPConnection 檢查開放端口狀態

這樣，你的 Windows 伺服器就可以正確開放端口並提供服務了。

## 憑證

在 Windows 上產生 HTTPS 憑證（TLS/SSL）通常有幾種方式，以下是兩種常見方法：

1.	 使用 Let’s Encrypt（推薦）
2.	 使用 OpenSSL 生成自簽憑證（適用於內部測試環境）

### Let’s Encrypt

方法 1：使用 Let’s Encrypt（免費且自動續約）

Let’s Encrypt 提供免費 SSL 憑證，你可以使用 Certbot 來取得。

步驟 1：安裝 Certbot

Certbot 支援 Windows，可從官方下載 Certbot Windows 版 並安裝。

步驟 2：使用 Certbot 取得憑證

開啟 PowerShell（管理員權限）並執行：

certbot certonly --standalone -d yourdomain.com --preferred-challenges http

	•	--standalone：Certbot 會啟動一個臨時 Web 伺服器來驗證域名，因此必須確保 80 端口未被佔用。
	•	-d yourdomain.com：換成你的網域名稱。
	•	憑證會存放在 C:\Certbot\live\yourdomain.com\

步驟 3：續約憑證

Let’s Encrypt 憑證有效期限為 90 天，可使用排程工作（Task Scheduler）執行：

certbot renew

### OpenSSL

方法 2：使用 OpenSSL 產生自簽憑證（適用內部測試）

如果只是內部測試，Windows 也可以使用 OpenSSL 生成自簽名憑證。

步驟 1：安裝 OpenSSL

- 下載 Windows 版 OpenSSL：https://slproweb.com/products/Win32OpenSSL.html
- 安裝完成後，確保 openssl.exe 可在命令提示字元中執行。

步驟 2：產生自簽憑證

開啟 PowerShell 或 cmd 並執行：

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mykey.key -out mycert.crt

這會產生：

- mykey.key（私鑰）
- mycert.crt（自簽憑證）

注意：自簽憑證不被瀏覽器信任，需要手動安裝到 Windows 信任的憑證存儲區。

### 既有憑證

> 我的瀏覽器已經裝有一個聯外的憑證，可以利用來成為網路伺服器的憑證嗎？如何取得？

通常，瀏覽器裡的憑證是為了驗證客戶端身份而設計的，所以它們通常不可用作伺服器憑證。這些憑證存放在憑證儲存中，而且它們主要是用來建立安全通訊（如SSL/TLS）連接的。如果你希望用於網路伺服器的憑證，通常需要取得伺服器專用的憑證，並且你需要擁有私鑰。

你無法直接將瀏覽器中安裝的憑證用作網路伺服器憑證，除非該憑證包含私鑰並且它是設計來用於伺服器身份認證的。此外，一些瀏覽器憑證可能無法導出。

若要使用，通常你需要從瀏覽器的憑證儲存區導出憑證及私鑰（通常是 .pfx 格式）。但如果只是CA提供的憑證，那就無法用來認證伺服器。

是否能使用瀏覽器中安裝的憑證作為伺服器憑證，取決於憑證是否包含私鑰並具有伺服器驗證的用途。一般來說，瀏覽器憑證通常只是用來確認伺服器身份，而不適用於伺服器端。若有私鑰且符合伺服器驗證需求（如包含網域名稱），則可以從瀏覽器中導出憑證（例如PFX格式），並配置於伺服器上來啟用HTTPS。

## Windows 上的 Nginx HTTPS 設定

Windows 版 Nginx 設定 HTTPS 方式與 Ubuntu 相似，但有一些特別注意事項：

1. 設定 Nginx HTTPS

開啟 nginx.conf，在 server 區塊中加入：

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate C:/nginx/certs/mycert.crt;
    ssl_certificate_key C:/nginx/certs/mykey.key;

    location / {
        root   html;
        index  index.html index.htm;
    }
}

注意 Windows 路徑格式，使用 / 而非 \。

2. 確保 Nginx 支援 OpenSSL

Windows 版 Nginx 內建 OpenSSL，但如果報錯，可使用 nginx -V 檢查是否有 --with-http_ssl_module。

3. 開啟 Windows 防火牆 443 端口

New-NetFirewallRule -DisplayName "開放HTTPS" -Direction Inbound -Protocol TCP -LocalPort 443 -Action Allow

4. 重新啟動 Nginx

nginx -s reload

Windows vs Ubuntu 的 Nginx 設定差異

|項目|Windows	|Ubuntu
-|:-|-
配置檔案位置|C:\nginx\conf\nginx.conf|/etc/nginx/nginx.conf
憑證路徑格式|C:/nginx/certs/|/etc/nginx/certs/
服務啟動方式|nginx.exe|systemctl restart nginx
防火牆端口設定|需手動開啟 443 端口|ufw allow 443/tcp
憑證取得方式|Certbot / OpenSSL 手動|certbot --nginx 自動配置

Windows 版 Nginx 主要差異在 路徑格式、服務管理方式、防火牆設定，其他 HTTPS 設定基本相同。

如果你的 Windows 是 伺服器環境（Windows Server），可以考慮使用 IIS 內建的 HTTPS 功能，避免 Nginx 相關的相容性問題。

Windows 版 Nginx 不 內建 LDAP 驗證功能，因此如果想讓 Nginx on Windows 使用 LDAP 進行登入驗證，通常需要額外的 外掛模組或代理方式。

方法 1：使用 Nginx LDAP 模組（僅適用於 Linux 版 Nginx）

在 Linux 環境，可以使用 nginx-auth-ldap 模組來直接支援 LDAP 驗證，但這個模組 不支援 Windows，因此 Windows Nginx 無法直接使用。

	✅ 適用環境：Linux
❌ 不適用於 Windows

方法 2：使用反向代理方式（適用於 Windows）

因為 Windows 版 Nginx 無法原生支援 LDAP，我們可以使用 外部的 LDAP 驗證服務，然後透過 Nginx 反向代理，讓 Nginx 依賴外部身份驗證機制。

步驟 1：使用 Apache HTTP Server + mod_authnz_ldap
	•	安裝 Apache（Apache Lounge 提供 Windows 版）
	•	啟用 mod_authnz_ldap 模組
	•	設定 Apache 讓 /auth 進行 LDAP 驗證

Apache httpd.conf 設定範例：

<Location "/auth">
    AuthType Basic
    AuthName "LDAP Login"
    AuthBasicProvider ldap
    AuthLDAPURL "ldap://ldap.example.com:389/ou=users,dc=example,dc=com?sAMAccountName?sub?(objectClass=person)"
    Require valid-user
</Location>

這樣 http://localhost/auth 就會進行 LDAP 驗證。

步驟 2：讓 Nginx 透過 Apache 進行 LDAP 驗證

在 nginx.conf 中設定：

server {
    listen 80;
    server_name myserver;

    location /secure/ {
        auth_request /auth_verify;
        proxy_pass http://backend_server;
    }

    location = /auth_verify {
        internal;
        proxy_pass http://localhost/auth;
        proxy_pass_request_body off;
        proxy_set_header Content-Length "";
        proxy_set_header X-Original-URI $request_uri;
    }
}

這樣，當使用者存取 /secure/，Nginx 會先檢查 /auth_verify，Apache 會與 LDAP 驗證後回傳結果。

	✅ 適用環境：Windows & Linux
❌ 需要額外安裝 Apache

方法 3：使用 Keycloak、Authelia 等身份驗證系統

另一種方法是使用 身份驗證代理系統（如 Keycloak 或 Authelia），讓 Nginx 透過它們驗證 LDAP 身份，這種方法更現代化，適用於企業環境。

	✅ 適用環境：Windows & Linux
❌ 需要額外部署身份驗證系統

結論

方法	適用 Windows Nginx	需要額外安裝	適用環境
方法 1：Nginx 內建 LDAP 模組	❌ 不適用	-	只適用 Linux
方法 2：Apache 反向代理 LDAP	✅ 適用	Apache	Windows & Linux
方法 3：Keycloak / Authelia	✅ 適用	Keycloak / Authelia	Windows & Linux

在 Windows 上運行 Nginx 並使用 LDAP 驗證，最佳方式是 方法 2（使用 Apache 代理） 或 方法 3（使用身份驗證系統）。

## LDAP

> Window nginx 如果想使用LDAP驗證登入，是否還需要安裝什麼模組或程式庫？

Windows 版 Nginx 不 內建 LDAP 驗證功能，因此如果想讓 Nginx on Windows 使用 LDAP 進行登入驗證，通常需要額外的 外掛模組或代理方式。

方法 1：使用 Nginx LDAP 模組（僅適用於 Linux 版 Nginx）

在 Linux 環境，可以使用 nginx-auth-ldap 模組來直接支援 LDAP 驗證，但這個模組 不支援 Windows，因此 Windows Nginx 無法直接使用。

- ✅ 適用環境：Linux
- ❌ 不適用於 Windows

方法 2：使用反向代理方式（適用於 Windows）

因為 Windows 版 Nginx 無法原生支援 LDAP，我們可以使用 外部的 LDAP 驗證服務，然後透過 Nginx 反向代理，讓 Nginx 依賴外部身份驗證機制。

步驟 1：使用 Apache HTTP Server + mod_authnz_ldap
- 安裝 Apache（Apache Lounge 提供 Windows 版）
- 啟用 mod_authnz_ldap 模組
- 設定 Apache 讓 /auth 進行 LDAP 驗證

Apache httpd.conf 設定範例：

<Location "/auth">
    AuthType Basic
    AuthName "LDAP Login"
    AuthBasicProvider ldap
    AuthLDAPURL "ldap://ldap.example.com:389/ou=users,dc=example,dc=com?sAMAccountName?sub?(objectClass=person)"
    Require valid-user
</Location>

這樣 http://localhost/auth 就會進行 LDAP 驗證。

步驟 2：讓 Nginx 透過 Apache 進行 LDAP 驗證

在 nginx.conf 中設定：

server {
    listen 80;
    server_name myserver;

    location /secure/ {
        auth_request /auth_verify;
        proxy_pass http://backend_server;
    }

    location = /auth_verify {
        internal;
        proxy_pass http://localhost/auth;
        proxy_pass_request_body off;
        proxy_set_header Content-Length "";
        proxy_set_header X-Original-URI $request_uri;
    }
}

這樣，當使用者存取 /secure/，Nginx 會先檢查 /auth_verify，Apache 會與 LDAP 驗證後回傳結果。

- ✅ 適用環境：Windows & Linux
- ❌ 需要額外安裝 Apache

方法 3：使用 Keycloak、Authelia 等身份驗證系統

另一種方法是使用 身份驗證代理系統（如 Keycloak 或 Authelia），讓 Nginx 透過它們驗證 LDAP 身份，這種方法更現代化，適用於企業環境。

- 	✅ 適用環境：Windows & Linux
- ❌ 需要額外部署身份驗證系統

### 結論

方法	適用 Windows Nginx	需要額外安裝	適用環境
- 方法 1：Nginx 內建 LDAP 模組	❌ 不適用	-	只適用 Linux
- 方法 2：Apache 反向代理 LDAP	✅ 適用	Apache	Windows & Linux
- 方法 3：Keycloak / Authelia	✅ 適用	Keycloak / Authelia	Windows & Linux

在 Windows 上運行 Nginx 並使用 LDAP 驗證，最佳方式是 方法 2（使用 Apache 代理） 或 方法 3（使用身份驗證系統）。


