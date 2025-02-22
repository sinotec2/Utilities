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

- 這個範例檢討售案與權利人之間的關聯性。
- 「權利人」：此處假設權利人是個投票的群體，否同意接受方案的條件從而接受方案，他們的決定將會是售案順利售出的關鍵。
- 「貢獻度」：雖然無從得知每個權利人對售案的態度，由於售案最後可能採行多數決、也可能使用共識決，不論如何，此處定義售案成功可以平均歸功於參與售案評估的每一個權利人，如此可以計算每個權利人對群體(公司或團隊)年度成交總額的貢獻比例程度。
- 以此討論年度間的差異，找出重要關鍵權利人、或者權利人對群體的態度轉變趨勢，提供決策參考。
- 本範例為使用`pivot_tables`、sort_values`等pandas中的重要模組。

### 程式功能概述

本程式主要負責讀取不同年度的 `crawler.csv` 檔案，分析各年度的權利人姓名（name）與金額（budg）之間的關係，並計算不同姓名的影響程度。

### 最終輸出兩個 CSV 檔案

- `dfnps.csv`：篩選出 2024 年金額比例小於 2022-2023 平均值的姓名。
- `dfnpsGTavg.csv`：篩選出 2024 年金額比例大於或等於 2022-2023 平均值的姓名。

## 程式碼說明

### ** 程式輸入**

- **主要輸入**：
  - `2022_crawler.csv`
  - `2023_crawler.csv`
  - `2024_crawler.csv`
  - `2025_crawler.csv`
- **輸入格式**：CSV 檔案，包含以下欄位：
  - `姓名`：含有姓名的字串資料。範例如下`{'張○○': ['經歷1：', '服務機關(構)名稱：○○大學（○○工程系），職稱：助...]}`
  - `金額`：專案的金額。
  - `是否售出`：布林值，表示是否售出。
  - `主辦部`：該售案的主辦單位。

### ** 主要邏輯與運算**

#### **(1) 讀取 CSV 檔案**

使用 `pandas.read_csv` 讀取 CSV 檔案，並存入 `DataFrame`。

```python
fname='/Users/user1/Downloads/2024_crawler.csv'
df=read_csv(fname, encoding='utf8')
```

#### **(2) 從 `姓名` 欄位解析出姓名**

- `s2names(s)` 函數負責解析姓名，透過 `find("':")` 來定位姓名的名稱。
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

### ** 建立年度資料處理迴圈**

讀取 `2022-2025` 四年的 CSV 檔案，並針對每一筆資料：
- 使用 `s2names()` 解析 `姓名` 欄位的姓名。
- 計算權利人對該售案金額的影響程度（平均分配給該售案權利人的所有姓名）。
- 將數據存入 `years`, `names`, `budgs`, `depgr` 等陣列。

```python
for fname in fnames[:-1]:
    yr = fname[23:27]
    df = read_csv(fname, encoding='utf8')
    for i in range(len(df)):
        s = df.loc[i, '姓名']
        if type(s) != str: continue
        name_list = s2names(s)
        budg = df.loc[i, '金額'] / len(name_list)
        if not df.loc[i, '是否售出']: budg *= -1
        for name in name_list:
            names.append(name)
            budgs.append(budg)
            depgr.append(df.loc[i, '主辦部'])
            years.append(yr)
```

#### **(4) 計算每位姓名的影響比例**

建立 `pivot_table()` 來彙總 `budg` 數值，並計算該姓名佔該年度總金額的比例。

```python
pv = pivot_table(dff, index=['year', 'name'], values=['budg'], aggfunc=sum).reset_index()
yr_sum = {i: dff.loc[dff.year.astype(int) == i, 'budg'].sum() for i in range(2022, 2026)}
pv.year = [int(i) for i in pv.year]
pv['budg_rate'] = [i / yr_sum[j] for i, j in zip(pv.budg, pv.year)]
```

#### **(5) 按 `budg_rate` 排序，姓名**

```python
pvm = pivot_table(pv, index=['name'], values=['budg_rate'], aggfunc=np.mean).reset_index()
pvms = pvm.sort_values(by='budg_rate', ascending=False).reset_index(drop=True)
```

### **(6) 篩選特定條件的姓名並輸出 CSV**

- **`dfnps.csv`**: 篩選出 `2024` 影響力 **低於** `2022-2023` 平均的姓名。
- **`dfnpsGTavg.csv`**: 篩選出 `2024` 影響力 **大於或等於** `2022-2023` 平均的姓名。

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
- **`dfnps.csv`**：2024 年影響力下降的姓名。
- **`dfnpsGTavg.csv`**：2024 年影響力上升或持平的姓名。

---

## **5. 注意事項**
1. **資料清理**：確保 `姓名` 欄位為 `str` 類型，否則 `s2names()` 可能會出錯。
2. **金額計算**：若姓名人數較多，`budg` 會被平均分配，需確認該計算方式是否符合業務邏輯。
3. **年度範圍**：目前程式支援 `2022-2025`，如需擴展，請修改 `fnames` 及 `yr_sum` 相關計算。
4. **CSV 輸出格式**：最終的 `dfnps.csv` 及 `dfnpsGTavg.csv` 會按照 `percent` 由高到低排序。


