---
layout: default
title:  Hugo簡介
parent: Hugo
grand_parent: Static Site Generators
nav_order: 1
last_modified_date: 2023-06-12 08:56:43
tags: Hugo
---

# Hugo簡介
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

### Hugo 和 Jekyll比較

Hugo 和 Jekyll 都是靜態網站生成器，主要用於構建靜態網站和部落格。以下是它們在**程式說明**和**結果發表**部落格方面的一些比較：

項目|Hugo|Jekyll|說明
-|-|-|-
語言|Go|Ruby|需要編譯成css
性能|快速編譯和執行、短的時間內生成大型網站|小型和中型網站上表現不錯|
主題和佈局|支援|支援|
模板語言|Go 模板|Liquid 模板語言|
部署|任何 Web 伺服器|同左、外加原生支援GitHub Pages|

- 共同點：
  - **靜態網站生成：** Hugo 和 Jekyll 都是靜態網站生成器，生成的網站可以輕鬆地部署到各種 Web 伺服器上。
  - **主題和佈局：** 兩者都支援主題和佈局，可以根據需求進行自定義。
  - **社區支援：** Hugo 和 Jekyll 都有活躍的社區，提供了大量的文檔和支援。
  - **版本控制：** 兩者都與版本控制系統（如 Git）良好集成，這使得多人協作和版本追蹤變得更容易。
- 選擇建議：
  - 如果性能是關鍵考慮因素，並且你更傾向於 Go 語言的話，Hugo 可能是更好的選擇。  
  - 如果你在使用 GitHub Pages，或者對 Ruby 和 Liquid 模板感到更熟悉，Jekyll 也是一個強大的選擇。
  - 最終的選擇取決於你的特定需求、習慣和偏好。

### 大型靜態網站生成器

對於一個大型靜態網站，使用 Gitea 作為版本控制系統，選擇靜態網站生成器時需要考慮多個因素。以下是針對這種情況的一些建議：

1. **Hugo:**
   - **性能優勢：** Hugo 是一個以 Go 語言編寫的生成器，具有卓越的性能。這使得它在大型網站上能夠快速生成靜態文件。
   - **部署簡單：** Hugo 生成的靜態文件可以輕鬆地部署到任何 Web 伺服器上，這樣可以更容易地整合到公司的內部環境中。

2. **Jekyll:**
   - **GitHub Pages 整合：** 如果你的內部資訊揭露使用 GitHub Pages 或與 GitHub 集成，Jekyll 是一個天然的選擇，因為 GitHub Pages 原生支援 Jekyll。
   - **Ruby 生態系統：** 如果你的團隊更熟悉 Ruby，Jekyll 提供了良好的支援，也有豐富的社區和主題。

3. **VuePress:**
   - **Vue.js 生態系統：** 如果你的公司在前端使用 Vue.js，VuePress 是一個基於 Vue 的生成器，它提供了簡單的擴展性和舒適的開發體驗。
   - **容易擴展：** VuePress 允許你使用 Vue 的組件系統，這使得它對於大型內容網站的構建和擴展非常友好。

4. **Gatsby:**
   - **React 生態系統：** 如果公司在前端使用 React，Gatsby 是一個建構於 React 之上的強大生成器。
   - **動態功能：** Gatsby 具有內置的動態功能，可用於構建更豐富的靜態網站，並能夠與各種數據源整合。

選擇生成器取決於你的團隊技術棧、對特定技術的熟悉程度以及網站的需求。不同的生成器有不同的特點，根據具體需求做出選擇是關鍵。

## 安裝

- source: [Install Hugo on macOS. ](https://gohugo.io/installation/macos/)
- GO：
  - 選擇go1.21.6.darwin-amd64.pkg （[X86-64](https://go.dev/dl/)）
  - PATH settings and TEST by [Download and install](https://go.dev/doc/install)
- [Dart Sass]()

## terminology

### Dart Sass

Dart Sass 是一種 Sass（Syntactically Awesome Stylesheets）的實現，是一種 CSS 預處理器，用於簡化和改進 CSS 的撰寫。Dart Sass 是 Sass 的官方版本之一，它使用 Dart 語言編寫，並由 Sass 官方團隊維護。

Sass 允許開發者使用一些類似於編程語言的語法，例如變數、巢狀規則、混合（Mixins）等，來更有效地編寫和維護 CSS 代碼。Dart Sass 提供了一個命令行工具，也可以通過集成到許多前端開發工具中，例如構建工具和集成開發環境。

要使用 Dart Sass，你需要安裝 Dart 環境，然後安裝 Dart Sass 套件。以下是一些常見的 Dart Sass 使用方式：

1. **使用命令行：** 透過命令行執行 Dart Sass，例如：
   ```bash
   sass input.scss output.css
   ```

2. **集成到構建工具：** 許多構建工具（如Webpack、Gulp、npm scripts 等）可以集成 Dart Sass，使其成為項目構建流程的一部分。

3. **使用 Sass 的擴展：** 一些集成開發環境和編輯器擴展可以直接支援 Sass，提供語法高亮、編譯、錯誤檢測等功能。

4. **通過線上編譯器：** 一些線上服務提供 Sass 的線上編譯，你可以在線上編寫 Sass 代碼，然後獲取編譯後的 CSS。

請注意，Dart Sass 和 Ruby Sass 是 Sass 的兩個主要實現，它們在某些方面可能有些區別。當前，官方推薦使用 Dart Sass，因為它是 Sass 生態系統的主要發展方向。