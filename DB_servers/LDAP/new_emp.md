---
layout: default
title:  LDAP
parent: DB_servers
last_modified_date: 2024-12-20 10:51:11
permalink: /DB_servers/LDAP/
has_children: true
tags: LDAP
---

{: .fs-6 .fw-300 }

# LDAP資料庫的新增

## Table of contents

{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 背景

- 新增同仁的資料是LDAP的日常，除了同仁的基本資料之外，最重要的是加入技術群組，以使用相對應的資源。
- 除了批次修改的做法之外，因同仁是個別報到，每個月最多2~4人，因此會需要每次添入技術群組。
- 因為技術組並不是集團所認定的正式組織，並不在MIS的制式資料庫，因此會需要人工加入，不能自帶。

### 程式目的

這段程式碼用於透過 `python_freeipa` 庫與 FreeIPA 伺服器互動，執行以下操作：

1. **連接 FreeIPA**：建立與伺服器的連線，使用 `admin` 帳戶登入。
2. **新增使用者**：根據提供的員工資料（如姓名、部門、職位等）來新增使用者。
3. **設定員工資料**：員工資料中的部門名稱會自動映射為對應的部門編號，並且密碼預設為員工編號的重複值。
4. **分組操作**：將使用者加入對應的使用者組（如 `carbon`）。
5. **結束操作**：登出 FreeIPA。

### 注意事項
- 確保 `python_freeipa` 庫已安裝並設定正確。
- `ldapmember/group_id.csv` 應包含有效的群組名稱與 GID。
- `DeptName` 必須與字典中的部門名稱匹配。

## 輸入輸出

### 程式輸入

1. **員工資訊** (`user` 字典)：包含員工編號、部門名稱、職務、姓名、使用者名稱和分組名稱等。
2. **部門對應字典** (`deptDict`)：定義部門名稱與部門編號的對應關係。
3. **群組資訊檔案** (`ldapmember/group_id.csv`)：提供群組名稱與 GID 的對應。

### 程式輸出

1. 在 FreeIPA 伺服器上新增一個包含以下資訊的使用者：
   - 姓名（包含姓與名）。
   - 電子郵件地址。
   - 部門與對應編號。
   - 群組成員關係。
2. 自動完成群組關聯，將新使用者添加至指定群組。

### 重要邏輯

1. **部門名稱轉換**：根據 `DeptName` 自動從 `deptDict` 查找並設定部門編號。
2. **密碼生成**：預設密碼為員工編號重複兩次 (`EmpNo * 2`)。
3. **群組 ID 映射**：讀取 `group_id.csv` 將群組名稱轉換為 GID。
4. **呼叫 FreeIPA API**：
   - `client.user_add`：新增使用者資料。
   - `client.group_add_member`：將新增的使用者加入指定群組。

### 較深奧的程式碼

### 1. **群組 ID 映射**

透過 `group_id.csv` 取得群組名稱與 GID 的對應關係，並建立字典：

```python
df = read_csv('ldapmember/group_id.csv')
gnam_id = {i: j for i, j in zip(df.group_name, df.GID)}
```

**解釋**：  

- `read_csv` 將 CSV 檔案轉換為 DataFrame。
- 使用字典生成式將 `group_name` 和 `GID` 映射成字典，便於快速查詢群組 ID。

---

### 2. **FreeIPA 使用者新增邏輯**

使用 `python-freeipa` 的 API 呼叫新增使用者：

```python
client.user_add(
    a_uid=user.get("UserName"),
    o_userpassword=user.get("EmpNo") * 2,  # 密碼為員工編號重複兩次
    o_mail=user.get("Email"),
    o_givenname=user.get("FirstName"),
    o_sn=user.get("LastName"),
    o_cn=user.get("EmpName"),
    o_loginshell="/sbin/nologin",  # 預設不允許登入
    o_ou=user.get("DeptName"),
    o_departmentnumber=deptDict.get(user.get("DeptName")),
    o_employeenumber=user.get("EmpNo"),
    o_title=user.get("DutyName"),
    o_gidnumber=gnam_id.get(user.get("UserGroup")),  # 設定群組 ID
)
```

**解釋**：  

- `a_uid` 是使用者帳號，從 `user` 字典取得。
- 密碼 (`o_userpassword`) 預設為員工編號的兩倍。
- 部門與群組 ID 使用對應字典 (`deptDict`, `gnam_id`) 自動填入。
- 使用 `o_loginshell="/sbin/nologin"` 限制登入。

---

### 3. **群組成員新增邏輯**

將使用者加入指定群組：

```python
client.group_add_member(a_cn=user.get("UserGroup"), o_user=user.get("UserName"))
```

**解釋**：  

- `a_cn` 是群組名稱，從 `user["UserGroup"]` 取得。
- `o_user` 是使用者名稱，指定將該使用者加入群組。

---

### 總結

上述程式碼包含對外部資料的動態映射 (`gnam_id`)、API 參數配置，以及 FreeIPA 的使用者與群組管理邏輯，實現高效且自動化的帳號管理功能。

