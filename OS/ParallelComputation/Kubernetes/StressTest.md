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

### 引數解析

程式說明：parse_args() 函數

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

