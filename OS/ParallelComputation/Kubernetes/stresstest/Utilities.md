---
layout: default
title:  共用程式
parent: System Stress Test
grand_parent: Kubernetes
last_modified_date: 2024-10-06 10:19:38
---

#  共用程式

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

## 紀錄測試過程與結果

函式說明：`setup_logging(verbose=False, log_to_file=False, args=None)`

此函式負責設定應用程式的日誌記錄系統，使開發者或系統管理員能夠監控並記錄程式的執行情況。日誌輸出可以控制到標準輸出，或存入文件（如使用者選擇了 --log-to-file 參數）。這個函式還會處理未捕獲的異常並將其記錄到日誌中。

### 輸入參數：

	•	verbose (bool, 預設: False)：
	•	控制日誌的詳細程度。如果為 True，日誌將包括更多的 debug 級別訊息。
	•	log_to_file (bool 或 str, 預設: False)：
	•	如果為 True，程式會將日誌輸出寫入文件。當指定為 str 時，日誌會寫入該文件路徑。若不指定具體的文件名，會自動生成一個文件存入 /tmp 目錄中。
	•	args (Namespace, 預設: None)：
	•	傳入程式的參數對象（通常是由 argparse 解析的命令行參數）。此參數用來記錄程式啟動時的參數，但會遮蔽敏感資訊（如 API token）。

### 功能詳解：

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

### 輸出：

	•	無明確返回值：此函式的主要目的是設置日誌系統及捕捉異常，沒有明確的返回值。當發生異常時，會將異常訊息記錄到日誌中。

### 應用場景中的注意事項：

	1.	檔案路徑權限：當生成日誌文件時，必須確保應用程式對 /tmp 或指定的路徑有寫入權限，否則會引發錯誤。
	2.	API Token 安全性：日誌記錄時會遮蔽敏感的 API token，以防洩露。應確保在任何情況下，不要將這些敏感資訊記錄到日誌中。
	3.	異常追蹤：未捕捉的異常會被記錄在日誌中，這對於程式故障的診斷非常有用，因此在設計生產環境中的日誌時應謹慎設置。


## 計時器函式

函式說明：`timeit(f)`

這個函式是一個裝飾器，用來計算並記錄某個函式的執行時間。當一個被裝飾的函式執行完成後，timeit 會自動計算該函式從開始到結束所耗費的時間，並將結果記錄到日誌中。

### 輸入參數：

	•	f：被裝飾的函式。它是一個任意函式，timeit 裝飾器會測量這個函式的執行時間並記錄結果。

### 功能詳解：

1.	裝飾器機制：
•	使用 `functools.wraps(f)` 來保留原函式的元數據，如函式名稱、文件、文檔字串等。這樣，裝飾後的函式仍然能夠像原函式一樣被辨識。
2.	執行時間計算：
•	`start_time = time.time()`：記錄函式執行前的時間戳。
•	在函式執行完成後，使用 `time.time() - start_time` 計算函式執行過程中耗費的時間。
3.	日誌記錄：
•	`LOG.info('Took %.3f seconds to %s', ...)`：記錄被裝飾函式的執行時間，格式化顯示到小數點後三位。
•	`f.__name__`：使用被裝飾函式的名稱來提供更加清晰的日誌信息。
4.	`try-finally` 機制：
•	裝飾器確保函式的執行時間即使在函式執行過程中發生異常時也能被正確記錄。`try` 區塊內執行函式，無論函式是正常結束還是拋出異常，`finally `區塊都會在結束時記錄時間。

### 輸出：

	•	裝飾後的函式：返回一個函式 wrapper，它是被裝飾函式的包裝版本，計算該函式的執行時間，並且不改變其輸入與輸出行為。

### 應用場景中的注意事項：

	1.	效能測試與調試：這個裝飾器非常適合在測試或調試過程中使用，可以迅速了解某些函式的執行效率。但在生產環境中，應控制日誌輸出的頻率，避免過多的 I/O 操作影響性能。
	2.	日誌配置：確保 LOG 變數已正確配置，且應根據需要設定適當的日誌等級（如 INFO 或 DEBUG），以便在適當的日誌層級下查看執行時間。
	3.	異常情況的覆蓋：無論函式是否正常返回或拋出異常，timeit 都會記錄其執行時間。因此，可以放心應用於那些有可能會拋出異常的函式中。

### 範例：

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

 