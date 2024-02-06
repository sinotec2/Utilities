---
layout: default
title:  Local DNS Settings
parent: Internal DNS
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

