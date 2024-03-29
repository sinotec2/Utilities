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

## 重複與衝突

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

### httpd重複啟動

FreeIPA 伺服器通常會包括 Apache HTTP Server 作為其架構的一部分，用於提供 Web 介面和其他相關服務。在大多數情況下，當您啟動 FreeIPA 伺服器時，系統應該會自動啟動 Apache HTTP Server。

您可以使用以下命令檢查 Apache HTTP Server 的狀態：

```bash
sudo systemctl status httpd
```

如果 Apache HTTP Server 已經在運行，您應該會看到類似以下的輸出：

```
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Wed 2023-01-04 15:30:00 UTC; 2min 30s ago
     Docs: man:httpd(8)
           man:apachectl(8)
 Main PID: 1234 (httpd)
   Status: "Total requests: 0; Current requests/sec: 0; Current traffic:   0 B/sec"
    Tasks: 55 (limit: 1150)
   CGroup: /system.slice/httpd.service
           ├─1234 /usr/sbin/httpd -DFOREGROUND
           ├─1235 /usr/sbin/httpd -DFOREGROUND
           ├─1236 /usr/sbin/httpd -DFOREGROUND
           └─...

```

如果看到 "Active: active (running)"，表示 Apache HTTP Server 正在運行。

如果因某種原因未自動啟動，您可以使用以下命令手動啟動 Apache：

```bash
sudo systemctl start httpd
```

確保 Apache HTTP Server 正確啟動後，您應該能夠訪問 FreeIPA Web 介面。

### SSL與TLS

是的，FreeIPA 在安裝過程中會配置和使用 SSL/TLS 以保護通信。這有助於確保在 FreeIPA 環境中的數據傳輸是安全的。

通常，FreeIPA 會使用自簽名的 SSL 憑證。這意味著您在首次連接到 FreeIPA Web 介面時，瀏覽器可能會顯示 SSL 警告，因為簽名憑證不是由廣泛受信任的證書機構（CA）簽發的。您可以選擇接受這些警告，或者如果需要更高的安全性，您可以將 FreeIPA 配置為使用由 CA 簽發的憑證。

總體而言，SSL/TLS 的使用有助於確保 FreeIPA 系統的安全通信和數據保護。

### httpd.conf

在 FreeIPA 中，`httpd.conf` 檔案通常不需要直接修改。相反，FreeIPA 使用 Apache 的配置碎片 (configuration snippets) 來管理不同的模塊和功能。

如果您需要調整 Apache 的配置，請查看 `/etc/httpd/conf.d/` 目錄，您可能會在這個目錄下找到 FreeIPA 相關的配置文件。比如，可能會有 `ipa.conf`、`ipa-pki-proxy.conf` 等。

在這些配置文件中，您可以找到有關 FreeIPA Web 介面和相關服務的 Apache 配置。請謹慎進行修改，最好在進行更改之前先備份文件。任何配置更改後，您應該重新啟動 Apache 服務以應用這些更改：

```bash
sudo systemctl restart httpd
```

總的來說，請儘量使用 FreeIPA 提供的工具和命令來管理系統，以確保一致性和兼容性。手動修改 Apache 配置時需要謹慎操作。

### 本地主從DNS

在設置多個內部 DNS 伺服器時，有一些重要的考慮事項：

1. **拓撲結構：** 確保 DNS 伺服器的拓撲結構合理。可能有主要的 DNS 伺服器和次要的 DNS 伺服器，以提高容錯性。這可以通過設置主從 DNS 配置或設置 DNS 集區實現。

2. **同步：** 確保所有 DNS 伺服器都在域名數據上保持同步。這可以使用區域傳送或 DNS 複製來實現，以便在主 DNS 伺服器上進行更改時，次要伺服器也能接收到這些更改。

3. **DNS 安全：** 考慮 DNS 安全性，例如 DNSSEC（DNS 安全擴展）。這有助於確保 DNS 數據的完整性和安全性。

4. **延遲和性能：** 考慮 DNS 查詢的延遲和性能。通過合理的拓撲和適當的伺服器配置，可以減少 DNS 查詢時間。

5. **故障恢復：** 考慮故障恢復機制，例如負載均衡和故障轉移。這有助於在某些 DNS 伺服器不可用時保持 DNS 服務的可用性。

6. **監控和日誌：** 設置監控和日誌機制，以追踪 DNS 伺服器的性能、運行狀態和可能的問題。

7. **防火牆和訪問控制：** 確保在網絡設備和伺服器上配置了正確的防火牆和訪問控制，以確保 DNS 流量得以順利傳輸。

8. **DNS 政策：** 確保制定了適當的 DNS 政策，例如訪問控制和解析規則。這有助於確保 DNS 被正確使用，同時提高安全性。

總體而言，建立多個內部 DNS 伺服器需要綜合考慮性能、安全性、可用性和容錯性等因素，以確保順利運作和滿足組織的需求。

