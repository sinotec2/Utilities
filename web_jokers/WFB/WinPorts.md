
## window 端口設定

### 開放端口

是的，Windows 系統作為網路伺服器時，通常需要開放特定的網路端口，才能讓外部用戶存取服務。例如：

	•	Web 伺服器（IIS、Apache、Nginx） → 需開放 80（HTTP）、443（HTTPS）
	•	遠端桌面（RDP） → 需開放 3389
	•	資料庫伺服器（MySQL、MSSQL） → 需開放 3306（MySQL） 或 1433（MSSQL）
	•	FTP 伺服器 → 需開放 21（FTP 控制端口）
	•	其他應用程式 → 依需求開放特定端口

### 防火牆設定

如何在 Windows 防火牆開放端口？

	1.	 打開「Windows Defender 防火牆」
	•	Win + R → 輸入 wf.msc → 按 Enter
	2.	 點擊「進階設定」（左側選單）
	3.	 選擇「輸入規則」 → 點擊 「新增規則」
	4.	 選擇「連接埠」 → 點擊「下一步」
	5.	 選擇「TCP 或 UDP」 → 輸入要開放的端口號，例如 80 或 443
	6.	 選擇「允許連線」 → 點擊「下一步」
	7.	 選擇適用的網路範圍（「私人」或「公用」）
	8.	 命名規則（例如「開放 HTTP 服務」） → 點擊「完成」

### 如何用 PowerShell 開放端口？

如果需要自動化開放端口，可以使用 PowerShell：

New-NetFirewallRule -DisplayName "開放80端口" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow

這樣就能允許 HTTP 服務（80 端口）從外部訪問 Windows 伺服器。

如果要刪除該規則，可執行：

Remove-NetFirewallRule -DisplayName "開放80端口"

### 其他考量

- 確認 Windows 防火牆沒有阻擋流量
- 若有防毒軟體，需檢查是否有額外的網路保護功能
- 如果 Windows 位於內部網路，還需要在企業防火牆或路由器上開放對應端口
- 使用 netstat -an 或 Get-NetTCPConnection 檢查開放端口狀態

這樣，你的 Windows 伺服器就可以正確開放端口並提供服務了。

