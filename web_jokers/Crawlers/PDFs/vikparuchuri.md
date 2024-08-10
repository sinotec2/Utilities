---
layout: default
title:  pdf2md檔案之AI轉換
parent: PDF檔案之下載與整理
grand_parent: Crawlers
nav_order: 99
last_modified_date: 2024-01-25 09:22:25
tags: Crawlers pdf
---

#  pdf2md檔案之AI轉換

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

- 一般文件**圖表隨文**的作法，雖然對讀者很方便，對程式卻很干擾，如何將圖、表、文三者區分開來解析，是一大挑戰！
- 除了**圖表隨文**、還有跳頁、頁首頁尾、2欄、轉置等等問題。
- [GitHub vikparuchuri/marker](https://github.com/VikParuchuri/marker)
- 範例在L:\nas2\sespub\epa_reports\B27\1070731A_台中發電廠新建燃氣機組計畫環境影響說明書\outputs\C07 有個範例，
- 把PDF轉譯成md檔含圖表。真的是大突破!
- 環境在L40 
- 指令：'conda activate py39;  marker_single  C07.PDF outputs --langs Chinese'
