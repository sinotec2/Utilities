---
layout: default
title:  Calendar Dimensions 
parent: Calendars
grand_parent: DB_servers
last_modified_date: 2024-08-21 14:52:11
tags: calendar
---

# 日曆資料庫的維度

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

### 所有變數或維度

- 事件時間：可重複、精確到5分鐘、可篩選、可排序
- 事件名稱：可能重複
- 事件類別（會議、報告、行程、其他）
- 分組（calID）：與部門相依、一對一
- 部門：與責任中心相依、一對一
- 責任中心：可在VPH類別合併
- 時距群組：
  - 1/7/14/30/90/180/365共7組、
  - 與事件相依、群組具有相容、階層關係
  - 雖然這項變數只是為篩選方便，但也有發展機會，
    - 例如交給LLM回答：這區間前5項最重要的事件，篩除重複的事件。

### 重複事件的篩選與輸出

