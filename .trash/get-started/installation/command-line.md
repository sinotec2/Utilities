---
layout: default
title:  使用命令列安裝 Streamlit
parent: streamlit之安裝 
grand_parent: streamlit
nav_order: 99
last_modified_date: 2025-03-26 08:32:07
tags: web
---

#  使用命令列安裝 Streamlit
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

本頁將引導您使用“venv”建立環境並使用“pip”安裝 Streamlit。這些是我們推薦的工具，但如果您熟悉其他工具，您也可以使用您喜歡的工具。最後，您將建立一個簡單的“Hello world”應用程式並運行它。如果您希望使用圖形介面來管理您的 Python 環境，請查看如何[使用 Anaconda Distribution 安裝 Streamlit](/get-started/installation/anaconda-distribution)。

## 先決條件

與任何程式設計工具一樣，為了安裝 Streamlit，你首先需要確保你的
計算機已正確設定。更具體地說，你需要：

1. **Python**

我們支援 [版本 3.8 至 3.12](https://www.python.org/downloads/)。

1. **Python 環境管理器**（建議）

環境管理器會建立虛擬環境，以隔離 Python 套件安裝專案.

我們建議使用虛擬環境，因為安裝或升級 Python 套件可能會對另一個包裹造成意外的影響。 Python 的詳細介紹環境，檢查[Python 虛擬環境：入門](https://realpython.com/python-virtual-environments-a-primer/)。

對於本指南，我們將使用 Python 附帶的「venv」。

1. **Python 套件管理器**

套件管理器負責安裝每個 Python 套件，包括 Streamlit。

對於本指南，我們將使用 Python 附帶的「pip」。

1. **僅限 MacOS：Xcode 命令列工具**

使用[這些說明]（https://mac.install.guide/commandlinetools/4.html）下載 Xcode 命令列工具
以便讓套件管理器安裝一些 Streamlit 依賴項。

1. **程式碼編輯器**

我們最喜歡的編輯是 [VS Code](https://code.visualstudio.com/download)，這也是我們在
我們所有的教程。

## 使用「venv」建立環境

1. 打開終端並導航到您的專案資料夾。

   ```bash
   cd myproject
   ```

2. 在終端機中輸入：

   ```bash
   python -m venv .venv
   ```

3. 您的專案中將出現一個名為「.venv」的資料夾。此目錄是安裝虛擬環境及其相依性的地方。

## 啟動你的環境

1. 在您​​的終端機中，根據您的作業系統，使用以下命令之一啟動您的環境。

   ```bash
   # Windows command prompt
   .venv\Scripts\activate.bat

   # Windows PowerShell
   .venv\Scripts\Activate.ps1

   # macOS and Linux
   source .venv/bin/activate
   ```
2.  一旦激活，您將在提示符號前看到括號中的環境名稱。 “（.venv）”

## 在你的環境中安裝 Streamlit

3. 在啟動環境的終端機中，輸入：

   ```bash
   pip install streamlit
   ```

4. 透過啟動 Streamlit Hello 範例應用程式測試安裝是否成功：

   ```bash
   streamlit hello
   ```

   如果這不起作用，請使用長格式命令：

   ```bash
   python -m streamlit hello
   ```

5. Streamlit 的 Hello 應用程式應該會出現在您的網頁瀏覽器的新分頁中！
<Cloud src="https://doc-mpa-hello.streamlit.app/?embed=true" height="700" />

6.完成後關閉終端機。

## 創建一個「Hello World」應用程式並運行它

1. 在專案資料夾中建立一個名為「app.py」的檔案。

   ```python
   import streamlit as st

   st.write("Hello world")
   ```

2. 任何時候您想要使用新的環境，您首先需要前往您的專案資料夾（`.venv` 目錄所在的位置）並執行命令來啟動它：

   ```bash
   # Windows command prompt
   .venv\Scripts\activate.bat

   # Windows PowerShell
   .venv\Scripts\Activate.ps1

   # macOS and Linux
   source .venv/bin/activate
   ```

3. 一旦激活，您將在終端提示符的開頭看到括號中的環境名稱。 “（.venv）”

4. 運行您的 Streamlit 應用程式。

   ```bash
   streamlit run app.py
   ```

   如果這不起作用，請使用長格式命令：

   ```bash
   python -m streamlit run app.py
   ```

5.  若要停止 Streamlit 伺服器，請在終端機中按下「Ctrl+C」。

6.  使用完此環境後，輸入以下指令返回正常 shell：

   ```bash
   deactivate
   ```

## 下一步是什麼？

閱讀我們的[基本概念](/get-started/fundamentals/main-concepts)以了解 Streamlit 的資料流模型。