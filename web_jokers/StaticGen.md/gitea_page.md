---
layout: default
title:  gitea page
parent: Static Site Generators
grand_parent: Web Jokers
last_modified_date: 2023-06-12 08:56:43
tags: blog 
---

# gitea page
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

### Codeberg

Codeberg Pages Server 是一個獨立的服務，通過 API 連接到 Gitea，從 Git 存儲庫中托管靜態頁面。它解決了 Gitea 中這一功能的缺失問題，並可以被其他 Gitea 實例部署，以向用戶提供靜態頁面托管服務。

主要功能包括自定義域名映射、緩存以及通過 Let’s Encrypt 自動生成和更新 SSL 憑證。

部署該服務需要一些系統管理和代碼編輯知識，但軟件本身易於部署。該文本還提供有關環境變量、對服務器開發的貢獻、以及測試和性能分析的信息。

此外，該網頁包含了指向 Codeberg 文檔、社區問題和其他由 Codeberg 提供的服務的[鏈接](https://codeberg.org/Codeberg/pages-server)。