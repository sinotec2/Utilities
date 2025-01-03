---
layout: default
title:  修改LDAP密碼
parent: LDAP
grand_parent: DB_servers
last_modified_date: 2025-01-03 16:47:42
tags: LDAP
---

{: .fs-6 .fw-300 }

# 修改LDAP密碼

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

- LDAP登入過程有票證的管理，這裡我們使用FreeIPA(自由的身分政策稽核)系統來進行代管，因此需要到FreeIPA介面去修改帳密。

## 登入

### 跳過https帳密檢核

- 前往公司內網伺服器[node03](https://node03.sinotech-eng.com/ipa/ui/)，因為是安全網站，會詢問帳密。這裡**不必理會**，直接按下`取消`跳過(可能會要按2次)。

![pngs/2025-01-03-16-55-15.png](pngs/2025-01-03-16-55-15.png)

- 輸入帳號、密碼(員編2次)、**不必理會**One-Time-Password

![pngs/2025-01-03-16-57-46.png](pngs/2025-01-03-16-57-46.png)

- 如果從來沒有登入過、或許久沒有登入，系統會要求確認。

### 修改密碼

- 在頁面的右上角會出現姓名，下拉選單中有`change password`

![pngs/2025-01-03-17-01-17.png](pngs/2025-01-03-17-01-17.png)

- 輸入原來密碼、給訂新的密碼、**不必理會**OTP (One-Time-Password)
- 按下`重置密碼`馬上就會生效!

![pngs/2025-01-03-17-02-14.png](pngs/2025-01-03-17-02-14.png)

## 不登入修改密碼

- 如果不想修改其他LDAP資訊，也可以直接在[這裡](http://node03.sinotech-eng.com:5000)修改密碼。

![pngs/2025-01-03-17-10-13.png](pngs/2025-01-03-17-10-13.png)

## 忘記密碼

- 只能找研資部同仁登入系統修改
