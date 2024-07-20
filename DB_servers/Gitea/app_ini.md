---
layout: default
title:  Gitea的初始化app.ini
parent: Gitea
grand_parent: DB_servers
last_modified_date: 2024-07-20 20:21:55
tags: gitea
---

#  Gitea的初始化 - app.ini

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

有關app.ini的介紹範例有很多，此處討論在地化過程中遭遇的困難與因應方式。

## 帳密與權限

gitea的安全性有很多種設定的方式。此處考量的重點包括：
- 組織內分享的需求
  - 有鑑於github-enterprice有其收費機制與強項，作為地端版本控制方案，組織的安全性與分享特性是優先考量的重要需求。
- 有別於MIS/ERP之身分管理
  - 避免資安漏洞
  - 隔開技術文件與機敏性業務，卻也有聯絡的可及性。
- 