---
layout: default
title:  MFA
parent: web filebrowser
grand_parent: Web Jokers
nav_order: 99
last_modified_date: 2025-02-14 08:32:07
tags: web
---

#  windows 系統的tls 憑證
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


> 怎麼樣的系統適合使用MFA？

多因素驗證（MFA, Multi-Factor Authentication）適合 需要高安全性 的系統，尤其是：

1. 涉及機敏資訊的系統
	•	政府與軍事系統（如國防、國安機關）
	•	醫療系統（如醫院電子病歷 EHR、健保系統）
	•	金融系統（如銀行、證券交易、加密貨幣交易所）
	•	企業內部系統（如 ERP、HR、人資系統）
	•	學術與研究機構（有機密研究數據的機構）

➡ 原因：這些系統存放大量機敏資訊，密碼洩漏可能導致重大損失。

2. 涉及遠端存取的系統
	•	VPN（虛擬私人網路）
	•	遠端桌面（RDP）與 SSH 伺服器
	•	雲端管理平台（AWS, Azure, GCP）
	•	DevOps 工具（如 GitHub, GitLab, Jenkins）
	•	客戶支援系統（如客服後台、CRM）

➡ 原因：這些系統可以從外部網路存取，密碼容易被攻擊，MFA 提供額外保護。

3. 公開或高風險的網路服務
	•	電子郵件服務（如 Gmail, Outlook, 企業郵件伺服器）
	•	社群平台（如 Facebook, LinkedIn, Twitter, Instagram）
	•	線上支付系統（如 PayPal, Apple Pay, Google Pay）
	•	線上學習平台（如 Coursera, Udemy, Moodle）
	•	內容管理系統（如 WordPress, Joomla, Drupal）

➡ 原因：這些服務經常受到釣魚攻擊與憑證洩露的威脅，MFA 可降低風險。

4. 企業內部的身份與存取管理（IAM）
	•	Active Directory（AD）與 FreeIPA
	•	身份提供者（如 Keycloak, Okta, Auth0, Azure AD）
	•	企業 SSO（Single Sign-On）
	•	開發者 API 與 Web 服務

➡ 原因：這些系統管理大量使用者帳號，MFA 可防止憑證洩露影響整個企業網路。

總結：哪些系統最適合用 MFA？

✅ 必須使用 MFA
✔ 遠端存取（VPN、SSH、RDP）
✔ 金融、政府、醫療等高機密系統
✔ 公開網路可存取的重要帳號（郵件、社群、雲端管理）
✔ 開發與 DevOps 相關帳號（GitHub, AWS, GitLab）

⚠ 建議使用 MFA
✔ 一般企業內部系統（ERP, HR, SSO）
✔ 內部開發與測試環境
✔ 需要合規要求（GDPR, HIPAA, PCI-DSS）的系統

❌ 可以不強制 MFA，但需加強密碼策略
✖ 一般使用者的個人網站或部落格
✖ 內部封閉網路的非機密系統

如果你的系統 涉及遠端存取、機敏資料，或經常受到攻擊，那就應該啟用 MFA。

