---
layout: default
title: WebFileBrowser
parent: Web Jokers
nav_order: 99
last_modified_date: 2025-02-13 14:40:16
tags: web
---

#  Web File Browser
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

## config init

### Synopsis

Initialize a new database to use with File Browser. All of this options can be changed in the future with the command 'filebrowser config set'. The user related flags apply to the defaults when creating new users and you don't override the options.

`filebrowser config init [flags]`

### Options

Name|Shorthand|Usage
-|:-:|-
addre|a|address to listen on
auth.header||HTTP header for auth.method=proxy
auth.method||authentication type
baseurl|b|base url
branding.disableExternal||disable external links such as GitHub links
branding.files||path to directory with images and custom styles
branding.name||replace 'File Browser' by this name
cert|t|tls certificate
commands||a list of the commands a user can execute
help|h|help for init
key|k|tls key
locale||locale for users
lockPassword||lock password
log|l|log output
perm.admin||admin perm for users
perm.create||create perm for users
perm.delete||delete perm for users
perm.download||download perm for users
perm.execute||execute perm for users
perm.modify||modify perm for users
perm.rename||rename perm for users
perm.share||share perm for users
port|p|port to listen on
recaptcha.host||use another host for ReCAPTCHA. recaptcha.net might be useful in China
recaptcha.key||ReCaptcha site key
recaptcha.secret||ReCaptcha secret
root|r|root to prepend to relative paths
scope||scope for users
shell||shell command to which other commands should be appended
signup|s|allow users to signup
sorting.asc||sorting by ascending order
sorting.by||sorting mode (name, size or modified)
viewMode||view mode for users

### Inherited

Name|Shorthand|Usage
-|:-:|-
config|c|config file path
database|d|database path

## window 端口設定

是的，Windows 系統作為網路伺服器時，通常需要開放特定的網路端口，才能讓外部用戶存取服務。例如：
	•	Web 伺服器（IIS、Apache、Nginx） → 需開放 80（HTTP）、443（HTTPS）
	•	遠端桌面（RDP） → 需開放 3389
	•	資料庫伺服器（MySQL、MSSQL） → 需開放 3306（MySQL） 或 1433（MSSQL）
	•	FTP 伺服器 → 需開放 21（FTP 控制端口）
	•	其他應用程式 → 依需求開放特定端口

如何在 Windows 防火牆開放端口？
	1.	打開「Windows Defender 防火牆」
	•	Win + R → 輸入 wf.msc → 按 Enter
	2.	點擊「進階設定」（左側選單）
	3.	選擇「輸入規則」 → 點擊 「新增規則」
	4.	選擇「連接埠」 → 點擊「下一步」
	5.	選擇「TCP 或 UDP」 → 輸入要開放的端口號，例如 80 或 443
	6.	選擇「允許連線」 → 點擊「下一步」
	7.	選擇適用的網路範圍（「私人」或「公用」）
	8.	命名規則（例如「開放 HTTP 服務」） → 點擊「完成」

如何用 PowerShell 開放端口？

如果需要自動化開放端口，可以使用 PowerShell：

New-NetFirewallRule -DisplayName "開放80端口" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow

這樣就能允許 HTTP 服務（80 端口）從外部訪問 Windows 伺服器。

如果要刪除該規則，可執行：

Remove-NetFirewallRule -DisplayName "開放80端口"

其他考量

- 確認 Windows 防火牆沒有阻擋流量
- 若有防毒軟體，需檢查是否有額外的網路保護功能
- 如果 Windows 位於內部網路，還需要在企業防火牆或路由器上開放對應端口
- 使用 netstat -an 或 Get-NetTCPConnection 檢查開放端口狀態

這樣，你的 Windows 伺服器就可以正確開放端口並提供服務了。
