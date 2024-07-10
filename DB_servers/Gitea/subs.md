---
layout: default
title:  Git submodules 和  subtrees
parent: Gitea
grand_parent: DB_servers
last_modified_date: 2024-06-27 09:00:54
tags: gitea
---

#  submodules 和 Git subtrees

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

Git submodules 和 Git subtrees 都是 Git 中用於管理多個儲存庫之關係的工具，但它們的用途和使用方法有所不同。

### Git submodules

Git submodules 是 Git 中用於嵌入一個 Git 儲存庫作為另一個儲存庫的一部分的機制。它允許您在一個儲存庫中管理多個儲存庫之間的依賴關係，並在項目中使用多個 Git 儲存庫。使用 Git submodules 的步驟如下：

- 在主要儲存庫中，使用 git submodule add 命令添加子模組儲存庫的 URL。這將在主要儲存庫中創建一個新的目錄，該目錄將是子模組儲存庫的克隆。
- 在子模組儲存庫中進行更改時，使用 git submodule update 命令更新主要儲存庫中的子模組。
- 在主要儲存庫中提交更改時，請記得提交子模組儲存庫的更改，並使用 git submodule status 命令查看子模組的狀態。
- Git submodules 的優點是可以嚴格控制儲存庫之間的依賴關係，並在項目中使用多個 Git 儲存庫。然而，使用 Git submodules 的缺點是它們的配置和使用比其他選擇更複雜，並且在管理和更新子模組時可能需要更多的工作。

### Git subtrees

Git subtrees 是 Git 中用於在一個儲存庫中嵌入另一個儲存庫的子目錄的機制。它允許您在一個儲存庫中管理多個儲存庫之間的關係，並在項目中使用多個 Git 儲存庫。

使用 Git subtrees 的步驟如下：

- 在主要儲存庫中，使用 git subtree add 命令添加子樹儲存庫的 URL。這將在主要儲存庫中創建一個新的目錄，該目錄將是子樹儲存庫的克隆。
- 在子樹儲存庫中進行更改時，可以使用 git subtree pull 命令更新主要儲存庫中的子樹
- 在主要儲存庫中提交更改時，請記得提交子樹儲存庫的更改，並使用 git subtree push 命令將更改推送回子樹儲存庫。
- Git subtrees 的優點是它們比 Git submodules 更簡單易用，並且可以更好地管理儲存庫之間的關係。然而，使用 Git subtrees 的缺點是它們可能不如 Git submodules 嚴格地控制儲存庫之間的依賴關係。

總之，Git submodules 和 Git subtrees 都是用於管理多個 Git 儲存庫之關係的工具，根據您的需求和喜好，您可以選擇使用其中一個或兩個。