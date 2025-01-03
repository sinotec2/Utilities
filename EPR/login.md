---
layout: default
title:  報修系統登入及管理
parent: ERPs
last_modified_date: 2025-01-02 14:32:37
tags: ERP
---

# 報修系統登入及管理

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

- Odoo是功能強大的企業資源計畫(ERP)系統平台，此次引用其保修系模組(maintenance)進行客製化，作為公司內部資訊設備報修系統的更新方案。往後還會在此平台持續開發好用的系統軟體、諸如程式學習平台、行動APP功能等等。

### 報修系統主要新增功能

- 個案進度查詢、管控
- 溝通紀錄
- 維護時間統計

### 需同仁配合事項

- 以LDAP帳號登入、鍵入問題，並且協調預期開始維修的時間。
- 修理完成後確認`完成`

## 登入系統

- 目前`odoo`沒有與AD帳號整合，而是LDAP帳密系統。

### 先修改密碼

- 使用者需先在[`FreeIPA`系統](https://node03.sinotech-eng.com/ipa/ui/)修改密碼或[免登入修改密碼](http://node03.sinotech-eng.com:5000)。先由**電子郵件名稱**（@左邊英數字串、不含伺服器網域）及**員編2次**作為密碼登入。（詳[修改LDAP密碼](https://sinotec2.github.io/Utilities/DB_servers/LDAP/FeeeIPAHandling/mod_pw/)）

![pngs/2025-01-03-17-16-05.png](pngs/2025-01-03-17-16-05.png)

- 以**電子郵件名稱**與新密碼登入系統
  - 不能出現`@mail.sinotech-eng.com`
  - 完整的電子郵件反而**無法登入**

![pngs/2025-01-03-17-24-36.png](pngs/2025-01-03-17-24-36.png)

### 不要點選旁支功能

- 此處修改密碼只限於`odoo`系統內有效，別處的LDAP應用沒有作用。
- 不要點選[還沒有帳戶]()，手動新增的帳戶**不會**自動帶入LDAP資訊：部門、員編、電子郵件、分機、職稱...，而且限制必須以**電子郵件**登入（含網域）。
- `超級使用者`指得不是`Admin`，而是`Odoo bot`。
- 管理資料庫：會需要12碼亂碼密碼與8碼`Admin`密碼。

## 新增維護請求

### 進入模組

![pngs/2025-01-03-17-25-29.png](pngs/2025-01-03-17-25-29.png)

![pngs/2025-01-03-17-26-09.png](pngs/2025-01-03-17-26-09.png)

### 新增維護請求的內容

![pngs/2025-01-03-17-26-54.png](pngs/2025-01-03-17-26-54.png)

![pngs/2025-01-03-17-29-04.png](pngs/2025-01-03-17-29-04.png)

### 請求預定日期時間

![pngs/2025-01-03-17-30-59.png](pngs/2025-01-03-17-30-59.png)

![pngs/2025-01-03-17-31-19.png](pngs/2025-01-03-17-31-19.png)
![pngs/2025-01-03-17-31-45.png](pngs/2025-01-03-17-31-45.png)

### 其他訊息

- 級別
- 文字訊息