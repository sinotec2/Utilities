---
layout: default
title:  calendar_sample.py
parent: Calendars
grand_parent: DB_servers
last_modified_date: 2024-08-19 17:48:01
tags: calendar
---

# calendar_sample.py

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

```bash
kuang@eng06 /nas2/kuang/MyPrograms/GoogleCalendarAPI
$ python calendar_sample.py --help
usage: calendar_sample.py [-h] [--auth_host_name AUTH_HOST_NAME] [--noauth_local_webserver] [--auth_host_port [AUTH_HOST_PORT ...]]
                          [--logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Simple command-line sample for the Calendar API.
Command-line application that retrieves the list of the user's calendars.

optional arguments:
  -h, --help            show this help message and exit
  --auth_host_name AUTH_HOST_NAME
                        Hostname when running a local web server.
  --noauth_local_webserver
                        Do not run a local web server.
  --auth_host_port [AUTH_HOST_PORT ...]
                        Port web server should listen on.
  --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level of detail.
```

## 參數說明

- 似乎把`client_secrets.json`檔案內有關`localhost:8080`改設成其他網頁也會有效果。(這點還有待證實，該網頁如何把訊息傳回給程式?)。

### 指定認證主機名稱

- `[--auth_host_name AUTH_HOST_NAME]`
- 這個方式是提供一個可以連線的認證主機，此時須提供主機名稱。如果主機在`/etc/hosts`中已經登陸，應該也可以直接以名稱連線。

### 提供認證主機ip及端口

- `[--auth_host_port [AUTH_HOST_PORT ...]]`
- 這個ip及端口須和`client_secrets.json`檔案內設定一致。

### noauth_local_webserver

- 當程式執行找不到**本地**的瀏覽器進行Oauth2認證，會出現`noauth_local_webserver`的建議，並出現一長串網址。
- 將網址輸入到任何瀏覽器，是可以進行認證，但認證結果無法回到程式。

