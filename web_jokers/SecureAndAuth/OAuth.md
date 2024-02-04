---
layout: default
title:  Google OAuth
parent: Web Jokers
last_modified_date: 2023-06-12 08:56:43
tags: OAuth
---

# Google OAuth
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

## Flask test

使用者的 Google 帳號密碼通常不應該被存儲在你的系統中，因為這樣可能會造成安全風險。相反，你應該考慮使用 Google 提供的 OAuth 2.0 驗證流程，讓使用者通過 Google 登入你的應用程序。

以下是實現這一目標的一般步驟：

1. **建立 Google 開發者帳號：** 登入 Google 開發者控制台（https://console.developers.google.com/），並創建一個新的項目。在項目中啟用 Google API，包括「Google+ API」和「Google Identity Toolkit API」。

2. **建立 OAuth 2.0 客戶端 ID：** 在控制台中，進入「憑證」部分，建立一個 OAuth 2.0 客戶端 ID。在這裡，你需要設定授權的重新導向 URI。

3. **使用 OAuth 2.0 驗證流程：** 在你的應用程序中，使用 OAuth 2.0 驗證流程。這通常包括將使用者重定向到 Google 登錄頁面，然後將授權碼交換為訪問令牌。你可以使用 Python 中的 OAuth 2.0 函式庫，例如 `oauthlib`、`requests-oauthlib` 等。

   下面是一個簡單的例子，使用 `requests-oauthlib`：

```python
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for

app = Flask(__name__)

# Replace these values with your own
client_id = 'your_client_id'
client_secret = 'your_client_secret'
redirect_uri = 'your_redirect_uri'
authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'

@app.route('/')
def index():
    google = OAuth2Session(client_id, redirect_uri=redirect_uri)
    authorization_url, state = google.authorization_url(authorization_base_url, access_type="offline", prompt="select_account")

    return redirect(authorization_url)

@app.route('/callback')
def callback():
    google = OAuth2Session(client_id, redirect_uri=redirect_uri)
    google.fetch_token(token_url, authorization_response=request.url, client_secret=client_secret)

    # Now you have the access token in google.token
    return 'Logged in successfully!'

if __name__ == '__main__':
    app.run(debug=True)
```

   在這個例子中，當用戶訪問應用程序首頁時，他們將被重定向到 Google 登錄頁面。在用戶成功登錄後，他們將被重定向回你的應用程序，並擁有一個訪問令牌。

請注意，這僅僅是一個簡單的例子，實際中你可能需要更複雜的流程來處理令牌的刷新、使用者的身份驗證等。建議閱讀相關的 OAuth 2.0 文檔以獲得更多信息。

## People API

在使用 OAuth 2.0 進行身份驗證時，成功登錄後，你可以使用訪問令牌向 Google API 發送請求，以獲取有關已登錄用戶的信息，包括他們的帳戶名稱。具體來說，你可以使用 Google 的「People API」（或以前的 Google+ API）來檢索用戶的基本信息。

以下是一個使用 `requests` 模組的簡單示例，以在成功驗證後獲取 Google 帳戶的使用者信息：

```python
import requests
from flask import Flask, request, redirect, session, url_for
from requests_oauthlib import OAuth2Session

app = Flask(__name__)

# Replace these values with your own
client_id = 'your_client_id'
client_secret = 'your_client_secret'
redirect_uri = 'your_redirect_uri'
authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'
userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'  # For Google+ API
# userinfo_url = 'https://people.googleapis.com/v1/people/me'  # For People API

@app.route('/')
def index():
    google = OAuth2Session(client_id, redirect_uri=redirect_uri)
    authorization_url, state = google.authorization_url(authorization_base_url, access_type="offline", prompt="select_account")

    return redirect(authorization_url)

@app.route('/callback')
def callback():
    google = OAuth2Session(client_id, redirect_uri=redirect_uri)
    google.fetch_token(token_url, authorization_response=request.url, client_secret=client_secret)

    # Now you have the access token in google.token
    # Let's use it to get user information
    user_info = google.get(userinfo_url).json()

    # Extract the user's account name
    account_name = user_info.get('email', 'Unknown')

    return f'Logged in successfully! User: {account_name}'

if __name__ == '__main__':
    app.run(debug=True)
```

在這個例子中，`/callback` 路由處理程序使用訪問令牌向 Google 的 People API 發送請求，以獲取用戶的基本信息。具體來說，這個示例使用了 Google+ API，但由於該 API 將於日後停用，建議使用新的 People API。

你可以根據你的需求使用不同的 Google API 端點來獲取用戶信息。要了解有關 People API 或其他相關 API 的更多信息，請查閱 Google 開發者文檔。

## google developers官網說明

- [使用 OAuth 2.0 存取 Google API ](https://developers.google.com/identity/protocols/oauth2?hl=zh-tw)

key=API_KEY


### 應用程式服務條款範例：

服務描述
本服務提供一個平台，使用者可以上傳、分享和訂閱圖片。使用者可以在平台上找到各種不同類型的圖片，包括但不限於自然風景、建築、人物、動物、飲食等。使用者可以自由地搜索、瀏覽和下載圖片，但必須遵守本服務的使用條款。
使用條款
使用者必須遵守本服務的使用條款，包括但不限於以下幾點：
使用者必須是合法的人個，不得使用虛擬人員或其他未經授權的身份進行註冊和使用。
使用者必須提供真實、準確的註冊信息，並保持註冊信息的更新。
使用者必須遵守相關的法律法規和公序良俗，不得進行任何不當行為，包括但不限於負面言論、侮辱、恐嚇、網絡攻擊等。
使用者必須保護自己的帳號密碼，不得洩露給任何第三方，並承擔因洩露帳號密碼所造成的全部後果。
使用者必須遵守本服務的相關規定，包括但不限於使用限制、訂閱限制、圖片使用限制等。
使用者必須遵守相關的版權法律，不得使用未經授權的圖片。
責任聲明
本服務僅提供平台，不涉及任何圖片的權利和責任。使用者在使用本服務時，應自行承擔相關的法律責任，包括但不限於版權、商標權、肖像權等。
服務修改
本服務僅供參考，並不保證一定會符合使用者的需求。本服務可能會因技術問題、系統升級、法律法規變更等原因而進行修改。使用者應時刻關注本服務的最新變更，並遵守相關規定。
服務終止
本服務可能會因技術問題、系統升級、法律法規變更、使用者違反服務條款等原因而終止。如本服務終止，使用者應立即停止使用本服務，並撤回自己上傳的圖片。本服務提供者不承擔因本服務終止所造成的任何損失。
法律聲明
本服務提供者不承擔任何使用者上傳或訂閱的圖片的權利和責任。使用者在使用本服務時，應自行承擔相關的法律責任，包括但不限於版權、商標權、肖像權等。
賠償責任
如使用者違反本服務的使用條款，導致本服務提供者承擔法律責任，使用者應承擔相應的賠償責任。
訴訟責任
如本服務提供者需要對使用者提起訴訟，使用者應承擔相應的訴訟費用和賠償責任。
其他條款
本服務提供者保留隨時修改或變更本服務的條款，使用者應時刻關注最新的服務條款。如使用者不同意本服務的條款變更，應立即停止使用本服務。
服務終止後的資料
在本服務終止後，使用者應立即將所有上傳的圖片從平台中刪除，並不得保留任何圖片資料。本服務提供者保留權利對使用者上傳的圖片進行備份和存儲，並保留相關的資料複製和存儲權利。
服務終止後的賠償責任
如本服務終止後，使用者因對本服務的依賴而承擔了損失，本服務提供者不承擔任何賠償責任。
服務終止後的資料保留
本服務提供者保留權利對使用者上傳的圖片進行備份和存儲，並保留相關的資料複製和存儲權利。使用者在本服務終止後，應將所有上傳的圖片從平台中刪除，並不得保留任何圖片資料。


### 應用程式隱私權政策範例：

我們關心您的隱私。
我們知道保護您的個人信息非常重要，因此我們將盡我所能來確保您的個人信息得到妥善保護。
我們的數據收集和使用方式。
當您使用我們的應用程式時，我們將收集您的個人信息，例如您的姓名、地址、電子郵件地址和使用習慣等。我們會使用這些信息來提供您的個性化服務，例如向您發送訊息或提供更好的用戶體驗。我們也會使用這些信息來分析您的使用情況，以便我們可以改進我們的產品和服務。
我們的數據共享和合作夥伴。
我們可能會與第三方合作，以提供我們的產品和服務。如果我們需要與第三方合作，我們會盡可能通知您，並提供您在此處保持您的個人信息保密的選項。
瀏覽器功能和cookie。
我們的應用程式可能使用瀏覽器功能，例如cookie，以實現更好的用戶體驗。您可以通過更改您的瀏覽器設置，以控制您瀏覽器是否接受cookie。
如何聯繫我們並對您的個人信息提出要求。
如果您想了解更多關於我們的隱私政策，或者如果您想要了解您的個人信息，請聯繫我們的客戶支持部門。您可以通過電子郵件、電話或書信聯繫我們。如果您擁有權限，您可以聯繫我們的客戶支持部門以更改您的個人信息。

### googleapiclient

```python
使用 OAuth 2.0 進行身份驗證通常涉及以下步驟：

1. **建立專案：** 在 Google 開發者控制台建立一個專案。這將為您提供用於身份驗證的 client ID 和 client secret。

2. **啟用 API：** 啟用您的專案所需的 API。這可以在 Google 開發者控制台的 "API 和服務" > "憑證" 頁面上完成。

3. **建立憑證：** 在 "API 和服務" > "憑證" 頁面，建立 OAuth 2.0 用戶端 ID。在建立時，您需要指定應用程式的類型（例如 Web 應用程式、原生應用程式、服務帳戶等）和重新導向 URI。

4. **獲取授權碼：** 在應用程式中導向用戶以獲取授權碼。使用 Google 提供的 OAuth 2.0 授權端點。

5. **獲取存取令牌：** 使用授權碼交換存取令牌。這通常是使用後端伺服器完成的，並需要將授權碼、用戶端 ID、用戶端密碼等信息提交到 OAuth 2.0 授權端點。

6. **使用 API：** 使用存取令牌調用所需的 API。將存取令牌包含在 API 請求中的標頭中。

以下是一個簡單的 Python 程式碼範例，使用 `google-auth` 庫進行 OAuth 2.0 身份驗證：

```python
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# 填入您的 client ID 和 client secret
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
REDIRECT_URI = 'your-redirect-uri'

# 獲取授權碼的 URL
auth_url = f'https://accounts.google.com/o/oauth2/auth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=https://www.googleapis.com/auth/drive.metadata.readonly&response_type=code'

# 導向用戶以獲取授權碼
print(f'請前往以下網址獲取授權碼：\n{auth_url}')

# 在獲取授權碼的同時，您也需要指定用戶端 ID、用戶端密碼等信息以獲取存取令牌
# 獲取授權碼之後，使用它來交換存取令牌
authorization_code = input('輸入獲取到的授權碼：')

# 交換授權碼以獲取存取令牌
credentials = Credentials.from_authorization_code(authorization_code, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)

# 使用 API（這裡以 Google Drive API 為例）
from googleapiclient.discovery import build

service = build('drive', 'v3', credentials=credentials)

# 使用 service 來進行 API 請求
# ...
```

在實際應用中，您需要更好地管理授權碼和存取令牌，並根據您的需求配置適當的 API 權限。確保保護應用程式的機密信息，例如 client secret。
```
