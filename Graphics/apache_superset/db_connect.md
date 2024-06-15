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

## Druid的連結

### superset  UI settings

Apache Superset 可以與 Apache Druid 整合，以便在 Superset 中查詢和視覺化 Druid 數據源。以下是連接 Apache Superset 到 Apache Druid 的基本步驟：

1. **確保 Druid 服務運行：** 在開始之前，確保您已成功設置並運行了 Apache Druid。您需要知道 Druid Broker 和 Coordinator 的位置。

2. **在 Superset 中添加 Druid 數據源：** 登錄到 Superset，然後轉到「Data」→「Databases」頁面。點擊右上角的「+」按鈕，選擇「Druid」數據庫類型。

3. **填寫 Druid 數據源的詳細信息：** 提供有關 Druid 數據源的詳細信息，包括數據庫名稱、Druid Broker 和 Coordinator 的地址等。在「Additional Parameters」部分，您可能需要提供一些額外的配置參數，具體取決於您的 Druid 部署。

4. **保存並測試連接：** 點擊「Save」保存 Druid 數據源配置。然後，您可以使用「Test Connection」按鈕測試是否能夠成功連接到 Druid 數據源。

5. **添加 Druid 表：** 成功測試連接後，轉到「Tables」頁面，然後點擊右上角的「+」按鈕，選擇「Druid」數據源。這將使您能夠在 Superset 中查詢 Druid 表。

6. **建立 Superset 查詢：** 現在您可以建立 Superset 中的查詢，並使用 Druid 數據源查詢和可視化數據。

請注意，Druid 數據源配置可能因您的 Druid 部署而異。確保您了解您的 Druid 部署的配置細節，以確保正確配置 Superset。

此外，請參考 Apache Superset 和 Apache Druid 的官方文檔，以獲取更詳細的信息和配置指南：

- [Apache Superset 官方文檔](https://superset.apache.org/docs/intro)
- [Apache Druid 官方文檔](https://druid.apache.org/docs/latest/)

### Docker compose

使用 Docker Compose 部署 Superset 通常是比較簡單和方便的方式，但確實可能需要一些額外的步驟來增加功能，如添加對 Druid 的支持。

以下是在使用 Docker Compose 部署的 Superset 中添加 Druid 支持的一種方式：

1. **修改 Docker Compose 文件：** 打開您的 Docker Compose 文件（通常是 `docker-compose.yaml`），尋找 Superset 服務的部分。

2. **在 Superset 服務中添加額外的 pip 安裝：** 在 Superset 服務的 `command` 或 `entrypoint` 中，添加對 Druid 的支持，例如：

    ```yaml
    services:
      superset:
        image: superset/superset:latest
        command: ["bash", "-c", "pip install apache-superset[druid] && superset run -p 8088 --with-threads --reload --debugger"]
        ports:
          - "8088:8088"
        # 其他配置...
    ```

    這將在啟動 Superset 服務時安裝 Druid 相關的 pip 套件。

3. **重新構建和啟動容器：** 在修改 Docker Compose 文件後，使用以下命令重新構建和啟動容器：

    ```bash
    docker-compose up --build
    ```

4. **進入 Superset 容器：** 使用以下命令進入正在運行的 Superset 容器：

    ```bash
    docker exec -it <superset_container_name> /bin/bash
    ```

    將 `<superset_container_name>` 替換為實際的 Superset 容器名稱。

5. **退出容器：** 在容器內安裝完 Druid 驅動程序後，退出容器：

    ```bash
    exit
    ```

6. **重新啟動 Superset 容器：** 使用以下命令重新啟動 Superset 容器，以使更改生效：

    ```bash
    docker-compose restart superset
    ```

這樣，您應該能夠在 Superset 中查詢和視覺化 Druid 數據源。

請注意，這僅是一種可能的方式，實際步驟可能因您的 Docker Compose 文件和配置而異。確保您的 Docker Compose 文件符合您的 Superset 部署的實際情況。

## mysql之連結

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

