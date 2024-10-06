---
layout: default
title:  Stress Test
parent: Kubernetes
grand_parent: Parallel Computation
last_modified_date: 2024-10-06 10:19:38
---

# Z2JH 壓力測試 

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

## 引數解析

### 程式說明：parse_args() 函數

1. 功能概述

parse_args() 是一個用於解析命令列引數的函數，該函數依賴 Python 的 argparse 模組來處理多種命令和選項。它專為壓力測試 JupyterHub 的運行環境而設計，具備多個子命令，能夠創建虛擬用戶與伺服器，進行負載測試，並能夠模擬使用者活動，或清理資源。

2. 輸入

該函數主要從命令列讀取多個引數，這些引數會影響測試工具的行為。輸入可以來自：

	•	環境變數（如 JUPYTERHUB_API_TOKEN 和 JUPYTERHUB_ENDPOINT）
	•	命令列引數（如 --count, --batch-size, --workers 等）

引數列表：

	•	--endpoint：JupyterHub API 的終端點，可由環境變數 JUPYTERHUB_ENDPOINT 獲取。
	•	--token：管理員 API token，用於創建虛擬用戶。可由環境變數 JUPYTERHUB_API_TOKEN 獲取。
	•	--dry-run：進行模擬測試，不執行實際操作。
	•	--log-to-file：將日誌輸出到文件。若無參數則生成臨時文件。
	•	--verbose：啟用詳細日誌記錄。
	•	--keep：保留創建的虛擬用戶/伺服器，預設會刪除資源。
	•	--count：指定創建的用戶數，預設為 100。
	•	--batch-size：設定批次大小，控制一次創建多少用戶/伺服器，預設為 10。
	•	--workers：指定活動模擬中要創建的工作執行緒數量。

3. 輸出

該函數返回 args，其中包含解析後的引數及其對應的值。這些引數將決定接下來壓力測試工具的運行行為。

4. 重要邏輯

	•	子命令的解析：
	•	stress-test：創建虛擬用戶並生成伺服器，用於壓力測試 JupyterHub 的伺服器創建能力。
	•	activity-stress-test：模擬用戶活動，不會生成伺服器，而是通過執行緒持續發送 API 請求模擬使用者行為。
	•	purge：刪除之前創建的虛擬用戶與伺服器。
	•	環境變數的使用：
如果命令列未提供 --endpoint 或 --token，該函數會嘗試從系統環境變數中讀取這些配置，這允許更靈活的運行環境配置。
	•	日誌管理：
--log-to-file 可以選擇性地指定是否將日誌寫入文件，或是在指定的文件路徑中存放。日誌記錄可幫助分析測試過程中的 API 請求性能。

5. 應用注意事項

	•	管理員權限：該工具必須擁有 JupyterHub 管理員的 API token 才能正常運行，否則無法創建虛擬用戶和伺服器。
	•	批次大小：--batch-size 需謹慎設定，因為過大的批次可能導致伺服器負載過高，預設限制為 64 並發創建。
	•	乾跑模式 (--dry-run)：此模式適合用於測試指令而不會對系統實際造成影響，適合進行試運行。
	•	多執行緒活動模擬 (--workers)：活動壓力測試可以模擬大量用戶的行為，應確保 Hub 的 API 有足夠的性能應對多執行緒的負載。

6. 範例應用

	•	模擬 200 個用戶，分 20 個批次創建伺服器：

```bash
python hub-stress-test.py --endpoint http://localhost:8000/hub/api --token <your-token> stress-test --count 200 --batch-size 20
```

	•	進行乾跑模式，模擬活動壓力測試：

```bash
python hub-stress-test.py --dry-run activity-stress-test --count 100 --workers 10
```

### workers 與核心數

--workers 的數量與 CPU 的核心數量密切相關，特別是在進行多執行緒的壓力測試時。因為每個 worker 執行緒都會消耗 CPU 資源，所以在設置 workers 數量時，應考慮節點可用的 CPU 資源。

關於 CPU 核心和 --workers 的關係：

	1.	CPU-bound 工作：如果每個 worker 主要進行計算密集型工作，則 worker 的數量不應超過 CPU 核心的數量（在你的情況下是 15 核心）。這是因為每個核心只能同時執行一個 worker。如果 workers 數量超過 CPU 核心，將導致 CPU 的上下文切換，影響性能。
	2.	I/O-bound 工作：如果 workers 主要是 I/O 密集型（例如等待 API 響應或文件讀寫），則可以設置比 CPU 核心數量更多的 workers。這是因為 I/O 操作通常會釋放 CPU，讓其他 workers 能夠繼續執行。實際上，在這種情況下你可以設置更多的 workers，可能是 CPU 核心數量的 2 倍或更多。

範例設置：

```bash
# CPU-bound 任務：如果每個 worker 都在進行計算密集型工作，例如數據處理或模擬，那麼在 15 核心的環境中，設置 15 個 workers 是合理的。超過這個數量會導致性能下降。
python hub-stress-test.py --count 100 --workers 15

# I/O-bound 任務：如果每個 worker 都是在進行網路請求或等待外部 API 響應，那麼你可以設置 2 倍或更多的 workers。例如，可以設置 30-40 個 workers 來充分利用 I/O 等待時間。
python hub-stress-test.py --count 100 --workers 30
```


如何調整 --workers：

	•	可以根據實際測試進行調整。首先設置一個略小於 CPU 核心數量的 worker 值（例如 10），然後逐步增加 worker 的數量，觀察 CPU 使用率和響應時間。
	•	如果 CPU 使用率達到 100%，但還有許多任務等待執行，則說明 workers 數量過多，需要減少。

結論：在你的 Minikube 設定中，最多可以設置 15 個 CPU-bound workers，或 30 到 40 個 I/O-bound workers，具體數字視任務性質而定。


### validate(args) 函式

這段 validate(args) 函式的功能是驗證使用者輸入的命令行參數，以確保它們符合特定的要求。主要的目的是防止無效或缺少必要參數，從而避免程序執行時出現不可預期的錯誤。

主要邏輯與說明：

	1.	命令驗證 (args.command == 'stress-test')
	•	如果使用者的指令是 stress-test，這段程式碼會檢查 batch_size 和 count 參數。
	•	args.batch_size < 1：如果 --batch-size 小於 1，拋出異常。這是因為 batch_size 表示一個批次的用戶或伺服器數量，必須至少有 1 批次。
	•	args.count < 1：如果 --count 小於 1，也會拋出異常。count 表示要創建的伺服器或使用者數量，必須至少創建 1 個。
	2.	API Token 驗證
	•	args.token is None：如果 --token 未提供，並且環境變數 JUPYTERHUB_API_TOKEN 也沒有設定，則拋出異常。API Token 是管理 JupyterHub 伺服器所必須的，沒有 Token 的話，無法進行伺服器管理或用戶創建的操作。
	3.	API Endpoint 驗證
	•	args.endpoint is None：同樣地，如果 --endpoint 未提供，且環境變數 JUPYTERHUB_ENDPOINT 也沒有設定，則會拋出異常。這是因為程式必須知道要對哪個 JupyterHub 伺服器進行壓力測試，沒有指定 endpoint 的話，無法連接到 JupyterHub。

函式的輸入與輸出：

	•	輸入：args，通常是從 argparse 解析的命令行參數。
	•	輸出：這個函式沒有明確的返回值。如果所有參數有效，它不會做任何事情，但如果有錯誤或缺失參數，則會拋出異常。

應用時的注意事項：

	1.	參數提供完整性：在執行命令之前，確保提供必要的參數，如 --token 和 --endpoint，這些都是運行 JupyterHub 壓力測試所需的關鍵內容。
	2.	數值有效性：batch_size 和 count 必須是正數，且合理地設置這些值，否則程式會立即拋出異常，停止執行。
	3.	環境變數配置：如果使用者不想在命令行中直接提供 --token 或 --endpoint，則必須在環境變數中設置 JUPYTERHUB_API_TOKEN 和 JUPYTERHUB_ENDPOINT。

此函式的目的是在執行壓力測試之前，防止不合理的輸入，從而確保程式在一個有效的環境下正常運行。

## 紀錄測試過程與結果

函式說明：setup_logging(verbose=False, log_to_file=False, args=None)

此函式負責設定應用程式的日誌記錄系統，使開發者或系統管理員能夠監控並記錄程式的執行情況。日誌輸出可以控制到標準輸出，或存入文件（如使用者選擇了 --log-to-file 參數）。這個函式還會處理未捕獲的異常並將其記錄到日誌中。

輸入參數：

	•	verbose (bool, 預設: False)：
	•	控制日誌的詳細程度。如果為 True，日誌將包括更多的 debug 級別訊息。
	•	log_to_file (bool 或 str, 預設: False)：
	•	如果為 True，程式會將日誌輸出寫入文件。當指定為 str 時，日誌會寫入該文件路徑。若不指定具體的文件名，會自動生成一個文件存入 /tmp 目錄中。
	•	args (Namespace, 預設: None)：
	•	傳入程式的參數對象（通常是由 argparse 解析的命令行參數）。此參數用來記錄程式啟動時的參數，但會遮蔽敏感資訊（如 API token）。

功能詳解：

	1.	文件路徑生成與日誌目錄設置：
	•	如果 log_to_file 被設置為 True 並且沒有提供具體的文件名，函式會自動生成一個帶有時間戳的文件名，並將日誌記錄到 /tmp 目錄下。生成的文件名格式類似於 hub-stress-test-YYYY-MM-DDTHH:MM:SS.log。
	•	如果 log_to_file 是一個字串（具體文件名），那麼日誌將寫入該文件。
	2.	日誌格式與等級設定：
	•	使用 logging.basicConfig 設定日誌的基本格式。當 verbose 為 True 時，日誌等級將被設為 DEBUG，顯示更多詳細訊息，否則預設為 INFO 等級。
	•	urllib3.connectionpool 的日誌等級被調整為 WARNING，以防止顯示不必要的連接細節訊息。
	3.	參數記錄：
	•	如果 log_to_file 被啟用，且有提供 args，函式會將用來啟動腳本的參數記錄到日誌中。然而，為了避免洩露敏感資訊，會將 args 中的 token 部分替換為 ***。
	4.	未捕獲異常處理：
	•	通過 sys.excepthook 來捕捉未被捕捉的異常，並將異常訊息記錄到日誌中，確保程式崩潰時也能追蹤到錯誤原因。

輸出：

	•	無明確返回值：此函式的主要目的是設置日誌系統及捕捉異常，沒有明確的返回值。當發生異常時，會將異常訊息記錄到日誌中。

應用場景中的注意事項：

	1.	檔案路徑權限：當生成日誌文件時，必須確保應用程式對 /tmp 或指定的路徑有寫入權限，否則會引發錯誤。
	2.	API Token 安全性：日誌記錄時會遮蔽敏感的 API token，以防洩露。應確保在任何情況下，不要將這些敏感資訊記錄到日誌中。
	3.	異常追蹤：未捕捉的異常會被記錄在日誌中，這對於程式故障的診斷非常有用，因此在設計生產環境中的日誌時應謹慎設置。


## 計時器函式

函式說明：timeit(f)

這個函式是一個裝飾器，用來計算並記錄某個函式的執行時間。當一個被裝飾的函式執行完成後，timeit 會自動計算該函式從開始到結束所耗費的時間，並將結果記錄到日誌中。

輸入參數：

	•	f：被裝飾的函式。它是一個任意函式，timeit 裝飾器會測量這個函式的執行時間並記錄結果。

功能詳解：

	1.	裝飾器機制：
	•	使用 functools.wraps(f) 來保留原函式的元數據，如函式名稱、文件、文檔字串等。這樣，裝飾後的函式仍然能夠像原函式一樣被辨識。
	2.	執行時間計算：
	•	start_time = time.time()：記錄函式執行前的時間戳。
	•	在函式執行完成後，使用 time.time() - start_time 計算函式執行過程中耗費的時間。
	3.	日誌記錄：
	•	LOG.info('Took %.3f seconds to %s', ...)：記錄被裝飾函式的執行時間，格式化顯示到小數點後三位。
	•	f.__name__：使用被裝飾函式的名稱來提供更加清晰的日誌信息。
	4.	try-finally 機制：
	•	裝飾器確保函式的執行時間即使在函式執行過程中發生異常時也能被正確記錄。try 區塊內執行函式，無論函式是正常結束還是拋出異常，finally 區塊都會在結束時記錄時間。

輸出：

	•	裝飾後的函式：返回一個函式 wrapper，它是被裝飾函式的包裝版本，計算該函式的執行時間，並且不改變其輸入與輸出行為。

應用場景中的注意事項：

	1.	效能測試與調試：這個裝飾器非常適合在測試或調試過程中使用，可以迅速了解某些函式的執行效率。但在生產環境中，應控制日誌輸出的頻率，避免過多的 I/O 操作影響性能。
	2.	日誌配置：確保 LOG 變數已正確配置，且應根據需要設定適當的日誌等級（如 INFO 或 DEBUG），以便在適當的日誌層級下查看執行時間。
	3.	異常情況的覆蓋：無論函式是否正常返回或拋出異常，timeit 都會記錄其執行時間。因此，可以放心應用於那些有可能會拋出異常的函式中。

範例：

```python
@timeit
def example_function():
    time.sleep(2)  # 模擬需要2秒鐘的操作
    return "done"

example_function()
```

在日誌中會出現：

```python
INFO: Took 2.002 seconds to example_function
```

## 取得請求

函式說明：get_session(token, dry_run=False, pool_maxsize=100)

此函式用來創建並設定一個 HTTP 請求的 requests.Session 物件，為進行壓力測試時設置必要的參數和行為。根據傳入的參數，函式可以返回一個模擬的 session 以進行 dry run（不實際進行請求），或返回一個有重試機制的 requests.Session 實例。

### 輸入請求參數：

	•	token：JupyterHub 管理員 API token，將被用於請求的認證標頭中，格式為 Authorization: token <token>。
	•	dry_run（預設值為 False）：當此值為 True 時，將返回一個模擬的 session，用於測試或演示；為 False 時，返回一個真正的 HTTP session。
	•	pool_maxsize（預設值為 100）：設置 HTTP 連接池的最大大小，用於控制 session 中的最大併發連接數。

### 請求功能詳解：

	1.	Dry Run：
	•	如果 dry_run 為 True，函式將返回一個模擬的 requests.Session 物件，這樣可以避免實際執行 HTTP 請求。此處使用 mock.create_autospec() 來創建一個模擬對象。
	2.	真正的 Session：
	•	如果 dry_run 為 False，則創建並返回一個帶有重試機制的 requests.Session 物件。
	•	標頭設置：為 session 的所有請求設置 Authorization 標頭，使用提供的 API token 作為身份驗證。
	•	重試機制：
	•	函式使用 urllib3.util.retry.Retry 來定義重試邏輯。會自動重試某些狀態碼（如 429, 503, 504）下的請求，這些錯誤通常可能在壓力測試中遇到。
	•	backoff_factor=0.5：重試間隔時間將會按此指數增長。
	•	status_forcelist：定義了需要重試的 HTTP 狀態碼，包括 429（請求過多）、503（服務不可用）、504（網關超時）。
	•	method_whitelist=False：此參數允許針對任何 HTTP 方法進行重試（不僅限於 GET 請求）。
	3.	HTTP Adapter：
	•	使用 HTTPAdapter 並設置 max_retries 和 pool_maxsize，從而配置 session 的連接池大小及重試行為。該 adapter 將會對 HTTP 和 HTTPS 請求都生效。
	4.	回應時間日誌：
	•	如果日誌級別設置為 DEBUG，會將 log_response_time 函式添加到 session 的 response hooks 中，從而在每次請求回應後記錄回應時間。

### 輸出：

	•	返回一個配置好的 requests.Session 物件。如果 dry_run 為 True，則返回模擬的 session；否則返回實際的 session。

### 應用場景中的注意事項：

	1.	重試邏輯：
	•	重試策略是針對壓力測試中的常見錯誤設置的，如過多請求或服務不可用。這樣能夠讓測試更具韌性，但要注意過多的重試可能會對伺服器造成更大負荷。
	2.	併發控制：
	•	pool_maxsize 設置了最大併發請求數。如果壓力測試的並發數量較大，可以增加此值，與測試所需的併發量匹配。
	3.	性能考量：
	•	每次請求的回應時間都會被記錄（當日誌級別為 DEBUG 時）。這對於診斷測試中的瓶頸非常有幫助，但可能會略微影響性能。

### 範例：

```python
# 創建一個帶有重試機制的 session
session = get_session(token='your_token_here')

# 使用 session 發送請求
response = session.get('https://example.com/api/data')
```

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

## 刪除測試使用者

函式說明：delete_users_after_stopping_servers(stopped, endpoint, session)

此函式的目的是在伺服器停止後，刪除對應的使用者帳號。

輸入參數：

	•	stopped：一個字典，鍵是使用者名稱，值是布林值，表示伺服器是否已經成功停止。只有伺服器停止的使用者才會被嘗試刪除。
	•	endpoint：JupyterHub API 的基本 URL，用於發送 API 請求以刪除使用者。
	•	session：已配置的 requests.Session，用於與 JupyterHub API 通信。

功能詳解：

	1.	遍歷 stopped 字典：
	•	逐一處理每個使用者，檢查伺服器是否已成功停止（was_stopped 為 True 的情況）。
	•	對於每個使用者，函式會呼叫 JupyterHub API 的 /users/{username} 接口來刪除該使用者。
	2.	API 刪除請求：
	•	若刪除成功，函式會在日誌中記錄該使用者已刪除的訊息。
	•	如果 API 返回 404 狀態碼，表示該使用者已經被刪除過，函式會記錄相關訊息。
	•	若出現其他錯誤（如非 404 的失敗狀態碼），函式會記錄警告，並將 success 標誌設為 False，表示刪除過程中出現問題。
	3.	返回值：
	•	True：如果所有使用者成功刪除。
	•	False：如果有任何使用者未能成功刪除。
	4.	@timeit 裝飾器：
	•	這個裝飾器會記錄函式執行的總時間，並將結果記錄在日誌中，方便進行效能追蹤。

輸出：

	•	返回布林值表示所有使用者是否成功刪除。若成功，返回 True；若有失敗的刪除操作，返回 False。

應用場景中的注意事項：

	1.	伺服器與使用者的依賴性：
	•	使用者的刪除操作依賴於伺服器是否已經成功停止。若伺服器未停止，則該使用者不會被刪除。因此，必須確保伺服器先前的停止請求順利完成。
	2.	API 請求錯誤處理：
	•	如果在刪除使用者時遇到其他錯誤（例如網絡問題或 API 服務故障），函式會記錄相關錯誤資訊，但會繼續處理後續的使用者，並最終返回 False 以指出問題。
	3.	批量操作的可擴展性：
	•	如果刪除大量使用者，應確保 API 有適當的資源和容錯機制來處理這些請求。若伺服器承載壓力過大，可能需要調整刪除批量的策略。

範例：

```python
# 刪除伺服器已停止的使用者
session = get_session(token='your_token_here')
endpoint = 'https://your-jupyterhub-url/hub/api'
stopped_servers = {'user1': True, 'user2': True, 'user3': False}  # 只有成功停止伺服器的使用者會被刪除
delete_success = delete_users_after_stopping_servers(stopped=stopped_servers, endpoint=endpoint, session=session)

if delete_success:
    print("All users were successfully deleted.")
else:
    print("Some users could not be deleted.")
```

在這個範例中，只有伺服器已成功停止的 user1 和 user2 會被嘗試刪除，user3 不會被處理。

## 異步刪除多個使用者

這個函式 delete_users 的目的是批量刪除使用者帳號，並確保使用者伺服器在刪除帳號之前已經停止。這是一個分批處理的過程，確保異步操作得以完成。

函式說明：delete_users(usernames, endpoint, session, batch_size=10)

輸入參數：

	•	usernames：一個包含使用者名稱的列表，這些使用者的帳號將會被刪除。
	•	endpoint：JupyterHub API 的基本 URL，用於發送 API 請求。
	•	session：requests.Session 實例，用於與 JupyterHub API 通信。
	•	batch_size（預設為 10）：每次處理的批量大小，用於限制同時停止伺服器的數量。

功能詳解：

	1.	停止伺服器：
	•	函式首先調用 stop_servers，以批量的方式停止所有使用者的伺服器。
	•	這一過程是異步的，因此批量處理可以有效提高停止伺服器的速度。
	2.	等待伺服器停止：
	•	當伺服器的停止請求發送後，wait_for_servers_to_stop 會等待伺服器真正停止。此時會輪詢伺服器狀態，直到所有伺服器都成功停止或超時。
	3.	刪除使用者帳號：
	•	當所有伺服器停止後，函式會調用 delete_users_after_stopping_servers，刪除對應的使用者帳號。
	•	刪除成功與否會根據 API 的回應進行記錄，並返回整體結果。
	4.	回傳結果：
	•	最終返回布林值，表示所有使用者是否成功刪除。
	5.	@timeit 裝飾器：
	•	計時整個批量操作的過程，並記錄執行所需的時間，以便後續分析效能。

具體步驟：

	1.	批量停止伺服器：透過 stop_servers 批量停止伺服器，這步驟為異步操作，批次大小由 batch_size 參數控制。
	2.	等待伺服器停止：當所有伺服器收到停止請求後，函式會輪詢狀態並等待伺服器完全停止。
	3.	刪除使用者：確保伺服器完全停止後，最後批量刪除使用者。

範例：

```python
# 批量刪除使用者帳號
session = get_session(token='your_token_here')
endpoint = 'https://your-jupyterhub-url/hub/api'
usernames = ['user1', 'user2', 'user3']

delete_success = delete_users(usernames=usernames, endpoint=endpoint, session=session, batch_size=5)

if delete_success:
    print("All users were successfully deleted.")
else:
    print("Some users could not be deleted.")
```

在這個範例中，函式會首先停止 user1、user2 和 user3 的伺服器，然後等待伺服器完全停止，最後刪除這些使用者。如果操作成功，返回 True；如果有任何錯誤，返回 False。

注意事項：

	1.	批量大小 (batch_size)：
	•	批量大小會影響操作的併發性，過大的批次可能會導致伺服器壓力過大，而過小的批次則可能影響操作效率。應根據實際伺服器承載能力來設置合適的 batch_size。
	2.	伺服器超時：
	•	如果伺服器在停止過程中出現異常，wait_for_servers_to_stop 會輪詢一段時間後超時並記錄錯誤。因此需設置合理的超時策略，避免過長等待。
	3.	錯誤處理：
	•	delete_users_after_stopping_servers 會記錄每個使用者的刪除結果，並確保即使部分操作失敗，整個批量過程不會中斷。

## 批次創建測試使用者

這個函式 create_users 旨在批量創建使用者，並且每次批次操作可以創建多個使用者，這樣可以提高效率。當遇到創建失敗的情況時，函式會嘗試刪除已創建的使用者，並記錄錯誤。讓我們來詳細分析這個函式：

函式說明：create_users(count, batch_size, endpoint, session, existing_users=[])

輸入參數：

	•	count：需要創建的使用者數量。
	•	batch_size：每批創建的使用者數量，用於分批發送請求，避免一次創建過多的使用者導致伺服器壓力過大。
	•	endpoint：JupyterHub API 的基本 URL，用於發送 API 請求。
	•	session：requests.Session 實例，用於與 JupyterHub API 通信。
	•	existing_users（可選）：已存在的使用者清單。如果是重新運行該腳本，可以通過這個參數來避免重複創建已存在的使用者。

功能詳解：

	1.	設置超時 (timeout)：
	•	函式計算出操作的超時時間，將其設置為批量大小和預設超時值的最大值，確保批次操作有足夠的時間完成。
	2.	批量創建使用者：
	•	透過批量 POST 請求到 /users API 端點，創建一組新的使用者帳號。
	•	每次請求會創建一個使用者名列表，並將該列表作為請求的 JSON 負載。
	3.	錯誤處理：
	•	如果創建使用者的請求失敗，函式會嘗試刪除該批次已創建的使用者，並記錄錯誤日誌。
	•	當創建失敗時，會引發一個異常，從而終止函式執行。
	4.	日誌記錄：
	•	在批次操作中，會記錄成功創建的使用者，方便日後追蹤。
	•	若操作失敗，會詳細記錄失敗的使用者及 API 響應的狀態碼和內容。
	5.	返回值：
	•	函式會返回一個包含所有已創建使用者列表的列表，供後續操作使用，例如創建伺服器等。

範例：

```python
# 使用示例
session = get_session(token='your_token_here')
endpoint = 'https://your-jupyterhub-url/hub/api'
users_to_create = 100

created_users = create_users(count=users_to_create, batch_size=10, endpoint=endpoint, session=session)

print("Created users:", created_users)
```

這個範例會創建 100 個使用者，每次批量創建 10 個使用者。函式會根據批次處理逐步創建使用者，並返回所有已創建的使用者。

注意事項：

	1.	批量大小 (batch_size)：
	•	批量大小會影響 API 請求的併發性。過大的批次可能會導致伺服器負載過高，而過小的批次則可能影響效率。根據伺服器的承載能力設置合適的 batch_size。
	2.	既有使用者處理：
	•	若重複執行腳本，可以使用 existing_users 參數來避免重複創建已存在的使用者。
	3.	錯誤處理和清理：
	•	當創建使用者失敗時，會嘗試刪除該批次中已成功創建的使用者，並記錄詳細錯誤信息。
	4.	伺服器壓力控制：
	•	大批量的使用者創建和刪除操作會對伺服器造成壓力，應根據實際情況調整 batch_size 和超時時間，並在需要時使用異步處理來提高性能。

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

## 輸入

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

## 應用時的注意事項

	•	超時設定: 確保 SERVER_LIFECYCLE_TIMEOUT 的值足夠大，以便給伺服器啟動留有充足的時間，特別是在系統負荷高或網路延遲的情況下。
	•	伺服器狀態檢查: 檢查伺服器的狀態時需確保 API 返回有效的響應，並妥善處理可能的異常情況。
	•	日誌管理: 在多用戶或高並發情境下，請注意日誌的數量和存儲，以避免日誌過多導致的性能問題。

## 查找所有已存在的 hub-stress-test 用戶

這段程式碼的功能是查找所有已存在的 hub-stress-test 用戶。以下是該程式碼的詳細說明：

輸入

	•	endpoint: 字串，表示 API 的基礎 URL，用於發送請求以獲取用戶列表。
	•	session: requests.Session 實例，用於管理 HTTP 請求和連接。

輸出

	•	返回一個包含所有現有 hub-stress-test 用戶的列表。若未找到用戶或發生錯誤，則返回空列表。

重要邏輯

	1.	發送請求:
	•	程式碼通過 session.get() 方法發送 GET 請求到 /users 端點，以獲取所有用戶的列表。設置了 120 秒的超時時間，以處理潛在的高用戶數情況。
	2.	處理響應:
	•	如果響應有效，則將其轉換為 JSON 格式並記錄總用戶數。
	•	接著，使用 filter 函數過濾出以 USERNAME_PREFIX 開頭的用戶，並記錄這些 hub-stress-test 用戶的數量。
	3.	錯誤處理:
	•	如果請求失敗，檢查狀態碼。如果是 403，則表示訪問令牌無效，拋出異常。
	•	若發生其他錯誤，記錄警告並返回空列表。

應用時的注意事項

	•	用戶數量: 由於可能有大量用戶，因此設置適當的超時時間是必要的，以避免請求因為超時而失敗。
	•	用戶名前綴: 確保 USERNAME_PREFIX 的值正確，以便正確過濾出相關的 hub-stress-test 用戶。
	•	異常處理: 在使用該函數時，需要妥善處理可能的異常情況，特別是無效令牌的情況，以防止後續操作受到影響。

## 執行測試流程

這段程式碼的功能是執行壓力測試，主要包括創建用戶、啟動伺服器、等待伺服器準備好以及可選地刪除用戶。以下是該程式碼的詳細說明：

輸入

	•	count: 整數，表示要創建的用戶數量。
	•	batch_size: 整數，表示每批創建的用戶數量。
	•	token: 字串，用於身份驗證的令牌。
	•	endpoint: 字串，表示 API 的基礎 URL。
	•	dry_run: 布林值，表示是否為模擬運行（不進行實際操作）。
	•	keep: 布林值，表示是否保留創建的用戶和伺服器。
	•	profile: 可選，字典，表示伺服器的配置文件。

輸出

	•	無返回值。若執行過程中發生錯誤，則會拋出異常。

重要邏輯

	1.	獲取會話:
	•	調用 get_session() 函數以獲取一個已設置身份驗證的請求會話。
	2.	處理批次大小:
	•	如果 batch_size 大於 count，則將 batch_size 調整為 count。
	3.	查找現有用戶:
	•	調用 find_existing_stress_test_users() 函數來獲取已存在的 hub-stress-test 用戶，以確定用戶名稱的起始索引。
	4.	創建用戶:
	•	調用 create_users() 函數按批次創建用戶。
	5.	啟動伺服器:
	•	調用 start_servers() 函數按批次啟動每個用戶的伺服器。
	6.	等待伺服器準備:
	•	調用 wait_for_servers_to_start() 函數以確保所有伺服器都已準備好。
	7.	刪除用戶（可選）:
	•	如果 keep 為 False，則平坦化用戶列表，並調用 delete_users() 函數來刪除所有用戶。若刪除失敗，則拋出異常。

應用時的注意事項

	•	用戶數量與批次大小: 確保 batch_size 和 count 的設置合理，以避免創建過多用戶造成系統負擔。
	•	模擬運行: 使用 dry_run=True 進行模擬運行可以幫助測試流程而不影響實際系統。
	•	保留用戶: 根據需求設置 keep，以決定是否保留創建的用戶和伺服器，避免在測試後清理資源。
	•	配置文件: 如有需要，通過 profile 參數傳遞伺服器配置，以確保伺服器按預期配置啟動。

## 清除所有測試使用者

這段程式碼的功能是刪除現有的壓力測試用戶。以下是該程式碼的詳細說明：

輸入

	•	token: 字串，用於身份驗證的令牌。
	•	endpoint: 字串，表示 API 的基礎 URL。
	•	dry_run: 布林值，表示是否為模擬運行（不進行實際操作）。

輸出

	•	無返回值。若刪除過程中發生錯誤，則會拋出異常。

重要邏輯

	1.	獲取會話:
	•	調用 get_session() 函數以獲取一個已設置身份驗證的請求會話。
	2.	查找現有用戶:
	•	調用 find_existing_stress_test_users() 函數以獲取已存在的 hub-stress-test 用戶。
	3.	刪除用戶:
	•	如果找到現有用戶，則提取用戶名稱並記錄即將刪除的用戶數量。
	•	調用 delete_users() 函數刪除這些用戶。如果刪除失敗，則拋出異常。

應用時的注意事項

	•	模擬運行: 使用 dry_run=True 進行模擬運行可以幫助測試刪除流程而不影響實際系統。
	•	用戶存在檢查: 在刪除用戶之前，確保有現有用戶可以刪除，以避免不必要的 API 調用。
	•	權限問題: 確保提供的 token 具備刪除用戶的權限，否則可能會導致授權失敗。
	•	日誌記錄: 透過日誌記錄刪除的用戶數量，方便後續的操作追蹤與調試。

## 同時啟動筆記活動的測試

這段程式碼的功能是執行一個筆記本活動測試，模擬多個用戶在 JupyterHub 上的活動，並測量每個活動更新的延遲時間。以下是該程式碼的詳細說明：

輸入

	•	count: 整數，表示要模擬的用戶數量。
	•	token: 字串，用於身份驗證的令牌。
	•	endpoint: 字串，表示 API 的基礎 URL。
	•	workers: 整數，表示同時工作的執行緒數量。
	•	keep: 布林值，表示是否在測試後保留用戶（預設為 False，刪除用戶）。
	•	dry_run: 布林值，表示是否為模擬運行（不進行實際操作）。

輸出

	•	無返回值。執行後在日誌中記錄活動更新的平均時間和最小/最大時間。

重要邏輯

	1.	獲取會話:
	•	通過 get_session() 函數獲取一個已設置身份驗證的請求會話，並根據 workers 設置最大連接數。
	2.	查找現有用戶:
	•	調用 find_existing_stress_test_users() 函數來查找已存在的用戶，以決定要創建的用戶數量。
	3.	創建缺少的用戶:
	•	如果需要創建的用戶數量大於零，則調用 create_users() 函數創建用戶，並將新用戶添加到用戶名列表中。
	4.	發送活動更新:
	•	定義 send_activity() 函數，為每個用戶發送活動更新，並記錄每次請求的延遲時間。請求的內容包括用戶的最後活動時間。
	5.	分批處理用戶:
	•	定義 chunk() 函數，將用戶分成批次以便並行處理。
	6.	持續檢查伺服器:
	•	定義 ping_hub() 函數，不斷向伺服器發送請求以檢查延遲時間，並記錄每次請求的延遲。
	7.	使用執行緒池進行併發處理:
	•	使用 ThreadPoolExecutor 同時發送活動更新請求，並啟動 ping_hub 進行伺服器檢查。
	8.	計算和記錄統計數據:
	•	在所有活動更新請求完成後，計算平均延遲時間並記錄到日誌中。
	9.	刪除用戶:
	•	如果 keep 參數為 False，則調用 delete_users() 刪除創建的用戶。

應用時的注意事項

	•	模擬運行: 設置 dry_run=True 進行模擬運行，以避免對實際用戶進行操作。
	•	用戶數量: 確保 count 和 workers 的設置合理，以避免過多或過少的請求影響性能測試結果。
	•	日誌記錄: 利用日誌功能記錄測試的詳細信息，以便於後續分析和調試。
	•	伺服器負載: 當大量用戶同時發送請求時，確保伺服器能承受相應的負載，以免造成服務不可用。
    