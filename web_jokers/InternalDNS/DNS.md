---
layout: default
title:  Local DNS Settings
parent: Security And Authentication
grand_parent: Web Jokers
last_modified_date: 2024-01-19 13:47:15
tags: SecAndAuth 
---

# 本地DNS的設置
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


## 本地DNS伺服器

在 Linux 平台上建立本機 DNS 伺服器通常涉及使用一些特定的軟體，如 BIND（Berkeley Internet Name Domain）等。 以下是一些步驟，你可以參考這些步驟在 Linux 上建立本機 DNS 伺服器：

1. **安裝 BIND:**
    - 使用你 Linux 發行版的套件管理器安裝 BIND。 在大多數發行版中，你可以使用以下指令：
      『`bash
      sudo apt-get update
      sudo apt-get install bind9 # 對於 Debian/Ubuntu
      ```

2. **配置 BIND:**
    - BIND 的設定檔通常位於 `/etc/bind/named.conf` 或類似的位置。 你需要編輯這個文件，配置網域解析的相關資訊。

3. **定義區域檔案:**
    - 在 BIND 的設定中，你需要定義區域文件，這些文件包含了 DNS 記錄。 通常，這些檔案位於 `/etc/bind` 目錄下。 你需要至少定義一個正向區域（用於 IP 位址到網域名稱的解析）和一個反向區域（用於網域名稱到 IP 位址的解析）。

4. **啟動 BIND 服務:**
    - 一旦 BIND 設定完成，你可以啟動 BIND 服務。 在大多數系統上，你可以使用以下命令：
      『`bash
      sudo service bind9 start # 對於 Debian/Ubuntu
      ```

5. **設定本地 DNS:**
    - 在你的電腦上，你需要設定本機 DNS 伺服器為你剛剛設定的 BIND 伺服器。 這可以透過編輯 `/etc/resolv.conf` 檔案來實現。

6. **測試:**
    - 使用 `nslookup` 或 `dig` 等工具測試你的本機 DNS 伺服器是否能夠正確解析網域名稱。

這只是一個基本的步驟概述，具體的步驟可能會因你所使用的 Linux 發行版和 BIND 版本而有所不同。 確保查看 BIND 的文檔以取得更詳細的指南。

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
