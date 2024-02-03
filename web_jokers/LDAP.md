

## 背景

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
(1) Mail2000 [模組] LDAP 登入驗證設定 – Openfind. https://openfind.zendesk.com/hc/zh-tw/articles/5337299077775-Mail2000-%E6%A8%A1%E7%B5%84-LDAP-%E7%99%BB%E5%85%A5%E9%A9%97%E8%AD%89%E8%A8%AD%E5%AE%9A.
(2) LDAP 設定說明 - MailGates 管理者手冊 - Chung Yuan Christian University. https://mailspam.cycu.edu.tw/mg/help/tw/adm/ldap.htm.
(3) Mail2000電子信箱_常見問題. http://doc.mail2000.com.tw/m2k/faq_sign-up_a2-3.htm.
(4) Mail2000 FAQ - Openfind 網擎資訊. https://www.openfind.com.tw/taiwan///products/dl/mail2000/Mail2000_FAQ.pdf.

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
(1) Mail2000 [模組] LDAP 登入驗證設定 – Openfind. https://openfind.zendesk.com/hc/zh-tw/articles/5337299077775-Mail2000-%E6%A8%A1%E7%B5%84-LDAP-%E7%99%BB%E5%85%A5%E9%A9%97%E8%AD%89%E8%A8%AD%E5%AE%9A.
(2) LDAP 設定說明 - MailGates 管理者手冊 - Chung Yuan Christian University. https://mailspam.cycu.edu.tw/mg/help/tw/adm/ldap.htm.
(3) Mail2000電子信箱_常見問題. http://doc.mail2000.com.tw/m2k/faq_sign-up_a2-3.htm.
(4) Mail2000 FAQ - Openfind 網擎資訊. https://www.openfind.com.tw/taiwan///products/dl/mail2000/Mail2000_FAQ.pdf.
(5) Mail2000 V7 使用者手冊 - Openfind 網擎資訊. http://manual.openfind.com.tw/m2kv7/sp1/tw/index.html.
(6) Mail2000 電子信箱：個人信箱常見問題 ─ 密碼問題. https://doc.mail2000.com.tw/m2k_faq_sign-up1.html.
(7) 2014 年 9 月：MailCloud雙重認證—為你的帳號多加一道鎖 - MailCloud 企業雲端服務. https://www.mailcloud.com.tw/htm/EDM/1409/index.html.
(8) Mail2000 常見問題. https://www.mail2000.com.tw/faq.htm.
(9) Mail2000可警示異常登入，強化密碼修改與自動轉寄保護 | iThome. https://bing.com/search?q=Mail2000+%e9%9b%bb%e9%83%b5%e4%bc%ba%e6%9c%8d%e5%99%a8+LDAP+%e6%94%af%e6%8f%b4.
(10) Mail2000可警示異常登入，強化密碼修改與自動轉寄保護 | iThome. https://www.ithome.com.tw/review/89957.
(11) Mail2000 線上說明系統 - Openfind Mail2000 電子信箱. https://www.mail2000.com.tw/help/index.html?e2-5.
(12) 如何使用郵件軟體收取信件？ - Openfind Mail2000 電子信箱. http://www.mail2000.com.tw/help/2-5.htm.
(13) Mail2000電子信箱—行動裝置設定資訊. https://www.mail2000.com.tw/rev9/mobile.html.
(14) Mail2000 電子信箱：手機收信特色功能. https://doc.mail2000.com.tw/intro_mobile_faq02.html.
(15) undefined. http://mail2000.com.tw.

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
