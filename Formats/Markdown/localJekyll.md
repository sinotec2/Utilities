---
layout: default
title: local Jekyll Webblog
parent: Markdown
grand_parent: Formats
last_modified_date: 2022-11-15 10:21:23
tags: note_system
---

# 本地git系統與部落格之發布
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 背景

- 地端、內部的git有其必要與特殊性，在機敏程式的發展與協作、內部訓練傳承、建立檔案連結等等歷程，有其特定的腳色功能。
- 進一步要問的就是：可否像GithubPage一樣，在git的平台上來執行jekyll的編譯，將md檔案也編成美美的部落格頁面?答案是肯定的。

## Jekyll、Gitea、Drone 和 Docker

- Josh Illes(2020) [Deploying a Jekyll Site with Drone and Gitea](https://joshilles.com/server/jekyll/gitea-drone-docker/)這個實例是用docker來布建所有的系統，包括[Gitea](https://about.gitea.com/)伺服器與[Drone](https://www.drone.io/)環境設定。  
- 這個網頁是一篇教學文章，介紹如何使用 **Jekyll**、**Gitea**、**Drone** 和 **Docker** 來建立一個個人的部落格平台。文章的主要內容如下：
  - **Jekyll** 是一個靜態網站生成器，可以將 Markdown 檔案轉換成 HTML 網頁，並提供多種主題和插件。
  - **Gitea** 是一個輕量級的 Git 服務，可以讓使用者在自己的伺服器上建立和管理 Git 倉庫，並提供網頁介面和 API。
  - **Drone** 是一個持續整合和持續交付的平台，可以自動化 Jekyll 網站的建置和部署，並支援 Docker 容器。
  - **Docker** 是一個開源的容器平台，可以讓使用者將應用程式和相關的環境打包成一個可移植的單元，並在任何支援 Docker 的系統上執行。
  - 文章詳細說明了如何安裝和設定這些工具，並提供了相關的程式碼和截圖，以及一些常見的問題和解決方法。
  - 文章還提供了一些參考資料，包括官方文件、教學影片和相關的部落格文章。 
  - 2024-01-20 10:47:34 (網址似乎關閉了，當時沒有下載全文、還好有下面另一篇,這次原諒我要全文照抄了)
- [ruanbekker(2019) Using Drone CI to Build a Jekyll Site and Deploy to Docker Swarm](https://blog.ruanbekker.com/blog/2019/04/23/using-drone-ci-to-build-a-jekyll-site-and-deploy-to-docker-swarm/)

## GitHub Pages 与 Gitee Pages 上的 Jekyll

## 使用 Drone CI 建置 Jekyll 網站並部署到 Docker Swarm

- 來源：阮貝克的博客2019年4月23日下午 5:57
- 在這篇文章中，我將向您展示如何使用無人機設定 CICD 管道來建置 jekyll 網站並部署到 docker swarm。

###  環境概覽

- Jekyll 的程式碼庫：我們的程式碼將託管在 Github 上（我將示範如何從頭開始設定它）
- 秘密儲存：我們的秘密，例如 ssh 金鑰、群組主機位址等將儲存在無人機秘密管理器中
- Docker Swarm：Docker Swarm 使用 Traefik 作為 HTTP 負載平衡器
- 無人機伺服器和代理：如果您沒有無人機，您可以在 docker 上[設定無人機伺服器和代理](https://blog.ruanbekker.com/blog/2019/04/18/setup-a-drone-cicd-environment-on-docker-with-letsencrypt/)，您也可以查看一下[官網說明cloud.drone.io](https://cloud.drone.io/)
- 工作流程：

>1. * 每當 github 上收到對 master 的推播時，管道就會被觸發
>2. * 我們的 github 儲存庫中的內容將被複製到容器上的代理
>3. * Jekyll 將會建置並使用 rsync 將輸出傳送到 docker swarm
>4. * docker-compose.yml將使用scp傳送至docker swarm主機
>5. * docker stack 將透過 ssh 進行部署

### 本地安裝 Jekyll

在本地安裝 Jekyll，因為我們將使用它來建立初始網站。我使用的是 Mac，所以我將使用`brew`. 對於其他作業系統，請查看[Jekyll官網這篇文章](https://jekyllrb.com/docs/installation/)。

我將以減肥部落格為例進行示範。

- 安裝Jekyll：

```bash
$ brew install jekyll
```

- 繼續建立一個新網站來託管您的 jekyll 網站的資料：

```bash
$ jekyll new blog-weightloss
```

### 建立 Github 儲存庫

首先我們需要建立一個空的 github 儲存庫，在我的範例中是github.com/ruanbekker/blog-weightloss.git. 建立儲存庫後，變更為jekyll new命令建立的目錄：

```bash
$ cd blog-weightloss
```

- 現在初始化git，設定遠程，添加jekyll資料並推送到github：

```bash
$ git init
$ git remote add origin git@github.com:ruanbekker/blog-weightloss.git # <== change to your repository
$ git add .
$ git commit -m "first commit"
$ git push origin master
```

您應該在 github 儲存庫上看到您的資料。

### 在無人機伺服器網站上創造秘鑰

- 登入 Drone UI，同步儲存庫，啟動新儲存庫並前往設置，您將在其中找到機密部分。
- 加入以下秘鑰：

```bash
Secret Name: swarm_host
Secret Value: ip address of your swarm

Secret Name: swarm_key
Secret Value: contents of your private ssh key

Secret Name: swarm_user
Secret Value: the user that is allowed to ssh
```

- 您應該看到以下內容：

![](https://user-images.githubusercontent.com/567298/56619871-5c4fc480-6627-11e9-8820-c9d4ddff698c.png)

### 增加無人機配置

Drone程式會從根目錄的檔案.drone.yml中，尋找有關如何執行其任務的說明。讓我們在其中繼續指定我們要使用的管道：

```bash
$ vim .drone.yml
```

並增加無人機配置：

```bash
pipeline:
  jekyll-build:
    image: jekyll/jekyll:latest
    commands:
      - touch Gemfile.lock
      - chmod a+w Gemfile.lock
      - chown -R jekyll:jekyll /drone
      - gem update --system
      - gem install bundler
      - bundle install
      - bundle exec jekyll build

  transfer-build:
    image: drillster/drone-rsync
    hosts:
      from_secret: swarm_host
    key:
      from_secret: swarm_key
    user:
      from_secret: swarm_user
    source: ./*
    target: ~/my-weightloss-blog.com
    recursive: true
    delete: true
    when:
      branch: [master]
      event: [push]

  transfer-compose:
    image: appleboy/drone-scp
    host:
      from_secret: swarm_host
    username:
      from_secret: swarm_user
    key:
      from_secret: swarm_key
    target: /root/my-weightloss-blog.com
    source:
      - docker-compose.yml
    when:
      branch: [master]
      event: [push]

  deploy-jekyll-to-swarm:
    image: appleboy/drone-ssh
    host:
      from_secret: swarm_host
    username:
      from_secret: swarm_user
    key:
      from_secret: swarm_key
    port: 22
    script:
      - docker stack deploy --prune -c /root/my-weightloss-blog.com/docker-compose.yml apps
    when:
      branch: [master]
      event: [push]
```

### 通知

如果您想收到有關建置的通知，可以新增slack上的通知步驟，作為最後一步。

為此，請建立一個新的 Webhook 集成，您可以按照[這篇文章](https://blog.ruanbekker.com/blog/2019/04/18/setup-a-slack-webhook-for-sending-messages-from-applications/)取得逐步指南。獲得 Webhook 後，請前往 Secrets 並創建一個`slack_webhookSecret`。

然後應用通知步驟，如下所示：

1 
2 
3 
4 
5 
6 
7 
8 9 10 
11 12 13 14





	

  notify-via-slack:
    image: plugins/slack
    webhook:
      from_secret: slack_webhook
    channel: system_events
    template: >
      
        [DRONE CI]: ** : /
        ( -  | )

      
        [DRONE CI]: ** : /
        ( -  | )
      

根據狀態，您應該會收到類似如下的通知：

影像
新增 Docker 組合

接下來，我們需要宣告將 jekyll 服務部署到 swarm 所需的 docker compose 檔案：

1

	

$ vim docker-compose.yml

並填入此資訊（只需更改您自己的環境/設定的值）：

1 
2 
3 
4 
5 6 
7 
8 
9 
10 
11 
12 
13 
14 
15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 
30 31 32 33


















	

version: '3.5'

services:
  myweightlossblog:
    image: ruanbekker/jekyll:contrast
    command: jekyll serve --watch --force_polling --verbose
    networks:
      - appnet
    volumes:
      - /root/my-weightloss-blog.com:/srv/jekyll
    deploy:
      mode: replicated
      replicas: 1
      labels:
        - "traefik.backend.loadbalancer.sticky=false"
        - "traefik.backend.loadbalancer.swarm=true"
        - "traefik.backend=myweightlossblog"
        - "traefik.docker.network=appnet"
        - "traefik.entrypoints=https"
        - "traefik.frontend.passHostHeader=true"
        - "traefik.frontend.rule=Host:www.my-weightloss-blog.com,my-weightloss-blog.com"
        - "traefik.port=4000"
      update_config:
        parallelism: 2
        delay: 10s
      restart_policy:
        condition: on-failure
      placement:
        constraints:
          - node.role == manager
networks:
  appnet:
    external: true

推送到Github

現在我們需要將我們的.drone.yml和推docker-compose.yml送到 github。由於儲存庫是在無人機上啟動的，任何對 master 的推送都會觸發管道，因此在這次推送之後，我們應該去無人機上查看管道的運作。

新增未追蹤的檔案並推送到github：

1 
2 
3 
4

	

$ git add .drone.yml
$ git add docker-compose.yml
$ git commit -m "add drone and docker config"
$ git push origin master

當您轉到無人機用戶介面時，您應該看到管道輸出，它看起來或多或少像這樣（看看它有多漂亮！:D）

影像
測試傑基爾

如果部署已完成，您應該能夠在配置的網域上存取您的應用程式。我造訪 Jekyll 時的回應截圖：

影像

絕對令人驚奇！我真的很喜歡無人機！


