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

### 設定檔案

- 舊版中文說明[freeipa（5）文件和日志位置](https://blog.csdn.net/senvenks/article/details/42640165)

|位置名稱|用途|重要選項說明
-|-|-
`/etc/httpd/conf.d/`||
`ipa-pki-proxy.conf`|PKI（Public Key Infrastructure）Proxy 配置|[Dogtag](https://www.freeipa.org/page/V4/Dogtag_GSS-API_Authentication)
`nss.conf`|用於配置 Apache HTTP Server 以支援 NSS（Network Security Services）模組，進行 SSL/TLS 加密和安全通信|
`ipa.conf`|IPA主要設定檔|[33版模板](https://github.com/freeipa/freeipa/blob/master/install/share/ipa.conf.template)
`ipa-rewrite.conf`|重寫規則用於修改 HTTP 請求的 URI 或其他相關屬性，以適應 FreeIPA 的身份管理和單點登入（SSO）機制|
`ipa-kdc-proxy.conf`|kerberos伺服器代理設定|
