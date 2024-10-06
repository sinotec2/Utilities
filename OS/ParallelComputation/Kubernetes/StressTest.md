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

python hub-stress-test.py --endpoint http://localhost:8000/hub/api --token <your-token> stress-test --count 200 --batch-size 20


	•	進行乾跑模式，模擬活動壓力測試：

python hub-stress-test.py --dry-run activity-stress-test --count 100 --workers 10


### workers 與核心數

--workers 的數量與 CPU 的核心數量密切相關，特別是在進行多執行緒的壓力測試時。因為每個 worker 執行緒都會消耗 CPU 資源，所以在設置 workers 數量時，應考慮節點可用的 CPU 資源。

關於 CPU 核心和 --workers 的關係：

	1.	CPU-bound 工作：如果每個 worker 主要進行計算密集型工作，則 worker 的數量不應超過 CPU 核心的數量（在你的情況下是 15 核心）。這是因為每個核心只能同時執行一個 worker。如果 workers 數量超過 CPU 核心，將導致 CPU 的上下文切換，影響性能。
	2.	I/O-bound 工作：如果 workers 主要是 I/O 密集型（例如等待 API 響應或文件讀寫），則可以設置比 CPU 核心數量更多的 workers。這是因為 I/O 操作通常會釋放 CPU，讓其他 workers 能夠繼續執行。實際上，在這種情況下你可以設置更多的 workers，可能是 CPU 核心數量的 2 倍或更多。

範例設置：

	•	CPU-bound 任務：如果每個 worker 都在進行計算密集型工作，例如數據處理或模擬，那麼在 15 核心的環境中，設置 15 個 workers 是合理的。超過這個數量會導致性能下降。

python hub-stress-test.py --count 100 --workers 15


	•	I/O-bound 任務：如果每個 worker 都是在進行網路請求或等待外部 API 響應，那麼你可以設置 2 倍或更多的 workers。例如，可以設置 30-40 個 workers 來充分利用 I/O 等待時間。

python hub-stress-test.py --count 100 --workers 30



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

在這個範例中，只有 user1 和 user2 會被等待完全停止，而 user3 由於停止請求未成功發送，因此不會被進一步檢查。
