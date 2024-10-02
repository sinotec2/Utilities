---
layout: default
title:  samba connected through LDAP authentication
parent: LDAP
grand_parent: Security And Authentication
last_modified_date: 2024-10-02 20:29:52
tags: LDAP gitea
---

#  LDAP 帳密認證SAMBA連線
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

## GPT4o

是的，可以將 **Samba** 與 **FreeIPA** 或 **LDAP** 伺服器集成，讓 Samba 使用 LDAP 中的用戶來進行身份驗證。通過這種方式，Samba 可以自動生成和管理 Samba 用戶，並且使用與 LDAP/FreeIPA 相同的用戶和密碼。

以下是實現該功能的主要步驟和配置思路：

### 1. 設定 FreeIPA/LDAP 作為 Samba 認證後端

Samba 支持使用 LDAP 作為用戶和組的數據庫。這意味著你可以使用 FreeIPA 的 LDAP 資料來讓 Samba 執行身份驗證。

### 2. 安裝所需的軟體

首先需要安裝 Samba 和相應的 LDAP 模塊：

```bash
yum install samba samba-client samba-winbind samba-winbind-clients
```

### 3. 配置 Samba 連接到 FreeIPA/LDAP

#### 編輯 `smb.conf` 文件

在 `/etc/samba/smb.conf` 文件中，您需要配置 Samba 來使用 LDAP 進行認證。下面是一個範例配置：

```ini
[global]
   workgroup = YOUR_WORKGROUP
   security = user
   passdb backend = ldapsam:ldap://your-ldap-server
   ldap suffix = dc=sinotech-eng,dc=com
   ldap user suffix = ou=People
   ldap group suffix = ou=Groups
   ldap machine suffix = ou=Computers
   ldap admin dn = cn=Directory Manager
   ldap ssl = off
   ldap passwd sync = yes
```

其中：
- `ldap suffix` 是您的 LDAP 目錄的基本 DN。
- `ldap user suffix` 是 LDAP 中存儲用戶的子目錄。
- `ldap admin dn` 是 LDAP 中有權限修改 Samba 密碼的管理員帳戶。

#### 設置 Samba 用戶同步

為了讓 Samba 能夠自動生成使用者帳戶，您可以使用 `smbldap-tools` 來實現 Samba 使用者的同步和自動生成。這些工具允許通過 LDAP 資料庫來管理 Samba 用戶和組。

安裝 `smbldap-tools`：（yum is deprecated）

```bash
yum install smbldap-tools
```

然後在 `smbldap.conf` 中設置與 LDAP 的連接信息，將其指向 FreeIPA 或其他 LDAP 伺服器。(deprecated,   設定詳見[官網](https://wiki.samba.org/index.php/1.0:_Configuring_Samba))

### 4. 配置自動同步

FreeIPA 本身也支持管理 Samba 所需的 LDAP 屬性，如 Samba NT 密碼、LM 密碼和 SambaSID。可以通過 FreeIPA 插件來實現自動同步，或編寫腳本來在新建用戶時自動生成 Samba 所需的屬性。

#### 配置 Samba 和 FreeIPA 密碼同步

你可以通過設置 FreeIPA 伺服器來自動同步 LDAP 和 Samba 密碼，這樣用戶更改 FreeIPA 密碼時會自動更新 Samba 密碼。這需要啟用 `ipa-samba` 模塊，並確保 FreeIPA 中的 Samba 使用者資料（如 `sambaSID` 和 `sambaNTPassword`）正確設置。

### 5. 測試配置

配置完成後，通過以下命令來測試 Samba 是否能夠使用 FreeIPA 的 LDAP 進行身份驗證：

```bash
smbclient -L localhost -U <ldap-user>
```

這應該會提示輸入 LDAP 用戶的密碼，並列出可用的共享資源。

### 6. 自動生成 Samba 使用者帳密

在 FreeIPA 中創建用戶時，可以自動生成所需的 Samba 屬性（如 `sambaSID`、`sambaNTPassword`）。這可以通過 FreeIPA 中的自定義規則實現，或者在用戶創建後手動使用 `smbldap-useradd` 命令來將用戶添加到 Samba 資料庫。

### 7. 參考工具

- [**smbldap-tools**](https://wiki.samba.org/index.php/4.1_smbldap-tools): 用來同步和管理 Samba 和 LDAP 用戶。
- [**ipa-samba-setup**](): FreeIPA 提供的 Samba 支持模塊。

### 總結

通過將 FreeIPA/LDAP 與 Samba 集成，可以實現 Samba 使用 LDAP 中的帳號和密碼進行身份驗證，同時通過腳本或工具自動生成 Samba 需要的帳號屬性。

## Claude3

是的，可以讓 SAMBA 服務讀取 LDAP 認證並自動生成 SAMBA 使用者帳號和密碼。這種配置可以提供更集中化的使用者管理，特別適合大型網路環境。以下是實現這個目標的基本步驟和考慮事項：

### 基本步驟和考慮事項

1. LDAP 配置：

   - 確保你有一個正常運行的 LDAP 服務器，如 OpenLDAP。
   - 在 LDAP 中存儲用戶資訊，包括用戶名、UID、GID 等。

2. SAMBA 配置：
   - 安裝支持 LDAP 的 SAMBA 版本。
   - 修改 SAMBA 的配置文件（通常是 /etc/samba/smb.conf），添加 LDAP 相關設置。

3. PAM（Pluggable Authentication Modules）配置：
   - 配置 PAM 以使用 LDAP 進行認證。
   - 這允許系統級別的 LDAP 認證，SAMBA 可以利用這點。

4. NSS（Name Service Switch）配置：
   - 配置 NSS 以從 LDAP 獲取用戶和組資訊。

5. SAMBA-LDAP 整合：
   - 使用 smbpasswd 或 pdbedit 工具將 SAMBA 帳戶資訊同步到 LDAP。

6. 自動創建用戶腳本：
   - 編寫腳本自動從 LDAP 讀取用戶資訊。
   - 使用這些資訊自動在 SAMBA 中創建對應的用戶。

### 範例配置

smb.conf 的部分內容：

```bash
[global]
   workgroup = WORKGROUP
   security = user
   passdb backend = ldapsam:ldap://ldap.example.com
   ldap suffix = dc=example,dc=com
   ldap user suffix = ou=Users
   ldap group suffix = ou=Groups
   ldap admin dn = cn=admin,dc=example,dc=com
   ldap ssl = start tls
   ldap passwd sync = yes
```

### 注意事項

1. 安全性：確保 LDAP 連接使用 SSL/TLS 加密。
2. 權限管理：仔細規劃 LDAP 中的用戶權限，以確保正確的訪問控制。
3. 密碼同步：考慮如何處理密碼同步問題，特別是當用戶在 LDAP 中更改密碼時。
4. 效能：大型環境中，考慮使用 LDAP 緩存以提高性能。
5. 備份：定期備份 LDAP 數據，以防數據丟失。

實施這樣的設置需要對 LDAP、SAMBA 和 Linux 系統管理有深入的了解。建議在測試環境中先進行充分的測試和驗證，然後再部署到生產環境。

