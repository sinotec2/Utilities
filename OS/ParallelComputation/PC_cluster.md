---
layout: default
title:  PC計算叢集的相應設定
parent:   Parallel Computation
grand_parent: Operation Systems
last_modified_date: 2022-04-25 12:20:36
---
# PC計算叢集的相應設定
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

## 使用者設定

- 可否設定特定的window使用者名稱，當以其登入window是，設定可接受Guacamole的遠端遙控，而以其他人登入時，則否？

Guacamole本身並沒有直接的機制來限制特定Windows使用者名稱的遠程遙控訪問權限。Guacamole的身份驗證機制通常是基於用戶提供的憑據（例如用戶名和密碼）。

然而，你可以在Windows系統上使用相應的權限和安全設置來達到類似的目標。具體來說，你可以配置Windows使用者帳戶的權限，確保只有特定的使用者擁有遠程桌面訪問的權限，而其他使用者則沒有。這可以在Windows的"遠程桌面使用者"組或類似的組織單位中進行配置。

在Guacamole方面，你仍然需要提供這些Windows使用者的憑據，以便Guacamole能夠進行LDAP身份驗證或其他支援的身份驗證方法。確保設定Guacamole的LDAP或其他身份驗證方式，以與Windows上的使用者管理系統協同工作。