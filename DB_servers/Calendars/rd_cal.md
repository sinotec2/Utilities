

### 程式概述

這個 Python 程式的主要功能是從 Google Calendar API 擷取事件資料，並處理這些資料以便進行進一步的分析或儲存。程式會針對特定時間範圍內的日曆事件進行查詢，將結果轉換為一個 `DataFrame`，並最終將這些資料輸出為 CSV 檔案。

### 主要模組與工具

1. **`sys`, `subprocess`**：用於系統級操作，例如執行 Shell 指令。
2. **`datetime`, `timedelta`, `timezone`**：處理日期和時間相關的操作。
3. **`pandas`**：數據處理工具，用於處理和儲存從 Google Calendar 擷取的事件。
4. **`oauth2client`, `googleapiclient`**：Google API 認證與服務操作的工具。
5. **`anthropic`**：用於對事件摘要進行分類的 NLP 工具。

### 程式詳細說明

#### 1. 指令與參數

```python
cmd = "grep title /nas2/VuePressSrc/Sup.calendars/zh/E1/*md | grep -v READ | cut -d':' -f3"
cats = subprocess.check_output(cmd, shell=True).decode('utf8').strip('\n')
ICTcalendar_id = "25ae42ff6cf09e84f742882600ca7da7374bc357b97d9c8bffad8c3dcfa226d6@group.calendar.google.com"
id_dpt = {ICTcalendar_id: 'ICT'}
```

- 這段程式碼使用 Shell 指令從特定路徑中提取檔案標題，並將其轉換為字串形式儲存在變數 `cats` 中。
- `ICTcalendar_id` 是特定 Google Calendar 的 ID，並被用於識別這些日曆的資料。

#### 2. 主函數 `main`

```python
def main(ndays, calendar_id):
    # 初始化 Google Calendar 服務
    service, _ = sample_tools.init(
        argv="", name="calendar", version="v3", doc=None,
        filename="/nas2/kuang/MyPrograms/GoogleCalendarAPI/calendar_sample.py",
        scope="https://www.googleapis.com/auth/calendar.readonly",
    )

    # 計算查詢的時間範圍
    today = (datetime.now() + timedelta(days=-1)).replace(hour=9, minute=0)
    future_dates = [today + timedelta(days=i) for i in range(ndays + 1)]
    time_min = today.strftime('%Y-%m-%dT%H:%M:00Z')
    time_max = (today + timedelta(days=ndays)).strftime('%Y-%m-%dT%H:%M:00Z')

    try:
        calendar_list_entry = next((entry for entry in service.calendarList().list().execute()["items"]
                                     if entry["id"] == calendar_id), None)
        if calendar_list_entry:
            print(calendar_list_entry["summary"])
            events_result = service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max).execute()
            events = events_result.get('items', [])

            if not events:
                return DataFrame()

            data = [process_event(e, future_dates) for e in events]
            df = DataFrame(data, columns=['datetime', 'length', 'category', 'event'])
            df['department'] = id_dpt[calendar_id]
            df['period'] = ndays
            df['group'] = calendar_list_entry["summary"]
            return df

    except client.AccessTokenRefreshError:
        print("The credentials have been revoked or expired, please re-run the application to re-authorize.")
```

- **參數**：
  - `ndays`：查詢的未來天數。
  - `calendar_id`：Google Calendar 的 ID，用於標識要查詢的日曆。
- **功能**：
  - 初始化 Google Calendar API 的服務並設定查詢的時間範圍。
  - 查詢日曆中的事件，並將其轉換為資料框 (DataFrame)。
  - 如果事件包含重複發生 (recurrence)，則進行特別處理。

#### 3. 事件處理

- **`process_event(event, future_dates)`**：根據事件的類型（單次或每週重複）進行處理。
- **`out_weekly(start_dict, end_dict, future_dates)`**：針對每週重複的事件，返回一個日期和事件的列表。
- **`out_single(start_dict, end_dict)`**：處理單次事件，返回事件的時間和摘要。

#### 4. 分類函數 `summ_cate`

```python
def summ_cate(summ):
    api_key = "your-api-key-here"  # 將 API 金鑰移至環境變數或安全的配置檔中
    client = Anthropic(api_key=api_key)
    prompt = f"我會給你一個事件的摘要，請就其內容，將其歸類在{cats}等類中的某一類，請不要說明理由，直接給類別名稱即可。事件摘要: {summ}"
    return client.messages.create(
        model='claude-3-5-sonnet-20240620',
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    ).content[0].text
```

- **功能**：使用 NLP 模型對事件摘要進行自動分類，將其歸類到先前提取的類別中。

#### 5. 主程式入口

```python
if __name__ == "__main__":
    df0 = DataFrame()
    for calID in id_dpt:
        for ndays in [1, 7, 14, 31, 90]:
            df = main(ndays, calID)
            if not df.empty:
                df0 = concat([df0, df], ignore_index=True)

    df0.set_index('period').to_csv('whole.csv')
```

- **功能**：遍歷多個日曆 ID 和多個時間範圍，將所有日曆事件合併成一個大表格並儲存為 CSV 檔案。

### 修改與擴充建議

- **API 金鑰**：將 API 金鑰移到環境變數或安全的配置文件中，不要硬編碼在程式裡。
- **錯誤處理**：增強對 API 調用的錯誤處理機制，確保程式在出現異常時不會崩潰。
- **日曆 ID 配置**：可以將日曆 ID 配置為可讀取的外部文件，以便更容易地添加或修改。

這份說明提供了一個清晰的指引，有助於新進工程師了解程式的結構和功能，並能夠順利地進行後續的修改與擴充。

