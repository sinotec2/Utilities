---
layout: default
title:  使用者管理
parent: System Stress Test
grand_parent: Kubernetes
last_modified_date: 2024-10-06 10:19:38
---

# 使用者管理

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

    