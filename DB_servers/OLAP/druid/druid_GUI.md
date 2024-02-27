---
layout: default
title:  GUI介紹
parent: Apache Druid
grand_parent: DB_servers
grand_parent: OLAP
last_modified_date: 2024-02-23 03:37:47
tags: DB_servers Druid
---

# Druid GUI的詳細功能介紹
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

- 這裏介紹瀏覽器界面的詳細功能，官網資料詳見網頁主控台[Web console](https://druid.apache.org/docs/latest/operations/web-console)。
- Druid 提供的這個 Web 控制台，用於載入資料、管理資料來源和任務以及查看伺服器狀態和段資訊。您也可以在控制台中執行 SQL 和本機 Druid 查詢。
- 稱之為主控台的意思，表示並不是所有的功能都能在此進行，還是需要靠命令列、其他GUI設計、LDAP設定等等。

### 啟動

- 啟用下列叢集設定以使用 Web 控制台。請注意，這些設定預設為啟用。
  - 啟用路由器的管理代理程式。
  - 為叢集中的Broker進程啟用Druid SQL 。
  - 路由器服務託管 Web 控制台。透過以下位址存取 Web 控制台：`http://<ROUTER_IP>:<ROUTER_PORT>`

### 安全說明

在設定了Druid 使用者權限後，API 或 Web 控制台的任何使用者實際上都具有與啟動 Druid 的使用者相同等級的存取權，不論對本機檔案和網路服務。最佳實踐是避免以 root 使用者身分啟動 Druid，並使用 Druid 權限或網路防火牆來限制潛在的使用者對敏感資源執行存取權。

## 主頁

- 主頁共有7張卡片、提供 Druid 群集的綜觀概述。每張卡片都是可點擊的、並連結到相應的分頁。
- 主頁視圖顯示以下卡片
  - 狀態：按一下此卡以取得有關 Druid 版本、以及叢集上載入的所有擴充功能。
  - 資料來源：目前已經載入的資料表
  - 段：Druid是時間序列的OLAP，其架構是時間上的段落、以及數據的版本時間等等標籤。
  - 監事：對於使用者查詢工作的監控
  - 任務：硬體資源的分配(slot)
  - 服務：叢集運作的情形
  - 尋找：

您可以從主頁的導覽存取資料載入器和查找重要功能的分頁。

![](https://druid.apache.org/assets/images/web-console-01-home-view-99f09e8760740e04b982b4d4c56fe6ed.png)

## 查詢(Query)

基於 SQL 的攝取和多階段查詢任務引擎使用查詢視圖，該視圖為您提供編輯和使用 SQL 查詢的 UI。您應該在 Druid 24.0 及更高版本中自動看到此 UI，因為預設會載入多階段查詢擴充功能。

以下螢幕截圖顯示了查詢各部分的描述：

![](https://druid.apache.org/assets/images/ui-annotated-7932933ce7ad968aa0f5e3ef2aeca5e0.png)

### 多階段查詢視圖的說明

1. 按此進入查詢分頁：您可以在多階段、支援標籤的查詢檢視中、觸發查詢的指令、並查看結果。所有其他視圖與非增強版本相比沒有變化。您仍然可以透過導覽至URL來存取原始查詢檢視。您可以透過選項卡 (3) 的存在來#query判斷您正在查看更新的查詢檢視。
2. Druid下拉選單：顯示可用的資料來源、架構和欄位。
3. 查詢SQL程式碼標籤：可讓您一次管理和執行多個查詢。點擊加號圖示以開啟新分頁。若要操作現有選項卡，請按一下選項卡名稱。(編按：query的內容並不會存在伺服器，而是存在客戶端的cookies，如果清空瀏覽記錄，查詢程式碼將會消失。重要程式碼敬請另存備份。)
4. 連接外部資料：選項卡列包含一些有用的工具，包括這項聯外按鈕，可對外部資料進行取樣、使用適當的定義建立初始查詢EXTERN，然後您可以根據需要進行編輯。
5. 最近的查詢任務：按下相左展開的按鈕，可以開啟最近任務面板。您可以查看叢集中所有使用者目前正在執行的查詢和先前的查詢。它相當於Ingestion視圖中的Task視圖，過濾器為：`type='query_controller'`
6. 您可以按一下每個查詢條目以附加到新選項卡中的該查詢。
7. 您可以下載有關您可以共享的查詢的所有相關詳細資訊的存檔。
8. “運行”按鈕運行查詢。
9. 當您輸入 INSERT/REPLACE 查詢時，將出現「預覽」按鈕。它內聯運行查詢，不使用 INSERT/REPLACE 子句，並新增了 LIMIT，以便您預覽單擊Run時將攝取的資料。新增的 LIMIT 使查詢運行得更快，但提供的結果不完整。
10. 引擎選擇器可讓您選擇將查詢傳送到哪個引擎（API 端點）。預設情況下，它會根據查詢分析自動選擇要使用的端點，但您可以明確選擇特定引擎。您也可以從此選單配置引擎特定的上下文參數。
11. 當您選擇sql-msq-task引擎時，將出現最大任務選擇器。它允許您配置平行計算的資源。
12. 更多選單 ( ... ) 包含以下有用的工具：
  - 解釋 SQL 查詢向EXPLAIN PLAN FOR您顯示SQL 查詢傳回的邏輯計畫。
  - 查詢歷史記錄顯示您先前執行過的查詢。
  - 將攝取規範轉換為 SQL可讓您將本機批次攝取規範轉換為等效的 SQL 查詢。
  - 透過任務 ID 附加標籤可讓您根據在此叢集上執行的查詢的任務 ID 建立新分頁。
  - 開啟查詢詳細檔案可讓您開啟透過 (7) 在任何叢集上產生的詳細檔案。
13. 查詢計時器指示查詢已經運作多久了。
14. （取消）連結取消目前正在執行的查詢。
15. 主進度條顯示查詢的整體進度。進度是根據即時報告 (16) 中的各個計數器計算的。
16. 目前階段進度條顯示目前正在執行的查詢階段的進度。如果多個階段同時執行，則保守地顯示最早執行階段的資訊。
17. 即時查詢報告顯示所有階段（過去、現在和未來）的詳細資訊。查詢運行時會顯示即時報告。如果需要，您可以隱藏該報告。查詢完成後，您可以透過點擊查詢時間指示器或從「最近的查詢任務」面板 (6) 來存取它們。
18. 您可以透過點擊三角形來展開即時查詢報告的每個階段，以顯示每個工作線程和每個分區的統計資料。

## 資料載入器分頁

{% include note.html content="您可以使用資料載入器、透過逐步精靈建立攝取的規範。" %}

![](https://druid.apache.org/assets/images/web-console-02-data-loader-1-fcc691fda096b9d9fb00f9a5cd30293f.png)

選擇資料位置後，請依照一系列步驟操作，顯示資料攝取時的增量預覽。填寫每個步驟所需的詳細資訊後，您可以透過點擊「下一步」導航到下一步。您也可以透過頂部導航在步驟之間自由導航。

使用頂部導覽進行導覽時，底層規格不會被修改，而按一下「下一步」則會嘗試使用適當的預設值填入後續步驟。

### 資料載入器攝取

![](https://druid.apache.org/assets/images/web-console-03-data-loader-2-6eb770d4034261a96b968deb305f1258.png)

資料來源視圖顯示目前在叢集上載入的所有資料來源及其大小和可用性。從資料來源視圖中，您可以編輯保留規則、配置自動壓縮以及刪除資料來源中的資料。

資料來源被劃分為按時間區塊組織的一個或多個段。若要顯示片段時間線，請切換顯示片段時間軸選項。

與任何由 Druid SQL 查詢支援的視圖一樣，您可以從省略號選單中按一下檢視資料表的 SQL 查詢來直接執行底層 SQL 查詢。

## 資料來源

您可以查看和編輯保留規則以確定資料來源的一般可用性。

![](https://druid.apache.org/assets/images/web-console-04-datasources-d0ac928b0107a903b7c99fd8dff2fc39.png)

保留

Segments視圖顯示叢集中的所有段。每個部分都有一個提供更多資訊的詳細視圖。段 ID 還可以方便地分解為資料來源、開始、結束、版本和分區列，以便於過濾和排序。

![](https://druid.apache.org/assets/images/web-console-05-retention-e5f87124a1e9c252043a45b84a6039ed.png)

## 段

從此視圖中，您可以檢查現有主管的狀態以及暫停、恢復和重設它們。主管監督索引任務的狀態，以協調交接、管理故障並確保維持可擴展性和複製要求。點擊省略號圖示並選擇Submit JSON Supervisor手動提交主管規格。

![](https://druid.apache.org/assets/images/web-console-06-segments-2a1f30ad959f3af6b5bbe9818f29674d.png)

## 監事

點擊任何主管的放大鏡圖示即可查看其進度的詳細報告。
![](https://druid.apache.org/assets/images/web-console-07-supervisors-dc27d65a42df39922d4ad9cff556faf8.png)

- 監事身分

任務表可讓您查看目前正在運行和最近完成的任務。為了更輕鬆地導航任務，您可以按類型、資料來源或狀態對它們進行分組。點選省略號圖示並選擇「提交 JSON 任務」 ，手動提交任務。

![](https://druid.apache.org/assets/images/web-console-08-supervisor-status-07ece8b3920e682c3264c779053801a0.png)

## 任務

點擊任意任務的放大鏡圖示以查看有關該任務的更多詳細資訊。

![](https://druid.apache.org/assets/images/web-console-0.7-tasks-d53bfa761253b59a0bd368825f8b5c48.png)

任務狀態

透過「服務」視圖，您可以查看組成叢集的節點的目前狀態。您可以按類型或層對節點進行分組，以獲得有意義的摘要統計資料。

![](https://druid.apache.org/assets/images/web-console-09-task-status-3bc2b07f8ebe5dca9d6259d011b97d47.png)

## 服務

從主頁視圖中的「尋找」卡或按一下頂級導覽中的省略號圖示存取「尋找」視圖。您可以在此處建立和編輯查詢時間查找。

![](https://druid.apache.org/assets/images/web-console-10-servers-a6657c30723d278409d8d884d3655ed1.png)

## 尋找

從主頁視圖中的「尋找」卡或按一下頂級導覽中的省略號圖示存取「尋找」視圖。您可以在此處建立和編輯查詢時間[查找](https://druid.apache.org/docs/latest/querying/lookups)。

![](https://druid.apache.org/assets/images/web-console-13-lookups-337b7e84ed82f5580448a5ba083f91c1.png)