---
layout: default
title: Windows系統的LDAP設定
parent: web filebrowser
grand_parent: Web Jokers
nav_order: 99
last_modified_date: 2025-02-13 14:40:16
tags: web
---

#  Windows HTTPS 的LDAP設定
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

- ✅ 適用環境：Windows & Linux
- ❌ 需要額外部署身份驗證系統

## 結論

方法|適用 Windows Nginx|需要額外安裝|適用環境
-|-|-|-|
方法 1：Nginx 內建 LDAP 模組|❌ 不適用|-|只適用 Linux
方法 2：Apache 反向代理 LDAP	|✅ 適用	|Apache|Windows & Linux
方法 3：Keycloak / Authelia	|✅ 適用	|Keycloak / Authelia|Windows & Linux

在 Windows 上運行 Nginx 並使用 LDAP 驗證，最佳方式是 方法 2（使用 Apache 代理） 或 方法 3（使用身份驗證系統）。

## LDAP tunings

> Window Apache httpd 連線到centos的LDAP伺服器，通過ou的群組認證，卻不能回到網頁，出現平台或記憶體不足報錯，使用個別使用者檢核則沒有問題，可能是什麼原因？

當 Windows 上的 Apache HTTPD 連接 CentOS LDAP 伺服器，使用 OU 群組認證 時出現「平台或記憶體不足」錯誤，而單獨使用者驗證沒有問題，可能的原因包括：

### 可能的問題點

1.	 LDAP 群組查詢結果過大，導致記憶體耗盡
  若 OU (組織單位) 內的使用者數量龐大，Apache HTTPD 可能在處理群組驗證時耗盡記憶體或 CPU，導致錯誤。
- 解決方案：
  - 減少 LDAP 查詢範圍，改用 require ldap-group 而不是 require ldap-filter 來精確匹配群組。
  - 檢查 LimitRequestBody、LimitRequestFieldSize 等 HTTPD 參數，調整為較大值。

2.	 LDAP 查詢超時 (Timeout)
	•	群組驗證可能需要多層級的查詢，例如檢查 memberOf 屬性，若 LDAP 伺服器回應過慢，HTTPD 可能報錯。
	•	解決方案：
	•	調整 Apache LDAPTimeout 設定，例如：

LDAPTimeout 10


	•	使用 LDAP 索引來加速查詢 (slapd.conf 或 cn=config 中優化索引)。
	•	測試手動查詢 LDAP，確認回應時間：

ldapsearch -x -LLL -H ldap://centos-server -D "cn=admin,dc=example,dc=com" -W -b "ou=group,dc=example,dc=com"


	3.	Apache HTTPD 模組 (mod_ldap) 記憶體問題
	•	mod_ldap 和 mod_authnz_ldap 模組在驗證大量使用者時可能出現記憶體管理問題，導致錯誤。
	•	解決方案：
	•	增加 Apache MaxMemFree 限制，例如在 httpd.conf 加入：

MaxMemFree 512


	•	測試降低 LDAPCacheEntries，避免快取過多 LDAP 查詢：

LDAPCacheEntries 100


	4.	LDAP 群組配置方式不支援
	•	部分 LDAP 伺服器使用 memberUid 而非 memberOf 來存儲群組資訊，這可能與 Apache HTTPD 的 LDAP 群組驗證方式不匹配。
	•	解決方案：
	•	在 Apache 設定中使用 AuthLDAPGroupAttributeIsDN off，例如：

AuthLDAPGroupAttributeIsDN off



建議的排查步驟
	1.	檢查 Apache 記憶體使用狀況 (Task Manager 或 htop)。
	2.	測試 單一群組驗證 (require ldap-group 而非 require ldap-filter)。
	3.	監控 LDAP 伺服器負載 (top、htop、journalctl -u slapd 等)。
	4.	縮小查詢範圍，減少 LDAP 回應時間。

這些步驟應該能幫助你找到問題的根本原因。

## 中文群組名稱

> 回到ou那題，何以一樣的條件、我在centos/ubuntu平台上可以運作？win上卻不行，是因為編碼沒有處理好嗎？我的群組名稱是中文的。

###

你的問題可能與編碼和Windows 上的 Apache LDAP 模組支援有關，以下是幾個可能的原因：

可能的原因
	1.	LDAP 查詢時的編碼問題（高機率）
	•	CentOS/Ubuntu 預設使用 UTF-8，而 Windows 可能會使用其他編碼（如 CP950、GBK、Big5 等）。
	•	如果你的群組名稱是中文，而 Apache 連線 LDAP 時未正確處理編碼，可能會造成認證失敗或 LDAP 回傳異常。
	2.	Windows 上的 Apache HTTPD 編碼設定
	•	Windows 版的 httpd 可能沒有正確處理 LDAP 回應的非 ASCII 字元，導致無法匹配 OU 群組名稱。
	•	確保 Apache 啟用了 Unicode 支援，特別是在 mod_ldap 和 mod_authnz_ldap 的設定中。
	3.	Windows 上的 OpenLDAP 客戶端行為不同
	•	Windows 上的 mod_ldap 可能與 Linux 版有所不同，可能使用了不同的編碼方式來查詢 LDAP。
	4.	HTTPD 與 LDAP 伺服器的連線機制不同
	•	CentOS/Ubuntu 可能使用 GSSAPI（Kerberos） 來認證 LDAP，而 Windows 版的 HTTPD 可能沒有完整支援這些機制。

解決方案

1. 強制 LDAP 查詢使用 UTF-8

試試在 httpd.conf 中加上：

LDAPDefaultAuthzProvider on

或在 .htaccess 中加：

AddDefaultCharset UTF-8

確保 Apache 送出 LDAP 查詢時使用 UTF-8。

2. 檢查 mod_authnz_ldap 是否正確安裝

Windows 版 Apache 需要額外啟用 LDAP 模組，請確保 httpd.conf 有這些設定：

LoadModule ldap_module modules/mod_ldap.so
LoadModule authnz_ldap_module modules/mod_authnz_ldap.so

3. 嘗試將 OU 名稱改成 ASCII

若可能，請測試：
	•	先將 LDAP 內的 群組名稱改為英文，看看 Windows 能否認證成功。
	•	如果英文可以，但中文不行，那就是Windows 版 Apache 無法正確處理 UTF-8 的 LDAP 查詢。

4. 直接用 ldapsearch 測試

在 Windows 上的 CMD 或 PowerShell 試試：

ldapsearch -H ldap://你的LDAP伺服器 -D "你的管理員DN" -W -b "dc=你的公司,dc=com" "(cn=你的中文群組名)"

如果這裡查不到，代表 Windows 上的 LDAP 客戶端沒處理好中文編碼。

5. 設定 Apache 讓 mod_ldap 使用 UTF-8

如果可能的話，在 Apache 設定 httpd.conf 裡加：

LDAPCharsetConfig utf8

或：

SetEnv LDAPCONF /etc/ldap/ldap.conf

然後在 ldap.conf（Windows 版 Apache 可能是 C:\Apache24\conf\ldap.conf）中：

BASE dc=你的公司,dc=com
URI ldap://你的LDAP伺服器
SIZELIMIT 0
TIMELIMIT 0
DEREF never

### 結論

如果 CentOS/Ubuntu 可以，但 Windows 不行，很可能是 Windows 版的 Apache mod_ldap 或 mod_authnz_ldap 沒有正確處理 UTF-8 編碼。

優先測試：

1.	 ldapsearch 是否能在 Windows 查到 OU 群組（可測試中文、英文）。
2.	 在 httpd.conf 設定 AddDefaultCharset UTF-8。
3.	 嘗試修改 LDAP 群組名稱為英文來測試。
4.	 確保 Windows 上 mod_ldap 和 mod_authnz_ldap 正常運作。


