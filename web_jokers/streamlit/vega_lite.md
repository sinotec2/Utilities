---
layout: default
title: vega_lite
parent: streamlit
grand_parent: Web Jokers
nav_order: 99
last_modified_date: 2025-03-26 08:32:07
tags:
  - web
---
# vega_lite

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


## graph types
- [Single-View Plots](https://vega.github.io/vega-lite/examples/#single-view-plots)
    - [Bar Charts](https://vega.github.io/vega-lite/examples/#bar-charts)
    - [Histograms, Density Plots, and Dot Plots](https://vega.github.io/vega-lite/examples/#histograms-density-plots-and-dot-plots)
    - [Scatter & Strip Plots](https://vega.github.io/vega-lite/examples/#scatter--strip-plots)
    - [Line Charts](https://vega.github.io/vega-lite/examples/#line-charts)
    - [Area Charts & Streamgraphs](https://vega.github.io/vega-lite/examples/#area-charts--streamgraphs)
    - [Table-based Plots](https://vega.github.io/vega-lite/examples/#table-based-plots)
    - [Circular Plots](https://vega.github.io/vega-lite/examples/#circular-plots)
    - [Advanced Calculations](https://vega.github.io/vega-lite/examples/#advanced-calculations)
- [Composite Marks](https://vega.github.io/vega-lite/examples/#composite-marks)
    - [Error Bars & Error Bands](https://vega.github.io/vega-lite/examples/#error-bars--error-bands)
    - [Box Plots](https://vega.github.io/vega-lite/examples/#box-plots)
- [Layered Plots](https://vega.github.io/vega-lite/examples/#layered-plots)
    - [Labeling & Annotation](https://vega.github.io/vega-lite/examples/#labeling--annotation)
    - [Other Layered Plots](https://vega.github.io/vega-lite/examples/#other-layered-plots)
- [Multi-View Displays](https://vega.github.io/vega-lite/examples/#multi-view-displays)
    - [Faceting (Trellis Plot / Small Multiples)](https://vega.github.io/vega-lite/examples/#faceting-trellis-plot--small-multiples)
    - [Repeat & Concatenation](https://vega.github.io/vega-lite/examples/#repeat--concatenation)
- [Maps (Geographic Displays)](https://vega.github.io/vega-lite/examples/#maps-geographic-displays)
- [Interactive](https://vega.github.io/vega-lite/examples/#interactive)
    - [Interactive Charts](https://vega.github.io/vega-lite/examples/#interactive-charts)
    - [Interactive Multi-View Displays](https://vega.github.io/vega-lite/examples/#interactive-multi-view-displays)
- [Community Examples](https://vega.github.io/vega-lite/examples/#community-examples)
## [Interactive Charts](https://vega.github.io/vega-lite/examples/#interactive-charts)

- Bar Chart with Highlighting on Hover and Selection on Click
- Histogram with Full-Height Hover Targets for Tooltip
- Interactive Legend
- Scatterplot with External Links and Tooltips
- Rectangular Brush
- Area Chart with Rectangular Brush
- Paintbrush Highlight
- Scatterplot Pan & Zoom
- Query Widgets
- Interactive Average
- Multi Series Line Chart with an Interactive Line Highlight
- Multi Series Line Chart with an Interactive Point Highlight
- Multi Series Line Chart with Labels
- Multi Series Line Chart with Tooltip
- Multi Series Line Chart with Tooltip
- Isotype Grid
- Brushing Scatter Plot to show data on a table
- Selectable Heatmap
- Bar Chart with a Minimap
- Interactive Index Chart
- Focus + Context - Smooth Histogram Zooming
- Dynamic Color Legend
- Search Input
- Change zorder on hover
### **一、圖表類型分類**
#### **1. 條形圖（Bar Chart）**
- 懸停高亮、點擊選擇的條形圖
- 帶迷你圖的條形圖
#### **2. 直方圖（Histogram）**
- 全高懸停提示工具提示的直方圖）
- 焦點+上下文平滑縮放直方圖）
#### **3. 散點圖（Scatterplot）**
- 帶外部鏈接和工具提示的散點圖
- 平移縮放散點圖
- 刷選散點圖聯動表格數據
- 畫筆高亮散點圖
- 矩形刷選散點圖
#### **4. 面積圖（Area Chart）**
- 帶矩形刷選的面積圖
#### **5. 折線圖（Line Chart）**
- 交互式線條高亮的多系列折線圖
- 交互式點高亮的多系列折線圖
- 帶標籤的多系列折線圖
- 帶工具提示的多系列折線圖（重複項，可合併)
- 具互動平均值的折線圖
- 互動指數圖表（可能為折線圖變種）
#### **6. 熱圖（Heatmap）**
- 可選擇的熱圖
#### **7. 其他特殊圖表**
- 等距網格圖（常用於數據可視化中的圖標排列）
### **二、交互功能分類**
#### **1. 懸停與高亮（Hover & Highlighting）**
- 懸停高亮（如條形圖、折線圖）
- 懸停時改變層級- 畫筆高亮（通過選框動態高亮數據點）
- 直方圖全高懸停觸發工具提示
#### **2. 點擊與選擇（Click & Selection）**
- 點擊選擇（如條形圖）
- 可點擊選擇的熱圖
#### **3. 刷選與區域選擇（Brushing）**
- 矩形刷選工具（用於框選數據範圍）
- 散點圖刷選聯動表格
- 面積圖矩形刷選
#### **4. 縮放與導航（Zoom & Navigation）** 
- 散點圖平移縮放（Scatterplot Pan & Zoom） 
- 焦點 + 上下文 
- 直方圖平滑縮放（Smooth Histogram Zooming，焦點+上下文模式） 
- 迷你圖導航（Minimap，如條形圖中的縮略圖） 
#### **5. 工具提示與標籤（Tooltips & Labels）** 
- 懸停提示（Tooltips，如散點圖、折線圖） 
- 資料標籤（Labels，如折線圖直接標註數值） 
### **三、元件與控件分類** 
#### **1. 圖例（Legend）** 
- 互動式圖例（Interactive Legend，如點擊切換系列顯示） 
- 動態顏色圖例（Dynamic Color Legend，隨資料變化更新） 
#### **2. 外部互動元件** 
- 查詢控件（Query Widgets，如篩選器、下拉菜單） 
- 搜索輸入框（Search Input，用於資料過濾） 
- 外部連結（External Links，散點圖中鏈接到外部頁面） 
#### **3. 資料聯動（Data Linking）** 
- 散點圖與表格資料聯動（Brushing Scatter Plot to show data on a table） 
### **四、重複項與說明** 
- **含工具提示的多系列折線圖** 出現兩次，可合併為一項。 
- **互動指數圖** 可能屬於折線圖變種，需結合具體場景判斷。 
- **圖示網格** 屬於非傳統統計圖表，常用於資訊圖表設計。
##  [Interactive Multi-View Displays](https://vega.github.io/vega-lite/examples/#interactive-multi-view-displays)

### **一、按交互功能與技術分類** 
#### **1. 強調交互過濾與高亮的工具/方法** 
- **Crossfilter (Filter)** 
 - 功能：基於多維數據的過濾交互，用於動態篩選數據子集。 
 - 特點：通過不同視覺元素（如圖表、濾鏡）的聯動，實現數據的交叉過濾。 
- **Crossfilter (Highlight)** 
 - 功能：在Crossfilter基礎上強化**高亮顯示**功能，用於標註關鍵數據點或子集。 
 - 特點：強調交互時的視覺反饋（如顏色高亮、邊框突出），幫助用戶聚焦重點。 
#### **2. 交互式多維數據視覺化** 
- **Interactive Scatterplot Matrix** 
 - 功能：通過多個散點圖的矩陣排列，展示多變量之間的相關性。 
 - 特點：支持交互式選擇（如單擊、框選），實時更新子圖數據，適用於探索性數據分析（EDA）。 
- **Interactive Dashboard with Cross Highlight** 
 - 功能：綜合多個視覺組件（如圖表、地圖、表格）的交互式儀表板，支持組件間的高亮聯動。 
 - 特點：用戶操作某一組件時（如選中數據點），其他組件同步高亮顯示相關數據，增強數據關聯性分析。 
### **二、按應用主題與場景分類** 

- **Seattle Weather Exploration** 
 - 主題：西雅圖氣象數據的可視化探索（如溫度、降水、季節性趨勢等）。 
 - 場景：氣象分析、環境科學或城市規劃。 
 - taking summaries in block area(time line) 
- **Connections among Major U.S. Airports** 
 - 主題：美國主要機場的航線網絡連接分析（如航班流量、樞紐機場影響力等）。 
 - 場景：交通運輸、航空物流或地理網絡分析。
 - hover lines showing
- **An interactive scatter plot of global health statistics by country and year** 
 - 主題：全球各國健康指標（如預期壽命、嬰兒死亡率、醫療資源等）的時空分布與關聯分析。 
 - 場景：公共衛生、國際發展或社會科學研究。
 - 年度左右拉bar

## 參考

- case example: [資料科學第六週-期中了！用Streamlit展示文字資訊與圖表(**阿盧老師Coding嚕**2024)](https://codinglu.tw/index.html)
- official sites [st.line_chart](https://docs.streamlit.io/develop/api-reference/charts/st.line_chart)
- [Data Visualisation in Data Science](https://vda-lab.github.io/visualisation-tutorial/index.html)
 - [Vega-Lite tutorial](https://vda-lab.github.io/visualisation-tutorial/vegalite_landing_page.html)