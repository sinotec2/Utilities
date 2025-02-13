---
layout: default
title: Windows 上的 Nginx HTTPS 設定
parent: web filebrowser
grand_parent: Web Jokers
nav_order: 99
last_modified_date: 2025-02-13 14:40:16
tags: web
---

#  Windows 上的 Nginx HTTPS 設定
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

Windows 版 Nginx 設定 HTTPS 方式與 Ubuntu 相似，但有一些特別注意事項：

1. 設定 Nginx HTTPS

開啟 nginx.conf，在 server 區塊中加入：

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate C:/nginx/certs/mycert.crt;
    ssl_certificate_key C:/nginx/certs/mykey.key;

    location / {
        root   html;
        index  index.html index.htm;
    }
}

注意 Windows 路徑格式，使用 / 而非 \。

2. 確保 Nginx 支援 OpenSSL

Windows 版 Nginx 內建 OpenSSL，但如果報錯，可使用 nginx -V 檢查是否有 --with-http_ssl_module。

3. 開啟 Windows 防火牆 443 端口

New-NetFirewallRule -DisplayName "開放HTTPS" -Direction Inbound -Protocol TCP -LocalPort 443 -Action Allow

4. 重新啟動 Nginx

nginx -s reload

Windows vs Ubuntu 的 Nginx 設定差異

|項目|Windows	|Ubuntu
-|:-|-
配置檔案位置|C:\nginx\conf\nginx.conf|/etc/nginx/nginx.conf
憑證路徑格式|C:/nginx/certs/|/etc/nginx/certs/
服務啟動方式|nginx.exe|systemctl restart nginx
防火牆端口設定|需手動開啟 443 端口|ufw allow 443/tcp
憑證取得方式|Certbot / OpenSSL 手動|certbot --nginx 自動配置

Windows 版 Nginx 主要差異在 路徑格式、服務管理方式、防火牆設定，其他 HTTPS 設定基本相同。

如果你的 Windows 是 伺服器環境（Windows Server），可以考慮使用 IIS 內建的 HTTPS 功能，避免 Nginx 相關的相容性問題。


