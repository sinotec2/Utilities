---
layout: default
title:  Local DNS Conflicts
parent: Internal DNS
grand_parent: Web Jokers
last_modified_date: 2024-01-19 13:47:15
tags: SecAndAuth 
---

# 本地DNS可能的衝突
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



### 內部與外部的衝突

### 內外DNS重複設定問題

確保你的本地 DNS 伺服器配置正確，僅在區域網路中提供服務，對外部網域不造成影響。檢查路由器或網路設定，防止本機 DNS 伺服器向外部公開，確保僅為區域網路提供服務。

若要使用自建的本機 DNS 伺服器，需將裝置或網路設定中的 DNS 更改為本機 DNS 伺服器的 IP 位址，確保網域解析透過自建的 DNS 伺服器進行。

使用公共 DNS 服務時，需將 DNS 設定更改為本地 DNS 伺服器的 IP 位址，以充分利用自建的 DNS 服務。藉此可在本地自訂網域解析，但需注意本機 DNS 伺服器配置或記錄不足可能導致解析失敗。

若在網路設定中將 DNS 變更為本機 DNS 伺服器的 IP 位址，而該伺服器無相應 DNS 解析規則，裝置可能無法正常存取互聯網。解決方法是在本機 DNS 伺服器配置中新增上游 DNS 伺服器，將未知的網域請求轉送給公共 DNS 伺服器，確保同時提供自訂解析和正常的網際網路存取。

透過在本機 DNS 伺服器的設定檔中新增上游 DNS 伺服器的 IP 位址，如下所示：
```
forwarders {
     8.8.8.8; // 可新增其他上游 DNS 伺服器的 IP 位址
};
```
確保本機 DNS 伺服器能夠在無法解析自訂網域名稱時轉送請求給公用 DNS 伺服器，保障裝置正常存取網際網路。


### 內部DNS是否造成衝突

在一個公司內部擁有多個內部 DNS 伺服器通常是正常的，但要確保這些伺服器能夠協同工作而不引起衝突。以下是一些建議：

1. **區域劃分：** 將公司內部的網路劃分為不同的區域，並確保每個內部 DNS 伺服器只負責特定區域的解析。這樣可以避免衝突和混亂。

2. **域名空間管理：** 在不同的 DNS 伺服器之間進行域名空間的管理，確保每個伺服器擁有獨立的區域和主機名管理。避免重複的主機名和域名。

3. **DNS Forwarding：** 如果有多個 DNS 伺服器，可以配置其中一些伺服器作為其他伺服器的轉發器。這樣，其中一個伺服器可以處理外部查詢，而其他伺服器只需要處理內部查詢。

4. **同步設定：** 如果有多個 DNS 伺服器，確保它們之間的設定和資料同步。這樣可以確保一致性，避免查詢時的不一致情況。

5. **DNS 層級的安全性：** 考慮實施 DNSSEC（DNS Security Extensions）等安全機制，以確保 DNS 查詢的安全性。

綜上所述，通常情況下，多個內部 DNS 伺服器是可以共存的，但需要進行良好的管理和配置，以確保整體的 DNS 系統正確運作。

### FreeIPA server vs network-scripts 

FreeIPA（Free Identity, Policy and Audit）是一個整合性的身分識別管理解決方案，它包含了許多不同的元件，包括 LDAP、Kerberos、DNS 等。它不僅僅是 DNS 或網路配置管理的工具。

在CentOS系統上，`/etc/sysconfig/network-scripts/` 目錄通常用於配置網路介面的相關設定，如IP地址、網路協議等。但是FreeIPA作為身分識別管理的工具，主要關注在身分識別、授權和審計等方面，並且不直接影響CentOS網路設定的目錄。

在啟用FreeIPA伺服器之後，網路配置通常仍然由CentOS的標準網路設定工具來管理。FreeIPA的設定通常是透過自身的管理界面或命令行工具進行的，而不是直接透過 `/etc/sysconfig/network-scripts/` 目錄。

因此，FreeIPA的上線不會直接影響CentOS標準網路配置目錄下的檔案，除非你在FreeIPA的設定中有明確的配置指示需要改變網路設定。
