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

### 連線

- httpd :[在 apache httpd 內採用 Kerberos 進行驗証](https://wiki.centos.org/zh(2d)tw(2f)HowTos(2f)HttpKerberosAuth.html）
- NFS:[如何設定讓 NFS 共用資料夾使用 Kerberos？](https://kb.synology.com/zh-tw/DSM/tutorial/how_to_set_up_kerberized_NFS)

## Apache Druid 設定

根據[Apache Druid官方文檔](https://druid.apache.org/docs/latest/development/extensions-core/druid-kerberos/)，我將簡要描述Druid的Kerberos設定。中文詮釋版，可以詳見[Apache Druid 安裝Kerberos驗證系統](./druid_kbr.md)

1. **Kerberos驗證機制**：Apache Druid的Kerberos擴展可用於保護Druid進程的HTTP端點。它使用簡單且受保護的GSSAPI協商機制SPNEGO。要啟用Kerberos驗證，請確保在擴展的加載列表中包含`druid-kerberos`。

2. **設定步驟**：
    - 在`extensions`配置中添加`druid-kerberos`。
    - 創建一個名為`MyKerberosAuthenticator`的驗證器，並將其添加到`authenticatorChain`中。
    - 配置`MyKerberosAuthenticator`的屬性，例如`serverPrincipal`（SPNEGO服務主體）、`serverKeytab`（SPNEGO服務密鑰表）等。
    - 設置`cookieSignatureSecret`以簽署身份驗證Cookie。
    - 可選：指定`authorizerName`以將請求定向到相應的授權器。

3. **注意事項**：
    - Druid進程使用的SPNEGO主體必須以HTTP開頭，並且必須具有形式為“HTTP/_HOST@REALM”的格式。
    - 請注意，Kerberos驗證器的`excludedPaths`屬性已被移除，因為路徑排除功能現在由所有驗證器/授權器通用地處理，請參閱主要的身份驗證文檔。

希望這些簡要說明對您有所幫助！如果您需要更詳細的信息，請參閱官方文檔¹²³。

來源: 與 Bing 的交談， 2024/2/3
(1) Kerberos Apache® Druid. https://druid.apache.org/docs/latest/development/extensions-core/druid-kerberos/.
(2) Authentication and Authorization | Apache® Druid. https://druid.apache.org/docs/latest/operations/auth/.
(3) Enable Kerberos authentication in Apache Druid - Cloudera. https://docs.cloudera.com/HDPDocuments/HDP3/HDP-3.1.4/adding-druid/content/druid_enable_kerberos_authentication.html.
