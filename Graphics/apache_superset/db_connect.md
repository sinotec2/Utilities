---
layout: default
title:  數據庫的連接
parent: apache_superset
grand_parent: Graphics
last_modified_date: 2024-06-15 11:00:11
tags: apache_superset graphics
---

# superset連接到外部資料庫

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

在 Superset 中連接到其他數據庫（例如 MySQL）時，確實需要一些配置。錯誤訊息中的 `OperationalError` 提示 Superset 無法連接到 MySQL 服務器，可能是因為 MySQL 伺服器不允許來自 Superset 服務器的連接。

以下是一些可能需要檢查和配置的地方：

1. **MySQL 伺服器設定：** 確保 MySQL 伺服器允許來自 Superset 伺服器的連接。您可能需要在 MySQL 的設置中確認以下事項：

   - MySQL 伺服器是否允許遠程連接。
   - Superset 伺服器的 IP 地址是否在 MySQL 的許可名單中。

   在 MySQL 伺服器的配置文件中，可以設置 `bind-address` 來指定允許連接的 IP 地址。同時，確保 MySQL 使用者有權限從 Superset 伺服器連接。

2. **Superset 數據庫配置：** 在 Superset 中，確保您的數據庫連接字符串（`SQLALCHEMY_DATABASE_URI`）正確並包含了 MySQL 伺服器的地址、用戶名和密碼。這通常可以在 Superset 的配置文件（`superset_config.py`）中找到。

   範例配置：

   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql://username:password@mysql_server/db_name'
   ```

   請替換 `username`、`password`、`mysql_server` 和 `db_name` 為實際的 MySQL 連接資訊。

3. **防火牆設定：** 如果有防火牆，確保 MySQL 伺服器和 Superset 伺服器之間的連接端口是打開的。MySQL 默認使用 3306 端口，您可能需要確保此端口是可訪問的。

4. **MySQL 驅動程序安裝：** 確保 Superset 中安裝了與 MySQL 通信所需的相應 Python 驅動程序。您可以使用以下命令安裝 `mysqlclient`：

   ```bash
   pip install mysqlclient
   ```

請注意，這僅是一些常見的檢查點，具體步驟可能因您的環境而異。確保 MySQL 伺服器的設置允許 Superset 伺服器連接，同時確保 Superset 的配置正確並包含正確的 MySQL 連接信息。

