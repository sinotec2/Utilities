---
layout: default
title: keycloak
parent: web filebrowser
grand_parent: Web Jokers
nav_order: 99
last_modified_date: 2025-02-13 14:40:16
tags: web
---

#  keycloak
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


## Keycloak vs FreeIPA

> Keycloak 和FreeIPA是不是功能類似？這兩者都必須同時存在嗎？

Keycloak 和 FreeIPA 在某些方面有相似功能，但它們的核心用途不同，因此是否需要同時存在，取決於你的需求。

### 區別

1. Keycloak vs. FreeIPA 的主要區別

功能|Keycloak|FreeIPA
-|-|-
主要用途|單一登入 (SSO)、身份聯合 (Federation)、存取管理|企業級身份管理 (IDM)、LDAP 目錄服務、Kerberos 認證
身份驗證|OAuth2、OIDC、SAML|Kerberos、LDAP、RADIUS
使用者管理|內建用戶管理，也可連接 LDAP/AD	內建|LDAP 目錄，完整用戶管理
存取控制|角色型 (RBAC)、細粒度權限管理|基於 POSIX、Kerberos 與 SUDO 規則
協議支援|支援現代 Web 身份驗證協議 (OAuth2, OpenID Connect, SAML)|主要基於 Kerberos、LDAP
典型應用場景|Web 應用、微服務身份驗證、SSO|企業 IT 環境的帳號管理、Linux 伺服器存取控制

## 協力

2. 是否需要同時使用？

這取決於你的環境需求：

如果 FreeIPA 已經在使用，還需要 Keycloak 嗎？
- 不需要 如果你只需要一個內部的 LDAP/Kerberos 伺服器來管理 Linux 伺服器的使用者帳戶、SSH 登入、Samba 驗證等，那 FreeIPA 就足夠了。
- 需要 如果你有許多 Web 應用或 API 需要 SSO (OAuth2/OIDC/SAML) 支援，那麼 Keycloak 會更合適，因為 FreeIPA 本身並不直接支援這些協議。

如果 Keycloak 已經在使用，還需要 FreeIPA 嗎？
- 不需要 如果你只需要 Web 應用的身份管理，且 Keycloak 自己的使用者存儲 (內建資料庫或連接 AD) 就能滿足需求，那就不需要 FreeIPA。
- 需要 如果你需要完整的身份管理 (LDAP/Kerberos) 來管理 Linux 伺服器存取、SSH 登入、Samba、NFS 權限控制，那麼 FreeIPA 是更好的選擇，Keycloak 只能做 Web 認證。

### 整合

3. Keycloak 與 FreeIPA 整合

如果需要同時使用這兩者，Keycloak 可以設定為使用 FreeIPA 作為身份驗證來源：
1. Keycloak 連接 FreeIPA (LDAP) 作為使用者存儲
- Keycloak 可以透過 LDAP 連接 FreeIPA，讓 FreeIPA 管理使用者，而 Keycloak 提供 OAuth2/SAML 登入。
2. Keycloak 透過 FreeIPA 的 Kerberos 驗證
- 若 FreeIPA 啟用了 Kerberos，Keycloak 可設定 SPNEGO，允許自動登入 (Single Sign-On)。
3. FreeIPA 管理 Linux 伺服器，Keycloak 管理 Web 應用
- FreeIPA 負責 Linux 伺服器存取權限，Keycloak 負責 Web 應用的登入與授權。

### 結論

- 如果你的環境以 Linux 伺服器為主，FreeIPA 更適合
- 如果你的環境有許多 Web 應用，Keycloak 更適合
- 如果同時需要管理 Linux 伺服器與 Web 應用，兩者可以整合

