---
layout: default
title:  LDAP登入Apache2.4代理網頁
parent: LDAP
grand_parent: Security And Authentication
last_modified_date: 2024-02-15 14:52:16
tags: LDAP gitea
---

#  LDAP登入Apache2.4代理網頁
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

- [Apache with LDAP authentication by Oriol Tauleria(2020)](https://medium.com/@uri.tau/apache-and-ldap-cc7bff1f629d)
  - 這一篇應該指得只有LDAP驗證與授權，而不是整個IPA，據[稱](https://serverfault.com/questions/746478/how-to-install-freeipa-server-with-apache-ssl-tls-virtualhosts-already-present)Apache ssl/tsl服務與FreeIPA是相衝突的。
  - 意思應該指的是遠端Apache的ssl.conf是沒有必要、只要有ldap.conf。
- [官網](https://httpd.apache.org/docs/2.4/mod/mod_authnz_ldap.html)
- [Enterprise Linux 實戰講座:利用 LDAP 整合 Apache 網頁驗證林彥明2006](https://linux.vbird.org/somepaper/20060111-ldap_and_apach_auth.pdf)

![](https://miro.medium.com/v2/resize:fit:720/format:webp/1*_9Z7CCn7tHvyRRpe4I0ysA.png)

### GPT 看法

設定Apache來代理具有LDAP驗證的網頁是一種常見的用例，尤其在需要集中驗證和訪問控制的企業環境中。一些與此設置相關的常見討論和挑戰包括：

1. **集中驗證：**
   LDAP驗證允許組織將用戶驗證集中管理。用戶可以使用他們的LDAP憑據訪問各種服務，增強安全性並減少單獨登錄憑據的需求。

2. **訪問控制：**
   LDAP與Apache的整合實現了細粒度的訪問控制。管理員可以根據LDAP用戶屬性、組成員身份或其他標準定義訪問策略，確保只有授權用戶可以訪問特定資源。

3. **單點登錄（SSO）：**
   實現SSO通常是這種設置中的討論點。用戶使用他們的LDAP憑據驗證一次，然後無需再次登錄即可訪問多個服務。這提升了用戶體驗並簡化了管理。

4. **LDAP組映射：**
   LDAP組映射到Apache訪問控制指令的話題很常見。它允許管理員基於LDAP組成員身份靈活動態地控制訪問管理。

5. **SSL/TLS安全性：**
   討論通常圍繞著確保Apache和LDAP服務器之間通信的安全性。確保SSL/TLS加密對於在傳輸過程中保護敏感的驗證信息至關重要。

6. **LDAP連接問題的故障排除：**
   設置LDAP連接有時可能具有挑戰性。討論可能集中在排除常見連接問題上，確保Apache能夠正確地與LDAP服務器通信。

7. **用戶和組同步：**
   確保用戶和組信息在LDAP目錄和Apache之間同步是重要的。討論可能涉及自動同步和更新用戶/組數據的機制。

8. **錯誤處理和日誌記錄：**
   配置正確的錯誤處理和記錄是關鍵的考慮因素。這有助於診斷問題、監視驗證嘗試，確保系統安全且維護良好。

9. **性能注意事項：**
   根據部署的規模，可能會涉及性能討論。對LDAP查詢進行優化、緩存策略和負載平衡可能對大型部署很重要。

10. **Web應用程序集成：**
    討論可能涉及將LDAP驗證與特定Web應用程序（例如CMS、論壇）集成。這涉及了解Web應用程序如何與Apache和LDAP進行用戶身份驗證。

11. **LDAP服務器冗餘性：**
    討論可能涉及確保LDAP服務器冗餘性和故障轉移機制，以防止LDAP服務器故障造成的中斷。

通過解決這些方面，組織可以建立一個強大且安全的LDAP驗證設置，為集中訪問控制和用戶管理打下基礎。

## shake hand with Apache

### mod_nss_to_mod_ssl

官網[這份文件](https://www.freeipa.org/page/V4/mod_nss_to_mod_ssl)提到了在Apache中使用`mod_ssl` 取代 `mod_nss` 的計畫，這是一項遠離使用NSS（Network Security Services）並轉向使用OpenSSL的大型改動的一部分。目標Fedora版本是Fedora 28。

**用途：**
- `mod_ssl` 是普遍使用的。
- `mod_ssl` 使用平整的PEM文件而不是一組複雜的工具來操作證書數據庫。

**設計：**
- `mod_nss` 的證書數據庫深度整合到IPA中，是RA代理證書和CA鏈的來源。
- 在新安裝中，會生成證書/密鑰文件，跟蹤並取消跟蹤證書，安裝CA證書，驗證服務器證書及其鏈，更改ssl.conf指令，處理PKCS＃12的安裝。
- 在升級現有安裝中，任何修改`nss.conf`的用戶可能會使升級變得脆弱。
- 在升級過程中，可能需要刪除`/etc/httpd/alias`中的Server-Cert，以避免混淆。

**實施：**
- 依賴於更新的`certmonger`。
- 在升級失敗的情況下，將需要手動指導用戶進行轉換為`mod_ssl`數據庫所需的更改。

**特性管理：**
- 無界面(UI)和命令行(CLI)的特性變更。
  
**配置：**
- 替換一些`NSS`相關的配置，並刪除不再需要的配置。
  
**使用方式：**
- 對於一般用戶來說，這個過渡應該是透明的，但在定制`nss.conf`的情況下，需要將其遷移到`ssl.conf`。
  
**測試計劃：**
- 需要測試不同情境，包括新安裝、升級、創建副本、替換證書和更新。
  
**KRA（Key Recovery Authority）：**
- 需要測試基本的保險庫操作，包括REST操作。
  
**卸載：**
- 在卸載時，應該能夠恢復相應的配置文件和刪除Apache證書和密鑰。

總體而言，這是一項從NSS到OpenSSL的轉換計劃，其中包括新安裝、升級、替換、更新和卸載等各種情境的測試和操作。

### Apache使用SNI實現基於名稱的SSL虛擬主機與Kerberos登錄

- 官網文件[Apache_SNI_With_Kerberos](https://www.freeipa.org/page/Apache_SNI_With_Kerberos)

**簡介：**
Apache 2.2.12引入了SNI（Server Name Indication）到mod_ssl的TLS支持中，而RHEL6則引入了2.2.15，其中包含了這項技術。這使得多個站點能夠使用單個IP，每個站點都有自己的證書，基本上是基於名稱的SSL虛擬主機。

**注意事項：**
- SNI的可行性取決於客戶端和服務器端，並且具有一些限制。
- 由於這需要初始請求中的主機標頭，因此它對封包檢查和記錄是開放的，不同於傳統SSL。

**IPA/SSSD配置：**
SSSD不需要任何特殊配置，但是如果`ipa-getcert list`顯示任何錯誤，如`CA_UNREACHABLE`，當拓撲中有多個副本時，值得檢查`/etc/ipa/default.conf`，確保服務器正在使用IPA拓撲進行證書請求。

**Apache配置：**
1. 初始SSL Apache配置：
    - 添加IPA服務：`ipa service-add HTTP/`
    - 安裝必需的軟件：`yum install httpd mod_ssl`
    - 創建證書存儲目錄：`mkdir /etc/httpd/certs`
    - 允許Certmonger寫入目錄：`semanage fcontext -a -t cert_t ‘/etc/httpd/certs(/.*)?’ && restorecon -v /etc/httpd/certs`
    - 通過Certmonger請求證書/密鑰對：`ipa-getcert request -r -f /etc/httpd/certs/default.crt -k /etc/httpd/certs/default.key -N CN=uname -n -D uname -n -K HTTP/uname -n`

2. 添加基於名稱的虛擬站點：
    - 在IPA中添加虛擬主機：`ipa dnsrecord-add example.com dummyhost --a-rec=10.180.80.1`
    - 添加虛擬主機並管理它：`ipa host-add dummyhost.example.com --desc="Dummy Host" --location=" " && ipa host-add-managedby dummyhost.example.com --hosts=" "`
    - 添加IPA服務和主機：`ipa service-add HTTP/dummyhost.example.com && ipa service-add-host HTTP/dummyhost.example.com --hosts=" "`
    - 通過Certmonger請求虛擬主機的證書/密鑰對：`ipa-getcert request -r -f /etc/httpd/certs/dummyhost.crt -k /etc/httpd/certs/dummyhost.key -N CN=dummyhost.example.com -D dummyhost.example.com -K HTTP/dummyhost.example.com`
    - 配置Apache以使用名稱為基礎的虛擬主機：修改`/etc/httpd/conf.d/ssl.conf`

3. 添加Kerberos身份驗證：
    - 安裝mod_auth_kerb模塊：`yum install mod_auth_kerb`
    - 創建存儲Keytab的目錄：`mkdir /etc/httpd/keytabs`，允許Certmonger寫入目錄：`semanage fcontext -a -t httpd_keytab_t '/etc/httpd/keytabs/(.*)?'`
    - 獲取默認Keytab：`ipa-getkeytab -s -p HTTP/uname -n -k /etc/httpd/keytabs/default`
    - 獲取虛擬主機特定的Keytab：`ipa-getkeytab -s -p HTTP/dummyhost.example.com -k /etc/httpd/keytabs/dummyhost`
    - 配置Apache以使用Kerberos身份驗證：修改`/etc/httpd/conf.d/ssl.conf`

**結論：**
如果按照上述步驟進行配置，並且一切正常運行，那麼服務器應該已經配置好，可以輕鬆添加新的虛擬主機，每個主機都有自己的SSL證書（通過Certmonger跟踪和更新），並且在標準RHEL6安裝中，除了標準RHEL存儲庫之外，IPA基礎結構用於所有身份驗證。