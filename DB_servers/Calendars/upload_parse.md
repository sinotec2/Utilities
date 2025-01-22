---
layout: default
title:  定期上載檔案並啟動內嵌解析
parent: Calendars
grand_parent: DB_servers
last_modified_date: 2024-12-25 20:11:11
tags: calendar
---

# 定期上載檔案並啟動內嵌解析

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

- 這一題似乎也該放在AIEE/NLP/RAGFlow項目，因為是呼叫RAGFlow的API後台批次作業方式。
- 最後的完成品，是`streamlit`的伺服器，是個RAGFlow的對話框。

## 程式說明

### 目的

- [upload_parse.py](./upload_parse.py)這支程式的功能是將一個 CSV 檔案上傳到 RAGFlow 的資料集，同時在上傳之前刪除現有的文件。

### 程式說明

- 以下是程式碼的簡要概述：

1. **匯入庫**：程式碼從 `ragflow_sdk` 匯入必要的模組。
2. **定義函數**：`get_ids` 函數用來獲取指定資料集中所有文件的 ID。
3. **設置 API 連接**：初始化 RAGFlow 對象，並設置 API 金鑰和基本 URL。
4. **訪問資料集**：列出名稱為 "google_calendar_events" 的資料集，並選擇第一個資料集。
5. **刪除現有文件**：
   - 嘗試使用文件 ID 刪除資料集中的所有文件。
   - 如果沒有找到文件，則會打印 'nofile to delete'。
6. **上傳新文件**：讀取一個 CSV 檔案並將其上傳至資料集。
7. **解析上傳的文件**：最後，獲取新上傳文件的 ID，並開始異步解析。

在運行此程式碼之前，請確保將 `"ragflow-***"` 替換為聊天開啟者實際的 API 金鑰。

### 重要邏輯

1. `get_ids`函式：
  在 RAGFlow dataset中進行操作，必須指定文件`ids`，而該`ids`會在每次新增檔案隨機產生，所以行動前需先取得這些`ids`。
2. 刪除既有檔案的必要性：
  - RAGFlow會將檔案載入記憶體，而不是動態連結檔案，因此必須先刪除記憶體中既有的檔案，以便載入相同檔案名稱的內容。
  - 然而可能記憶體中沒有任何內容、將會得不到`ids`，這時程式會報錯。
3. 上載檔案必須以二進位檔案的格式載入。
  - 此處是以整個csv檔案上載，其實並不有利解讀，
  - 拆成小檔案版本尚未嘗試(拆分邏輯是？)。可能會需要`for loop`
4. 重新嵌入向量：
  - 是以`async_parse_documents(ids)`方式。
  - 將會歷遍所有上載的文件

### 程式碼

```python
$ cat ./upload_query.py
#!/opt/anaconda3/envs/py311/bin/python
from ragflow_sdk import RAGFlow, Session

def get_ids(dataset):
    documents = dataset.list_documents()
    return [document.id for document in documents]

api_key="ragflow-***"
url='http://node02.sinotech-eng.com:8080'
aid_name='GoogleCanlendarAid'

rag_object = RAGFlow(api_key=api_key,base_url=url)
dataset = rag_object.list_datasets(name="google_calendar_events")
dataset = dataset[0]
try:
    ids=get_ids(dataset)
    dataset.delete_documents(ids=ids)
except:
    print('nofile to delete')
with open('/nas2/kuang/MyPrograms/GoogleCalendarAPI/whole.csv', 'rb') as file:
    file_content = file.read()
dataset.upload_documents([{"displayed_name": "whole.csv", "blob": file_content}])
ids=get_ids(dataset)
dataset.async_parse_documents(ids)
```

