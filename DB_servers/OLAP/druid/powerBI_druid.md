---
layout: default
title:  powerBI連線Druid 
parent: Apache Druid
grand_parent: DB_servers
grand_parent: OLAP
last_modified_date: 2024-01-07 20:26:18
tags: DB_servers Druid
---

# powerBI連線Druid
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

- [power bi direct query to druid](https://community.fabric.microsoft.com/t5/Desktop/power-bi-direct-query-to-druid/td-p/1942391)

## bing solutions

是的，PowerBI 可以連結到 Apache Druid 伺服器。你需要從一個空白查詢開始，然後在進階編輯器中貼上你的片段¹。但是，如果你之前沒有創建過查詢，或者你的 Druid 叢集有安全設定，那麼可能需要一些時間來完成設定¹。以下是一個簡單的連接範例¹：

```json
let  
    Query1 = Json.Document (Web.Contents ("paste_url:paste_port/druid/v2/?pretty", [Headers= [#\"Content-Type\"=\"application/json\"], Content=Text.ToBinary ( \" { \"\"queryType\"\": \"\"groupBy\"\", \"\"dataSource\"\": \"\"paste_your_table\"\", \"\"dimensions\"\": [\"\"dimension1\"\"] , \"\"granularity\"\": \"\"all\"\", \"\"aggregations\"\": [  {  \"\"name\"\": \"\"metric1\"\",  \"\"type\"\": \"\"longSum\"\",  \"\"fieldName\"\": \"\"metric1\"\"  }  ], \"\"intervals\"\": [ \"\"2020-07-27T00:00:00.000/2020-08-03T00:00:00.000\"\" ] }   \" ) ] )),  
    totable = Table.FromList (Query1, Splitter.SplitByNothing (), null, null, ExtraValues.Error),  
    expand = Table.ExpandRecordColumn (totable, \"Column1\", {\"version\", \"timestamp\", \"event\"}, {\"Column1.version\", \"Column1.timestamp\", \"Column1.event\"}) 
in  
    expand
```

請注意，這只是一個範例，你需要將其中的 `paste_url`, `paste_port`, `paste_your_table`, `dimension1`, `metric1` 等替換為你的實際值。此外，如果你的 Druid 叢集有安全設定，你可能需要添加額外的驗證頭部分。¹ 如果你需要進一步的幫助，請隨時告訴我！

來源: 與 Bing 的交談， 2024/1/29
(1) Re: How to Connect Apache Druid to Power Bi ([Desktop/Service](https://community.fabric.microsoft.com/t5/Power-Query/How-to-Connect-Apache-Druid-to-Power-Bi-Desktop-Service/m-p/3079473)).
(2) 【超详细】Apache Durid从入门到安装详细教程 - 知乎. https://zhuanlan.zhihu.com/p/558085506.
(3) 大数据Apache Druid（三）：Druid集群搭建 - 知乎. https://zhuanlan.zhihu.com/p/555432134.
(4) undefined. https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview.
