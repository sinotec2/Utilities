---
layout: default
title:  模板的組成及應用
parent: VuePress
grand_parent: Static Site Generators
nav_order: 99
last_modified_date: 2024-07-31 08:56:43
tags: VuPress
---

#  VPH模板的組成及應用
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

- VuePress Hope v2 雖然功能完整，但因為範例軟件包檔案龐雜、相依性綿密，經整理縮減到60mb還是太大，無法作為推廣模板。
- 此處提出殼層、核心切割處理構想，只需推廣核心模板，大小約6mb，採減法原則。
- 模板的架構、維護、應用等等細節，在此處說明嗎。
- VPH程式銜接、Gitea act_runner的設定，則見於其他網頁。

## 工作原理與架構

- 架構上，模板區分為**固定的殼層**與**變動的核心**2部分。
- 筆記會放在kernel repo的中文目錄/zh下，
    - 模板容量約為6mb、採減法、替換原則
    - 可以自行發展分支（sidebar）、
    - 切換其他Repo(navibar)
    - 如果要寫英文系統，直接在根目錄發展
- 核心模板的根目錄有工作區
    - .github/workflows/main.yml
        - CI/CD 的程序
        - 不需要維護
        - (ssh -t "mkdir -p ..."尚未解決）
    - .vuepress
        - 控制上欄與左側邊欄
        - 其他樣式控制
    - .git:要記得定期清空歷史紀錄
- 殼層共用的軟件包約有40mb、壓縮後約有10mb
    - 因為不會需要常常修改，不要存在個人倉儲
    - 日常是以壓縮檔輸入到act_runner，如果修改要記得覆蓋舊的壓縮檔
    - 殼層其他週邊軟件包經檢討，即使清除也不會大幅減少編譯時間，約略減少10-20秒

## kernel

### home README.md

### Navigators

### Sidebars

### Fronter

### Markdowns

## shell

 

## ToDo's


