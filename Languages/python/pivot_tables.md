---
layout: default
title: pivot_table
parent:   python
grand_parent: Languages
last_modified_date: 2024-01-02 13:33:58
tags: UML
---

# pivot_table 之使用

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


### 程式功能概述

本程式主要負責讀取不同年度的 `crawler.csv` 檔案，分析各年度的評審委員（name）與決標金額（budg）之間的關係，並計算不同評審的影響程度。

### 最終輸出兩個 CSV 檔案

- `dfnps.csv`：篩選出 2024 年決標金額比例小於 2022-2023 平均值的評審。
- `dfnpsGTavg.csv`：篩選出 2024 年決標金額比例大於或等於 2022-2023 平均值的評審。

## 程式碼說明

### ** 程式輸入**

- **主要輸入**：
  - `2022_crawler.csv`
  - `2023_crawler.csv`
  - `2024_crawler.csv`
  - `2025_crawler.csv`
- **輸入格式**：CSV 檔案，包含以下欄位：
  - `評審委員`：含有評審委員的字串資料。
  - `決標金額`：專案的決標金額。
  - `是否得標`：布林值，表示是否得標。
  - `主辦部`：該標案的主辦單位。

### ** 主要邏輯與運算**

#### **(1) 讀取 CSV 檔案**

使用 `pandas.read_csv` 讀取 CSV 檔案，並存入 `DataFrame`。

```python
fname='/Users/kuang/Downloads/2024_crawler.csv'
df=read_csv(fname, encoding='utf8')
```

#### **(2) 從 `評審委員` 欄位解析出姓名**

- `s2names(s)` 函數負責解析姓名，透過 `find("':")` 來定位評審委員的名稱。
- 迴圈解析字串內容，並將姓名存入 `names` 陣列。

```python
def s2names(s):
    names = []
    i = 0
    while i < len(s):
        end = s.find(":'", i)
        if end == -1:
            break
        start = s.find("'", end - 4)
        name = s[start+1:end]
        names.append(name)
        i = end + 1
    return names
```

### **(3) 建立年度資料處理迴圈**
讀取 `2022-2025` 四年的 CSV 檔案，並針對每一筆資料：
- 使用 `s2names()` 解析 `評審委員` 欄位的姓名。
- 計算該標案決標金額的影響程度（平均分配給該標案的所有評審）。
- 將數據存入 `years`, `names`, `budgs`, `depgr` 等陣列。

```python
for fname in fnames[:-1]:
    yr = fname[23:27]
    df = read_csv(fname, encoding='utf8')
    for i in range(len(df)):
        s = df.loc[i, '評審委員']
        if type(s) != str: continue
        name_list = s2names(s)
        budg = df.loc[i, '決標金額'] / len(name_list)
        if not df.loc[i, '是否得標']: budg *= -1
        for name in name_list:
            names.append(name)
            budgs.append(budg)
            depgr.append(df.loc[i, '主辦部'])
            years.append(yr)
```

### **(4) 計算每位評審的影響比例**
建立 `pivot_table()` 來彙總 `budg` 數值，並計算該評審佔該年度總金額的比例。

```python
pv = pivot_table(dff, index=['year', 'name'], values=['budg'], aggfunc=sum).reset_index()
yr_sum = {i: dff.loc[dff.year.astype(int) == i, 'budg'].sum() for i in range(2022, 2026)}
pv.year = [int(i) for i in pv.year]
pv['budg_rate'] = [i / yr_sum[j] for i, j in zip(pv.budg, pv.year)]
```

### **(5) 按 `budg_rate` 排序評審影響力**
```python
pvm = pivot_table(pv, index=['name'], values=['budg_rate'], aggfunc=np.mean).reset_index()
pvms = pvm.sort_values(by='budg_rate', ascending=False).reset_index(drop=True)
```

### **(6) 篩選特定條件的評審並輸出 CSV**
- **`dfnps.csv`**: 篩選出 `2024` 影響力 **低於** `2022-2023` 平均的評審。
- **`dfnpsGTavg.csv`**: 篩選出 `2024` 影響力 **大於或等於** `2022-2023` 平均的評審。

```python
idx = np.where(df_name_yr.y2022 * df_name_yr.y2023 * df_name_yr.y2024 > 0)

names, percent = [], []
for i in idx[0]:
    avg = (df_name_yr.loc[i, 'y2022'] + df_name_yr.loc[i, 'y2023']) / 2.
    if df_name_yr.loc[i, 'y2024'] < avg:
        name = df_name_yr.loc[i, 'name']
        names.append(name)
        percent.append(round(100 * list(pvms.loc[pvms.name == name, 'budg_rate'])[0], 3))

dfnp = DataFrame({'name': names, 'percent': percent})
dfnps = dfnp.sort_values(by='percent', ascending=False).reset_index(drop=True)
dfnps.to_csv('dfnps.csv', index=False)
```

---

## **4. 程式輸出**
- **`dfnps.csv`**：2024 年影響力下降的評審。
- **`dfnpsGTavg.csv`**：2024 年影響力上升或持平的評審。

---

## **5. 注意事項**
1. **資料清理**：確保 `評審委員` 欄位為 `str` 類型，否則 `s2names()` 可能會出錯。
2. **決標金額計算**：若評審人數較多，`budg` 會被平均分配，需確認該計算方式是否符合業務邏輯。
3. **年度範圍**：目前程式支援 `2022-2025`，如需擴展，請修改 `fnames` 及 `yr_sum` 相關計算。
4. **CSV 輸出格式**：最終的 `dfnps.csv` 及 `dfnpsGTavg.csv` 會按照 `percent` 由高到低排序。

---

此手冊適合年輕工程師快速理解程式邏輯，並作為後續維護與擴充的參考依據。

