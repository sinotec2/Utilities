---
layout: default
title: csv_ldap
parent: streamlit
grand_parent: Web Jokers
nav_order: 99
last_modified_date: 2025-03-26 08:32:07
tags:
  - web
---

# csv_ldap

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


這是一個使用 streamlit 和 LDAP 進行登入驗證的 Python 程式。以下是該程式的功能：

- 使用者可以輸入他的使用者名稱和密碼，並按下「登入」按鈕進行 LDAP 驗證。
- 如果使用者的憑證有效，則程式會將他的部門資訊存儲到 session_state 中。
- 如果使用者已經登入並選擇了部門，則程式會顯示選定部門的統計表。
- 如果使用者未輸入有效的憑證或選擇無效的部門，則程式會顯示錯誤訊息。

以下是程式中的主要部分：

- ldap_login 函數用於 LDAP 驗證。它需要使用者的使用者名稱和密碼作為參數，並返回一個 Connection 物件。
- get_ldap_credentials 函數用於從 session_state 中取得使用者的憑證。它返回一對使用者名稱和密碼。
- authenticate_user 函數用於驗證使用者是否已經登入並選擇了部門。它需要使用者的使用者名稱和密碼作為參數，並返回一個布林值表示使用者是否已經登入並選擇了部門。
- main 函數用於程式的主要部分。它首先初始化 session_state，然後顯示一個側邊欄以進行 LDAP 驗證。如果使用者按下「登入」按鈕，則程式會執行 authenticate_user 函數來驗證使用者的憑證。如果憑證有效，則程式會將選定部門的統計表存儲到 session_state 中。如果使用者已經登入並選擇了部門，則程式會顯示選定部門的統計表。

```python
# coding: utf-8
import streamlit as st
import pandas as pd
from ldap3 import Server, Connection, ALL
import json

# LDAP 登入驗證函數
def ldap_login(username, password):
    BASE_DN = "dc=sinotech-eng,dc=com"
    user = f"uid={username},cn=users,cn=accounts,{BASE_DN}"
    server = Server('ldap://node03.sinotech-eng.com', get_info=ALL)
    try:
        conn = Connection(server, user, password, auto_bind=True)
    except:
        st.error('無效的憑證')  # 顯示錯誤訊息
        return None
    return conn

# 從 session_state 中取得使用者憑證
def get_ldap_credentials():
    username = st.session_state['username']
    password = st.session_state['password']
    return username, password

# 驗證使用者登入
def authenticate_user(username, password):
    conn = ldap_login(username, password)
    if not conn:
        st.error('無法連線至 LDAP 伺服器')  # 顯示錯誤訊息
        return False
    conn.unbind()  # 結束連線
    return True

# 主函數
def main():
    # 初始化 session_state
    vars = ['username', 'password', 'login_form', 'submit', 'departments', 'department']
    for var in vars:
        if var not in st.session_state:
            st.session_state[var] = None

    st.title('部門統計表檢視')  # 設定標題

    # 側邊欄進行 LDAP 驗證
    with st.sidebar:
        st.markdown("LDAP 驗證")
        username = st.text_input('使用者名稱', on_change=check_username, key='username')  # 使用者名稱輸入框
        password = st.text_input('密碼', type='password', key='password')  # 密碼輸入框
        submit = st.button(label='登入')  # 登入按鈕

        if submit and authenticate_user(username, password):
            departments = gps.get(username, [])
            st.session_state['departments'] = departments  # 儲存部門資訊到 session_state
            st.session_state['submit'] = True  # 標記登入成功
            if departments:
                st.success('登入成功!')  # 顯示成功訊息
            else:
                st.error('登入失敗，請檢查使用者名稱和密碼。')  # 顯示錯誤訊息

        if st.button("清空並重新開始"):
            st.session_state.clear()  # 清空所有 session_state 變數
            return 
        
    # 如果已登入，顯示部門選擇
    if st.session_state['departments']:
        departments = st.session_state['departments']
        st.session_state['department'] = st.selectbox('選擇部門', departments)

    # 主內容區域
    with st.container():
        if not st.session_state['submit'] or not st.session_state['departments']:
            st.warning('請登入並選擇部門')  # 提示登入或選擇部門
        elif st.session_state['department']:
            department = st.session_state['department']
            display_statistics(department)  # 顯示選定部門的統計表
        else:
            st.warning('請選擇部門')  # 提示選擇部門

# 驗證使用者名稱是否有效
def check_username():
    username = st.session_state['username']
    if username in gps:
        return True
    else:
        st.error('使用者名稱不被允許')  # 顯示錯誤訊息
        return False

# 顯示部門統計表
def display_statistics(department):
    file_path = f'./{department}_statistics.csv'
    try:
        df = pd.read_csv(file_path)
        st.write(f'{department} 部門統計表')  # 顯示部門名稱
        st.dataframe(df)  # 顯示統計表
    except FileNotFoundError:
        st.error(f'找不到 {department} 部門的統計表。')  # 顯示錯誤訊息

if __name__ == '__main__':
    # 載入部門對應的 JSON 檔案
    with open('sirs_gps.json', 'rb') as f:
        gps = json.load(f)
    main()
```
