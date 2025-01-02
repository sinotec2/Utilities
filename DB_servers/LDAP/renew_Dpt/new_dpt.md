---
layout: default
title:  update the department names
parent: LDAP
grand_parent: DB_servers
last_modified_date: 2025-01-02 14:07:50
has_children: true
tags: LDAP
---

{: .fs-6 .fw-300 }

# 部門名稱之更新(增)

## Table of contents

{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 背景

- 因為部門名稱並不會常常更新，就趁這一次徹底來檢討一下LDAP資料庫的正確性，也把歷次更新有些模糊的概念一併予以統一。修改的重點如下：
- kerberos票證及密碼的有效期限：會卡到API的修改權限
- 使用`user_dn`似乎有些紀錄`user_mod`不能登入修改，還好使用`a_uid`還可以執行。這有賴`uid`保證、絕對、不會重複。

## kerberos與密碼政策

- kerberos票證的有效性：正常來說，這個票證會需要常常更新，來提高系統的安全性。但是因為系統也還沒有正式發布實施，同仁登入情形也不是很踴躍，結果卻卡到API更新的權限，反而不利發展。<記得發布後要修改有效日期!!!>

```bash
# act as root
kinit admin
for i in $(ipa user-find --all --raw --size=1000  | grep uid\: | awkk 2);do 
   ipa user-mod $i --password-expiration=9999-12-31Z 
   done
ipa pwpolicy-show #(not changed)
```

## 取得所有使用者名稱

```bash
ipa user-find --all --raw --size=1000  | grep uid\: | awkk 2 > /nas2/kuang/MyPrograms/passwd_FreeIPA/ldapmember/all_uid.txt
```

## ipython執行重點

### 登入ldap

```python
from python_freeipa import ClientMeta

## 連線FreeIPA
client = ClientMeta("node03.sinotech-eng.com", verify_ssl=False)
client.login("admin", "***")
```

### 新部門使用者

```python
ES=read_csv('../ES.csv',encoding='big5')
for u in list(ES['Email：']):
    if type(u)==float:continue
    username_to_find = u.split('@')[0]
    user = client.user_find(uid=username_to_find)

    if user['count'] > 0:  # Check if user exists
        user_info = user['result'][0]

        if user_info.get('ou') == '...部':
            continue
        # Modify the user's organizational unit, assuming 'ou' is the correct parameter
        try:
            client.user_mod(a_uid=username_to_find, ou='...部')
            print(f'Modified user {username_to_find} to move to ...部')
        except Exception as e:
            print(f'Failed to modify user {username_to_find}: {e}')
    else:
        print(f'User {username_to_find} not found.')
```

### 舊部門名稱統一

```python
deptDict = {
    "oldname": "newname",
   ...
    }

with open('all_uid.txt','r') as f:
    uids=[i.strip('\n') for i in f]

for u in uids:
    username_to_find = u
    user = client.user_find(uid=username_to_find)

    if user['count'] > 0:  # Check if user exists
        user_info = user['result'][0]
        try:
            ou=user_info.get('ou')[0]
        except Exception as e:
            ou=user_info.get('ou')
        if ou not in deptDict:
            continue
        # Modify the user's organizational unit, assuming 'ou' is the correct parameter
        try:
            client.user_mod(a_uid=username_to_find, ou=deptDict[ou])
            print(f'Modified user {username_to_find}')
        except Exception as e:
            print(f'Failed to modify user {username_to_find}: {e}')
    else:
        print(f'User {username_to_find} not found.')
```

## 確認所有部門名稱都正確

```bash
ipa user-find --all --raw --size=1000  | grep ou\: \
|grep -v ...部|grep -v ...部
```

