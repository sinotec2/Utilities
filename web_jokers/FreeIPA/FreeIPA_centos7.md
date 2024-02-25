---
layout: default
title:  FreeIPA on centos7
parent: FreeIPA
grand_parent: Web Jokers
last_modified_date: 2024-02-05 11:25:52
tags: LDAP
---

#  LDAP on CENTOS 7
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

- 參考 [使用CentOS 7安裝FreeIPA, Jovepater(2021)](https://jovepater.com/article/centos-7-freeipa-installation/)以及[CentOS 7 安装 FreeIPA 主从复制 by Zhanming's blog(2019)](https://qizhanming.com/blog/2019/04/29/how-to-install-freeipa-server-and-replica-on-centos-7)

### results

```bash
Next steps:
        1. You must make sure these network ports are open:
                TCP Ports:
                  * 80, 443: HTTP/HTTPS
                  * 389, 636: LDAP/LDAPS
                  * 88, 464: kerberos
                  * 53: bind
                UDP Ports:
                  * 88, 464: kerberos
                  * 53: bind
                  * 123: ntp

        2. You can now obtain a kerberos ticket using the command: 'kinit admin'
           This ticket will allow you to use the IPA tools (e.g., ipa user-add)
           and the web user interface.

Be sure to back up the CA certificates stored in /root/cacert.p12
These files are required to create replicas. The password for these
files is the Directory Manager password
```


### upgrade repairments

- 因python程式的近版，過去python 2的習慣語法無法l在新的版本中因應，造成困擾。
- 修正程式
  - `/usr/lib/python2.7/site-packages/ipaserver/install/plugins/upload_cacr`
- 修正項目
  - 原程式：`trust_flags.has_key`
  - `trust_flags`可能是個class或者是tuple，如果是class，其中的`has_key`屬性，其實就是第1個引數的名稱(一個boolean)，
  - 現在的python不會這樣解讀了。

## Terminology

### FQDN

FQDN 代表「Fully Qualified Domain Name」，完全合格的域名。這是一個完整的、精確描述特定位置的域名。FQDN 包括主機名（hostname）和域名（domain name）的全部組成部分。

一個標準的 FQDN 的結構如下：

```
hostname.domain.top-level-domain
```

- `hostname`: 主機名，代表特定的主機或設備。
- `domain`: 域名，代表特定的網域。
- `top-level-domain`: 最頂層的域，通常是國家代碼或通用頂級域（如 .com、.org）。

例如，`www.example.com` 是一個 FQDN，其中：
- `www` 是主機名。
- `example` 是域名。
- `.com` 是頂級域。

FQDN 的主要作用是唯一地標識網際網路上的特定主機。這在網路通信、DNS 解析和許多其他網路相關的應用中都是重要的。

