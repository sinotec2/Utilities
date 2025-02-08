---
layout: default
title:  postgres
parent: DB_servers
last_modified_date: 2024-11-06 10:51:11
tags: DB_servers
---

# postgres注意事項
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

- macOS的[安裝](https://etrex.tw/free_chatbot_book/mac_dev/postgresql.html),特別注意：
  - 使用`brew services start postgresql`第一次啟動，新增`postgres`使用者，才能使用`psql -U postgres`登入。
