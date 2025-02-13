


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

方法|適用 Windows Nginx	需要額外安裝	適用環境
方法 1：Nginx 內建 LDAP 模組	❌ 不適用	-	只適用 Linux
方法 2：Apache 反向代理 LDAP	✅ 適用	Apache	Windows & Linux
方法 3：Keycloak / Authelia	✅ 適用	Keycloak / Authelia	Windows & Linux

在 Windows 上運行 Nginx 並使用 LDAP 驗證，最佳方式是 方法 2（使用 Apache 代理） 或 方法 3（使用身份驗證系統）。

