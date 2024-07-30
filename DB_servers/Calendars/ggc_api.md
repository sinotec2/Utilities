---
layout: default
title:  Google Calendar API
parent: Calendars
grand_parent: DB_servers
last_modified_date: 2024-07-29 18:54:53
tags: calendar
---

# Google Calendar API

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

- 這個主題雖有很多的技術文件支援，但因為Google也進步的很快，很多功能日新月異，GPT's來不及更新，反而會提供舊的、錯的訊息，就連官網的說明也不見得是最新，還是找到github上的原始碼、經過測試驗證比較可靠。
- 新版的API似乎不再支援`cRUL`、原因不明，
  - 可能因為需要指定的條件太多，還有`ACCESS_TOKEN`的取得也是層層關卡，到底是GET還是POST搞不清楚，乾脆用程式語言來做比較直接。
  - 但實際作業過程，還是產出或引用到許多json檔案的訊息，只是是用比較完整的語言工具來操作。

|![](2024-07-29-19-05-34.png)|
|:-:|
|[官網快速入門的語言選項](https://developers.google.com/calendar/api/guides/overview?hl=zh-tw)|

- 除了語言的選項之外，OAuth2的說明也是偏向Workspace開放者。對一般使用者而言只能一面揣摩、一面慢慢前進。
  - 最明顯的議題就是內/外部使用者和`redirect_uris`的匹配。充滿許多邏輯上的問題。
  - 明明是外部使用者，內部uris也可以接受？
  - workspace使用者也是只有少數代表號？
  - 所謂內部使用者要使用*google calendar*，沒有gmail可以嗎？似乎也是不可能。
- 還有最最奇怪的是程式碼和程式說明似乎不是同一套。
  - [Google Workspace官網說明](https://developers.google.com/calendar/api/guides/overview?hl=zh-tw)是2024-07-24更新。要到下載區才會連到[google-api-python-client][gapi]
  - [程式碼][gapi]的相關[說明](https://googleapis.github.io/google-api-python-client/docs/)，前者時常在更新，後者最新是2～10年前。python範例是2年前。

## 憑證

- 為了得到API的存取憑證（`ACCESS_TOKEN`），需要有專案、有OAuth客戶端金鑰，登入OAuth伺服器通過驗證後，才能得到`ACCESS_TOKEN`。官網的圖有著很好的示範效果。

|![](https://developers.google.com/static/identity/protocols/oauth2/images/flows/authorization-code.png)|
|:-:|
|[使用 OAuth 2.0 訪問 Google API](https://developers.google.com/identity/protocols/oauth2?hl=zh-cn)|
- 以下是官網的步驟，其下注解乃實際執行的經驗。

1. 為 Google Workspace 應用程式、擴充功能或整合建立 Google Cloud 專案。
   - 專案是計費單元，這可以理解，但是“機構”是什麼？似乎就不是個人帳戶有的層次了。
   - 還好是並不會要求押信用卡帳號才能開專案。
2. 在 Google Cloud 專案中啟用要使用的 API（選取*Google calendar API*）。
   - 這一點也很容易理解。
   - 但是專案中如果已經有其他既有的服務，就會出現連結的問題。
   - 建議還是一個專案其下只開啟一個服務，會比較單純。
3. 瞭解針對 Google Workspace 開發作業時，驗證和授權的運作方式。
   - 可能其他服務可以接受單一API金鑰。*Google calendar API*只接受 OAuth2雙重認證。
   - 複雜的伺服器服務會區分計費單元，有個別的OAuth2憑證、甚至輪轉使用等等資安考量作法。此處先以*Google calendar*讀取、彙總為目標，設定單一的OAuth2憑證即可。
   - 選定電腦應用程式、給定一個外部的網頁及服務名稱，這點還可以再修改。
4. 設定 OAuth 同意聲明，確保使用者能夠瞭解及核准應用程式存取其資料的權限。
   - 參考[選擇 Google Calendar API 範圍](https://developers.google.com/calendar/api/auth?hl=zh-tw)給定*Google calendar*相關的API伺服器的授權
  ```bash
  https://www.googleapis.com/auth/calendar.readonly
  https://www.googleapis.com/auth/calendar
  https://www.googleapis.com/auth/calendar.events.readonly
  https://www.googleapis.com/auth/calendar.events
  ```
   - 似乎在程式碼中也可以設定`SCOPES`，此處是否必要還有待確認。
1. 建立登入憑證，用來驗證應用程式的使用者或服務帳戶。
   - 似乎不必建立“服務帳戶”，因為測試階段OAuth2是用白名單來進行認證，服務帳戶是機械帳戶，也無法通過OAuth認證。

## 程式庫安裝

- python版本，不小於3.7、官網說明則為>=3.10。
- 實際：3.9似乎對*Google calendar API*還可運行。

```bash
pip install google-api-python-client oauth2client
```

## 測試程式

### 客戶端驗證金鑰

- client_secrets.json
- `[[...]]`內容為專案設定結果
- `redirect_uris`似乎不影響結果，設為`localhost`要記得將顯示(`$DISPLAY`)設到正確的終端機IP就可以了。

```json
{
  "installed": {
    "client_id": "[[INSERT CLIENT ID HERE]]",
    "client_secret": "[[INSERT CLIENT SECRET HERE]]",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "client_email": "",
    "redirect_uris": [
      "urn:ietf:wg:oauth:2.0:oob",
      "oob"
    ],
    "client_x509_cert_url": "",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs"
  }
}
```

### 執行程式

- 程式名稱不要取token.py、calendar.py，會發生無窮迭代呼叫的bug。

```python
import sys

from oauth2client import client
from googleapiclient import sample_tools


def main(argv):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv,
        "calendar",
        "v3",
        __doc__,
        __file__,
        scope="https://www.googleapis.com/auth/calendar.readonly",
    )

    try:
        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list["items"]:
                print(calendar_list_entry["summary"])
            page_token = calendar_list.get("nextPageToken")
            if not page_token:
                break

    except client.AccessTokenRefreshError:
        print(
            "The credentials have been revoked or expired, please re-run"
            "the application to re-authorize."
        )


if __name__ == "__main__":
    main(sys.argv)
```

### 結果

- 會啟動瀏覽器、進入Oauth2認證。只有白名單的使用者可以通過認證。
- `uri="http://localhost:8080/?code=4/***&scope=https://www.googleapis.com/auth/calendar.readonly"`
- `The authentication flow has completed.` 

```bash
$ python ical.py        
/Users/kuang/.conda/envs/py39/lib/python3.9/site-packages/oauth2client/_helpers.py:255: UserWarning: Cannot access calendar.dat: No such file or directory
  warnings.warn(_MISSING_FILE_MESSAGE.format(filename))

Your browser has been opened to visit:

    https://accounts.google.com/o/oauth2/auth?client_id=***.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar.readonly&access_type=offline&response_type=code

If your browser is on a different machine then exit and re-run this
application with the command-line parameter

  --noauth_local_webserver

Authentication successful.
研資部
台灣的節慶假日
研資部公用日曆
工作成果提交
工程服務
Kuang's Office
MIS
```

## TODO's

- 邀請代表使用者訪問所有的日曆
- 彙總所有日曆中指定行程
  - 預定出差
  - 預定休假
  - 計畫成果提交計畫

[gapi]: https://github.com/googleapis/google-api-python-client "google-api-python-client程式碼與範例"