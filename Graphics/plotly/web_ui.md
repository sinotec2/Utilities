---
layout: default
title:  web UI
parent: plotly程式庫
grand_parent: Graphics
last_modified_date: I2024-02-20 14:48:38
tags: plotly graphics
---

#  web UI
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

Streamlit 是一個專為 Python 設計的函式庫，但在 .NET 和 JavaScript 生態系統中，也有類似 Streamlit 的工具和框架，可以用於快速建立資料驅動的 Web 應用。

### .NET 生態系中的方案

1. **Blazor**：
 - **描述**：Blazor 是 Microsoft 提供的框架，允許使用 C# 和 .NET 來建立互動式 Web 應用程式。它可以運行在伺服器端（Blazor Server）或客戶端（Blazor WebAssembly）。
 - **優點**：使用 C# 編寫程式碼，強型別系統，良好的整合 .NET 生態系統，元件模型支持，適合建構複雜的企業級應用。
 - **範例程式碼**：
 ```csharp
 @page "/counter"

 <h3>Counter</h3>

 <p>Current count: @currentCount</p>

 <button class="btn btn-primary" @onclick="IncrementCount">Click me</button>

 @code {
 private int currentCount = 0;

 private void IncrementCount()
 {
 currentCount++;
 }
 }
 ```

2. **ASP.NET Core with Razor Pages**：
 - **描述**：ASP.NET Core 是一個跨平台的高效能框架，用於建立現代、基於雲端的 Web 應用。 Razor Pages 是 ASP.NET Core 中的程式設計模型，讓頁面開發變得更簡單和更有效率。
 - **優點**：與 ASP.NET Core 框架緊密整合，豐富的功能，強大的安全性和效能，適合企業級應用開發。
 - **範例程式碼**：
 ```csharp
 public class IndexModel : PageModel
 {
 public void OnGet()
 {
 }
 }
 ```

### JavaScript 生態系中的方案

1. **Dash by Plotly**（Python）：
 - **描述**：雖然 Dash 主要是為 Python 設計的，但它有 JavaScript 擴展，可以透過 React 元件進行擴展。
 - **優點**：專注於資料視覺化，具有強大的互動功能，適合需要豐富圖表和互動的應用。
 - **範例程式碼**（Python 部分）：
 『`python
 import dash
 import dash_core_components as dcc
 import dash_html_components as html

 app = dash.Dash(__name__)

 app.layout = html.Div(children=[
 html.H1(children='Hello Dash'),

 html.Div(children='''
 Dash: A web application framework for Python.
 '''),

 dcc.Graph(
 id='example-graph',
 figure={
 'data': [
 {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
 {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'NYC'},
 ],
 'layout': {
 'title': 'Dash Data Visualization'
 }
 }
 )
 ])

 if __name__ == '__main__':
 app.run_server(debug=True)
 ```

2. **React**：
 - **描述**：React 是一個用於建立使用者介面的 JavaScript 程式庫，特別適用於建立單頁應用程式（SPA）。它提供了一個元件模型，方便多用和組合 UI 元件。
 - **優點**：強大的組件生態系統，高度靈活和可擴展，廣泛的社區支援和資源，適合構建各種類型的 Web 應用。
 - **範例程式碼**：
 ```javascript
 import React, { useState } from 'react';

 function Counter() {
 const [count, setCount] = useState(0);

 return (
 <div>
 <h1>Counter</h1>
 <p>Current count: {count}</p>
 <button onClick={() => setCount(count + 1)}>Click me</button>
 </div>
 );
 }

 export default Counter;
 ```

這些工具和框架在各自的生態系統中提供了類似 Streamlit 的功能，能夠幫助開發者快速建立互動式的資料驅動 Web 應用。

