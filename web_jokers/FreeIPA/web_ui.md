---
layout: default
title:  Web UI design
parent: FreeIPA
grand_parent: Web Jokers
last_modified_date: 2024-02-14 10:32:19
tags: FreeIPA
---

# 網頁介面設計
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

## 密碼系統

### 2FA

[manageiq：2-Factor Authentication](https://www.manageiq.org/docs/reference/latest/auth/ipa_2fa.html)

## 程式位置

  ```bash
root@node03 /etc/httpd/conf.d
# grep share *

ipa.conf:WSGIImportScript /usr/share/ipa/wsgi.py process-group=ipa application-group=ipa
ipa.conf:WSGIScriptAlias /ipa /usr/share/ipa/wsgi.py
ipa.conf:Alias /ipa/session/cookie "/usr/share/ipa/gssapi.login"
ipa.conf:Alias /ipa/errors "/usr/share/ipa/html"
ipa.conf:Alias /ipa/config "/usr/share/ipa/html"
ipa.conf:<Directory "/usr/share/ipa/html">
ipa.conf:Alias /ipa/ui/fonts/open-sans "/usr/share/fonts/open-sans"
ipa.conf:Alias /ipa/ui/fonts/fontawesome "/usr/share/fonts/fontawesome"
ipa.conf:<Directory "/usr/share/fonts">
ipa.conf:Alias /ipa/ui "/usr/share/ipa/ui"
ipa.conf:<Directory "/usr/share/ipa/ui">
ipa.conf:Alias /ipa/wsgi "/usr/share/ipa/wsgi"
ipa.conf:<Directory "/usr/share/ipa/wsgi">
ipa.conf:Alias /ipa/migration "/usr/share/ipa/migration"
ipa.conf:<Directory "/usr/share/ipa/migration">
ipa-kdc-proxy.conf:#   # ipa-ldap-updater /usr/share/ipa/kdcproxy-disable.uldif
ipa-kdc-proxy.conf:#   # ipa-ldap-updater /usr/share/ipa/kdcproxy-enable.uldif
ipa-kdc-proxy.conf:WSGIImportScript /usr/share/ipa/kdcproxy.wsgi \
ipa-kdc-proxy.conf:WSGIScriptAlias /KdcProxy /usr/share/ipa/kdcproxy.wsgi
```

## logo

`https://node03.sinotech-eng.com/ipa/ui/images/header-logo.png`
