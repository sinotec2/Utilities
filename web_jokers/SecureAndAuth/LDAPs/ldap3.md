---
layout: default
title:  python ldap3 module
parent: LDAP
grand_parent: Security And Authentication
last_modified_date: 2025-02-21 20:29:52
tags: LDAP ldap3
---

#  python ldap3 module
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

## 說明

### 連線

- 定義`Server`：
  - 目前先連`ldap`,沒有ssl/tls、
  - `get_info`：使用ALL函式。
- 連線
  - 不必特別先binding，可以用`auto_bind=True`，但是必須在結束後`unbind`。(其他的`auto_bind`選項無法連線)
  - `user`欄位：不必給提示(`user=user`)，必須是完整的`domain name`。
  - `password`欄位：也不必給提示(`password=password`)，直接給值就好。
  - 如果連不上，有可能是serveer錯誤、也可能是credential 錯誤，用`try`來辨識。如果連線錯誤，不給回值。

### ldap上的搜尋

- 連線(`binding`)後必須搜尋，來驗證連線的合法性。
- 回值為一個`boolean`，如果不給容器`(result)`，似乎不能運作。
- 回復前不要`unbind`，要在確認前保持`bind`。

### 連線驗證

- `conn.response_to_json()`這個函式是新版的，GPT無法回復。
- 不需要真的指定`json`檔案名稱，因為這個函式的回覆是個`boolean`
- 同樣的，也可以將回復輸出到txt等型態，除了寫檔案之外，也會回復`boolean`。

### 後續DOM

- 是否關閉原來的畫面？可能不需要。可以在`streamlit`開啟多個畫面。

## 程式碼

```python
import streamlit as st
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, MODIFY_ADD, MODIFY_DELETE

def ldap_login(username, password):
    BASE_DN = "dc=sinotech-eng,dc=com"
    user=f"uid={username},cn=users,cn=accounts,dc=sinotech-eng,dc=com"
    server = Server('ldap://node03.sinotech-eng.com', get_info=ALL)
    try:
        conn = Connection(server,user, password, auto_bind=True)
    except:
        st.error('invalidCredentials')
        return
    result=conn.search(BASE_DN, '(objectClass=*)', attributes=['*'])
    return conn

def get_ldap_credentials():
    username = st.session_state['username']
    password = st.session_state['password']
    return username, password

def authenticate_user(username, password):
    ldap_credentials = get_ldap_credentials()
    conn = ldap_login(username, password)
    if not conn:
        st.error('not connected')
        return
    if conn.response_to_json() == None:
        st.error('Failed to authenticate user.')
        return
    conn.unbind()
    return True

st.header('LDAP Login')

st.session_state.__init__()


if 'username' not in st.session_state:
    st.session_state['username'] = ''  # or any default value you prefer

# Similar initialization for 'password' if needed
if 'password' not in st.session_state:
    st.session_state['password'] = ''

placeholder = st.empty()

# 使用佔位符顯示一些內容
with placeholder.container():
    st.write("這是第一個頁面的內容。")
    with st.form('login_form'):
        username = st.text_input('Username')
        password = st.text_input('Password', type='password', key='password')
        submit = st.form_submit_button(label='Login')
        if submit:
            if authenticate_user(username, password):
                st.success('Login successful!')
                st.success(f'<a href="https://node03.sinotech-eng.com/Sup.calendars/zh/" > 轉到新網址</a>')  # Redirect to dashboard
        if username is None:
            username = st.session_state['username'] = st.text_input("Enter your username")
    if st.button("清空並重新開始"):
        placeholder.empty()
        st.write("這是新的頁面的內容。")
```