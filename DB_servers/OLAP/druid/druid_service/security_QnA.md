---
layout: default
title:  Security Q&A
parent: Apache Druid Services
grand_parent: Apache Druid
last_modified_date: 2024-01-07 20:26:18
tags: DB_servers Druid
---

# Apache Druid Security Q&A
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

- 安全與權限管理是伺服器的基礎設定。在測試與生產階段有很大的差異。

## 安全防護

Apache Druid 提供了一系列的安全措施，以確保系統的穩定性和數據的安全性。以下是一些 Apache Druid 安全措施的主要特點：

1. **Authentication（身份驗證）：** Druid 提供了基於 HTTP Basic 身份驗證的方式，可以使用各種身份驗證方法，如 LDAP、Kerberos 等，以確保只有授權的使用者能夠訪問系統。

2. **Authorization（授權）：** Druid 的授權機制通過 Role-Based Access Control（RBAC）實現，管理員可以定義用戶和角色，然後授予這些角色不同的權限，以確保數據的安全訪問。

3. **TLS/SSL 支援：** Druid 支援使用 TLS/SSL 進行加密通信，以保護數據在傳輸過程中的安全性。

4. **Segment Encryption（段加密）：** Druid 支援對數據段進行加密，保護數據在磁盤上的安全性。

5. **Audit Logging（審計記錄）：** Druid 記錄了所有的系統和用戶操作，以便審計和追蹤系統的使用情況。

6. **Secure Coordinator Communication（安全的協調器通信）：** 在 Druid 集群中，協調器之間的通信可以進行加密，以防止中間人攻擊。

7. **Kerberos 整合：** Druid 提供了對 Kerberos 的支援，允許使用者通過 Kerberos 進行身份驗證和授權。

8. **Preventative Measures（預防措施）：** Druid 提供了一系列的預防措施，以防止一些常見的安全問題，例如防止SQL注入攻擊。

9. **適用於雲平台的 IAM 整合：** 针对云平台，Druid 可与相应云平台的身份和访问管理（IAM）服务集成，以提供更高级别的身份验证和授权。

10. **密碼保護的設定：** Druid 允許對配置中的敏感信息進行加密，保護這些信息不受未授權的訪問。

實施這些安全措施可以幫助 Druid 在企業環境中更好地滿足數據安全和訪問控制的需求。需要注意的是，安全措施的實施可能會根據具體的 Druid 版本和部署情境有所不同，建議查閱相應版本的官方文檔以獲取最新的資訊。

## 權限管理

Druid 提供了一些機制來管理用戶訪問權限，但這可能需要透過其他工具或自定義的解決方案來實現更細緻的權限控制。

基本上，Druid 主要有以下幾種權限機制：

1. **Segment-level Security：** Druid 支援在段級別（segment-level）實現安全性。這意味著你可以限制用戶只能查看某些段（segments），以控制他們對數據的訪問。

2. **Query Granularity：** 你可以使用查詢級別（query granularity）來控制用戶對數據的訪問程度。這可以限制用戶僅能查詢某些特定的字段。

3. **Coarse-Grained Access Control：** Druid 支援對服務層進行粗粒度的訪問控制。這允許你根據 IP 地址或其他一般性的方式來限制用戶對 Druid 服務的訪問。

4. **Authentication and Authorization Plugins：** Druid 支援自定義的身份驗證（authentication）和授權（authorization）插件。這使得你可以根據特定的需求實現更複雜的權限管理。

然而，要實現更具體和差異化的權限管理，可能需要結合 Druid 的基本機制，使用外部的身份驗證系統或設計自定義的授權邏輯。這可能包括整合 LDAP、使用 Apache Ranger 等外部權限管理工具，或者實現自定義的 Druid 插件。詳細實現方式取決於你的具體需求和環境。

### LDAP

在 Druid 中，你可以透過配置相應的插件和設置來實現與 LDAP（Lightweight Directory Access Protocol）的整合。以下是一個簡單的步驟指南：

1. **配置 Common Runtime Properties：** 在 Druid 的配置文件（`common.runtime.properties`）中，你需要添加一些與 LDAP 相關的設置。這可能包括 LDAP 伺服器的地址、端口、基本 DN（Distinguished Name）等。

```properties
# LDAP Configuration
druid.ldap.url=ldap://your-ldap-server:389
druid.ldap.userSearchBase=ou=people,dc=example,dc=com
druid.ldap.userSearch=(uid=%s)
```

2. **配置 Authentication 和 Authorization：** 在 Druid 的配置文件中，你需要配置身份驗證（authentication）和授權（authorization）的相關插件，以與 LDAP 整合。以下是一個簡單的示例：

```properties
# Authentication Configuration
druid.auth.authenticatorChain=["ldap"]
druid.auth.authenticator.ldap.type=ldap
druid.auth.authenticator.ldap.initialAdminUser=username
druid.auth.authenticator.ldap.initialAdminPassword=password

# Authorization Configuration
druid.auth.authorizerName=metadata
```

3. **啟用 HTTPS（可選）：** 如果你的 LDAP 通信需要加密，你可能需要啟用 Druid 的 HTTPS 支持。這涉及到配置 SSL 以保護通信。

4. **重新啟動 Druid 服務：** 在應用了相應的配置後，重新啟動 Druid 服務，讓配置生效。

請注意，以上僅為一個簡單的示例，實際配置取決於你的 LDAP 伺服器和 Druid 的版本。在實施之前，建議參考 Druid 官方文檔，特別是與你使用的 Druid 版本相對應的文檔，以獲得更具體的信息。

### 其他插件

在 Druid 中，除了 LDAP 插件外，還有其他一些與權限管理相關的插件。以下是一些 Druid 中用於權限管理的插件：

1. **BasicAuthentication：**
   - **描述：** 基本身份驗證插件，通過使用者名稱和密碼進行身份驗證。
   - **配置範例：**
     ```properties
     # Authentication Configuration
     druid.auth.authenticatorChain=["basic"]
     druid.auth.authenticator.basic.type=basic
     druid.auth.authenticator.basic.initialAdminUser=username
     druid.auth.authenticator.basic.initialAdminPassword=password
     ```
- see [Basic Security](https://druid.apache.org/docs/latest/development/extensions-core/druid-basic-security/)
2. **MetadataStoreAuthorizer：**
   - **描述：** 元數據存儲授權插件，是 Druid 預設的授權插件。它基於元數據中的規則控制用戶對 Druid 的訪問權限。
   - **配置範例：**
     ```properties
     # Authorization Configuration
     druid.auth.authorizerName=metadata
     ```

3. **PermissiveAuthorizer：**
   - **描述：** 一個寬鬆的授權插件，允許所有操作，通常用於測試或開發環境。
   - **配置範例：**
     ```properties
     # Authorization Configuration
     druid.auth.authorizerName=permissive
     ```

這些插件提供了在 Druid 中配置不同類型權限管理策略的選擇。在使用這些插件時，需要仔細閱讀相關的官方文檔，確保插件的配置與 Druid 的版本相符合。配置中可能需要指定用於初始化的管理員用戶和密碼等信息，以確保正確的權限設定。

