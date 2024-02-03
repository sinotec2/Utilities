---
layout: default
title:  Druid Q&A
parent: Apache Druid
grand_parent: DB_servers
grand_parent: OLAP
last_modified_date: 2024-01-07 20:26:18
tags: DB_servers Druid
---

# Apache Druid General Q&A
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

### Linux 方案

是的，Kerberos 在 Linux 系統上有相應的實現和支援。通常，Linux 上使用 MIT Kerberos（Massachusetts Institute of Technology Kerberos）作為 Kerberos 的實現。MIT Kerberos 提供了一套完整的 Kerberos 協議套件，可用於 Linux 系統的身份驗證和安全性需求。

在許多 Linux 發行版中，你可以透過套件管理系統安裝 MIT Kerberos 相關套件，例如在 Ubuntu 上可以使用以下命令安裝：

```bash
sudo apt-get install krb5-user krb5-config
```

這樣就能夠在 Linux 上進行 Kerberos 相關配置和使用。當然，具體的安裝方式可能會因 Linux 發行版而異，你可以參考相應發行版的文檔或官方指南進行配置。

