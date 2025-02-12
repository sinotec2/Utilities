---
layout: default
title: Drop and Execute
parent:   Parallel Computation
grand_parent: Operation Systems
last_modified_date: 2022-04-25 12:20:36
---

# 上傳與遠端執行
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

## 問題

> 我有一個工作站提供轉檔的服務，怎麼樣的非同步策略最為合理、符合現代化的系統架構。目前我是讓使用者把檔案放在特定的目錄，工作站排程檢查執行程式。

## 多頭執行策略

你的目前策略是 基於檔案系統的輪詢機制（Polling），即定期檢查特定目錄，找出新檔案並處理。這種方式簡單易行，但對於高併發、大量檔案的場景可能會有 延遲高、資源浪費 的問題。要讓系統更加現代化，可以考慮以下幾種非同步策略：

### 檔案事件驅動（推薦）

概念：使用 檔案監控機制（如 inotify、fswatch），當新檔案進入目錄時，立即觸發轉檔程序，避免輪詢造成的資源浪費。

技術方案：

- Linux：inotify、watchdog（Python）
- Windows：ReadDirectoryChangesW（Windows API）
- 跨平台：watchdog（Python 庫，支援 Linux/Windows/macOS）

優勢：

- ✅ 即時觸發，降低延遲
- ✅ 不消耗 CPU 進行無用輪詢
- ✅ 更適合大規模檔案處理

適用場景：

- 檔案量大，但每個轉檔處理時間短
- 需要即時回應使用者的轉檔請求

### 佇列（Queue）+ 任務分派

概念：讓使用者上傳檔案時，透過 API 或 CLI 提交 任務資訊 到工作佇列（Queue），轉檔服務根據佇列分派任務，並回報結果。

技術方案：

- 訊息佇列：RabbitMQ、Redis Queue、Kafka
- 任務佇列：Celery（Python）、RQ（Redis Queue）

流程：

1.	 使用者將檔案放入特定目錄或上傳 API
2.	 應用程式將檔案路徑與參數提交到佇列
3.	 工作站後端監聽佇列，有新任務時自動拉取並轉檔
4.	 轉檔完成後，更新狀態並通知使用者（Email、Webhook 等）

優勢：

- ✅ 非同步 處理，能平行處理多個檔案
- ✅ 彈性擴展，可多台機器併行處理
- ✅ 可靠性高，可以儲存任務狀態，系統異常後可重啟繼續執行

適用場景：

- 高併發、多使用者轉檔需求
- 需要追蹤轉檔狀態（成功/失敗）

3. 混合模式（事件驅動 + 佇列）（最靈活）

概念：

- 透過 檔案監控 觸發轉檔
- 但真正執行的轉檔工作透過 佇列 管理，確保任務可追蹤

技術架構：

1.	 watchdog 監控檔案變動
2.	 檔案被偵測到後，將轉檔任務推送到 RabbitMQ / Redis Queue
3.	 轉檔工作站從佇列拉取任務，執行轉檔
4.	 轉檔完成後，結果存入資料庫，通知使用者

優勢：

- ✅ 即時觸發 + 任務管理，兼顧效率與可追蹤性
- ✅ 能應對突發負載，避免瞬間大量檔案導致 CPU 爆滿
- ✅ 更容易擴展，可加入多個工作節點

適用場景：

- 需要即時轉檔，但希望有佇列來管理負載
- 可能未來要擴展到 多台工作機 負責轉檔

### 結論

如果你目前是 輪詢機制，建議逐步升級：

- 1️⃣ 小量檔案、低頻率轉檔 ➝ 用 檔案監控（inotify, watchdog），降低 CPU 輪詢浪費
- 2️⃣ 大量併發、多使用者、多台工作站 ➝ 用 佇列（RabbitMQ, Redis Queue）+ 任務分派
- 3️⃣ 希望即時觸發 + 控制負載 ➝ 混合模式（事件驅動 + 佇列），最佳化系統

這樣能讓你的轉檔工作站 更即時、更具彈性、更容易擴展！

## web file browsers

> 介紹一下開源領域/Github 的web file browsers方案

### 開源

以下是幾款知名的開源 Web 文件管理器(source:[10個開源的基於WEB的文件管理器](https://linuxstory.org/10-open-source-web-based-file-managers/zh-tw/))

1.	 [eXtplorer](http://extplorer.net/)提供移動、複製、編輯、搜索、刪除、下載和上傳功能。此外，您也能用 eXtplorer 創建和提取檔案、文件夾和新文件。其主要功能是讓您通過 FTP 訪問文件。為了正常使用，伺服器的 PHP 最低版本要求為 4.3，並且必須更新 JavaScript。  ￼
2. AjaXplorer：絕大多數瀏覽器都支持這個文件管理器，並且它能輕易地自動適應類似於手機一樣的小屏幕瀏覽。目前 iOS 版的程序已經被開發出來，安卓版的也將很快完成。要運行 AjaXplorer，您需要一個支持 PHP 5.1 或更高版本的 Web 伺服器。它允許您直接從伺服器串流傳輸視頻內容。  ￼
3. KFM：這個免費和開源的文件管理器可以作為 FCKeditor、CKeditor、TinyMCE 之類的富文本編輯器的插件。如果您正在使用基於 Linux 的操作系統，那麼您需要 PHP 5.2 或更高版本，而 Mac OS X 和 Windows 分別需要 MySQL 4.1 或更高版本和 MySQL 5.0 或更高版本。它有自己的搜索引擎，附帶了一個文本編輯器，可以高亮顯示語法。它還帶有 MP3 播放和視頻播放選項。  ￼
4.	 [Filebrowser](https://blog.csdn.net/2302_76672693/article/details/136207788):這是一款可以讓您在指定目錄下管理文件的 Web 應用，提供上傳、刪除、預覽、重命名和編輯文件的功能。它還支持創建多個用戶，每個用戶可以有自己的目錄。Filebrowser 簡潔高效，適合需要輕量級文件管理解決方案的用戶。  ￼
5.	 Filestash：這是一個開源、跨平台且功能強大的 Web 文件管理器，致力於簡化現代多源文件系統的訪問與管理。Filestash 整合了多種雲存儲服務，如 Dropbox、Google Drive、SFTP、FTP、WebDAV 等，並提供統一的操作介面。用戶可以在一個集中化的平台上進行文件瀏覽、上傳、下載、編輯、同步和共享等操作。  ￼

### Github

以下是幾個在 GitHub 上值得關注的開源 Web 文件瀏覽器項目：

1. [FileBrowser](https://github.com/filebrowser/filebrowser):這是一個開源的 Web 文件管理器，提供在指定目錄內管理文件的介面。用戶可以上傳、刪除、預覽、重命名和編輯文件。它支持創建多個用戶，每個用戶可以擁有自己的目錄。該項目以 Go 語言編寫，提供單個靜態二進制文件，易於部署和使用。  ￼
2.	 [Web File Browser](https://github.com/cgdave/webfilebrowser):這是一個用 PHP 編寫的簡單開源文件瀏覽器，僅包含一個文件。它允許用戶通過輕量級的 Web 界面創建、刪除、編輯、複製、重命名、移動和上傳文件和目錄。安裝簡便，只需將單個 PHP 文件上傳到目標目錄即可。  ￼
3.	 [Fibr](https://github.com/ViBiOh/fibr):這是一個旨在提供簡單文件系統瀏覽的項目。它是一個單一的靜態二進制文件，內嵌 HTML 模板，無需使用 JavaScript 框架。Fibr 旨在與多種平台兼容，包括 x86_64、arm、arm64 架構。  ￼

## inotify

- 煎炸熊[這篇新作](https://note.artchiu.org/2024/01/16/inotify-tools-%E7%9B%A3%E6%8E%A7%E6%AA%94%E6%A1%88%E8%AE%8A%E5%8B%95%E3%80%81%E8%A7%B8%E7%99%BC%E8%99%95%E7%90%86%E5%8B%95%E4%BD%9C/)有蠻多應用範例與開啟。

