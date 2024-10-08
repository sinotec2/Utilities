---
layout: default
title:  RefDoc of calendar API
parent: Calendars
grand_parent: DB_servers
last_modified_date: 2024-08-20 10:53:12
tags: calendar
---

# RefDoc of calendar API

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

- 官網：[ref docs](https://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html)
- [quickstart.py](https://developers.google.com/calendar/api/quickstart/python?hl=zh-tw)
- 日曆整體的設定：[CalendarList](https://developers.google.com/calendar/api/v3/reference/calendarList?hl=zh-tw#methods)
- [events.insert()](https://developers.google.com/calendar/api/guides/create-events?hl=zh-tw)

## 每天自動連線

是的，OAuth 2.0 可以實現自動化登錄，而不必每天輸入密碼。這通常是通過「刷新令牌」機制來實現的。

刷新令牌 (Refresh Token)

OAuth 2.0 提供了一種稱為「刷新令牌」的機制，可以在訪問令牌（Access Token）過期後，無需再次輸入用戶名和密碼來獲取新的訪問令牌。以下是這一過程的工作原理：

1. 初次授權：
   - 用戶在第一次授權時，應用程序會獲取一個訪問令牌和一個刷新令牌。
   - 訪問令牌通常有一個較短的有效期（例如一小時），而刷新令牌的有效期較長（可以是幾天、幾個月，甚至更長）。
2. 使用訪問令牌：
   - 在訪問令牌有效期內，應用程序可以使用它來訪問受保護的資源。
3. 訪問令牌過期：
   - 當訪問令牌過期後，應用程序可以使用刷新令牌來請求新的訪問令牌，而無需用戶再次輸入用戶名和密碼。
4. 自動更新：
   - 當應用檢測到訪問令牌過期時，它會自動使用刷新令牌向 OAuth 伺服器請求一個新的訪問令牌，從而保持用戶的登錄狀態。

這種方法的好處：

- 用戶體驗：用戶不需要頻繁地輸入憑證，可以提供更流暢的用戶體驗。
- 安全性：即使訪問令牌被竊取，由於其短暫的有效期，攻擊者的使用時間有限。此外，刷新令牌通常只會在安全的後端服務器上使用，進一步減少風險。
- 自動化：可以在腳本或應用程序中實現自動化處理，無需人工干預。

使用時的注意事項：

- 安全存儲：刷新令牌應該安全地存儲在應用程序中，避免被未授權的用戶或應用程序訪問。
- 刷新頻率：不應該過於頻繁地刷新令牌，這可能會觸發 OAuth 提供者的安全警告或限制。

通過正確設置 OAuth 2.0，你可以讓應用程序自動處理令牌更新，從而實現自動化登錄，而不需要用戶每天輸入密碼。

