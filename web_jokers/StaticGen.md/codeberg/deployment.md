---
layout: default
title:  CPS 簡介與比較
parent: Codeberg
grand_parent: Static Site Generators
last_modified_date: 2024-06-22 10:21:24
tags: Codeberg 
---

# Codeberg pages-server簡介與比較

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


## 部署

> 警告：一些注意事項適用
> 您需先具備系統管理知識以及程式碼理解和建構知識，以便您最終可以編輯那些原本是不可配置項目、和(或)僅適用於代碼山的特定設定。
> 將來，我們將嘗試減少這些，並使託管 Codeberg 頁面像設定 Gitea 一樣簡單。
> 如果您考慮在實踐中使用頁面，請考慮先聯絡我們，然後我們將嘗試分享一些基本步驟並記錄管理員的當前用法（雖然此一狀態可能會發生變化）。

部署軟體本身非常容易。您可以取得目前版本的二進位檔案或自行構建(詳[build](#build))，按如下所述配置環境，然後就完成了。

困難的部分是添加自訂網域支援（如果您打算使用它）。 SSL 憑證（請求 + 續訂）由 Pages Server 自動處理，但如果您想在共用 IP 位址（而不是獨立的）上執行它，則需要將反向代理設定為不終止 TLS 連接，但將IP 層級的請求轉送到頁面伺服器。

- 您可以在`examples/haproxy-sni`資料夾中查看概念驗證，尤其是查看`haproxy.cfg` 的這一部分。
  - 該[docker-compose.yml](https://codeberg.org/Codeberg/pages-server/src/branch/main/examples/haproxy-sni/docker-compose.yml)需要[適度修改](#)才能執行。

如果您想測試更改，可以開啟 PR 並要求build_pr_image新增標籤。這將觸發 PR 的構建，從而建立一個用於測試的 docker 映像。

環境變數
ACME_ACCEPT_TERMS（預設：使用自簽名憑證）：將此設為「true」以接受 ACME 提供者的服務條款。
ACME_API（預設值：https://acme-v02.api.letsencrypt.org/directory）：將其設為https://acme.mock.director以使用無效憑證而不進行任何驗證（非常適合偵錯）。 ZeroSSL 將來可能會更好，因為它沒有速率限制，並且不會與官方 Codeberg 憑證（使用 Let's Encrypt）衝突，但我還無法讓它工作。
ACME_EAB_KID& ACME_EAB_HMAC（預設：不使用 EAB）：EAB 憑證，例如 ZeroSSL。
ACME_EMAIL（預設：noreply@example.email）：設定傳送到 ACME API 伺服器的電子郵件以接收例如續訂提醒。
ACME_USE_RATE_LIMITS（預設值：true）：將此設為 false 以停用速率限制，例如使用 ZeroSSL。
DNS_PROVIDER（預設：使用自簽名憑證）：主網域通配符的 ACME DNS 提供者的程式碼。請參閱https://go-acme.github.io/lego/dns/以了解可用值和其他環境變數。
ENABLE_HTTP_SERVER（預設值：false）：將此設為 true 以啟用 HTTP-01 質詢並將所有其他 HTTP 請求重新導向至 HTTPS。目前僅適用於連接埠 80。
GITEA_API_TOKEN（預設值：空）：Gitea 實例存取非公開（例如有限）儲存庫的 API 令牌。
GITEA_ROOT（預設值：）https://codeberg.org：上游 Gitea 實例的根。
HOST& PORT（預設：[::]& 443）：監聽位址。
LOG_LEVEL（預設值：警告）：設定此項目以指定日誌記錄等級。
NO_DNS_01（預設值false：）：停用 ACME DNS。這意味著通配符憑證是自簽署的，並且所有網域和子網域都將具有不同的憑證。因為這可能會導致 ACME 提供者的速率限制，所以對於開放註冊或大量使用者/組織的 Gitea/Forgejo 實例，不建議使用此選項。
PAGES_DOMAIN（預設值：）codeberg.page：頁面的主域。
RAW_DOMAIN（預設值raw.codeberg.page：）：原始資源的域（必須是 的子域PAGES_DOMAIN）。

## Build and Run the image

### build

- docker官網雖然也有一個版本，但是似乎不是給所有人下載的。
- 自行編譯：使用下列指令

```bash
(py39) 16:40@kuang:~/GitHub/pages 
$ docker build -t pages-server . 
$ docker images #(檢視是否成功編譯)
```

### running forgejo/gitea

```bash
docker run -e USER_GID=2000 -e USER_UID=2000  -p 3000:3000 -p 9022:22 -e FORGEJO__server__SSH_PORT=9022  -v /home/git:/srv/git mstreicherde/forgejo 
```

- 這個範例的使用者(2000:2000)必須是`/home/git`的擁有者，這個方案適用於多人的git。
- 如果改成實際單一的使用者，可以考慮下列指令

```bash
docker run -e USER_GID=501 -e USER_UID=20  -p 3000:3000 -p 9022:22 -e FORGEJO__server__SSH_PORT=9022  -v /Users/kuang/MyPrograms/git:/srv/git forgejo/gitea &
```

### running pages-server

- 因官網並未提供執行建議，以下以[anythingLLM的執行方式](https://docs.useanything.com/installation/self-hosted/local-docker#recommend-way-to-run-dockerized-anythingllm)類比推敲

```bash
export STORAGE_LOCATION=$HOME/anythingllm && \
mkdir -p $STORAGE_LOCATION && \
touch "$STORAGE_LOCATION/.env" && \
docker run -d -p 3001:3001 \
--cap-add SYS_ADMIN \
-v ${STORAGE_LOCATION}:/app/server/storage \
-v ${STORAGE_LOCATION}/.env:/app/server/.env \
-e STORAGE_DIR="/app/server/storage" \
mintplexlabs/anythingllm
```

- 端口
  - 範例中內外都是3001。[官網案例](https://codeberg.org/Codeberg/pages-server/src/branch/main/examples/haproxy-sni/docker-compose.yml)影像暴露的端口是一般靜態網頁的80/443。



    ACME_ACCEPT_TERMS (default: use self-signed certificate): Set this to "true" to accept the Terms of Service of your ACME provider.
    ACME_API (default: https://acme-v02.api.letsencrypt.org/directory): set this to https://acme.mock.director to use invalid certificates without any verification (great for debugging). ZeroSSL might be better in the future as it doesn't have rate limits and doesn't clash with the official Codeberg certificates (which are using Let's Encrypt), but I couldn't get it to work yet.
    ACME_EAB_KID & ACME_EAB_HMAC (default: don't use EAB): EAB credentials, for example for ZeroSSL.
    ACME_EMAIL (default: noreply@example.email): Set the email sent to the ACME API server to receive, for example, renewal reminders.
    ACME_USE_RATE_LIMITS (default: true): Set this to false to disable rate limits, e.g. with ZeroSSL.
    DNS_PROVIDER (default: use self-signed certificate): Code of the ACME DNS provider for the main domain wildcard. See https://go-acme.github.io/lego/dns/ for available values & additional environment variables.
    ENABLE_HTTP_SERVER (default: false): Set this to true to enable the HTTP-01 challenge and redirect all other HTTP requests to HTTPS. Currently only works with port 80.
    GITEA_API_TOKEN (default: empty): API token for the Gitea instance to access non-public (e.g. limited) repos.
    GITEA_ROOT (default: https://codeberg.org): root of the upstream Gitea instance.
    HOST & PORT (default: [::] & 443): listen address.
    LOG_LEVEL (default: warn): Set this to specify the level of logging.
    NO_DNS_01 (default: false): Disable the use of ACME DNS. This means that the wildcard certificate is self-signed and all domains and subdomains will have a distinct certificate. Because this may lead to a rate limit from the ACME provider, this option is not recommended for Gitea/Forgejo instances with open registrations or a great number of users/orgs.
    PAGES_DOMAIN (default: codeberg.page): main domain for pages.
    RAW_DOMAIN (default: raw.codeberg.page): domain for raw resources (must be subdomain of PAGES_DOMAIN).

## adaptations of haproxy-sni example

### source

- [pages-server/examples/haproxy-sni/docker-compose.yml](https://codeberg.org/Codeberg/pages-server/src/branch/main/examples/haproxy-sni/docker-compose.yml)

### deployment on macOS

- 因為使用了haprox,原本的`httpd`必須停止
- caddy的影像只是個範例，並沒有實質的作用

```yml
$ cat docker-compose.yml
version: '3'
services:
  haproxy:
    image: haproxy
    ports: ['125.229.149.182:8083:80']
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
      - ./dhparam.pem:/etc/ssl/dhparam.pem:ro
      - ./haproxy-certificates:/etc/ssl/private/haproxy:ro
    cap_add:
      - NET_ADMIN
  gitea:
    image: gitea/gitea
    ports: ['125.229.149.182:3000:3000']
    volumes:
      - ./gitea-www:/srv:ro
      - ./gitea.Caddyfile:/etc/caddy/Caddyfile:ro
  pages:
    image: pages-server:latest
    ports: ['125.229.149.182:8085:80']
    volumes:
      - ./pages-www:/srv:ro
      - ./pages.Caddyfile:/etc/caddy/Caddyfile:ro
```

### 共用docker的網路

- last glance
  
```bash
$ docker-compose up -d
WARN[0000] /Users/kuang/GitHub/pages/examples/haproxy-sni/docker-compose.yml: `version` is obsolete 
WARN[0000] Found orphan containers ([haproxy-sni-pages-1]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up. 
[+] Running 4/4
 ✔ Network proxy-network            Created                                                                                                                              0.0s 
 ✔ Network haproxy-network          Created                                                                                                                              0.0s 
 ✔ Container haproxy-sni-gitea-1    Started                                                                                                                              0.3s 
 ✔ Container haproxy-sni-haproxy-1  Started                                                                                                                              0.4s 
(base) 21:26@kuang:~/GitHub/pages/examples/haproxy-sni 
$ docker ps                                        
CONTAINER ID   IMAGE           COMMAND                  CREATED          STATUS          PORTS                                    NAMES
7311a3a44c92   forgejo/gitea   "/usr/bin/entrypoint…"   15 seconds ago   Up 15 seconds   22/tcp, 125.229.149.182:3000->3000/tcp   haproxy-sni-gitea-1
(base) 21:26@kuang:~/GitHub/pages/examples/haproxy-sni 
$ docker network connect haproxy-network    haproxy-sni-gitea-1
(base) 21:27@kuang:~/GitHub/pages/examples/haproxy-sni 
$ docker run -h sinotec24.com -p 8084:80 -e GITEA_ROOT="sinotec24.com" -e PAGES_DOMAIN="sintec24.pages" -e GITEA_ROOT="http://sinotec24.com:3000" -e HOST="sinotec24.com" -e PORT="8084" --network haproxy-network pages-server:latest
1:28PM ERR A fatal error occurred error="could not create new gitea client: Get \"http://sinotec24.com:3000/api/v1/version\": dial tcp 192.168.32.3:3000: connect: connection refused"
```

- 似乎抓得到ip:host，但存取被拒，應為TOKEN沒設
- 在docker-compose內宣告network名稱

```yml
version: '3' 
networks:
  proxy-net:
    name: proxy-network
  haproxy-net:
    name: haproxy-network
services:
  haproxy:
    image: haproxy
    ports: ['125.229.149.182:8083:80']
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
      - ./dhparam.pem:/etc/ssl/dhparam.pem:ro
      - ./haproxy-certificates:/etc/ssl/private/haproxy:ro
    cap_add:
      - NET_ADMIN
    networks:
      - haproxy-net
      - proxy-net
  gitea:
    image: forgejo/gitea
    ports: ['125.229.149.182:3000:3000']
    volumes:
      - ./gitea-www:/srv:ro
      - ./gitea.Caddyfile:/etc/caddy/Caddyfile:ro
      - ./gitea-www/data:/data/gitea
    networks:
      - proxy-net
```