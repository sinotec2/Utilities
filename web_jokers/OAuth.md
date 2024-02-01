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
