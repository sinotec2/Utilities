---
layout: default
title: k8s的網路設定
nav_order: 99
parent: 地端JupyterHub伺服器
grand_parent: Web Jokers
last_modified_date: 2024-09-16 14:30:21
tags: operation_systems
---

# k8s的網路設定

## Table of contents

{: .no_toc .text-delta }

1. TOC
{:toc}

---
- [medium](https://weng-albert.medium.com/%E6%B7%BA%E8%AB%87kubernetes%E5%85%A7%E9%83%A8%E7%B6%B2%E8%B7%AF%E9%80%9A%E4%BF%A1%E7%9A%84%E5%9F%BA%E6%9C%AC%E8%A7%80%E5%BF%B5-e9d993e01423)

## NGINX反向代理

- 當大量使用者同時登入 JupyterHub 伺服器的 8080 端口時，Nginx 可以透過一些標頭（headers）來傳遞每位使用者的真實 IP，讓後端伺服器能夠正確地辨識每個使用者的 IP 地址。
- 這在進行負載平衡或反向代理時非常重要，因為直接請求會被視為來自 Nginx 伺服器的 IP。

### 使用 Nginx 傳遞真實 IP 設置

在 Nginx 配置中，通常會使用以下幾個標頭來傳遞真實的客戶端 IP 給後端伺服器：

''
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;

這些標頭的功能如下：
	•	X-Real-IP：直接傳遞客戶端的真實 IP 地址。
	•	X-Forwarded-For：傳遞所有代理伺服器的 IP 地址列表，最後一個 IP 是客戶端的真實 IP。
	•	X-Forwarded-Proto：標記原始請求的協議（HTTP 或 HTTPS），讓後端知道請求的安全性。

JupyterHub 設置接收真實 IP

在 JupyterHub 中，為了讓應用識別到這些標頭，你可以在其配置檔（jupyterhub_config.py）中增加以下設定，讓 JupyterHub 知道請求是透過反向代理進來的：

# 設置反向代理模式
c.ConfigurableHTTPProxy.command = ['configurable-http-proxy', '--ip', '0.0.0.0', '--port', '8080']
c.JupyterHub.trusted_ips = ['Nginx IP Address']  # 將Nginx伺服器的IP加入信任列表

	•	c.JupyterHub.trusted_ips：將 Nginx 伺服器的 IP 地址加入信任清單，這樣 JupyterHub 會信任從 Nginx 傳遞過來的 X-Real-IP 和 X-Forwarded-For 標頭。

TCP/IP 層的連接追蹤

每一個使用者的請求會在 TCP 層建立一個獨立的連接，並透過 Nginx 的反向代理轉發給後端。這意味著，即便是同一瞬間大量的使用者請求，Nginx 也會通過這些標頭傳遞每位使用者的真實 IP，並保持正確的連接追蹤。

Nginx 的連線限制與流量控制

若擔心瞬間大量登入造成伺服器負擔，可以透過 Nginx 的 連線限制 和 流量控制 模組來管理，減少過多連接造成的系統資源耗損：

# 定義連線的限制區塊
http {
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

    server {
        # 限制每個IP的並發連線數
        limit_conn conn_limit 10;
        
        # 限制請求速率
        limit_req zone=req_limit burst=20 nodelay;

        location / {
            proxy_pass http://0.0.0.0:8080;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}

這樣配置後，Nginx 可以限制每個 IP 地址的並發連線數量（limit_conn）以及請求速率（limit_req），從而有效減少瞬間大量請求對伺服器的壓力。

總結

透過上述的 Nginx 標頭設置、JupyterHub 配置以及 Nginx 連線控制，伺服器可以在瞬間大量使用者登入時正確地辨識和回應每位使用者的真實 IP。