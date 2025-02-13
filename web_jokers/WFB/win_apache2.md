---
layout: default
title: Apache2
parent: web filebrowser
grand_parent: Web Jokers
nav_order: 99
last_modified_date: 2025-02-13 14:40:16
tags: web
---

#  Apache2
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

> Window系統如何安裝Apache2 網路伺服器？

### 安裝程序

在 Windows 系統 上安裝 Apache 2 網頁伺服器，可以透過 Apache Lounge 提供的 Windows 版本來安裝，以下是詳細步驟：

方法 1：使用 Apache Lounge 安裝（建議）

步驟 1：下載 Apache 伺服器
	•	前往 Apache Lounge 官方網站
	•	下載 最新的 Windows 版 Apache 2.x（Win64 或 Win32）

步驟 2：解壓縮 Apache
	•	將下載的 ZIP 檔案解壓縮到 C:\Apache24（或其他目錄）
	•	例如：C:\Apache24\bin\httpd.exe 是 Apache 主要執行檔

步驟 3：安裝 Apache 為 Windows 服務
	1.	打開命令提示字元（cmd），並以 系統管理員身分 執行
	2.	移動到 Apache 安裝目錄：

cd C:\Apache24\bin


	3.	安裝 Apache 服務：

httpd.exe -k install


	4.	啟動 Apache 服務：

httpd.exe -k start


	5.	確認 Apache 是否運行：
	•	在瀏覽器中打開 http://localhost
	•	如果看到「It works!」，表示 Apache 成功運行

方法 2：使用 XAMPP 安裝（適合初學者）

如果不想手動配置，可以使用 XAMPP（內建 Apache、MySQL、PHP）：
	1.	下載 XAMPP
	2.	安裝後，在 XAMPP 控制面板 點擊「Start」啟動 Apache
	3.	在瀏覽器輸入 http://localhost 確認是否運行

Apache 重要設定

修改 httpd.conf 配置

Apache 的主要設定檔案位於：

C:\Apache24\conf\httpd.conf

	•	修改 監聽埠（Port）：

Listen 8080

這樣 Apache 會在 http://localhost:8080 運行

	•	修改 網站根目錄：

DocumentRoot "C:/www"
<Directory "C:/www">
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>

這樣網站根目錄變成 C:\www

如何移除 Apache
	•	停止服務：

httpd.exe -k stop


	•	移除 Apache 服務：

httpd.exe -k uninstall


	•	手動刪除 C:\Apache24 目錄

### 結論

安裝方式|適合對象|特點
|-|-|-
Apache Lounge（手動安裝）|進階用戶|可手動設定，較靈活
XAMPP（自動安裝）|初學者|一鍵安裝，內建 MySQL、PHP

如果你只需要 Apache 網頁伺服器，建議 使用 Apache Lounge，可獨立安裝、靈活配置。
