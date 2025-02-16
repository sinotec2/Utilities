---
layout: default
title: Keycloak 實現 MFA
parent: web filebrowser
grand_parent: Web Jokers
nav_order: 99
last_modified_date: 2025-02-13 14:40:16
tags: web
---

#   Keycloak 實現 MFA
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

> Keycloak 怎麼實現MFA?

### 可行方案

Keycloak 的多因素驗證（MFA）可以透過 Authenticator 機制來實現，支援的 MFA 方式包括：

1. OTP（一次性密碼）

- TOTP（基於時間的 OTP）：使用 Google Authenticator、Microsoft Authenticator、FreeOTP 等應用程式生成驗證碼。
- HOTP（基於計數器的 OTP）：較少使用。

2. WebAuthn（FIDO2）

- 允許使用 指紋、Windows Hello、YubiKey 等生物辨識或硬體金鑰驗證。
	
3.	 Recovery Codes（備用驗證碼）

- 使用者可以預先產生一組備用驗證碼，當其他 MFA 方式無法使用時可作為替代方案。

4.	 推播通知（需額外整合）

- Keycloak 本身沒有內建推播 MFA，但可以透過外部服務（如 Duo Security）來實現。

## 設定 Keycloak MFA

### 1. 開啟 MFA 驗證

	1.	 登入 Keycloak 管理介面。
	2.	 選擇你的 Realm（領域）。
	3. 在左側選單中點選 Authentication > Flows。
	4.	 找到 Browser 流程，點選 Actions > Copy（建立一個可編輯的流程）。
	5.	 在新建的流程中，點選 Add execution，選擇 OTP Form，然後點選 Required。

### 2. 設定 MFA 規則

	1.	 進入 Authentication > Required Actions，啟用 Configure OTP。
	2.	 進入 Authentication > OTP Policy，設定 OTP 的演算法、有效時間、碼長（通常 6 位數）等。

### 3. 測試 MFA

	1.	 使用普通帳號登入，會跳出 設定 MFA 的畫面。
	2.	 掃描 QR Code（使用 Google Authenticator 或 FreeOTP）。
	3.	 輸入 OTP 驗證碼完成設定。

之後，使用者每次登入時都需要輸入 OTP，才可完成身份驗證。

## 進階應用

- 強制特定使用者群組啟用 MFA：可以使用 條件性流程（Conditional Flow），讓特定群組（如 Admin）必須使用 MFA。
- 允許使用 WebAuthn（FIDO2）：在 Authentication Flows 新增 WebAuthn Authenticator，並啟用 WebAuthn 設定。
- 整合外部 MFA 服務（如 Duo Security）：透過 Keycloak 外掛程式來支援 Duo Push 通知驗證。

這樣，你就能在 Keycloak 上成功啟用 MFA，提升登入安全性！

