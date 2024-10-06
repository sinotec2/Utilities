---
layout: default
title:  引數與執行
parent: System Stress Test
grand_parent: Kubernetes
last_modified_date: 2024-10-06 10:19:38
---

#  引數與執行

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


## 主程式

這段 Python 程式碼是一個指令行應用，用於在 JupyterHub 上執行壓力測試或清除用戶。主要功能包括創建大量用戶、啟動伺服器、模擬筆記本活動並刪除用戶。以下是詳細說明：

### 輸入參數

這段程式碼透過 `argparse` 解析命令列參數，並支援以下命令：
- **purge**: 刪除用戶。
- **stress-test**: 執行壓力測試，包括創建用戶並啟動伺服器。
- **activity-stress-test**: 模擬用戶的筆記本活動並測量伺服器反應時間。

### 輸出

程式本身不直接輸出到標準輸出，而是使用日誌系統來記錄執行過程中的訊息和錯誤。可以根據需要將日誌輸出到檔案或終端。

### 重要邏輯

1. **引入和設置**:
   - 程式首先引入了常見的 Python 庫，如 `requests`、`concurrent.futures` 和 `logging` 等。它設定了基本的日誌格式，並配置了超時和重試的參數。

2. **主函式** (`main`)：
   - 透過 `parse_args()` 解析命令列參數，並根據參數來執行相應的操作。
   - `validate()` 用於檢查參數的合法性。
   - 根據 `args.command` 的值，選擇調用不同的函式來執行相應的操作：
     - `purge_users()`：刪除用戶。
     - `run_stress_test()`：執行用戶壓力測試。
     - `notebook_activity_test()`：模擬用戶活動壓力測試。

3. **壓力測試**:
   - 當執行 `stress-test` 命令時，程式會執行如下步驟：
     1. 查找現有的壓力測試用戶。
     2. 根據需要創建缺少的用戶。
     3. 啟動新創建用戶的伺服器。
     4. 等待伺服器啟動完成。
     5. 根據 `keep` 參數的設定，決定是否保留或刪除這些用戶。

4. **筆記本活動模擬**:
   - 當執行 `activity-stress-test` 命令時，程式會模擬用戶筆記本的活動，並測量伺服器的反應時間。
   - 使用多執行緒處理來同時模擬多個用戶的活動請求。

5. **錯誤處理**:
   - 所有的主要邏輯都包裹在 `try-except` 區塊中，並且在發生錯誤時會記錄錯誤日誌，然後退出程式。

### 應用時的注意事項

- **日誌配置**：程式使用 `LOG` 來記錄所有的執行過程，應根據測試需求設定日誌輸出目標（終端或檔案）。
- **timeout 設置**：`DEFAULT_TIMEOUT` 和 `SERVER_LIFECYCLE_TIMEOUT` 設置了伺服器創建和運行過程的最大等待時間，根據環境調整這些參數可能提高測試的效率。
- **dry_run 模式**：使用 `dry_run` 參數可以在不實際執行任何操作的情況下模擬壓力測試，這對於初步測試或調試非常有用。
- **命令選擇**：根據不同的測試需求選擇相應的命令，確保伺服器和用戶的清理或保留符合預期。

這個程式對於測試 JupyterHub 在高負載情況下的表現非常有用，也能幫助管理大量用戶的伺服器維護。

### 程式碼

```python
#!/usr/bin/env python3

import argparse
from concurrent import futures
from datetime import datetime, timedelta
import functools
import json
import logging
from unittest import mock
import os
import random
import sys
import time

import requests
from requests import adapters
from urllib3.util import retry


LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
LOG = logging.getLogger('hub-stress-test')

# POST /users/{name}/servers can take over 10 seconds so be conservative with
# the default timeout value.
DEFAULT_TIMEOUT = 30

# The default timeout for waiting on a server status change (starting/stopping)
SERVER_LIFECYCLE_TIMEOUT = 60

USERNAME_PREFIX = 'hub-stress-test'

def main():
    args = parse_args()
    setup_logging(verbose=args.verbose, log_to_file=args.log_to_file,
                  args=args)
    try:
        validate(args)
    except Exception as e:
        LOG.error(e)
        sys.exit(1)

    try:
        if args.command == 'purge':
            purge_users(args.token, args.endpoint, dry_run=args.dry_run)
        elif args.command == 'stress-test':
            run_stress_test(args.count, args.batch_size, args.token,
                            args.endpoint, dry_run=args.dry_run,
                            keep=args.keep, profile=args.profile)
        elif args.command == 'activity-stress-test':
            notebook_activity_test(args.count, args.token,
                                   args.endpoint, args.workers, keep=args.keep,
                                   dry_run=args.dry_run)
    except Exception as e:
        LOG.exception(e)
        sys.exit(128)


if __name__ == "__main__":
    main()
```

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
