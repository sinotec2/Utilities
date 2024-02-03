---
layout: default
title:  Kerberos
parent: Apache Druid
grand_parent: DB_servers
grand_parent: OLAP
last_modified_date: 2024-01-07 20:26:18
tags: DB_servers Druid
---

# Kerberos 
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

- Kerberos是一種電腦網路授權協定，用來在非安全網路中，對個人通信以安全的手段進行身分認證。
- 這個詞又指麻省理工學院為這個協定開發的一套電腦軟體。軟體設計上採用客戶端/伺服器結構，並且能夠進行相互認證，即客戶端和伺服器端均可對對方進行身分認證。

### centos方案

是的，你可以在 CentOS 上建置 Kerberos。CentOS 是一個基於 Red Hat Enterprise Linux 的開源 Linux 發行版，支援使用 MIT Kerberos 作為 Kerberos 的實現。

以下是在 CentOS 上安裝 MIT Kerberos 的基本步驟：

1. 使用 root 權限，使用套件管理器（yum）安裝 krb5-workstation 和 krb5-libs 套件：

   ```bash
   sudo yum install krb5-workstation krb5-libs
   ```

2. 編輯 `/etc/krb5.conf` 文件，配置 Kerberos 客戶端。這個文件包含了 Kerberos 的設定信息，你需要指定 Kerberos 伺服器的地址、域等設定。

3. 使用 `kinit` 命令來獲取 Kerberos 機票（ticket）：

   ```bash
   kinit your_username
   ```

   這會要求你輸入你的 Kerberos 帳號密碼。

4. 驗證 Kerberos 機票：

   ```bash
   klist
   ```

   這將顯示你的 Kerberos 機票信息。

這只是一個簡單的指南，具體的步驟可能會因 CentOS 版本而異。你可以參考 CentOS 文檔或 MIT Kerberos 官方文檔以取得更詳細的信息。

### ubuntu方案

是的，Kerberos 在 Linux 系統上有相應的實現和支援。通常，Linux 上使用 MIT Kerberos（Massachusetts Institute of Technology Kerberos）作為 Kerberos 的實現。MIT Kerberos 提供了一套完整的 Kerberos 協議套件，可用於 Linux 系統的身份驗證和安全性需求。

在許多 Linux 發行版中，你可以透過套件管理系統安裝 MIT Kerberos 相關套件，例如在 Ubuntu 上可以使用以下命令安裝：

```bash
sudo apt-get install krb5-user krb5-config
```

這樣就能夠在 Linux 上進行 Kerberos 相關配置和使用。當然，具體的安裝方式可能會因 Linux 發行版而異，你可以參考相應發行版的文檔或官方指南進行配置。

