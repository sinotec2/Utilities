---
layout: default
title:  LDAP
parent: Security And Authentication
grand_parent: Web Jokers
last_modified_date: 2024-01-19 13:47:15
tags: SecAndAuth 
---

# LDAP
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

### AD vs LDAP

活動目錄Active Directory (AD) 和輕量級目錄訪問協定LDAP (Lightweight Directory Access Protocol) 是兩個用於身份驗證和帳戶管理的不同概念。以下是對比它們的一些主要特點：

**Active Directory (AD):**

1. **概念：** AD 是由 Microsoft 開發的目錄服務，提供了一個集中式的帳戶管理和身份驗證系統。
   
2. **使用場域：** 主要用於 Windows 環境，特別是企業中使用 Windows Server 的情況。AD 還包括其他功能，如群組政策、DNS 管理等。

3. **整合性：** AD 通常與其他 Microsoft 產品和服務（如 Exchange、SharePoint 等）集成得更緊密。

4. **安全性：** 提供高度的安全性，支持 Kerberos 協議，並有豐富的安全功能，如密碼政策、帳戶鎖定等。

5. **管理工具：** 使用者和資源的管理通常透過 Windows Server 上的 Active Directory Users and Computers 工具進行。

**LDAP (Lightweight Directory Access Protocol):**

1. **概念：** LDAP 是一個開放標準的通訊協議，用於訪問和維護分散式目錄信息服務。

2. **使用場域：** LDAP 是跨平台的，可用於各種操作系統和應用程式，並且不僅限於 Windows 環境。常見於企業、學術機構和網際網路應用。

3. **整合性：** LDAP 是一個通用協議，可以與多種應用程式和服務集成，包括電子郵件、網路服務、VPN 等。

4. **安全性：** 提供基本的安全性，可以透過 SSL/TLS 進行加密，但相對於 AD，可能需要額外的配置和擴充。

5. **管理工具：** LDAP 沒有固定的管理工具，管理通常透過 LDAP 客戶端工具、Web 管理介面或自定義程式實現。

**應用場域時機選擇：**

- **選擇 AD：** 在 Windows 環境中，特別是當組織使用 Microsoft 產品時，AD 提供了更緊密的整合和管理功能。

- **選擇 LDAP：** 當需要跨平台支持，或者在非 Windows 環境中運行的情況下，LDAP 提供了更靈活的選擇。

總體而言，AD 和 LDAP 都有其優勢和適用場景，選擇取決於組織的需求、環境和技術堆棧。

LDAP有可能讓使用者自行登記其個資、由程式判斷應賦予什麼樣的角色權限，而不是人工進行審查管理嗎？

## 注意事項

是的，LDAP 可以被設計為允許使用者自助註冊和管理其個人資料，同時由程式進行角色和權限的判斷。 這通常涉及到自服務入口網站和自動化的身份管理流程。

在這種情況下，LDAP 目錄可能會提供以下功能：

1. **自服務入口網站：** 提供使用者介面，允許使用者自行註冊、更新和管理其個人資訊。 這可以包括基本的個人資訊、密碼重設、安全問題答案等。

2. **自動化身分識別管理流程：** 使用工作流程或規則引擎，對使用者進行身份驗證和授權的自動管理。 這可以包括根據使用者提供的資訊自動分配角色和權限。

3. **存取控制：** 使用適當的存取控制清單（ACLs）和策略，確保使用者只能存取他們有權存取的資訊和資源。

4. **稽核和日誌：** 記錄使用者的註冊、更新和角色/權限變更等活動，以便進行稽核和合規性檢查。

需要確保實施這樣的系統時要考慮到安全性和合規性要求，以防止濫用和確保用戶資料的隱私保護。 同時，應設立適當的機制來檢測和防範潛在的濫用行為。

## 方案

### Linux方案

是的，有一些開源的身份管理解決方案可以與LDAP結合使用，提供自助服務入口網站和自動化身分管理。 以下是一些常見的開源身分管理解決方案：

1. **FreeIPA:**
    - **官方網站：** [FreeIPA](https://www.freeipa.org/)
    - **描述：** FreeIPA 是一個整合了 LDAP 目錄服務、Kerberos 認證和 DNS 的身份管理解決方案。 它提供了 Web 介面，使用戶能夠自行管理密碼、SSH 金鑰等。
    - [demo](https://ipa.demo1.freeipa.org/ipa/ui/)

2. **FusionDirectory:**
    - **官方網站：** [FusionDirectory](https://www.fusiondirectory.org/)
    - **描述：** FusionDirectory 是一個基於 PHP 的系統管理解決方案，它使用 LDAP 作為後端。 它提供了 Web 介面，用於使用者和組織的管理。

3. **Keycloak:**
    - **官方網站：** [Keycloak](https://www.keycloak.org/)
    - **描述：** Keycloak 是一個開源的身份和存取管理解決方案，支援 OpenID Connect、OAuth 2.0 等協定。 它可以與 LDAP 集成，提供單一登入（SSO）和身份驗證服務。

4. **LemonLDAP::NG:**
    - **官方網站：** [LemonLDAP::NG](https://lemonldap-ng.org/welcome)
    - **描述：** LemonLDAP::NG 是一個 Web 單一登入解決方案，支援多種驗證後端，包括 LDAP。 它還提供了一些自助服務入口網站功能。

這些解決方案都提供了強大的功能，可以與 LDAP 集成，支援使用者自助服務、自動化身分管理和存取控制。 在選擇解決方案時，請根據您的特定需求和環境來做出合適的選擇。

### macOS方案

這些開源身分管理解決方案主要設計用於 Linux 等作業系統，其中一些可能需要特定的程式庫或依賴項，可能需要適應 macOS 環境。 在 macOS 上建立完整的身份管理系統可能會有一些挑戰。

如果你在 macOS 上尋找身分管理的解決方案，你可能需要考慮以下幾點：

1. **Directory Utility:**
    - macOS 自帶的 Directory Utility 提供了一些基本的 LDAP 設定和管理功能。 你可以在系統偏好設定的「使用者與群組」部分找到 Directory Utility。

2. **OpenLDAP:**
    - OpenLDAP 是一款開源的 LDAP 實現，可在 macOS 上安裝和運行。 你可以使用 Homebrew 或其他套件管理工具安裝。

3. **Keycloak:**
    - Keycloak 是一個獨立的身份和存取管理解決方案，支援多種平台。 你可以在 macOS 上安裝 Keycloak 並與其他系統整合。

請注意，macOS 並不是專門設計用於建立企業級身分識別管理解決方案的作業系統。 因此，對於生產環境，可能需要考慮使用專為此設計的作業系統，例如 Linux。 在 macOS 上建構身分識別管理系統時，可能需要適應性更強的配置和管理。

## LDAP的應用

### Gitea

是的，Gitea 支持使用 LDAP 進行登入。LDAP（Lightweight Directory Access Protocol）是一種用於存儲和檢索目錄信息的協定，它通常用於集中式身份驗證和授權管理。

以下是在 Gitea 中配置 LDAP 登入的一般步驟：

1. 登入 Gitea：使用管理員帳戶登入到 Gitea。

2. 轉到 "Site Administration"：點擊右上角的管理員頭像，然後選擇 "Site Administration"。

3. 進入 "Authentication" 設置：在左側的選單中，找到 "Authentication" 選項，然後選擇 "Authentication Sources"。

4. 新增 LDAP 身份驗證源：點擊 "New Authentication Source" 按鈕，然後選擇 "LDAP" 作為身份驗證類型。

5. 配置 LDAP 連接：填寫所需的 LDAP 連接信息，包括主機、端口、基本 DN（Distinguished Name）等。

6. 測試連接：通常，您可以使用 "Test Connection" 按鈕來測試 LDAP 連接是否正常。

7. 設置用戶名屬性：根據您的 LDAP 設置，請確保正確設置用戶名屬性，例如 "uid" 或 "sAMAccountName"。

8. 完成配置：完成所有必要的配置後，點擊 "Submit" 或 "Save" 以應用變更。

以上僅為一般步驟，實際操作可能因 Gitea 版本而異。建議參考 Gitea 的官方文檔或相應版本的管理介面以進行準確的配置。

### mail2000

根據[Mail2000 V7 使用者手冊](http://manual.openfind.com.tw/m2kv7/sp1/tw/index.html)，**Mail2000** 可以接受 **LDAP** 認證。以下是設定步驟：

1. 確認底層 **LDAP pam conf** 設定完成：
    - 編輯 `/webmail/etc/daemon_pam.conf`，新增以下行：
        ```
        Module = pam auth sufficient 2 /webmail/pam_modules/pam_ldap.so SELF SET_COOKIE|UPD_LOC_PASS
        ```
    - 重新啟動 **Mail2000** 服務：
        ```
        /webmail/tools/restartshm
        /webmail/tools/reloadini
        ```

2. 進入 **Mail2000** 管理者介面：
    - 開啟 **LDAP 登入驗證**：
        - 選擇 **[開啟]**。
    - 填寫基本組態驗證設定：
        - **Base LDAP 資料搜尋起點**：指定 **RDN**。
        - **LDAP 資料主機**：填入 **Root DN** 的相關資訊。
        - **Password**：填入 **Root DN** 的密碼。
        - **Host**：填入 **LDAP** 資料主機名稱，例如 `ldap.openfind.com.tw` 或 `127.0.0.1`。您也可以設定多台 **LDAP** 伺服器，用逗號隔開。
        - **Port**：填入 **LDAP** 資料主機的連接埠。
        - **TLS 安全性傳輸設定**：如果使用 **TLS**，請設定相應的連接埠（例如：636）。

3. 進階組態驗證設定：
    - 設定取得帳號 **DN** 和帳號 **ID** 的過濾條件和資料欄位。

4. 設定完成後，點選 **[確定]** 儲存設定值，並點選旁邊的 **[測試]** 以驗證設定是否正確。

如果設定值正確，您將看到 **"測試成功"** 的訊息。¹²

來源: 與 Bing 的交談， 2024/2/4

- (1) Mail2000 [模組] LDAP 登入驗證設定 – [Openfind](https://openfind.zendesk.com/hc/zh-tw/articles/5337299077775-Mail2000-%E6%A8%A1%E7%B5%84-LDAP-%E7%99%BB%E5%85%A5%E9%A9%97%E8%AD%89%E8%A8%AD%E5%AE%9A).
- (2) LDAP 設定說明 - MailGates 管理者手冊 - [Chung Yuan Christian University](https://mailspam.cycu.edu.tw/mg/help/tw/adm/ldap.htm).
- (3) [Mail2000電子信箱_常見問題](http://doc.mail2000.com.tw/m2k/faq_sign-up_a2-3.htm).
- (4) Mail2000 FAQ - Openfind [網擎資訊](https://www.openfind.com.tw/taiwan///products/dl/mail2000/Mail2000_FAQ.pdf).

根據[Mail2000 V7 使用者手冊](http://manual.openfind.com.tw/m2kv7/sp1/tw/index.html)，**Mail2000** 可以同時接受 **LDAP** 認證和其內部設定的帳號密碼管理系統。以下是設定步驟：

1. 確認底層 **LDAP pam conf** 設定完成：
    - 編輯 `/webmail/etc/daemon_pam.conf`，新增以下行：
        ```
        Module = pam auth sufficient 2 /webmail/pam_modules/pam_ldap.so SELF SET_COOKIE|UPD_LOC_PASS
        ```
    - 重新啟動 **Mail2000** 服務：
        ```
        /webmail/tools/restartshm
        /webmail/tools/reloadini
        ```

2. 進入 **Mail2000** 管理者介面：
    - 開啟 **LDAP 登入驗證**：
        - 選擇 **[開啟]**。
    - 填寫基本組態驗證設定：
        - **Base LDAP 資料搜尋起點**：指定 **RDN**。
        - **LDAP 資料主機**：填入 **Root DN** 的相關資訊。
        - **Password**：填入 **Root DN** 的密碼。
        - **Host**：填入 **LDAP** 資料主機名稱，例如 `ldap.openfind.com.tw` 或 `127.0.0.1`。您也可以設定多台 **LDAP** 伺服器，用逗號隔開。
        - **Port**：填入 **LDAP** 資料主機的連接埠。
        - **TLS 安全性傳輸設定**：如果使用 **TLS**，請設定相應的連接埠（例如：636）。

3. 進階組態驗證設定：
    - 設定取得帳號 **DN** 和帳號 **ID** 的過濾條件和資料欄位。

4. 設定完成後，點選 **[確定]** 儲存設定值，並點選旁邊的 **[測試]** 以驗證設定是否正確。

如果設定值正確，您將看到 **"測試成功"** 的訊息。¹²

來源: 與 Bing 的交談， 2024/2/4

- (1) Mail2000 [模組] LDAP 登入驗證設定 – [Openfind](https://openfind.zendesk.com/hc/zh-tw/articles/5337299077775-Mail2000-%E6%A8%A1%E7%B5%84-LDAP-%E7%99%BB%E5%85%A5%E9%A9%97%E8%AD%89%E8%A8%AD%E5%AE%9A).
- (2) LDAP 設定說明 - MailGates 管理者手冊 - [Chung Yuan Christian University](https://mailspam.cycu.edu.tw/mg/help/tw/adm/ldap.htm).
- (3) Mail2000電子信箱_[常見問題](http://doc.mail2000.com.tw/m2k/faq_sign-up_a2-3.htm).
- (4) Mail2000 FAQ - [Openfind 網擎資訊](https://www.openfind.com.tw/taiwan///products/dl/mail2000/Mail2000_FAQ.pdf).
- (5) Mail2000 V7 使用者手冊 - Openfind [網擎資訊](http://manual.openfind.com.tw/m2kv7/sp1/tw/index.html).
- (6) Mail2000 電子信箱：個人信箱常見問題 ─ [密碼問題](https://doc.mail2000.com.tw/m2k_faq_sign-up1.html).
- (7) 2014 年 9 月：MailCloud雙重認證—為你的帳號多加一道鎖 - [MailCloud 企業雲端服務](https://www.mailcloud.com.tw/htm/EDM/1409/index.html).
- (8) Mail2000 常見問題. https://www.mail2000.com.tw/faq.htm.
- (9) Mail2000可警示異常登入，強化密碼修改與自動轉寄保護, [iThome](https://bing.com/search?q=Mail2000+%e9%9b%bb%e9%83%b5%e4%bc%ba%e6%9c%8d%e5%99%a8+LDAP+%e6%94%af%e6%8f%b4).
- (10) Mail2000可警示異常登入，強化密碼修改與自動轉寄保護, [iThome](https://www.ithome.com.tw/review/89957).
- (11) Mail2000 線上說明系統 - [Openfind Mail2000 電子信箱](https://www.mail2000.com.tw/help/index.html?e2-5).
- (12) 如何使用郵件軟體收取信件？ - [Openfind Mail2000 電子信箱](http://www.mail2000.com.tw/help/2-5.htm).
- (13) Mail2000電子信箱—[行動裝置設定資訊](https://www.mail2000.com.tw/rev9/mobile.html).
- (14) Mail2000 電子信箱：[手機收信特色功能](https://doc.mail2000.com.tw/intro_mobile_faq02.html).
- (15) [undefined]((http://mail2000.com.tw).

## 外部使用

將 LDAP 用於外部登入可以提供額外的安全性，但在將內部 Druid 伺服器暴露給外部時，需要特別注意安全性問題。以下是一些建議的做法：

1. **使用 SSL/TLS 加密：** 確保外部登入和 Druid 伺服器之間的通信是加密的，這可以通過配置 SSL/TLS 來實現。

2. **適當的權限控制：** 在 LDAP 中配置適當的權限，確保只有授權的用戶可以訪問 Druid 伺服器。這有助於減少潛在的安全風險。

3. **雙因素身份驗證 (2FA)：** 對於外部登入，實施雙因素身份驗證，這可以提高安全性，即便帳戶密碼被猜測或洩漏，仍需要額外的驗證步驟。

4. **IP 點對點存取控制：** 考慮實施 IP 點對點存取控制，僅允許來自特定 IP 範圍的用戶訪問 Druid 伺服器。

5. **監控和日誌：** 實施監控機制和日誌記錄，以便能夠追蹤和檢視外部登入的活動，並及時響應可能的安全事件。

6. **定期安全審查：** 定期進行安全性審查，檢查配置、權限、日誌和監控，以確保 Druid 伺服器的安全性。

7. **保持更新：** 確保 Druid 伺服器和相關的軟體都是最新版本，並應用任何安全性修補程序。

8. **防火牆設置：** 在防火牆上設置適當的規則，僅允許必要的通信流量進入和離開 Druid 伺服器。

以上建議是為了加強外部登入的安全性，同時確保內部 Druid 伺服器的安全性。請注意，實施這些安全措施需要仔細計劃，根據實際情況進行調整。

[realm]: <> "`Realm` 這個英文詞在中文中可以翻譯為「領域」、「領土」、「範圍」等，具體的翻譯可能取決於上下文和使用的領域。在不同的上下文中，`realm` 可以有不同的含義：
1. **網路安全和身份驗證：** 在網路安全領域，`realm` 常用來表示一個身份驗證或授權的區域或範圍。例如，某個網站可能有不同的 `realms`，每個 `realm` 代表一個獨立的身份驗證區域，用戶需要在進入不同的 `realm` 時提供相應的憑證。
2. **遊戲：** 在遊戲中，`realm` 可能指的是遊戲中的一個虛構世界、區域或伺服器。例如，在多人線上遊戲中，不同的 `realms` 可能代表不同的遊戲伺服器，玩家可以在這些伺服器中選擇進行遊戲。
3. **神話和文學：** 在文學和神話中，`realm` 可以指的是一個王國、領域或領土，常用於描述特定的區域或國度。
總的來說，`realm` 是一個相對通用的詞彙，其含義可能因上下文而異。在科技和網路領域，它通常與身份驗證、安全性或虛擬空間有關。"