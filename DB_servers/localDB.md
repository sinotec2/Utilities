---
layout: default
title:  localDB
parent: DB_servers
last_modified_date: 2024-01-16 10:51:11
tags: DB_servers
---

# localDB
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
以下為使用 SQL Server Express LocalDB 的簡明使用說明（繁體中文），涵蓋安裝、建立/啟動執行個體、連線、共用、管理與疑難排解重點。

1. 先決條件與安裝
- LocalDB 隨 SQL Server Express 安裝媒體提供；安裝時在「功能選取 / 共用功能」勾選 LocalDB，或直接使用 SqlLocalDB.msi 安裝檔安裝[^22]。  
- Visual Studio 亦可透過工作負載或個別元件安裝 LocalDB[^38]。

2. LocalDB 概念重點
- LocalDB 是針對開發人員的輕量型 SQL Server 執行個體：不使用服務，按需啟動；系統會使用共用的 LocalDB 二進位檔集，且每個執行個體由單一使用者擁有（未共用時只有擁有者可見）[^52,^63]。  
- 支援兩種執行個體：自動執行個體（名稱固定為 MSSQLLocalDB）與具名執行個體（由使用者建立）[^39,^30]。  
- LocalDB 預設排序為 SQL_Latin1_General_CP1_CI_AS（不可變更）[^10]。  
- 限制範例：不支援遠端透過 SSMS 管理、不支援 FILESTREAM、不能當合併式複寫訂閱者，Service Broker 僅允許本機佇列等[^10]。

3. 使用命令列工具 SqlLocalDB.exe（管理執行個體）
- 工具位置通常為 SQL Server Tools 目錄，或可從文件參考使用[^22]。  
- 常用命令（語法摘要）[^24,^48]:
  - 建立：SqlLocalDB.exe create "InstanceName" [Version] [-s]（-s 建立後啟動）[^24]。  
  - 刪除：SqlLocalDB.exe delete "InstanceName"[^48]。  
  - 啟動：SqlLocalDB.exe start "InstanceName"（成功時回傳執行個體管道名稱）[^74]。  
  - 停止：SqlLocalDB.exe stop "InstanceName" [-i | -k]（-i NOWAIT，-k 強制終止進程）[^48,^74]。  
  - 列出與檢視：SqlLocalDB.exe info (或 info "InstanceName")，列出使用者擁有的執行個體與詳細資訊（含執行個體管道）[^48,^55]。  
  - 列出版本：SqlLocalDB.exe versions[^48]。  
  - 共用 / 取消共用：SqlLocalDB.exe share "OwnerSIDOrAccount" "PrivateName" "SharedName" 以及 SqlLocalDB.exe unshare "SharedName"（也可用簡略參數）[^48]。  
  - 追蹤：trace on|off 開啟/關閉 API 呼叫追蹤[^55]。  
- 注意命名：若名稱含空格或特殊字元，請以雙引號括住；LocalDB 具名執行個體名稱可達 128 字元且允許大部分 Unicode 字元，但會剔除前後空格，並禁止某些檔名非法字元[^76,^63]。

4. 建立並啟動具名執行個體的範例
- 建立並啟動：
  - SqlLocalDB.exe create "LocalDBApp1" （可加版本號或省略，預設為工具版本）  
  - SqlLocalDB.exe start "LocalDBApp1"  
  - SqlLocalDB.exe info "LocalDBApp1" 會回傳執行個體管道名稱，例如 np:\\.\pipe\LOCALDB#F365A78E\tsql\query；可用此管道在需時連線[^28]。

5. 連線到 LocalDB
- 自動執行個體（最簡單）：使用連接字串 Server=(localdb)\MSSQLLocalDB;Integrated Security=true 連線到目前使用者的自動執行個體[^6]。  
- 使用檔案附加資料庫：Server=(LocalDB)\MSSQLLocalDB;Integrated Security=true;AttachDbFileName=D:\Data\MyDB1.mdf[^6]。  
- 若需直接使用具名管道（例如舊版 .NET）：Server=np:\\.\pipe\LOCALDB#<id>\tsql\query; 其中 <id> 由 info 命令輸出取得[^37]。  
- 連線到共用執行個體：使用 (localdb)\.\SharedName 作為伺服器名稱（注意需有適當登入）[^16]。

6. 共用執行個體（允許其他使用者存取）
- 由執行個體擁有者透過 SqlLocalDB.exe share 指定共用名稱；只有系統管理員可建立共用執行個體，或由擁有者取消共用。其他使用者透過 (localdb)\.\SharedName 連線，且需相對應的 Windows 或 SQL 驗證登入[^32]。  
- 共用/取消共用示例（範例流程）[^24]:
  - SqlLocalDB.exe create "DeptLocalDB"  
  - SqlLocalDB.exe share "DeptLocalDB" "DeptSharedLocalDB"  
  - SqlLocalDB.exe start "DeptLocalDB"  
  - 其他使用者連線：sqlcmd -S (localdb)\.\DeptSharedLocalDB -U <user> -P <password>（或使用 Windows 驗證）

7. 管理與權限
- LocalDB 執行個體由建立者擁有；若資料庫檔案儲存在共用位置，擁有該檔案系統存取者均可開啟該資料庫；若儲存在使用者資料夾，僅擁有者與系統管理員可存取[^27]。  
- 內建帳戶（例如 NT AUTHORITY\SYSTEM）可能遇到檔案系統重新導向造成管理問題，建議改用一般 Windows 帳戶擁有執行個體[^20]。

8. 典型工作流程（快速上手）
- 安裝 LocalDB。  
- 使用自動執行個體連線（Server=(localdb)\MSSQLLocalDB;Integrated Security=true）立即開始開發與測試。  
- 若需獨立隔離環境或特殊版本，建立具名執行個體：SqlLocalDB.exe create "MyInstance" [version] -s；使用 SqlLocalDB.exe info 取得管道並以 sqlcmd/SSMS 連線（輸入管道作為伺服器名稱）[^28,^37]。  
- 若多人需連線，將具名執行個體設定為共用並由其他使用者以 (localdb)\.\SharedName 連線[^32,^24]。

9. 疑難排解要點
- 首次連線可能需要等待自動執行個體建立與啟動，若逾時請稍候再試[^6]。  
- 若需要執行個體管道名稱但不確定，執行 SqlLocalDB.exe info "InstanceName" 取得管道字串並使用 np: 連線[^28]。  
- 若系統資料庫損毀或需要重設，自動執行個體可刪除（Delete），下次啟動時會重新建立[^40]。  
- 參考 Microsoft 文件中的「疑難排解」或 LocalDB 錯誤訊息頁面以取得特定錯誤碼說明[^12]。

10. 參考命令速查（常用）
- 建立並立即啟動：SqlLocalDB.exe create "Name" [Version] -s  
- 啟動：SqlLocalDB.exe start "Name"  
- 停止：SqlLocalDB.exe stop "Name"  
- 刪除：SqlLocalDB.exe delete "Name"  
- 列出所有實例：SqlLocalDB.exe info  
- 檢查指定實例詳情：SqlLocalDB.exe info "Name"  
- 共用：SqlLocalDB.exe share "Owner" "PrivateName" "SharedName"  
- 取消共用：SqlLocalDB.exe unshare "SharedName"  
- 列出安裝版本：SqlLocalDB.exe versions

結語
- LocalDB 是一個輕量、免管理且適合開發測試的內嵌 SQL Server 解決方案；若需多人存取或長期生產使用，請評估是否改用完整的 SQL Server 或 Azure SQL 服務。上述步驟與命令均可在 Microsoft Docs 的 LocalDB 與 SqlLocalDB 文件中找到詳細說明[^22,^24,^5]。

（若需要：我可以幫你產生可直接複製貼上的範例指令清單、連接字串範例或在 Windows/Visual Studio 中的圖文教學。）

