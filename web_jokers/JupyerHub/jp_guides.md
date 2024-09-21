---
layout: default
title:  JPH 使用指引
parent: 地端JupyterHub伺服器
grand_parent: Web Jokers
last_modified_date: 2024-09-21 14:21:19
tags: Jupyter notebook

---

# Jupyter notebook/SES JPH 使用指引

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

- Jupyter notebook 是以網頁瀏覽器作為平台、提供執行/發展python專案的整合發展環境(Integrated Development Environment, IDE)，因此其畫面操作非常直覺，網路上也有非常多的指引教學，此處推介幾處作為參考，實際上機作業之後就能順利上手。
- 對於習慣鍵盤作業方式的老手，此處也列出減碼表作為參考對照。
- 作為地端的遠端計算伺服器，Sinotech-Eng Service JupyterHub的使用，也有些注意事項需要說明。

## 推介使用說明

- [kiwi lee(2020)@Medium](https://sean22492249.medium.com/skiwitch-talk-code-creates-the-world-2-f848557997e6)
  - 作者介紹Jupyter的特點很好記：Debug Fast/Display Easy/Extension Huge/Support Good
  - 安裝：這是在個人電腦上的程序，JupyterHub免安裝、免啟動，直接用瀏覽器開啟伺服器就好。

## 重要快速鍵

- source: [notebook.community Jupyter Notebook 的快速鍵](https://notebook.community/karst87/ml/00_basic/901_JupyterNotebook%20的快捷键)
- 命令模式 (按鍵 Esc 開啟)
- Shift-Enter : 執行本單元，選取下個單元
- Ctrl-Enter : 運行本單元
- Alt-Enter : 運行本單元，在其下方插入新單元
- Shift-J : 擴大選取下方單元
- A : 在上方插入新單元
- B : 在下方插入新單元
- X : 剪切選取的單元
- C : 複製選取的單元
- Shift-V : 貼到上方單元
- V : 貼到下方單元
- Z : 恢復刪除的最後一個單元
- D D : 刪除選取的單元
  
## 地端伺服器使用說明

### 位置與資源

- 個別端口：[node01.sinotech-eng.com:8080](http://node01.sinotech-eng.com:8080/)
- 平衡負載同一入口(建置中)
- 個別使用者可以使用的計算資源
  - CPU：2核
  - 記憶體：4GB
  - 儲存空間：10GB(暫時)  

### 帳密註冊

- 並無後台資料庫進行帳密註冊的蒐集管理。帳密註冊只提供單一登入(Single Sign On, SSO)使用。系統將以cookies做為辨識。
- 伺服器重啟之前，系統只認使用者的本機cookies，系統沒有設計**登出**機制。
- 如需以另一組帳密登入，需刪除瀏覽器的訪問紀錄。

### 左側面板切換

- 自上到下JupyterHub左側面板的分頁依序是
  - 檔案清單：列出使用者目前在伺服器虛擬機上的檔案，可以按照名稱、時間排序。
  - 核心清單
  - 筆記目錄（新）
  - 插件清單（新）
- 不同於個人版的 Jupyter Notebook, JupyterHub 將檔案清單、核心清單等等功能集中到左側欄框面板，而不再是可以關閉的網頁分頁，以避免被使用者不小心關閉了、找不到內容。
- 地端的 JupyterHub 與網路版的[JupyterLite](https://jupyter.org/try-jupyter/lab/)功能又多了插件(Plugins)的列表，點選後會在左側面板中出現伺服器提供的插件清單。

### 檔案傳送

- JupyterHub 是個遠端的伺服器平台，因此會有檔案上、下載的傳輸需求。這可以
- 在左側面板的檔案清單中進行，或
  - 點選上載(Upload Files)符號，將檔案上載到伺服器。
  - 下載：需點選檔案後按滑鼠出現選項下載。**不會**詢問下載目錄，一律下載到本機個人的`下載`(Downloads)目錄。
  - **無法**上/下載目錄。但可以執行`tar`指令，建議先將整個目錄壓縮成`tgz`(`tar -cvfz Dir.tgz Dir/*`)再上/下傳。
- 瀏覽列`File`下拉選單中進行

### 瀏覽與執行

- 點選(雙擊)檔案後會在中央面板出現檔案內容。
  - 如果是`ipynb`檔案，即為一般的Jupyter notebook檔案，執行方式可以參考[前述使用說明](#推介使用說明)。
  - 如果是其他類型的檔案，會按照其附加檔名開啟相應的顯示器或編輯器。
- 正常狀態下進入 JypyterHub 伺服器畫面會出現Launcher(開啟空白ipynb或終端機的功能選項入口)，如果分頁不慎關閉了，也可以從瀏覽列`File`下拉選單中再此開啟。

### 使用者環境的建置與啟用

- 