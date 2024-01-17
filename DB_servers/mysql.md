---
layout: default
title:  mysql
parent: DB_servers
last_modified_date: 2024-01-16 10:51:11
tags: mysql
---

# mysql
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

## mysql安裝

在 Linux 中，安裝 MySQL 可以透過軟體套件管理器來完成。 以下是一些常見的 Linux 發行版的安裝步驟。

### Ubuntu/Debian 系統

在 Ubuntu 或 Debian 系統中，可以使用下列命令來安裝 MySQL：

```bash
sudo apt update
sudo apt install mysql-server
```

安裝過程中，系統會要求你設定 MySQL 的 root 使用者密碼。

### CentOS/RHEL 系統

在 CentOS 或 RHEL 系統中，可以使用下列指令來安裝 MySQL：

```bash
sudo yum install mysql-server
```

安裝完成後，啟動 MySQL 服務，並設定開機自啟動：

```bash
sudo systemctl start mysqld
sudo systemctl enable mysqld
```

### Arch Linux 系統

在 Arch Linux 系統中，可以使用下列指令來安裝 MySQL：

```bash
sudo pacman -S mysql
```

安裝完成後，啟動 MySQL 服務：

```bash
sudo systemctl start mysqld
```

### 其他 Linux 發行版

對於其他 Linux 發行版，你可以查看對應發行版的文件或使用其套件管理器來安裝 MySQL。 一般來說，MySQL 的軟體套件在大多數主流 Linux 發行版的官方軟體倉庫中都是可用的。

安裝完成後，你可以使用 `mysql` 命令列客戶端來連接 MySQL 資料庫，並進行對應的設定。 例如：

```bash
mysql -u root -p
```

這將提示你輸入 root 使用者密碼，並進入 MySQL 的命令列介面。

請注意，具體的安裝步驟可能會因 Linux 發行版的不同而有所差異。 在安裝之前，建議查閱相應發行版的文件以獲取詳細資訊。

## mysql啟用

在 Linux 上安裝 MySQL，您可以參考以下步驟：

1. **下載 MySQL 安裝包**：您可以從 MySQL 的官方網站下載對應的安裝包¹²。

2. **解壓安裝包**：使用 `tar -zxvf` 命令解壓下載的安裝包¹²。

3. **創建 MySQL 用戶和用戶組**：使用 `groupadd mysql` 和 `useradd -r -g mysql mysql` 命令創建 MySQL 用戶和用戶組¹²。

4. **創建數據目錄並賦予權限**：使用 `mkdir -p /data/mysql` 和 `chown mysql:mysql -R /data/mysql` 命令創建數據目錄並賦予權限¹²。

5. **修改配置文件**：修改 `/etc/my.cnf` 配置文件，並添加相應的配置信息¹²。

6. **初始化 MySQL**：使用 `mysqld --initialize --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql` 命令初始化 MySQL¹²。

7. **啟動 MySQL**：使用 `/usr/local/mysql/support-files/mysql.server start` 命令啟動 MySQL¹²。

8. **修改 root 用戶的密碼**：使用 `mysqladmin -uroot -p password` 命令修改 root 用戶的密碼¹²。

請注意，這些步驟可能會因為您的 Linux 發行版和 MySQL 版本的不同而有所變化。在進行操作時，請確保您已經根據您的具體情況進行了適當的調整。希望這些資訊對您有所幫助！

來源: 與 Bing 的交談， 2024/1/17
(1) Linux 安装Mysql 详细教程（图文教程） - [CSDN博客](https://blog.csdn.net/bai_shuang/article/details/122939884).
(2) 实战篇：手把手教你Linux安装Mysql（细致入微） - [腾讯云](https://cloud.tencent.com/developer/article/1863236).
(3) 在Linux上安装MySQL - [知乎](https://zhuanlan.zhihu.com/p/666440382).
(4) Linux下安装mysql（仅学习） - [知乎](https://zhuanlan.zhihu.com/p/87069388).
(5) undefined. [baidu](https://pan.baidu.com/s/1-pgv4cChPPdqU_JFI5H33Q).
(6) undefined. [dev.mysql](http://dev.mysql.com).
(7) undefined. [dev.mysql](https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.2).

## mycnf內容設定
