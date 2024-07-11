---
layout: default
title:  Gitea的Actions
parent: Gitea
grand_parent: DB_servers
last_modified_date: 2024-06-27 09:00:54
tags: gitea
---

#  Gitea的Actions

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

- Gitea的Actions功能與自動連續整合發布有密切的關係。也是活化地端文件系統的核心引擎。整體作業架構如下圖所示。

![](img/2024-07-10-21-45-38.png)

- 此處著重說明Gitea內部的設定與管理。

### Actions vs Runners

- Actions指的是Github/Gitea等等倉儲內的一系列行動
  - 行動由某一個runner docker負責執行
  - 行動內容按照倉儲內指定目錄的工作流程（`.yml`）檔案指派其細節，包括程序、軟體版本、指令細節、