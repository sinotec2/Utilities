---
layout: default
title:  FreeIPA Utilities
parent: FreeIPA
grand_parent: Web Jokers
last_modified_date: 2024-02-14 09:24:41
tags: FreeIPA
---

# FreeIPA工具
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

### 检查FreeIPA相关的服务状态

```bash
#所有服務狀態
sudo ipactl status

#ipa 伺服器狀態
sudo systemctl status ipa.service
```

### 重啟web UI

- 因同屬Apache家族，啟動httpd就自然會啟動ipa的網路伺服器(其設定檔案都在`/etc/httpd/conf.d/`目錄下)

```bash
sudo systemctl restart httpd
```


### 設定檔案

- 舊版中文說明[freeipa（5）文件和日志位置](https://blog.csdn.net/senvenks/article/details/42640165)

|位置名稱|用途|重要選項說明
-|-|-
`/etc/httpd/conf.d/`|ipa系統相關代理、網頁安全等設定|
`ipa-pki-proxy.conf`|PKI（Public Key Infrastructure）代理配置|[Dogtag](https://www.freeipa.org/page/V4/Dogtag_GSS-API_Authentication)
`nss.conf`|用於配置 Apache HTTP Server 以支援 NSS（Network Security Services）模組，進行 SSL/TLS 加密和安全通信|
`ipa.conf`|IPA主要設定檔|[33版模板](https://github.com/freeipa/freeipa/blob/master/install/share/ipa.conf.template)
`ipa-rewrite.conf`|重寫規則用於修改 HTTP 請求的 URI 或其他相關屬性，以適應 FreeIPA 的身份管理和單點登入（SSO）機制|
`ipa-kdc-proxy.conf`|kerberos伺服器代理設定|

## 批次新增

- FreeIPA提供了批量添加使用者的功能。您可以使用`ipa`命令行工具的`user-add`子命令，通过提供用户信息的CSV文件批量添加用户。以下是一般的步骤：
- 注意：需要先通過kerberos驗證

```bash
# kinit admin@SINOTECH-ENG.COM
Password for admin@SINOTECH-ENG.COM:

```

1. **创建用户CSV文件：**
   创建一个包含新用户信息的CSV文件，例如`users.csv`。该文件的内容可能如下所示：

   ```csv
   username,firstname,lastname,email
   user1,John,Doe,john.doe@example.com
   user2,Jane,Smith,jane.smith@example.com
   ```

2. **使用`ipa user-add`命令：**
   运行以下命令，通过指定CSV文件来批量添加用户：

   ```bash
   ipa user-add --first=firstname --last=lastname --email=email username
   ```

   使用`--csv`选项指定CSV文件：

   ```bash
   ipa user-add --csv=users.csv
   ```

   这将使用CSV文件中的用户信息批量添加用户。

请确保在执行此操作之前，已经连接到FreeIPA服务器并具有适当的权限。有关更多详细信息，您可以查阅FreeIPA的相关文档或运行`man ipa`命令以获取`ipa`命令的手册页。

## 從 FreeIPA 上簽發憑證的流程

- [如何從 NSSDB (certutil) 中取出 pem 格式的 key](https://blog.davy.tw/posts/how-to-extract-pem-format-key-from-nssdb-certutil/)

