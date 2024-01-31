---
layout: default
title:  Druid數據探索
parent: Apache Druid
grand_parent: DB_servers
grand_parent: OLAP
last_modified_date: 2024-01-29 12:57:32
tags: DB_servers Druid
---

# Druid explore數據探索
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

- Will Xu (AUG 11, 2023) [Introducing Apache Druid 27.0.0](https://imply.io/blog/introducing-apache-druid-27-0-0/)：文中介紹了很多27版的特色，其中第一項就是**Explore**，可以將簡單的查詢轉成視覺化的彩色圖表。
- 入口：在上方最右邊的`...`，下拉選單中選擇指北針Explore(experimental)

![](explore_png/2024-01-31-13-29-05.png)

- 進入頁面，左方sidebar是來源(Source)，選擇資料表後，會出現欄位名稱，同樣的，點選後可以篩選(Filter)或顯示(Show)
- 