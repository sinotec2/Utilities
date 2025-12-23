---
layout: default
title: Front End Frameworks
parent: Web Jokers
nav_order: 99
last_modified_date: 2025-10-13 14:40:16
tags: web
---

# 前端框架
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

前端框架是一套預先設計好的程式碼結構，用於簡化和組織網頁應用程式的開發，以解決傳統手動編寫HTML、CSS 和JavaScript 程式碼時遇到的程式碼散亂、重複和難以維護的問題。 

常見的前端框架包括React、Vue.js 和Angular，它們提供結構性的方式來管理應用程式的複雜度、提升開發效率並減少冗餘程式碼。 

## 前端框架的優點

- 提升開發效率： 提供許多內建功能（如路由管理、狀態管理），讓開發者能專注於應用程式的特定功能，而不是處理常見問題。 
- 減少重複程式碼： 框架鼓勵使用元件化方式，讓程式碼可重複使用，使程式碼更簡潔易讀。 
- 提高可維護性與擴展性： 提供明確的組織結構和模式，特別是在大型專案中，能讓程式碼更容易管理和擴展。 
- 解決跨瀏覽器問題： 過去瀏覽器在處理JavaScript 時存在差異，框架（例如早期的jQuery）能提供統一的介面來處理這些問題。 

## 常見的前端框架

- React： 由Facebook 開發，適用於中大型應用程式，以其元件化的設計和彈性著稱。 
- Vue.js： 輕量且靈活，適合初學者和小型專案，同時也可用於大型應用，其開發模式（如MVVM）易於理解。 
- Angular： 由Google 開發，是一個功能完善的框架，特別適用於大型和複雜的應用程式開發，基於組件和指令式HTML。 
- Svelte： 一個較新的選擇，不同於其他框架，它在建構時期會將程式碼編譯成高效的原生JavaScript。 

## 如何選擇框架？

選擇哪一個框架取決於多種因素，包括： 

- 專案規模與複雜度： 大型專案可能更適合Angular，而中小型專案可能更適合React 或Vue。
- 團隊技能和時間： 考量團隊成員現有的知識和技能，以及專案的時程和預算。

## 名詞解釋

### MVVM

以下說明依據你提供的文件內容與一般前端工程實務，針對「MVVM」做中文解釋，並補充與前端框架（如你文件提到的 Vue/React/Angular 與 ECharts 整合）相關的實作重點。內容以清楚、可重現為導向。

#### 什麼是 MVVM

- MVVM 是一種軟體架構設計模式，全名為 Model-View-ViewModel。
- 目的：將使用者介面（UI）與業務/資料邏輯分離，讓開發、測試與維護更容易。

#### 三個主要角色

- Model（模型）
  - 負責資料與業務邏輯（例如從 API 取得的資料結構、驗證、儲存等）。
  - 不包含與 UI 直接相關的顯示邏輯。
- View（視圖）
  - 使用者實際看到與互動的介面（HTML、CSS、圖表容器等）。
  - 不直接處理業務邏輯；只描述要顯示的內容與交互元件（例如 ECharts 的 DOM 容器）。
- ViewModel（視圖模型）
  - 位於 View 與 Model 之間，承擔資料轉換、狀態管理與接合 UI 事件的責任。
  - 負責將 Model 的資料轉為 View 可用的格式（例如把後端回傳的 result 轉成 ECharts 的 option 中的 data、legend、xAxis 等）。
  - 處理使用者互動（按鈕、點擊圖表事件）並更新 Model 或通知 View 更新。

#### MVVM 的運作方式（流程）

1. Model 更新（如 API 回來新資料）。
2. ViewModel 接收或取用 Model 的資料，做必要的轉換或合併（資料清洗、格式化）。
3. ViewModel 將格式化後的資料暴露給 View（通常透過資料綁定或設定函式）。
4. View 自動（或透過框架）反映新的資料；反之，使用者操作 View（例如點擊圖表）會由 ViewModel 接手處理並可能更新 Model。

#### 為什麼常用在前端（與框架的關聯）

- 現代前端框架（如 Vue、Angular）本身就是以 MVVM/類 MVVM 概念實現的：Component 作為 View + ViewModel 的結合，透過雙向綁定或單向資料流把資料與 UI 綁起來。
- 在你提供的文件中有提到「會把圖表做成 component、將資料用 AJAX / fetch 取得並做 mapping」，這正是 ViewModel 負責的工作：取得 result（Model），轉為 ECharts option（供 View 使用）並處理 chart.on('click') 等事件，示例如下（概念性）：
  - Model：後端 API 回傳的 result（包含 name、attr、AVG、OBP、SLG 等欄位）。
  - ViewModel：在 component 裡 fetch 資料後產生 option 物件（title、legend、xAxis、series）。
  - View：一個有固定寬高的 div，echarts.init 並 setOption(option) 顯示圖表。

與你提供內容的對應（實務重點）

- 在 ECharts 範例中，setOption 使用的一大塊資料就是從 Model（AJAX/Flask）來的，ViewModel 角色會：
  - 驗證與清洗 result（例如確保 result['attr'] 為月份陣列、數值陣列長度一致）。
  - 建構 legend 列表與 series 物件陣列（如範例中的 AVG/OBP/SLG）並放入 option 中。
  - 綁定互動事件（chart.on('click', handler)）並在 handler 中決定要向後端發 request 或更新本地狀態。
- 若專案使用 Vue，則通常在 component 的 data/computed/methods（或 setup + reactive）中實作 ViewModel 行為；若使用純 JS，也可以把這些邏輯封在一個 class 或 module 中，讓 view（DOM 與 echarts init）只負責呈現。

簡短範例（概念性流程）

1. fetch('/api/data') → 回傳 result（Model）。
2. viewModel.process(result) → 回傳 option（轉換、填補缺值、格式化）。
3. view.doRender(option) → 呼叫 echarts.init + setOption。
4. user click → chart.on('click', e) → viewModel.handleClick(e) → 可能更新 Model 或導向其他畫面。

#### 總結要點

- MVVM 幫助把「資料取得/處理」與「UI 呈現」分離，對大型或可維護的前端專案很有幫助。
- 在實作 ECharts 圖表時，把 data fetch / mapping / option 建構 / 事件處理等邏輯放在 ViewModel（或 component 的邏輯層）可以讓 View（DOM、圖表初始化與渲染）更乾淨且可重用。

### DOM

DOM，即文件物件模型（Document Object Model），是將HTML或XML文件轉換為樹狀結構的程式介面。 

它讓程式語言（如JavaScript）可以存取、修改文件內容、樣式及結構，並可為節點附加事件處理器。 

本質上，DOM是一個將網頁與程式語言連結起來的橋樑，瀏覽器透過這個模型來理解和操作網頁。 


