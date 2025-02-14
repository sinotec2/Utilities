---
layout: default
title:  windows 系統的tls 憑證
parent: web filebrowser
grand_parent: Web Jokers
nav_order: 99
last_modified_date: 2025-02-14 08:32:07
tags: web
---

#  windows 系統的tls 憑證
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

在 Windows 上產生 HTTPS 憑證（TLS/SSL）通常有幾種方式，以下是兩種常見方法：

1. 使用 Let’s Encrypt（推薦）
2. 使用 OpenSSL 生成自簽憑證（適用於內部測試環境）

## Let’s Encrypt

方法 1：使用 Let’s Encrypt（免費且自動續約）

Let’s Encrypt 提供免費 SSL 憑證，你可以使用 Certbot 來取得。

步驟 1：安裝 Certbot

Certbot 支援 Windows，可從官方下載 Certbot Windows 版 並安裝。

步驟 2：使用 Certbot 取得憑證

開啟 PowerShell（管理員權限）並執行：

```bash
certbot certonly --standalone -d yourdomain.com --preferred-challenges http
```

- `--standalone`：Certbot 會啟動一個臨時 Web 伺服器來驗證域名，因此必須確保 80 端口未被佔用。
- `-d yourdomain.com`：換成你的網域名稱。
- 憑證會存放在 C:\Certbot\live\yourdomain.com\

步驟 3：續約憑證

Let’s Encrypt 憑證有效期限為 90 天，可使用排程工作（Task Scheduler）執行：

  ```bash
  certbot renew
  ```

## OpenSSL

方法 2：使用 OpenSSL 產生自簽憑證（適用內部測試）

如果只是內部測試，Windows 也可以使用 OpenSSL 生成自簽名憑證。

步驟 1：安裝 OpenSSL

- 下載 Windows 版 OpenSSL：https://slproweb.com/products/Win32OpenSSL.html
- 安裝完成後，確保 openssl.exe 可在命令提示字元中執行。

步驟 2：產生自簽憑證

開啟 PowerShell 或 cmd 並執行：

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mykey.key -out mycert.crt
```

這會產生：

- mykey.key（私鑰）
- mycert.crt（自簽憑證）

注意：自簽憑證不被瀏覽器信任，需要手動安裝到 Windows 信任的憑證存儲區。

## 既有憑證

> 我的瀏覽器已經裝有一個聯外的憑證，可以利用來成為網路伺服器的憑證嗎？如何取得？

通常，瀏覽器裡的憑證是為了驗證客戶端身份而設計的，所以它們通常不可用作伺服器憑證。這些憑證存放在憑證儲存中，而且它們主要是用來建立安全通訊（如SSL/TLS）連接的。如果你希望用於網路伺服器的憑證，通常需要取得伺服器專用的憑證，並且你需要擁有私鑰。

你無法直接將瀏覽器中安裝的憑證用作網路伺服器憑證，除非該憑證包含私鑰並且它是設計來用於伺服器身份認證的。此外，一些瀏覽器憑證可能無法導出。

若要使用，通常你需要從瀏覽器的憑證儲存區導出憑證及私鑰（通常是 .pfx 格式）。但如果只是CA提供的憑證，那就無法用來認證伺服器。

是否能使用瀏覽器中安裝的憑證作為伺服器憑證，取決於憑證是否包含私鑰並具有伺服器驗證的用途。一般來說，瀏覽器憑證通常只是用來確認伺服器身份，而不適用於伺服器端。若有私鑰且符合伺服器驗證需求（如包含網域名稱），則可以從瀏覽器中導出憑證（例如PFX格式），並配置於伺服器上來啟用HTTPS。

