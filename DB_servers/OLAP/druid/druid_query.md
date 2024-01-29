---
layout: default
title:  Druid查詢範例
parent: Apache Druid
grand_parent: DB_servers
grand_parent: OLAP
last_modified_date: 2024-01-29 12:57:32
tags: DB_servers Druid
---

# Druid查詢範例
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

- 

```sql
SELECT
  廢棄物代碼,
  SUM(申報量) AS sum_申報量
FROM df0_clean
WHERE 事業機構管編 = 'L0200473'
GROUP BY 廢棄物代碼
ORDER BY sum_申報量 DESC
```