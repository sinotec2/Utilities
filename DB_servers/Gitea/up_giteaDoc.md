---
layout: default
title:  Docker Running of Gitea
parent: Gitea
grand_parent: DB_servers
last_modified_date: 2024-07-20 20:01:58
tags: gitea
---

#  以docker影像執行Gitea伺服器

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

### 特色

docker 影像提供Gitea服務的好處與必要性如下

- 不會受到其他軟體設定的干擾
- 自動重啟：工作站停機再開，docker會自動重啟，不需人工維護。
- 隨時保持程式在最新的狀態
- 沒有後台登入、沒有維護的必要性
- 清楚的程式與資料界線，便於[備份]()、隨時可以重啟、韌性超強。
  - 即使面臨軟硬體或資安破壞，也可以在最短時間內復原。
- 具有移植與分殖能力、便於延展擴散。
  - 當組織的庫存量增加時，延展與分殖是非常有必要的。

### 資源

- [docker hub](https://hub.docker.com/r/gitea/gitea)
- docker影像安裝及維運[說明](https://docs.gitea.com/installation/install-with-docker-rootless/)
- copilot assistant

## docker與主機的使用者設定

### 設定要求

- 此二者需要整合以利檔案的傳送
  - docker範例為`1000:1000`，此組`gid:uid`可以/必須在`docker-compose.yml`或`docker run -e`更改（詳[up_giteaDoc.cs](#up_giteadoccs)）。
  - 命令列執行需為`git:git`
- 需先新增使用者`git:git`（`134:142`@eng06），並將其加在至少2個群組
  - `docker`：此群組內成員才能執行`docker`系列指令
  - `SESAir`（或其他編修權限之群組）：具有技術文件系統的編修權限，可以在後台提供補充或協助。
- 主機`APP_DATA_PATH`的所有者與權限：`git:git`

### 跨主機設定

- 如果分散不同主機公用同一個`APP_DATA_PATH`，另外要特別注意`gid:uid`的同一，以避免發生資料無法存入的問題。
- 如果`APP_DATA_PATH`要在`samba`託管的nas上正確存取，還需要在`samba`主機上正確新增。
- 必要時可以使用下列指令來更動

  ```bash
  sudo usermod -u new_uid username
  sudo groupmod -g new_gid groupname
  sudo find / -group old_gid -exec chgrp new_gid {} \;
  ```

- 注意
  - 使用者`git`必須先登出
  - gitea docker image必須先下線

## 主機、影像的APP_DATA_PATH對應

### 主機APP_DATA_PATH

- 命令列啟動Gitea，伺服器會在`/opt/gitea/data`目錄下開設並更新目錄內容。
- 如果拿此app.ini提供給docker，目錄將永遠無法對應。
- app.ini效力範圍，只限定在docker影像之內。

### 影像的APP_DATA_PATH

- [gitea/gitea:latest]()影像中的`APP_DATA_PATH`設定很僵化，因此以主機上來調整會比較容易一些。
- `AppPath`、`WorkPath`、`CustomPath`、`ConfigFile`
- docker image上的設定值為：（[詳下列docker logs輸出]()）

```bash
gitea  | 2024/07/20 16:24:08 cmd/web.go:113:showWebStartupMessage() [I] * AppPath: /usr/local/bin/gitea
gitea  | 2024/07/20 16:24:08 cmd/web.go:114:showWebStartupMessage() [I] * WorkPath: /data/gitea
gitea  | 2024/07/20 16:24:08 cmd/web.go:115:showWebStartupMessage() [I] * CustomPath: /data/gitea
gitea  | 2024/07/20 16:24:08 cmd/web.go:116:showWebStartupMessage() [I] * ConfigFile: /data/gitea/conf/app.ini
```

## up_giteaDoc.cs

### 程式碼

```bash
$ cat up_giteaDoc.cs
docker run \
    -d --name=gitea   \
    -e USER_UID=134   \
    -e USER_GID=142   \
    -v /opt:/data   \
    -v ./app.ini:/data/gitea/conf/app.ini   \
    -v /etc/timezone:/etc/timezone:ro   \
    -v /etc/localtime:/etc/localtime:ro  \
    -p 200.200.32.153:3000:3000   \
    -p 222:22   gitea/gitea:latest
```
