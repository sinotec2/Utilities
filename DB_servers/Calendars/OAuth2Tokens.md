---
layout: default
title:  自動登錄與令牌們的管理
parent: Calendars
grand_parent: DB_servers
last_modified_date: 2024-08-19 18:54:53
tags: calendar
---

# 自動登錄與令牌們的管理

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

## 2種令牌與自動登錄

是的，OAuth 2.0 可以實現自動化登錄，而不必每天輸入密碼。這通常是通過「刷新令牌」機制來實現的。

### 刷新令牌 (Refresh Token)

OAuth 2.0 提供了一種稱為「刷新令牌」的機制，可以在訪問令牌（Access Token）過期後，無需再次輸入用戶名和密碼來獲取新的訪問令牌。以下是這一過程的工作原理：

1. **初次授權**：
   - 用戶在第一次授權時，應用程序會獲取一個訪問令牌和一個刷新令牌。
   - 訪問令牌通常有一個較短的有效期（例如一小時），而刷新令牌的有效期較長（可以是幾天、幾個月，甚至更長）。

2. **使用訪問令牌**：
   - 在訪問令牌有效期內，應用程序可以使用它來訪問受保護的資源。

3. **訪問令牌過期**：
   - 當訪問令牌過期後，應用程序可以使用刷新令牌來請求新的訪問令牌，而無需用戶再次輸入用戶名和密碼。

4. **自動更新**：
   - 當應用檢測到訪問令牌過期時，它會自動使用刷新令牌向 OAuth 伺服器請求一個新的訪問令牌，從而保持用戶的登錄狀態。

### 這種方法的好處

- **用戶體驗**：用戶不需要頻繁地輸入憑證，可以提供更流暢的用戶體驗。
- **安全性**：即使訪問令牌被竊取，由於其短暫的有效期，攻擊者的使用時間有限。此外，刷新令牌通常只會在安全的後端服務器上使用，進一步減少風險。
- **自動化**：可以在腳本或應用程序中實現自動化處理，無需人工干預。

### 使用時的注意事項

- **安全存儲**：刷新令牌應該安全地存儲在應用程序中，避免被未授權的用戶或應用程序訪問。
- **刷新頻率**：不應該過於頻繁地刷新令牌，這可能會觸發 OAuth 提供者的安全警告或限制。

通過正確設置 OAuth 2.0，你可以讓應用程序自動處理令牌更新，從而實現自動化登錄，而不需要用戶每天輸入密碼。

## 如何获取 Refresh Token

要获得 OAuth 2.0 的刷新令牌（Refresh Token），通常是在用户首次进行授权时由授权服务器返回的。以下是详细的步骤以及刷新令牌的存储方法：

1. **初次授权流程**：
   - 用户通过授权码模式（Authorization Code Grant）或密码凭证模式（Password Credentials Grant）等方式登录。
   - 应用程序向授权服务器发送请求，通常包括 `client_id`、`redirect_uri`、`scope` 等信息。

2. **服务器响应**：
   - 如果用户授权成功，授权服务器会返回一个包含访问令牌（Access Token）和刷新令牌（Refresh Token）的响应。
   - 例如，在授权码模式下，应用程序首先接收到一个授权码（Authorization Code），然后将该码与客户端密钥（Client Secret）一起发送到授权服务器，服务器响应中会包含访问令牌和刷新令牌。

3. **示例请求与响应**：

   **请求：**

   ```http
   POST /oauth/token
   Host: authorization-server.com
   Content-Type: application/x-www-form-urlencoded

   grant_type=authorization_code&
   code=AUTH_CODE&
   redirect_uri=REDIRECT_URI&
   client_id=CLIENT_ID&
   client_secret=CLIENT_SECRET
   ```

   **响应**：以[calendar_sample.py](./calendar_sample.md)連線所得的`calendar.dat`內容為例

   ```json
   {
   "access_token": ***,
   "client_id": (same as client_secrets.json:{"installed":{"client_id":***}}),
   "client_secret": (same as client_secrets.json:{"installed":{"client_secret":***}}),
   "refresh_token": ***,
   "token_expiry": "2024-08-19T10:30:57Z",
   "token_uri": "https://oauth2.googleapis.com/token",
   "user_agent": null,
   "revoke_uri": "https://oauth2.googleapis.com/revoke",
   "id_token": null,
   "id_token_jwt": null,
   "token_response": {
         "access_token": (same as above),
         "expires_in": 3599,
         "refresh_token": (same as above),
         "scope": "https://www.googleapis.com/auth/calendar.readonly",
         "token_type": "Bearer"
         },
   "scopes": ["https://www.googleapis.com/auth/calendar.readonly"],
   "token_info_uri": "https://oauth2.googleapis.com/tokeninfo",
   "invalid": false,
   "_class": "OAuth2Credentials",
   "_module": "oauth2client.client"
   }
   ```

- 注意：
   - 與呼叫身分有關的變數：`"client_id"`、`"client_secret"`
   - `"token_response"`：將令牌相關的變數都集中在此處。

## Refresh Token 的存储位置

Refresh Token 的儲存需要特別注意安全性，因為它具有長期有效性，並且可以用於取得新的存取權杖。儲存位置的選擇因應用類型而異：

1. **Web 應用程式**：
 - **伺服器端儲存**：通常將 Refresh Token 儲存在伺服器端的資料庫或安全性儲存中，與使用者的會話或使用者標識關聯。這樣可以確保 Refresh Token 不會暴露給前端使用者。
 - **Cookie 中儲存（不建議）**：將 Refresh Token 儲存在瀏覽器的 HTTP-only 和 Secure Cookie 中，但存在一定的安全風險，特別是防止跨站腳本攻擊（XSS）。

2. **行動應用程式**：
 - **安全儲存**：在行動應用程式中，可以使用平台提供的安全儲存解決方案，例如 iOS 的 Keychain 或 Android 的加密 SharedPreferences。不要直接將 Refresh Token 儲存在未加密的本機儲存中。

3. **桌面應用程式**：
 - **安全儲存**：類似於行動應用程序，使用作業系統提供的安全儲存機制，如 Windows 的 Credential Vault 或 macOS 的 Keychain。

## 刷新令牌的使用

當存取令牌過期時，應用程式可以使用刷新令牌來獲取新的存取令牌，而無需用戶再次進行身份驗證：

若要在自動化登入流程中使用刷新令牌 (Refresh Token)，可以使用 Python 來編寫腳本，定期使用刷新令牌來取得新的存取權杖 (Access Token)，然後使用新的存取權杖進行授權請求。以下是具體的實作步驟和範例程式碼。

### 自動化登入的原理

1. **初次登入**：
 - 使用者透過授權流程登錄，取得初始的存取令牌和刷新令牌。
 - 將刷新令牌儲存在安全的地方，以便在存取令牌過期時使用。

2. **自動刷新令牌**：
 - 當存取令牌過期時，使用刷新令牌自動取得新的存取令牌，而不需要使用者再次登入。
 - 新的存取權令牌可以繼續用於存取受保護的資源。

3. **自動化腳本**：
 - 編寫一個 Python 腳本，定期檢查存取權杖是否過期，如果過期則自動使用刷新令牌以取得新的存取權杖。
 - 使用新的存取令牌繼續進行 API 請求。

### 示例代码

以下是使用 Python 和 `requests` 函式庫的範例，展示如何自動化使用刷新令牌來登入並取得新的存取權杖。

```python
import requests
import time

# 初始的客戶端配置
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REFRESH_TOKEN = 'your_refresh_token'
TOKEN_URL = 'https://authorization-server.com/oauth/token'

# 函數：使用刷新令牌取得新的存取令牌
def get_access_token(refresh_token):
   data = {
   'grant_type': 'refresh_token',
   'refresh_token': refresh_token,
   'client_id': CLIENT_ID,
   'client_secret': CLIENT_SECRET,
   }

   response = requests.post(TOKEN_URL, data=data)
   token_info = response.json()

   if response.status_code == 200:
      return token_info['access_token'], token_info.get('refresh_token', refresh_token)
   else:
      print(f"Error: {token_info.get('error_description', 'Failed to refresh token')}")
   return None, None

# 函數：自動化的API請求
def make_api_request(access_token, api_url):
   headers = {
   'Authorization': f'Bearer {access_token}'
   }

   response = requests.get(api_url, headers=headers)

   if response.status_code == 401: # 存取權杖可能已過期
   print("Access token expired, refreshing token...")
   new_access_token, new_refresh_token = get_access_token(REFRESH_TOKEN)
   if new_access_token:
   # 更新令牌並重試請求
      return make_api_request(new_access_token, api_url)
   elif response.status_code == 200:
      return response.json()
   else:
      print(f"Error: {response.status_code}")
   return None

# 範例：使用自動化腳本存取API
API_URL = 'https://api-server.com/protected-resource'
access_token, REFRESH_TOKEN = get_access_token(REFRESH_TOKEN)

if access_token:
   data = make_api_request(access_token, API_URL)
   print("Received data:", data)
```

### 關鍵點解析

1. **刷新令牌以取得新的存取令牌**
   - `get_access_token` 函數會使用現有的刷新令牌向授權伺服器請求新的存取權杖。
   - 傳回新的存取令牌，並更新刷新令牌（如果伺服器傳回了新的刷新令牌）。

2. **自動化 API 請求**：
   - `make_api_request` 函數負責向受保護的 API 發送請求，使用 Bearer 令牌進行授權。
   - 如果請求傳回 401 狀態碼，表示存取權杖可能已過期，此時會自動使用刷新權杖取得新的存取權令牌，並重試請求。

3. **儲存刷新令牌**：
   - 在實際應用中，刷新令牌應儲存在安全的地方，如環境變數、加密檔案等。

### 自動化登入的好處

- 使用刷新令牌實現自動化登錄，可以讓應用程式在無需用戶干預的情況下，長期保持授權狀態。這種方法尤其適用於需要頻繁存取 API 的應用程式或後台服務。

透過使用刷新令牌自動化來獲取新的存取令牌，你可以確保應用程式在存取令牌過期後仍然能夠正常運行，提升了系統的穩定性和使用者體驗。
