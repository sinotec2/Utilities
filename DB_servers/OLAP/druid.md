---
layout: default
title:  Druid
parent: OLAP
grand_parent: DB_servers
last_modified_date: 2024-01-07 20:26:18
tags: DB_servers Druid
---

# Druid Apache
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

Apache Druid（之前稱為Imply Druid）是一個快速、分散式、開源的分析型資料庫，主要用於 OLAP（Online Analytical Processing）工作負載。以下是一些 Apache Druid（Druid）的特點：

1. **快速查詢：** Druid 設計用於支援快速的查詢和分析，特別適用於大型數據集。

2. **即時數據更新：** Druid 提供即時數據更新的能力，支援即時數據的快速插入和查詢。

3. **分散式架構：** Druid 是一個分散式系統，可以擴展到多個節點，支援水平擴展，提供高可用性和容錯能力。

4. **列式儲存：** Druid 使用列式儲存格式，這有助於快速的分析和壓縮大量數據。

5. **支援多維數據模型：** Druid 支援多維數據模型，可以進行複雜的多維分析。

6. **自助式分析：** 使用者可以使用 SQL 或一些 Druid 提供的查詢語言進行自助式分析。

7. **豐富的生態系統：** Druid 生態系統包括一系列的工具和整合，以支援數據載入、監控、管理和查詢等方面。

Druid 主要用於處理即時數據、事件數據、日誌數據等工作負載，適用於需要快速查詢和分析的場景，例如業務智能、數據探勘、即時監控等。

### 完整介紹與比較

[ITxiaoshen blog](https://www.cnblogs.com/itxiaoshen/p/17081162.html#%E9%80%82%E7%94%A8%E5%9C%BA%E6%99%AF)

## 安裝

- [quick start](https://druid.apache.org/docs/latest/tutorials/)

## apache druid的可能缺點或弱勢。

### 一般性

Apache Druid是一個強大的實時數據分析系統，但它也有一些可能的缺點或弱勢：

1. **有限的join能力**：Druid適用於清洗好的數據實時寫入，不需要更新數據，所以數據在寫入Druid之前一般需要拉寬處理，在從Druid中查詢數據時，直接查詢這張寬表即可。在Druid最新版本0.21.1支持join，join右側的表都會自動存放內存再做關聯，這樣會降低性能¹。

2. **不支持多時間維度，所有維度為String類型**：Druid的數據模型主要是基於時間序列的，並且所有的維度都被存儲為字符串¹。

3. **只支持流式寫入，不支持實時數據更新**：如果需要更新數據，可以使用批處理作業完成¹。

4. **不支持精確去重**：Druid的數據模型並不直接支持精確的去重計數¹。

以上就是Apache Druid的一些可能的缺點或弱勢。希望這些信息對您有所幫助。如果您有其他問題，歡迎隨時提問。¹

來源: 與 Bing 的交談， 2024/1/26
(1) 大数据Apache Druid（一）：Druid简单介绍和优缺点 - [知乎](https://zhuanlan.zhihu.com/p/554605708).
(2) 熵简技术谈 | 实时OLAP引擎之Apache Druid：架构、原理和应用实践 - [知乎](https://zhuanlan.zhihu.com/p/178572172).
(3) 【超详细】Apache Durid从入门到安装详细教程 - [知乎](https://zhuanlan.zhihu.com/p/558085506).
(4) 十分钟了解 Apache Druid-腾讯云开发者社区-[腾讯云](https://cloud.tencent.com/developer/article/1603640).

### 單一節點資料量限制

Apache Druid在單一節點的資料量確實有一定的限制。如果單一節點的資料量過大，可能會導致系統性能下降，影響查詢速度和數據處理效率。

對於數G的資料庫，如果您的工作負載並不是非常大，並且您的查詢並不需要在短時間內返回大量數據，那麼使用單一節點的Apache Druid可能是可行的。但是，如果您的數據量和查詢需求預計會快速增長，或者您需要在短時間內處理大量查詢，那麼您可能需要考慮使用更多的節點，或者選擇其他更適合大數據處理的數據庫系統。

請注意，這些都是一般性的建議，具體情況可能會因您的具體需求和工作負載而異。在選擇數據庫系統時，最好根據您的具體需求和資源來做出決定。¹²。如果您有其他問題或需要更具體的建議，請隨時告訴我！

來源: 與 Bing 的交談， 2024/1/26
(1) Azure 上的 Apache NiFi - [Azure Architecture Center](https://learn.microsoft.com/zh-tw/azure/architecture/example-scenario/data/azure-nifi).
(2) 選擇資料庫 (DB) 的五大注意事項 - 程式愛好者 - [Medium](https://medium.com/程式愛好者/選擇資料庫-db-的五大注意事項-a719e134e7d).
(3) SharePoint 限制 - Service Descriptions | [Microsoft Learn](https://learn.microsoft.com/zh-tw/office365/servicedescriptions/sharepoint-online-service-description/sharepoint-online-limits).
(4) 查詢限制 - Azure 資料總管 - Azure Data Explorer | [Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/data-explorer/kusto/concepts/querylimits).

## _time generations

```python
from pandas import *
from datetime import datetime

df0=read_csv('df0.csv')

def convert_date_format(old_format_date_str):
    # 解析舊格式日期字符串
    old_format_date = datetime.strptime(old_format_date_str, "%m %d %Y %I:%M%p")

    # 將日期轉換為新格式
    new_format_date_str = old_format_date.strftime("%Y-%m-%d %H:%M:%S.%f")

    return new_format_date_str
old_date_str = "01 18 2021 4:10PM"
new_date_str = convert_date_format(old_date_str)
print(new_date_str)
df0['申報日期2']=[convert_date_format(i) for i in list(df0['申報日期'])]
df0.loc[0]
df0.to_csv('df0.csv',index=False)
```

## Columns selections

在將資料轉換成 Delta Lake 之前或之後進行篩選，取決於多個因素，包括數據量、性能需求、資料處理流程等。

以下是兩種方式的比較：

1. **先篩選後轉換成 Delta Lake:**
   - **優點:**
     - 可以減小 Delta Lake 表的大小，節省存儲空間。
     - 轉換成 Delta Lake 的過程只需處理真正需要的資料。
     - 如果篩選條件簡單且能在原始資料上有效執行，可能可以提高性能。
   - **缺點:**
     - 如果原始資料很大，並且篩選後的資料量相對較小，可能需要額外的步驟和資源來處理和管理兩個資料集。

2. **先轉換成 Delta Lake 再進行篩選:**
   - **優點:**
     - 簡化了轉換和管理的流程，只需處理一個資料集。
     - 如果 Delta Lake 表被多次查詢，可以避免重複的篩選操作。
   - **缺點:**
     - Delta Lake 表的大小可能相對較大，佔據較多的存儲空間。
     - 如果 Delta Lake 表的大小對性能產生影響，可能需要額外的管理和優化。

根據具體情況，你可能需要考慮以下因素：
- **資料量：** 如果原始資料很大，而篩選後的資料量相對較小，可能先篩選後再轉換成 Delta Lake 是一種節省空間和資源的方法。
- **查詢頻率：** 如果 Delta Lake 表經常被查詢，可以考慮先篩選再轉換，以避免每次查詢都要進行重複的篩選操作。
- **處理流程：** 根據整個資料處理流程的需求和結構，選擇最適合的方式。

總的來說，沒有一種方法適用於所有情況，最佳策略取決於具體的使用案例和需求。

是的，Apache Druid 提供了一個 HTTP API，允許遠端程式進行連接和與 Druid 集群進行通信。這個 API 提供了多種功能，包括查詢數據、查看集群狀態、提交索引建構任務等。

以下是 Druid 的一些主要 API 端點：

1. **Broker API：**
   - `/druid/v2`: 這是 Druid 的查詢 API 端點，用於提交和查詢數據。
   - `/status`: 提供有關集群健康狀態的信息。

2. **Coordinator API：**
   - `/druid/coordinator/v1`: 提供有關 Druid 集群的一致性、分片分發等信息。
   - `/druid/coordinator/v1/rules`: 管理自動分片分發的規則。

3. **Overlord API：**
   - `/druid/indexer/v1/task`: 提交和管理索引建構任務。

4. **Historical API：**
   - `/druid/historical/v1`: 用於歷史節點的查詢和查看索引信息。

5. **MiddleManager API：**
   - `/druid/indexer/v1/worker`: 提供有關中間管理器節點的信息。

這僅僅是一些 Druid API 的例子，實際上，Druid 提供了更多的 API 端點，以支持不同的功能和管理操作。你可以查閱 Druid 的官方文檔以獲取完整的 API 參考和相關信息。

## Druid記憶體的管理

Apache Druid 是一個開源的實時數據庫，通常用於快速查詢和分析大型數據集。Druid 的記憶體使用和配置主要取決於其不同的組件和配置。

以下是一些關於 Druid 記憶體使用的重要概念：

1. **JVM Heap 設置：** Druid 的主要組件運行在 Java 虛擬機（JVM）上，因此 JVM 的堆設置對於整體性能至關重要。你可以通過調整 Java 虛擬機的 `-Xmx` 和 `-Xms` 參數，來配置 Druid 的堆大小。這兩個參數分別表示 Java 虛擬機的最大和初始堆大小。

2. **Segment 讀取緩存：** Druid 中的 Segment 是數據的基本單位，而 Segment 讀取緩存用於緩存已經讀取的 Segment，以提高查詢性能。你可以配置 Segment 讀取緩存的大小。

3. **Historical 節點的 Offheap 記憶體：** 在 Druid 中，Historical 節點負責存儲歷史數據段。這些數據通常存儲在 Offheap 記憶體中，而不是 Java 堆中。你可以配置 Historical 節點上的 Offheap 記憶體的大小。

4. **MiddleManager 節點的 Offheap 記憶體：** MiddleManager 節點用於處理索引建構任務。與 Historical 節點類似，MiddleManager 也可以配置 Offheap 記憶體的大小。

5. **Broker 節點的記憶體：** Broker 節點通常用於處理查詢。你可以配置 Broker 節點的 JVM 堆大小，以及相關的記憶體參數。

6. **Coordinator 節點的內存：** Coordinator 節點主要負責元數據的管理。你可以配置 Coordinator 節點的 JVM 堆大小。

Druid 的記憶體使用可以根據具體的使用情境進行調整和配置。在設置 Druid 環境時，建議參考官方文檔以獲得最新和最準確的配置建議。

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

