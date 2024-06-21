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

此外，該網頁包含了指向 Codeberg 文檔、社區問題和其他由 Codeberg 提供的服務的[鏈接]([[2024-06-21]])。

### Codeberg vs httpd

Codeberg 是一個自託管的 Git 服務器，用於託管 Git 存儲庫。它與 httpd 或 Apache 的關係如下：
 * Codeberg 使用自己的 Web 服務器來提供 Git 存儲庫的訪問。 這意味著它不需要 httpd 或 Apache 才能運行。
 * Codeberg 可以與 httpd 或 Apache 一起使用以提供額外的功能。 例如，您可以使用 httpd 或 Apache 來提供對 Codeberg 存儲庫的 HTTPS 訪問。
具體來說，Codeberg 使用 Go 語言編寫，並使用自己的 Web 服務器來提供 Git 存儲庫的訪問。它還支持 WebDAV，這是一種允許用戶通過 Web 瀏覽器管理 Git 存儲庫的協議。
如果您想自託管 Git 存儲庫，Codeberg 是 httpd 或 Apache 的一個不錯的選擇。它易於使用且功能強大，並且可以與 httpd 或 Apache 一起使用以提供額外的功能。
以下是一些 Codeberg 的優點：
 * 自託管： 您擁有並控制自己的數據。
 * 開源： Codeberg 是開源的，這意味著您可以查看和修改其源代碼。
 * 免費： Codeberg 是免費使用的。
 * 功能強大： Codeberg 支持 Git 的所有功能，以及一些額外的功能，例如問題跟踪和 wiki。
以下是一些 Codeberg 的缺點：
 * 設置和維護可能需要一些技術知識。
 * 可能不如 GitHub 或 GitLab 等託管服務那樣可靠。
如果您正在尋找一個易於使用且功能強大的自託管 Git 服務器，那麼 Codeberg 是一個不錯的選擇。但是，如果您需要更可靠或更易於設置的解決方案，則可能需要考慮使用託管服務。




