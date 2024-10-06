---
layout: default
title:  伺服器管理
parent: System Stress Test
grand_parent: Kubernetes
last_modified_date: 2024-10-06 10:19:38
---

#  伺服器管理

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

## 等候伺服器停止

函式說明：wait_for_server_to_stop(username, endpoint, session)

此函式監控指定 JupyterHub 使用者的伺服器狀態，等待伺服器停止運行。在壓力測試或系統調度過程中，它用來確認某個使用者的 notebook 伺服器是否已關閉，並根據狀態回傳結果。

輸入參數：

	•	username：需要監控伺服器狀態的使用者名稱。
	•	endpoint：JupyterHub API 的基本 URL，用來查詢使用者的伺服器狀態。
	•	session：一個配置好的 requests.Session 實例，用於發送 API 請求。

功能詳解：

	1.	API 請求循環檢查：
	•	函式每秒對 /users/{username} 發送一個 GET 請求，目的是檢查該使用者的伺服器狀態。SERVER_LIFECYCLE_TIMEOUT 變數定義了最大檢查次數或超時時間。
	•	迴圈會持續直到伺服器停止，或者達到 SERVER_LIFECYCLE_TIMEOUT 設定的時間上限。
	2.	回應檢查：
	•	當伺服器停止時，使用者的 servers 字典應該是空的，這代表伺服器已成功關閉。若發現 servers 是空的，函式返回 True，表示伺服器已關閉。
	•	若伺服器未關閉，會記錄 DEBUG 級別的日誌，並持續嘗試。
	3.	404 狀態碼處理：
	•	如果回應狀態碼為 404，則表示該使用者可能已被刪除。這種情況也被認為是伺服器停止，並且函式返回 True。
	4.	異常處理：
	•	如果伺服器返回其他異常狀態碼或錯誤，函式會記錄警告，並繼續重試直到超時。
	5.	超時：
	•	如果在 SERVER_LIFECYCLE_TIMEOUT 設定的時間內伺服器仍未關閉，函式將返回 False，並記錄超時警告。

輸出：

	•	True：伺服器已成功停止，或使用者已被刪除。
	•	False：伺服器在指定時間內未能成功停止，並超時。

應用場景中的注意事項：

	1.	SERVER_LIFECYCLE_TIMEOUT 設定：
	•	這個變數應設置為一個合理的超時時間，根據系統負載情況決定。過短可能導致過早返回 False，過長則可能拖慢系統。
	2.	API 響應檢查：
	•	如果伺服器正在高負載運行，可能會遇到 503 等伺服器錯誤狀態。雖然函式沒有特別處理這些情況，但可以考慮增加重試邏輯。
	3.	伺服器停止的依賴性：
	•	假如系統在運行大規模壓力測試，可能需要依賴該函式來確保伺服器已經停止再進行下一步操作，避免伺服器資源浪費。

### 範例：

```python
# 檢查使用者 'user1' 的伺服器是否已停止
session = get_session(token='your_token_here')
result = wait_for_server_to_stop(username='user1', endpoint='https://your-jupyterhub-url/hub/api', session=session)

if result:
    print("伺服器已成功停止")
else:
    print("伺服器停止超時")
```
## 停下使用者的伺服器

函式說明：stop_server(username, endpoint, session, wait=False)

此函式的目的是通過 JupyterHub API 停止指定使用者的 notebook 伺服器。可以選擇是否等待伺服器停止後再返回結果，或只確認伺服器停止請求是否成功發送。

### 輸入參數：

	•	username：要停止伺服器的使用者名稱。
	•	endpoint：JupyterHub API 的基本 URL，用來發送停止伺服器的請求。
	•	session：一個經過配置的 requests.Session，用於發送 API 請求。
	•	wait（可選，預設為 False）：若設置為 True，則在發送停止請求後會等待伺服器完全停止再返回結果；若為 False，則只確認請求成功後立即返回。

### 功能詳解：

	1.	停止伺服器的請求：
	•	使用 HTTP DELETE 方法對 /users/{username}/server 端點發送 API 請求，該請求會告知 JupyterHub 停止該使用者的 notebook 伺服器。
	2.	狀態碼檢查：
	•	如果 API 回應狀態碼為 204，表示伺服器已成功停止，無需進一步等待或輪詢，函式返回 True。
	•	如果設置了 wait=True，在發送請求後會調用 wait_for_server_to_stop() 函式進行輪詢，直到伺服器完全停止或超時。
	3.	錯誤處理：
	•	若 API 請求失敗，會記錄警告，並返回 False，表示伺服器停止請求未成功。

### 輸出：

	•	True：
	•	當伺服器成功停止，或伺服器停止請求成功發送時返回（若未設置 wait）。
	•	False：
	•	當伺服器停止請求失敗時返回，或當輪詢期間伺服器未能成功停止。

### 應用場景中的注意事項：

	1.	非同步停止與等待選擇：
	•	設置 wait=False 可以使系統在發送請求後立即返回，不需要等待伺服器真正停止，這在高效能環境中尤其有用。
	•	設置 wait=True 時，系統會確保伺服器完全停止後才進行後續操作，適合需要嚴格控制伺服器資源的場景。
	2.	API 錯誤處理：
	•	當 API 請求失敗時（例如伺服器忙碌、無法連接等），需要進一步調查 resp.status_code 和 resp.content 來了解具體錯誤原因。
	3.	伺服器壓力測試應用：
	•	在進行壓力測試時，可能需要大量伺服器啟動和關閉。使用此函式可以高效地控制伺服器的啟停狀態，尤其是在集群運行大規模用戶負載時。

### 範例：

```python
# 停止 'user1' 的伺服器
session = get_session(token='your_token_here')
result = stop_server(username='user1', endpoint='https://your-jupyterhub-url/hub/api', session=session, wait=True)

if result:
    print("伺服器已成功停止")
else:
    print("伺服器停止失敗")
```

## 批次停止多個使用者的伺服器

函式說明：stop_servers(usernames, endpoint, session, batch_size)

此函式的目的是批量停止多個使用者的 notebook 伺服器，並使用 Python 的 ThreadPoolExecutor 來並行處理停止伺服器的請求。通過使用 @timeit 裝飾器，函式運行的時間也會被記錄。

### 輸入參數：

	•	usernames：要停止伺服器的使用者名稱列表。
	•	endpoint：JupyterHub API 的基本 URL，用於發送停止伺服器的請求。
	•	session：一個經過配置的 requests.Session，用於發送 API 請求。
	•	batch_size：並行處理的批次大小，也就是允許同時處理的最大伺服器停止請求數。

### 功能詳解：

	1.	批次停止伺服器：
	•	使用 ThreadPoolExecutor 來實現多線程的並行處理，每個使用者的伺服器停止請求都會由一個執行緒負責。
	•	每批次最大執行緒數量由 batch_size 控制，這樣可以有效避免一次性發出過多 API 請求，從而防止伺服器過載。
	2.	future_to_username 映射：
	•	每個提交給 ThreadPoolExecutor 的任務（executor.submit()）返回一個 Future 物件，並將其與對應的使用者名稱進行映射，這樣可以跟蹤每個使用者伺服器停止請求的完成狀態。
	3.	異步等待任務完成：
	•	futures.as_completed() 用於遍歷已完成的任務，每個已完成的任務會返回一個 Future 物件，通過該物件可以提取伺服器是否成功停止的結果。
	4.	結果儲存：
	•	每個使用者伺服器的停止結果（成功或失敗）會存入 stopped 字典，鍵為使用者名稱，值為布林值 True 或 False。
	5.	@timeit 裝飾器：
	•	裝飾器會記錄此函式執行的總時間，並在日誌中輸出執行時間，方便進行性能監控。

輸出：

	•	stopped：返回一個字典，鍵是使用者名稱，值為伺服器是否成功停止的布林值。

應用場景中的注意事項：

	1.	批次大小 (batch_size) 的選擇：
	•	batch_size 代表可以同時處理的伺服器停止請求數量，根據系統的硬體資源和 API 限制，選擇合適的批次大小可以提高效率，同時避免過載。
	•	在大量使用者的壓力測試中，過大的批次大小可能導致 JupyterHub 的 API 過載，而過小的批次大小則會降低並行處理的效率。
	2.	並行處理與伺服器資源：
	•	伺服器的 CPU 和 I/O 資源對這些並行處理的影響較大，建議根據系統資源適當調整 batch_size 的大小以達到最佳性能。
	3.	錯誤處理：
	•	對於每個伺服器的停止操作都應該仔細檢查結果，若有失敗，應進行進一步的錯誤處理或記錄以便後續分析。

### 範例：

```python
# 使用 batch_size = 5 並行停止 10 個使用者的伺服器
session = get_session(token='your_token_here')
usernames = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8', 'user9', 'user10']
stopped_servers = stop_servers(usernames=usernames, endpoint='https://your-jupyterhub-url/hub/api', session=session, batch_size=5)

for user, stopped in stopped_servers.items():
    print(f'User {user} server stopped: {stopped}')
```

## 等待一組使用者伺服器完全停止

函式說明：wait_for_servers_to_stop(stopped, endpoint, session)

此函式的目的是等待一組使用者伺服器完全停止，並根據伺服器停止的請求結果來決定是否要等待它們的最終停止狀態。

### 輸入參數：

	•	stopped：一個字典，鍵是使用者名稱，值是布林值，代表伺服器是否已經收到停止請求。當值為 True 時，函式會等待伺服器完全停止，並更新字典中的值為伺服器是否成功完全停止的結果。
	•	endpoint：JupyterHub API 的基本 URL，用於發送 API 請求以檢查伺服器的狀態。
	•	session：已配置的 requests.Session，用於與 JupyterHub API 通信。

### 功能詳解：

	1.	遍歷 stopped 字典：
	•	函式會逐一檢查字典中的每個使用者名稱及其對應的布林值（伺服器是否已發出停止請求）。
	•	如果伺服器已經收到停止請求 (was_stopped == True)，函式會呼叫 wait_for_server_to_stop 來確保伺服器已完全停止。
	2.	更新伺服器停止狀態：
	•	函式會更新 stopped 字典中的值，從代表伺服器「已發出停止請求」的布林值轉變為「伺服器是否完全停止」的最終結果，這樣便於後續邏輯處理。
	3.	@timeit 裝飾器：
	•	裝飾器會記錄整個等待伺服器停止的過程所花費的時間，並將結果記錄在日誌中，方便進行性能分析。

輸出：

	•	無直接輸出，但它會更新傳入的 stopped 字典，從而表示伺服器是否完全停止。

### 應用場景中的注意事項：

	1.	伺服器停止的狀態追蹤：
	•	對於每個伺服器，必須確保伺服器已經完全停止（不再運行）。如果有使用者的伺服器並未成功發出停止請求，則不會等待該伺服器停止。
	2.	伺服器停止的耗時：
	•	根據伺服器的配置和運行狀態，停止伺服器可能需要一些時間，因此這個過程可能會根據伺服器的數量和網絡延遲有所不同。
	3.	併發操作的影響：
	•	如果批量操作大量伺服器，請確保適當的資源和 API 限制，以防止系統過載或 API 拒絕服務（如過多的請求導致 429 錯誤）。

### 範例：

```python
# 等待之前已發出停止請求的伺服器完全停止
session = get_session(token='your_token_here')
endpoint = 'https://your-jupyterhub-url/hub/api'
stopped_servers = {'user1': True, 'user2': True, 'user3': False}  # True 表示伺服器已經收到停止請求
wait_for_servers_to_stop(stopped=stopped_servers, endpoint=endpoint, session=session)

for user, is_stopped in stopped_servers.items():
    print(f'User {user} server fully stopped: {is_stopped}')
```

在這個範例中，只有 user1 和 user2 會被等待完全停止，而 user3 由於停止請求未成功發送，因此不會被進一步檢查。

## 啟動JH伺服器

這個函式 start_server 用於在 JupyterHub 中為特定使用者啟動伺服器。如果提供了配置檔案 (profile)，則會在啟動伺服器時應用該配置檔案。下面是此函式的詳細說明：

函式說明：start_server(username, endpoint, session, profile=None)

輸入參數：

	•	username：使用者的名稱（帳號），用於指定要啟動伺服器的對象。
	•	endpoint：JupyterHub API 的基礎 URL，用於發送 API 請求。
	•	session：requests.Session 實例，用於與 JupyterHub API 通信。
	•	profile（可選）：伺服器配置檔案，指定伺服器啟動時要使用的特定配置檔案。這個檔案可以根據需求來決定是否需要使用不同的硬體或軟體環境。

功能詳解：

	1.	啟動伺服器請求：
	•	透過向 /users/{username}/server 發送 POST 請求來啟動指定使用者的伺服器。
	•	如果提供了 profile，則會將其作為 JSON 負載的一部分傳遞給 API，應用自定義配置。
	2.	成功日誌：
	•	如果伺服器啟動成功，函式會記錄一條日誌，表明伺服器正在為指定使用者啟動。
	3.	錯誤處理：
	•	如果伺服器啟動失敗，函式會記錄錯誤日誌，並顯示伺服器回應的狀態碼和錯誤內容。

代碼範例：

```python
# 使用範例
session = get_session(token='your_token_here')
endpoint = 'https://your-jupyterhub-url/hub/api'
username = 'test-user'

start_server(username, endpoint, session, profile='custom-profile')
```

此範例將為使用者 test-user 啟動伺服器，並應用名為 custom-profile 的伺服器配置檔案。如果沒有指定 profile，伺服器將會根據預設配置啟動。

錯誤處理考慮：

	•	當伺服器啟動失敗時，函式目前僅記錄錯誤，沒有實施進一步的錯誤處理。可以根據需要進行以下改進：
	1.	自動重試：在伺服器啟動失敗時嘗試重新啟動伺服器。
	2.	使用者刪除：在伺服器啟動失敗時，選擇是否自動刪除該使用者，避免出現孤立使用者的情況。
	3.	異常拋出：當伺服器啟動失敗時，可以選擇拋出異常，讓上層邏輯進行處理。

性能優化：

如果需要批量啟動多個使用者的伺服器，可以考慮將這個函式放在多執行緒或多進程環境中，利用並行性來提高速度，特別是在大規模使用者操作時。

### profile範例

在 JupyterHub 中，profile 參數用於指定伺服器啟動時所應用的配置。這些配置可能會根據不同的需求而有所不同，例如不同的資源限制（CPU、記憶體）、環境變數或其他自定義設置。以下是一些 profile 可能包含的內容和範例：

可能的 profile 內容

	1.	資源限制：
	•	指定 CPU 和記憶體的使用限制。
	•	例如：
```json
{
    "cpu": 2,
    "memory": "4G"
}
```

	2.	環境變數：
	•	定義伺服器啟動時需要的環境變數。
	•	例如：

```json
{
    "env": {
        "MY_ENV_VAR": "value",
        "ANOTHER_VAR": "another_value"
    }
}
```

	3.	映像檔：
	•	指定要使用的 Docker 映像檔。
	•	例如：

```python
{
    "image": "my-docker-image:latest"
}
```

	4.	啟動命令：
	•	定義伺服器啟動時的命令或參數。
	•	例如：

```python
{
    "cmd": ["jupyterhub-singleuser", "--NotebookApp.token='mytoken'"]
}
```

	5.	持久化儲存：
	•	指定要掛載的持久化儲存。
	•	例如：

```python
{
    "volumes": [
        {
            "name": "my-volume",
            "mountPath": "/home/jovyan/work"
        }
    ]
}
```


總合範例

下面是一個可能的完整 profile JSON，包含多個設置：

```json
{
    "name": "data-science",
    "cpu": 4,
    "memory": "8G",
    "env": {
        "PYTHON_ENV": "development",
        "API_KEY": "my_api_key"
    },
    "image": "my-data-science-image:latest",
    "cmd": ["jupyterhub-singleuser", "--NotebookApp.token='mytoken'"],
    "volumes": [
        {
            "name": "user-data",
            "mountPath": "/home/jovyan/data"
        }
    ]
}
```

使用範例

在 start_server 函式中使用這個配置：

```json
profile = {
    "name": "data-science",
    "cpu": 4,
    "memory": "8G",
    "env": {
        "PYTHON_ENV": "development",
        "API_KEY": "my_api_key"
    },
    "image": "my-data-science-image:latest",
    "cmd": ["jupyterhub-singleuser", "--NotebookApp.token='mytoken'"],
    "volumes": [
        {
            "name": "user-data",
            "mountPath": "/home/jovyan/data"
        }
    ]
}

start_server(username='test-user', endpoint='https://your-jupyterhub-url/hub/api', session=session, profile=profile)
```

注意事項

	•	請確保所使用的 profile 內容符合 JupyterHub 的配置要求，並且支持您所使用的服務器或 Docker 映像檔。
	•	這些配置需要根據實際需求進行調整。不同的使用案例和需求可能會有不同的 profile 設置。

## 同步開啟使用者伺服器

您的 start_servers 函數旨在使用 ThreadPoolExecutor 同時啟動多個 JupyterHub 筆記本伺服器。以下是函數的主要組成部分的說明，並提供一些改進建議，以提高其穩健性和功能性。

### 函數解析

	1.	日誌記錄：
	•	函數開始時記錄伺服器初始化過程，增強日誌的可見性。
	2.	ThreadPoolExecutor：
	•	使用 ThreadPoolExecutor 允許同時執行 start_server 函數，提高效率，特別是在啟動多個伺服器時。
	3.	遍歷用戶：
	•	外部循環遍歷用戶組（users），為每個組啟動一組新的伺服器。
	4.	提交任務：
	•	對於當前批次中的每個用戶名，將 start_server 函數提交給執行者，該執行者處理實際的伺服器啟動。

### 建議改進

	1.	錯誤處理：
	•	添加伺服器啟動失敗的錯誤處理。您可以捕獲異常並適當地記錄。
	2.	等待完成：
	•	您可能希望等待所有的未來任務完成，特別是如果您需要確保在繼續之前所有伺服器都已啟動。
	3.	參數驗證：
	•	在啟動操作之前考慮驗證 users、endpoint 和 session 參數。
	4.	動態工作數：
	•	而不是使用 len(usernames) 作為 max_workers，您可以設置一個全局限制，以避免過度加載 JupyterHub。

### 修訂函數

以下是結合這些建議的修訂版本：

```python
@timeit
def start_servers(users, endpoint, session, profile=None):
    LOG.info('正在啟動筆記本伺服器')
    futures_list = []
    
    for index, usernames in enumerate(users):
        thread_name_prefix = f'hub-stress-test:start_servers:{index}'
        with futures.ThreadPoolExecutor(max_workers=10, thread_name_prefix=thread_name_prefix) as executor:
            for username in usernames:
                future = executor.submit(start_server, username, endpoint, session, profile=profile)
                futures_list.append(future)
    
    # 等待所有未來任務完成並記錄結果
    for future in futures.as_completed(futures_list):
        try:
            future.result()  # 這將重新引發執行過程中捕獲的任何異常
        except Exception as e:
            LOG.error('啟動伺服器時出錯: %s', str(e))
```

### 主要變更

	•	錯誤處理：現在如果啟動伺服器失敗，會記錄錯誤信息。
	•	完成等待：它會等待所有提交的任務完成，以確保在結束函數之前所有伺服器都已啟動。
	•	最大工作數：設置最大工作數為 10，這可以根據您的需求進行調整。

最後的想法

這個修訂的函數更加穩健和信息豐富，能提供更好的洞察力以處理在伺服器啟動過程中可能出現的任何問題。根據預期負載和 JupyterHub 部署的能力，始終調整像 max_workers 這樣的參數。

## 異步等候啟動多個使用者伺服器

這段程式碼的功能是等待用戶的 Jupyter Notebook 伺服器啟動完成，並檢查伺服器的狀態。
以下是該程式碼的詳細說明：

### 輸入

	•	users: 一個包含用戶名列表的列表，每個內部列表代表一批用戶。
	•	endpoint: 字串，代表 API 的基礎 URL，用於發送請求以獲取用戶伺服器的狀態。
	•	session: requests.Session 實例，用於管理 HTTP 請求和連接。

### 輸出

	•	無直接輸出，但會記錄伺服器的啟動狀態，包括成功或失敗的日誌信息。

### 重要邏輯

	1.	伺服器檢查:
	•	逐個檢查用戶的伺服器狀態，透過發送 GET 請求到 API 端點以獲取該用戶的詳細資訊。
	•	使用 user.get('servers', {}).get('', {}) 獲取伺服器的狀態，特別是檢查伺服器是否已經準備好 (ready 屬性)。
	2.	循環檢查:
	•	使用 while 循環來多次檢查伺服器狀態，最多檢查 SERVER_LIFECYCLE_TIMEOUT 秒。
	•	如果伺服器在等待過程中失敗，則會記錄錯誤並中斷檢查。
	3.	日誌記錄:
	•	成功啟動的伺服器將記錄成功信息，若伺服器未能啟動或出現錯誤，則會記錄錯誤信息。

### 應用時的注意事項

	•	超時設定: 確保 SERVER_LIFECYCLE_TIMEOUT 的值足夠大，以便給伺服器啟動留有充足的時間，特別是在系統負荷高或網路延遲的情況下。
	•	伺服器狀態檢查: 檢查伺服器的狀態時需確保 API 返回有效的響應，並妥善處理可能的異常情況。
	•	日誌管理: 在多用戶或高並發情境下，請注意日誌的數量和存儲，以避免日誌過多導致的性能問題。
