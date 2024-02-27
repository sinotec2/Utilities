---
layout: default
title:  對照表之線上查找
parent: Apache Druid
grand_parent: DB_servers
grand_parent: OLAP
last_modified_date: 2024-02-20 09:39:31
tags: DB_servers Druid
---

# 對照表之線上查找
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

- 查找(Lookups)是 Apache Druid 中的一個概念，為將OLAP查詢結果中某個維度值（可選）替換為新值，從而允許類似資料表聯接的功能。
- 在 Druid 中使用查找功能，類似於連接資料倉儲中的維度表。
- 有關更多信息，請參閱 [維度規範](https://druid.apache.org/docs/latest/querying/dimensionspecs)。就這些文件而言，「**鍵**」指的是要匹配的維度值，而「**值**」指的是其替換。
- 因此，如果您想映射 appid-12345到，Super Mega Awesome App那麼**鍵**將是appid-12345，**值**將是 Super Mega Awesome App。
- 注意
  - Druid查找不僅支援鍵一對一映射到唯一值（例如國家/地區代碼和國家/地區名稱）的用例，還
  - 支援多個 ID 映射到相同值（例如多個 app-id）的用例映射到單一客戶經理。
  - 當查找是一對一時，Druid 能夠應用額外的查詢來重寫(參閱下面的更多細節)。

尋找沒有歷史記錄。他們總是使用當前數據。這意味著，如果特定應用程式 ID 的首席客戶經理發生更改，並且您發出包含查找的查詢來儲存應用程式 ID 與客戶經理的關係，則它將返回該應用程式 ID 的當前客戶經理，無論您查詢的時間範圍。

如果您需要資料時間範圍敏感的查找，則目前在查詢時不會動態支援此類用例，且此類資料屬於在 Druid 中使用的原始非規範化資料。

尋找通常預先載入到所有伺服器的記憶體。但是非常小的查找（大約幾十到幾百個條目）也可以使用「map」查找類型在本機查詢時間內內聯傳遞。有關詳細信息，請參閱 尺寸規格文件。

其他查找類型可作為擴充使用，包括：

透過lookups-cached-global從本機檔案、遠端 URI 或 JDBC 全域快取尋找。
透過kafka-extraction-namespace從 Kafka 主題全域快取尋找。

## 查詢語法

在Druid SQL中，可以使用LOOKUPfunction來查詢查找，例如：

```sql
SELECT
  LOOKUP(store, 'store_to_country') AS country,
  SUM(revenue)
FROM sales
GROUP BY 1
```

此LOOKUP函數也接受第三個參數，稱為replaceMissingValueWith常數字串。如果查找不包含所提供鍵的值，則LOOKUP函數將傳回該replaceMissingValueWith值而不是NULL，就像 一樣COALESCE。例如，LOOKUP(store, 'store_to_country', 'NA')相當於 COALESCE(LOOKUP(store, 'store_to_country'), 'NA').

可以使用JOIN 運算子查詢尋找：

```sql
SELECT
  store_to_country.v AS country,
  SUM(sales.revenue) AS country_revenue
FROM
  sales
  INNER JOIN lookup.store_to_country ON sales.store = store_to_country.k
GROUP BY 1
```

{% include note.html content="該函數具有該方法所沒有的LOOKUP自動查詢重寫功能，包括反向查找和上拉。如果這些重寫對您很重要，請考慮使用該函數而不是.JOINGROUP BYLOOKUPJOIN" %}

在本機查詢中，可以使用維度規範或擷取函數來查詢尋找。

## 查詢重寫

Druid 在使用該功能時可以進行兩種自動查詢重寫LOOKUP：反向查找和 通過 上拉GROUP BY。以下各節描述了這些重寫及其要求。

### 反向查找

當LOOKUP函數呼叫出現在WHERE查詢子句中時，Druid 會盡可能反轉它們。例如，如果查找表sku_to_name包含映射'WB00013' => 'WhizBang Sprocket'，那麼Druid會自動重寫此查詢：

```sql
SELECT
  LOOKUP(sku, 'sku_to_name') AS name,
  SUM(revenue)
FROM sales
WHERE LOOKUP(sku, 'sku_to_name') = 'WhizBang Sprocket'
GROUP BY LOOKUP(sku, 'sku_to_name')
```

進入這個：

```sql
SELECT
  LOOKUP(sku, 'sku_to_name') AS name,
  SUM(revenue)
FROM sales
WHERE sku = 'WB00013'
GROUP BY LOOKUP(sku, 'sku_to_name')
```

不同的是，在後一種情況下，數據伺服器在過濾時不需要應用該LOOKUP功能，並且可以更有效地利用sku.

下表包含在 Druid 預設空處理模式下何時可以反向呼叫「LOOKUP」的範例。範例清單是說明性的，但並不詳盡。

SQL|可逆嗎？
-|-
LOOKUP(sku, 'sku_to_name') = 'WhizBang Sprocket'|是的
LOOKUP(sku, 'sku_to_name') IS NOT DISTINCT FROM 'WhizBang Sprocket'|是的，對於非空文字
LOOKUP(sku, 'sku_to_name') <> 'WhizBang Sprocket'|不，除非sku_to_name是單射
LOOKUP(sku, 'sku_to_name') IS DISTINCT FROM 'WhizBang Sprocket'|是的，對於非空文字
LOOKUP(sku, 'sku_to_name') = 'WhizBang Sprocket' IS NOT TRUE|是的
LOOKUP(sku, 'sku_to_name') IN ('WhizBang Sprocket', 'WhizBang Chain')|是的
LOOKUP(sku, 'sku_to_name') NOT IN ('WhizBang Sprocket', 'WhizBang Chain')|不，除非sku_to_name是單射
LOOKUP(sku, 'sku_to_name') IN ('WhizBang Sprocket', 'WhizBang Chain') IS NOT TRUE|是的
LOOKUP(sku, 'sku_to_name') IS NULL|不
LOOKUP(sku, 'sku_to_name') IS NOT NULL|不
LOOKUP(UPPER(sku), 'sku_to_name') = 'WhizBang Sprocket'|是的，到UPPER(sku) = [key for 'WhizBang Sprocket']（UPPER功能仍然存在）
COALESCE(LOOKUP(sku, 'sku_to_name'), 'N/A') = 'WhizBang Sprocket'|是的，但請參閱下一項= 'N/A'
COALESCE(LOOKUP(sku, 'sku_to_name'), 'N/A') = 'N/A'|不，除非sku_to_name是單射，這允許 Druid 忽略COALESCE
COALESCE(LOOKUP(sku, 'sku_to_name'), 'N/A') = 'WhizBang Sprocket' IS NOT TRUE|是的
COALESCE(LOOKUP(sku, 'sku_to_name'), 'N/A') <> 'WhizBang Sprocket'|是的，但請參閱下一項<> 'N/A'
COALESCE(LOOKUP(sku, 'sku_to_name'), 'N/A') <> 'N/A'|不，除非sku_to_name是單射，這允許 Druid 忽略COALESCE
COALESCE(LOOKUP(sku, 'sku_to_name'), sku) = 'WhizBang Sprocket'|不，COALESCE只有當第二個參數是常數時才可逆
LOWER(LOOKUP(sku, 'sku_to_name')) = 'whizbang sprocket'|不，除此之外的功能COALESCE都是不可逆的
MV_CONTAINS(LOOKUP(sku, 'sku_to_name'), 'WhizBang Sprocket')|是的
NOT MV_CONTAINS(LOOKUP(sku, 'sku_to_name'), 'WhizBang Sprocket')|不，除非sku_to_name是單射
MV_OVERLAP(LOOKUP(sku, 'sku_to_name'), ARRAY['WhizBang Sprocket'])|是的
NOT MV_OVERLAP(LOOKUP(sku, 'sku_to_name'), ARRAY['WhizBang Sprocket'])|不，除非sku_to_name是單射

您可以看到 SQL 規劃期間產生的本機查詢的差異，您可以使用 進行檢索EXPLAIN PLAN FOR。以這種方式反向查找時，該lookup 函數消失並被更簡單的過濾器取代，通常類型為equals或in。

如果匹配鍵的數量超過查詢的sqlReverseLookupThreshold 或，則不會反轉查找。inSubQueryThreshold

此重寫增加了一些計劃時間，這對於較大的查找可能會變得很明顯，特別是如果許多鍵映射到相同的值。您可以在指標中看到對計劃時間的影響sqlQuery/planningTimeMs。您也可以測量 所花費的時間EXPLAIN PLAN FOR，它會規劃查詢但不執行它。

sqlReverseLookup: false可以透過在查詢上下文中設定來停用此重寫。

### 提取

標記為單射的查找可以通過GROUP BY. 例如，如果查找sku_to_name是單射的，Druid 會自動重寫此查詢：

```sql
SELECT
  LOOKUP(sku, 'sku_to_name') AS name,
  SUM(revenue)
FROM sales
GROUP BY LOOKUP(sku, 'sku_to_name')
```

進入這個：

```sql
SELECT
  LOOKUP(sku, 'sku_to_name') AS name,
  SUM(revenue)
FROM sales
GROUP BY sku
```

不同之處在於該LOOKUP函數直到GROUP BY完成後才應用，這加快了GROUP BY.

您可以看到 SQL 規劃期間產生的本機查詢的差異，您可以使用 進行檢索EXPLAIN PLAN FOR。以這種方式提取查找時，lookup函數呼叫通常從本機查詢的virtualColumnsordimensions部分移動到postAggregations.

sqlPullUpLookup: false可以透過在查詢上下文中設定來停用此重寫。

### 內射

單射查找適合最大的查詢重寫集。單射查找必須滿足以下「一對一查找」屬性：

查找表中的所有值必須是唯一的。也就是說，沒有兩個鍵可以映射到相同的值。
查找表必須為函數呼叫可能遇到的每個輸入定義一個鍵值對LOOKUP。例如，當呼叫 時LOOKUP(sku, 'sku_to_name')，sku_to_name查找表必須具有所有可能的鍵sku。
在 SQL 相容的空處理模式下（當 為druid.generic.useDefaultValueForNull = false預設值時）單射查找表不需要具有 的鍵null，因為LOOKUPofnull始終是null其本身。
當 時druid.generic.useDefaultValueForNull = true，a LOOKUPofnull檢索會對應到空字串鍵 ( ) 的值""。在此模式下，如果函數可能遇到空輸入值，則單射查找表必須具有空字串鍵LOOKUP。
為了確定查找是否是單射的，Druid 依賴injective您可以在查找定義中設定的屬性。一般來說，您應該設定injective: true滿足所需屬性的任何查找，以允許 Druid 盡快執行您的查詢。

Druid 不會驗證尋找是否滿足這些必需的屬性。injective: true如果您設定的查找表實際上不是一對一查找，則 Druid 可能會傳回不正確的查詢結果。

## 動態

以下記錄了可透過協調器存取的叢集範圍配置的行為。配置透過伺服器「層」的概念進行傳播。「層」被定義為一組應該接收一組查找的服務。例如，您可以將所有歷史記錄作為其任務資料來源的一部分__default，並將 Peons 作為其任務資料來源的各個層的一部分。查找層完全獨立於歷史層。

這些配置可透過以下 URI 範本使用 JSON 進行存取

```bash
http://<COORDINATOR_IP>:<PORT>/druid/coordinator/v1/lookups/config/{tier}/{id}
```

以下的所有 URI 均假定已http://<COORDINATOR_IP>:<PORT>預先新增。

如果您以前從未配置過查找，則必須發佈一個空的 json 物件{}來/druid/coordinator/v1/lookups/config初始化配置。

這些端點將傳回下列結果之一：

```bash
404 如果找不到資源
400 如果請求的格式有問題
202 如果請求被非同步接受（POST和DELETE）
200 如果請求成功（GET僅）
```

## 配置傳播

配置由協調器傳播到查詢服務流程（Broker / Router / Peon / Historical）。查詢服務程序有一個內部 API，用於管理進程上的查找，這些 API 供協調器使用。協調器定期檢查是否有任何進程需要載入/刪除查找並適當更新它們。

請注意，單一查詢服務程序只能同時處理 2 個同時尋找設定傳播請求。應用此限制是為了防止查找處理消耗太多伺服器 HTTP 連線。

## API

有關配置查找和查找狀態的參考，請參閱查找 API 。

## 配置

請參閱協調器配置的尋找動態配置。

若要設定 Broker/Router/Historical/Peon 以將其宣告為查找層的一部分，請使用下列屬性。

財產|描述|預設
-|-|-
druid.lookup.lookupTier|此進程的查找層。這是獨立於其他層的。|__default
druid.lookup.lookupTierIsDatasource|對於索引服務任務等某些事情，資料來源在任務的執行時間屬性中傳遞。此選項可從與任務的資料來源相同的值中取得 tierName。如果有的話，建議僅將其用作索引服務的 Peon 選項。若為真，druid.lookup.lookupTier則不得指定|"false"

若要設定動態設定管理員的行為，請在協調器上使用下列屬性：

財產|描述|預設
-|-|-
druid.manager.lookups.hostTimeout|每個主機處理請求的逾時（以毫秒為單位）|2000（2秒）
druid.manager.lookups.allHostTimeout|完成所有程序的查找管理的逾時（以毫秒為單位）。|900000（15 分鐘）
druid.manager.lookups.period|管理週期之間暫停多長時間|120000（2 分鐘）
druid.manager.lookups.threadPoolSize|可並發管理的服務行程數|10

## 重啟後儲存配置

可以在重新啟動時儲存配置，這樣進程就不必等待協調器操作來重新填入其查找。為此，設定以下屬性：

財產|描述|預設
-|-|-
druid.lookup.snapshotWorkingDir|用於儲存目前查找配置的快照的工作路徑，將此屬性保留為空將禁用快照/引導程式實用程式|無效的
druid.lookup.enableLookupSyncOnStartup|在啟動時啟用與協調器的查找同步過程。可查詢進程將從協調器取得並載入查找，而不是等待協調器為它們載入查找。如果叢集中沒有配置查找，使用者可以選擇停用此選項。|真的
druid.lookup.numLookupLoadingThreads|啟動時並行加載查找的執行緒數。一旦啟動完成，該執行緒池就會被銷毀。它在 JVM 的生命週期內不會保留|可用處理器 / 2
druid.lookup.coordinatorFetchRetries|在啟動同步期間重試從協調器取得查找 bean 清單的次數。|3
druid.lookup.lookupStartRetries|在啟動同步期間或運行時重試啟動每次查找的次數。|3
druid.lookup.coordinatorRetryDelay|在啟動同步期間重試從協調器取得查找清單之間的延遲時間（以毫秒為單位）。|60_000
內省查找
如果查找類型實作了LookupIntrospectHandler.

請求GET將/druid/v1/lookups/introspect/{lookupId}傳回完整值的映射。

ex：`GET /druid/v1/lookups/introspect/nato-phonetic`

```json
{
    "A": "Alfa",
    "B": "Bravo",
    "C": "Charlie",
    ...
    "Y": "Yankee",
    "Z": "Zulu",
    "-": "Dash"
}
```

GET可以透過以下方式檢索密鑰列表/druid/v1/lookups/introspect/{lookupId}/keys"

ex：`GET /druid/v1/lookups/introspect/nato-phonetic/keys`

```bash
[
    "A",
    "B",
    "C",
    ...
    "Y",
    "Z",
    "-"
]
```

請求GET將/druid/v1/lookups/introspect/{lookupId}/values"返回值列表。

ex：`GET /druid/v1/lookups/introspect/nato-phonetic/values`

```bash
[
    "Alfa",
    "Bravo",
    "Charlie",
    ...
    "Yankee",
    "Zulu",
    "Dash"
]
```