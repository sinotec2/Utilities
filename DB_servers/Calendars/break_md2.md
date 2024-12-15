---
layout: default
title:  break_md程式說明
parent: Calendars
grand_parent: DB_servers
last_modified_date: 2024-12-12 13:40:48
tags: calendar
---

# 將日將日曆按照屬性分配到正確的md檔案

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

- 雖然md檔案是靜態網頁，太常更新會降低其服務的速率。這邊還是交代一下階段性的成果。
- 整體作業流程

```bash
$ cat rev_cal.cs
#!/usr/bin/bash
cd /nas2/kuang/MyPrograms/GoogleCalendarAPI
source .env
/nas2/kuang/.conda/envs/py39/bin/python ical2.py
/nas2/kuang/.conda/envs/py39/bin/python break_md2.py
```

## 程式說明

這段程式碼的功能是從 CSV 檔案中提取部門事件資料，並根據這些資料更新 Markdown 文件，同時生成摘要信息。以下是對程式的詳細介紹、艱澀部分的提醒，以及修改建議。

### 輸入

- CSV 檔案：`whole.csv` 包含部門、事件、類別、時間等欄位，並解析日期。
- 環境變數：需要設定 ANTHROPIC_API_KEY 以使用 Anthropic API。

```bash
period,datetime,OutDT,event,category,department,group
1,2024-09-03 00:00:00+08:00,2024sep03_00:00tue(1d),諺-請假,同仁行程,WW,#管線組(中興+環興)
1,2024-09-04 00:00:00+08:00,2024sep04_00:00wed(1d),諺-請假,同仁行程,WW,#管線組(中興+環興)
1,2024-09-04 00:00:00+08:00,2024sep04_00:00wed(1d),陸-竹南頭份履約督導。,同仁行程,WW,#管線組(中興+環興)
1,2024-09-04 00:00:00+08:00,2024sep04_00:00wed(1d),何、揚-基隆市現場評鑑。,同仁行程,WW,#管線組(中興+環興)
```

### 輸出

- Markdown 文件：根據部門和事件類別生成對應的 Markdown 文件，並填入最新的事件摘要。

### 重要處理邏輯

- 文件讀取與處理：使用 `sub_str` 函數替換 Markdown 文件中的特定標籤（如 `lastUpdated` 和 `add{p}`），將內容更新為最新的事件摘要。
- 事件摘要生成：`summ_evnt` 函數通過調用 Anthropic API 根據部門事件生成摘要信息。
- 目錄結構管理：根據部門和事件類別創建相應的目錄結構，並將更新後的 Markdown 文件存放在正確的位置。

### 艱澀部分提醒

- API 使用：確保 ANTHROPIC_API_KEY 設置正確，否則程式會退出。
- 複製與替換邏輯： `shutil.copy` 和 `sub_str` 的使用需要注意文件是否存在，避免出現文件未找到的錯誤。
- 異常處理：目前程式中沒有包含完整的異常處理機制，可能導致運行時錯誤未被捕獲。

### 修改建議

- 異常處理：在文件操作和 API 調用中增加異常處理，以提高程式的穩定性。
- 日誌記錄：可以考慮添加日誌功能，記錄每次更新的詳細信息，方便後續查詢和錯誤排查。
- 性能優化：如果 CSV 檔案很大，可以考慮使用更高效的數據處理方法，例如使用 dask 或 modin 等庫來加速數據處理。

總結來說，這段程式碼有效地整合了事件資料的提取與更新，但在錯誤處理和性能方面還有提升的空間。

## md檔案的自動上載

```bash
$ cat /nas2/VuePressSrc/Sup.calendars/upload.cs

#!/usr/bin/bash
/usr/bin/git init
/usr/bin/git add .
dt=$(date +%Y%m%d)
/usr/bin/git commit -m "updated $dt"
/usr/bin/git push -f http://kuang:sinotec2@eng06.sinotech-eng.com:3000/Sup/calendars.git main
```
