---
layout: default
title:  mysql之安裝
parent: mysql
grand_parent: DB_servers
last_modified_date: 2024-01-16 10:51:11
tags: mysql
---

# mysql安裝

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

8. **修改 root 用戶的密碼**：使用 `mysqladmin -u root -p password` 命令修改 root 用戶的密碼¹²。

請注意，這些步驟可能會因為您的 Linux 發行版和 MySQL 版本的不同而有所變化。在進行操作時，請確保您已經根據您的具體情況進行了適當的調整。希望這些資訊對您有所幫助！

```bash
$ mysql -u root -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 3674967
Server version: 5.7.44 MySQL Community Server (GPL)

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> CREATE USER 'superset'@'%' IDENTIFIED BY 'superset';
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
mysql> CREATE USER 'superset'@'%' IDENTIFIED BY 'yckuang4139';
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
mysql> CREATE USER 'superset'@'%' IDENTIFIED BY 'ycKuang@4139'
    -> ;
Query OK, 0 rows affected (0.00 sec)

mysql> GRANT ALL PRIVILEGES ON your_database.* TO 'superset'@'%';
Query OK, 0 rows affected (0.00 sec)

mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.01 sec)

mysql>

```
來源: 與 Bing 的交談， 2024/1/17
(1) Linux 安装Mysql 详细教程（图文教程） - [CSDN博客](https://blog.csdn.net/bai_shuang/article/details/122939884).
(2) 实战篇：手把手教你Linux安装Mysql（细致入微） - [腾讯云](https://cloud.tencent.com/developer/article/1863236).
(3) 在Linux上安装MySQL - [知乎](https://zhuanlan.zhihu.com/p/666440382).
(4) Linux下安装mysql（仅学习） - [知乎](https://zhuanlan.zhihu.com/p/87069388).
(5) undefined. [baidu](https://pan.baidu.com/s/1-pgv4cChPPdqU_JFI5H33Q).
(6) undefined. [dev.mysql](http://dev.mysql.com).
(7) undefined. [dev.mysql](https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.2).

## mycnf內容設定

### 說明

MySQL 的設定檔是用來指定 MySQL 伺服器行為的檔案。 在 MySQL 中，設定檔通常被稱為 `my.cnf`（在 Windows 上可能是 `my.ini`）。 這個檔案包含了一系列設定選項，讓你可以自訂 MySQL 伺服器的各種方面，例如資料庫目錄、連接埠號碼、字元集、緩衝池大小等。

以下是一個典型的 MySQL 設定檔 `my.cnf` 的一些重要設定選項以及它們的意義：

1. **[mysqld] 部分：**
    這是 MySQL 伺服器的主要配置部分。 以下是其中一些常見的選項：

    - `datadir`：MySQL 資料庫檔案儲存的目錄路徑。
    - `port`：MySQL 伺服器監聽的連接埠號碼。
    - `character-set-server`：伺服器使用的字元集。
    - `max_connections`：允許的最大連線數。

    範例：
    ```ini
    [mysqld]
    datadir=/var/lib/mysql
    port=3306
    character-set-server=utf8mb4
    max_connections=100
    ```

2. **[client] 部分：**
    這是 MySQL 用戶端的設定部分，包含客戶端使用的預設字元集等選項。

    範例：
    ```ini
    [client]
    default-character-set=utf8mb4
    ```

3. **[mysql] 部分：**
    這是 MySQL 命令列客戶端的設定部分。

    範例：
    ```ini
    [mysql]
    default-character-set=utf8mb4
    ```

4. **[mysqldump] 部分：**
    這是 mysqldump 工具的設定部分。

    範例：
    ```ini
    [mysqldump]
    default-character-set=utf8mb4
    ```

設定檔通常位於以下位置之一：

- **Linux/Unix 系統：**
   - `/etc/my.cnf`
   - `/etc/mysql/my.cnf`
   - `/usr/etc/my.cnf`
   - `~/.my.cnf` （用戶級配置）

- **Windows 系統：**
   - `C:\ProgramData\MySQL\MySQL Server x.x\my.ini` （MySQL 安裝路徑）
   - `C:\Program Files\MySQL\MySQL Server x.x\my.ini` （MySQL 安裝路徑）

請注意，實際的設定檔路徑可能會因作業系統、MySQL 版本和安裝方式而異。 你可以透過 MySQL 的 `SHOW VARIABLES` 指令或 `mysqld --help --verbose` 指令來查看 MySQL 正在使用的設定檔路徑。

在修改設定檔之後，可能需要重新啟動 MySQL 伺服器以使變更生效。

### 範例

```bash
openkm@master /etc
$ cat my.cnf
# For advice on how to change settings please see
# http://dev.mysql.com/doc/refman/5.6/en/server-configuration-defaults.html

[mysqld]
#
# Remove leading # and set to the amount of RAM for the most important data
# cache in MySQL. Start at 70% of total RAM for dedicated server, else 10%.
# innodb_buffer_pool_size = 128M
#
# Remove leading # to turn on a very important data integrity option: logging
# changes to the binary log between backups.
# log_bin
#
# Remove leading # to set options mainly useful for reporting servers.
# The server defaults are faster for transactions and fast SELECTs.
# Adjust sizes as needed, experiment to find the optimal values.
# join_buffer_size = 128M
# sort_buffer_size = 2M
# read_rnd_buffer_size = 2M
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock

# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

# Recommended in standard MySQL setup
sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES

[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
```

## 重設root密碼

### yum

```bash
sudo yum install mysql-server mysql-client
```
安装期间，你将被要求设置 MySQL root 用户的密码。

### mysqladmin

在使用 `yum` 安裝 MySQL 的過程中，系統可能不會在安裝過程中詢問您設定 MySQL root 用戶的密碼⁵。這是因為密碼的設定通常在 MySQL 伺服器配置的步驟中完成⁵。

安裝完成後，您可以使用以下命令來設定 root 用戶的密碼³：

```bash
mysqladmin -u root password "your_new_password";
```

### skip-grant-tables

如果您在設定密碼時遇到問題，例如無法登入，您可以嘗試以下步驟來重設密碼²：
1. 在 `/etc/my.cnf` 文件中添加一行 `skip-grant-tables`，這樣可以繞過密碼驗證²。
2. 重啟 MySQL 服務²。
3. 登入 MySQL，然後使用以下 SQL 語句來修改密碼²：
    ```sql
    use mysql;
    update mysql.user set authentication_string=password('your_new_password') where user='root';
    flush privileges;
    quit;
    ```
4. 最後，刪除 `/etc/my.cnf` 文件中的 `skip-grant-tables`，然後再次重啟 MySQL 服務²。

請注意，這些命令需要在終端機或命令提示字元中執行。如果您在執行這些命令時遇到任何問題，請隨時告訴我，我會很樂意提供進一步的幫助！

來源: 與 Bing 的交談， 2024/1/23
(1) 如何在 Ubuntu 20.04 上安装 MySQL - [阿里云开发者社区](https://developer.aliyun.com/article/758177).
(2) Linux/UNIX 上yum安装 MySQL-腾讯云开发者社区-[腾讯云](https://cloud.tencent.com/developer/article/1888692).
(3) Linux CentOS7通过yum安装mysql-server - [CSDN博客](https://blog.csdn.net/zhang7761/article/details/109018190).
(4) MySQL :: MySQL 8.0 Reference Manual :: 2.5.1 Installing MySQL on Linux Using the MySQL Yum Repository. [dev.mysql](https://dev.mysql.com/doc/refman/8.0/en/linux-installation-yum-repo.html).
(5) Linux yum安装指定版本的MySQL（如MySQL5.7） - [CSDN博客](https://blog.csdn.net/li_wen_jin/article/details/105140360).
(6) [undefined](https://dev.mysql.com/downloads/repo/yum/).
(7) [undefined](https://www.cnblogs.com/cyl048/p/6879085.html).
(8) [undefined](http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm).

## 如何新增mysql的使用者帳密?

在 MySQL 中，你可以使用 `CREATE USER` 和 `GRANT` 語句來建立新使用者並授予權限。 以下是一些基本的步驟：

### 步驟1：登入 MySQL 伺服器

使用 MySQL 用戶端登入 MySQL 伺服器，可以使用以下命令：

```bash
mysql -u root -p
```

這將提示你輸入 MySQL root 使用者的密碼。

### 步驟2：建立新用戶

```sql
CREATE USER 'new_username'@'localhost' IDENTIFIED BY 'user_password';
```

- `new_username` 是你要建立的新使用者名稱。
- `localhost` 表示該使用者只能從本機連線到 MySQL。 如果你希望允許從任何地方連接，可以使用 `'%'` 來代替 `'localhost'`。
- `'user_password'` 是新使用者的密碼。 請使用安全的密碼。

### 步驟3：授予權限

接下來，你需要為新使用者授予適當的權限。 例如，如果你要為新使用者授予所有資料庫的全部權限，可以使用以下命令：

```sql
GRANT ALL PRIVILEGES ON *.* TO 'new_username'@'localhost' WITH GRANT OPTION;
```

- `*.*` 表示所有資料庫和所有資料表。
- `WITH GRANT OPTION` 允許該使用者授予權限給其他使用者。

### 步驟4：刷新權限

在進行了權限變更後，你需要刷新 MySQL 的權限表：

```sql
FLUSH PRIVILEGES;
```

### 範例：

假設你要建立一個用戶名為 `myuser`，密碼為 `mypassword`，並且具有對所有資料庫的全部權限的用戶，你可以執行以下 SQL 命令：

```sql
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';
GRANT ALL PRIVILEGES ON *.* TO 'myuser'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

請根據你的實際需求和安全性要求進行調整。 建立使用者並授予權限是資料庫安全的一個重要方面，確保僅為使用者提供他們實際需要的最小權限。

