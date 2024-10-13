---
layout: default
title:  MinIO儲存硬體之建議
parent: MinIO
grand_parent: DB_servers
last_modified_date: 2024-10-13 19:55:12
tags: DB_servers
---

# MinIO儲存硬體之建議
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

- [souurce](https://min.io/docs/minio/linux/operations/install-deploy-manage/deploy-minio-single-node-single-drive.html#storage-requirements)

### 儲存硬體之建議

以下要求總結了MinIO 硬體建議的儲存部分：

- 使用本地儲存

    與網路儲存（ NAS、SAN、NFS ）相比，直連儲存 (DAS) 具有顯著的效能和一致性優勢。 MinIO 強烈建議將**快閃記憶體**（NVMe、SSD）用於主要或「熱」資料。

- 對磁碟機使用 **[XFS](#xfs)** 格式化

    MinIO 強烈建議配置 **[XFS](#xfs)** 格式的磁碟機用於儲存。 MinIO 使用 **[XFS](#xfs)** 作為內部測試和驗證套件的一部分，為所有規模的效能和行為提供額外的信心。

- 重新啟動後保留磁碟機安裝和映射

    用於/etc/fstab確保跨節點重新啟動時驅動器到安裝映射的一致性。

    非 Linux 作業系統應使用等效的磁碟機安裝管理工具。

### 對驅動器的獨佔訪問

MinIO需要 對為物件儲存提供的磁碟機或磁碟區進行獨佔存取。任何其他進程、軟體、腳本或人員都不應直接對提供給 MinIO 的磁碟機或磁碟區或 MinIO 放置在其上的物件或檔案執行任何操作。

除非MinIO 工程部門指示，否則請勿使用腳本或工具直接修改、刪除或移動所提供驅動器上的任何資料分片、奇偶校驗分片或元資料文件，包括從一個驅動器或節點移動到另一個驅動器或節點。此類操作很可能會導致超出 MinIO 修復能力的廣泛損壞和資料遺失。

### 記憶體需求

版本 RELEASE.2024-01-28T22-35-53Z 中已變更： MinIO 在啟動時預先分配 2GiB 系統記憶體。

MinIO 建議每個主機至少使用 32GiB 記憶體。有關 MinIO 中記憶體分配的更多指導，請參閱記憶體。

## 部署單節點單驅動MinIO

以下程序部署由單一 MinIO 伺服器和單一磁碟機或儲存磁碟區組成的 MinIO。

```bash
網路檔案系統磁碟區破壞一致性保證

MinIO 嚴格的先寫後讀和先寫後列表一致性模型需要本機磁碟機檔案系統。

如果底層儲存磁碟區是 NFS 或類似的網路連線儲存卷，MinIO 無法提供一致性保證。
```

### 1）下載MinIO伺服器

以下選項卡提供了使用 RPM、DEB 或二進位檔案將 MinIO 安裝到 64 位元 Linux 作業系統上的範例。 RPM 和 DEB 套件會自動將 MinIO 安裝到必要的系統路徑並minio為systemctl. MinIO 強烈建議使用 RPM 或 DEB 安裝路徑。若要更新使用 管理的部署systemctl，請參閱更新 systemctl 管理的 MinIO 部署。

使用下列選項之一為在 Intel 或 AMD 64 位元處理器上執行 Linux 的電腦下載 MinIO 伺服器安裝檔。

RPM（RHEL）

使用以下命令下載最新穩定的 MinIO RPM 並安裝它。

```bash
wget https://dl.min.io/server/minio/release/linux-amd64/archive/minio-20241002175041.0.0-1.x86_64.rpm -O minio.rpm
sudo dnf install minio.rpm
```

DEB（Debian/Ubuntu）二進位

```bash
wget https://dl.min.io/server/minio/release/linux-amd64/archive/minio_20241002175041.0.0_amd64.deb -O minio.deb
sudo dpkg -i minio.deb
```

### 2) 建立systemd服務文件

.deb或軟體包.rpm將以下systemd服務文件安裝到/usr/lib/systemd/system/minio.service.對於二進位安裝，請在所有 MinIO 主機上手動建立此檔案。

```bash
注意

systemd在檢查/etc/systemd/...路徑之前檢查/usr/lib/systemd/...路徑並使用它找到的第一個檔案。為了避免衝突或意外的設定選項，請檢查該檔案是否僅存在於該/usr/lib/systemd/system/minio.service路徑中。

有關文件路徑搜尋順序的詳細信息，請參閱systemd.unit 的手冊頁。
```

```bash
[Unit]
Description=MinIO
Documentation=https://min.io/docs/minio/linux/index.html
Wants=network-online.target
After=network-online.target
AssertFileIsExecutable=/usr/local/bin/minio

[Service]
WorkingDirectory=/usr/local

User=minio-user
Group=minio-user
ProtectProc=invisible

EnvironmentFile=-/etc/default/minio
ExecStartPre=/bin/bash -c "if [ -z \"${MINIO_VOLUMES}\" ]; then echo \"Variable MINIO_VOLUMES not set in /etc/default/minio\"; exit 1; fi"
ExecStart=/usr/local/bin/minio server $MINIO_OPTS $MINIO_VOLUMES

# MinIO RELEASE.2023-05-04T21-44-30Z adds support for Type=notify (https://www.freedesktop.org/software/systemd/man/systemd.service.html#Type=)
# This may improve systemctl setups where other services use `After=minio.server`
# Uncomment the line to enable the functionality
# Type=notify

# Let systemd restart this service always
Restart=always

# Specifies the maximum file descriptor number that can be opened by this process
LimitNOFILE=65536

# Specifies the maximum number of threads this process can create
TasksMax=infinity

# Disable timeout logic and wait until process is stopped
TimeoutStopSec=infinity
SendSIGKILL=no

[Install]
WantedBy=multi-user.target

# Built for ${project.name}-${project.version} (${project.name})
```

預設情況下，該 `minio.service` 檔案作為 `minio-user` 使用者和群組運行。您可以使用groupadd和命令建立使用者和群組 `useradd` 。以下範例建立使用者和群組，並設定存取 MinIO 使用的資料夾路徑的權限。這些命令通常需要 root ( sudo) 權限。

```bash
groupadd -r minio-user
useradd -M -r -g minio-user minio-user
chown minio-user:minio-user /mnt/data
```

本範例中的磁碟機路徑由MINIO_VOLUMES環境變數指定。變更此處和環境變數檔案中的值，以符合 MinIO 使用的磁碟機的路徑。

或者，將User和Group值變更為系統主機上具有必要存取權限和權限的另一個使用者和群組。

MinIO 在github.com/minio/minio-service上發布了其他啟動腳本範例。

若要更新使用 管理的部署systemctl，請參閱更新 systemctl 管理的 MinIO 部署。

### 3）建立環境變數文件

在 處建立一個環境變數檔/etc/default/minio。 MinIO Server 容器可以使用該檔案作為所有環境變數的來源。

以下範例提供了一個啟動環境檔案：

```bash
# MINIO_ROOT_USER and MINIO_ROOT_PASSWORD sets the root account for the MinIO server.
# This user has unrestricted permissions to perform S3 and administrative API operations on any resource in the deployment.
# Omit to use the default values 'minioadmin:minioadmin'.
# MinIO recommends setting non-default values as a best practice, regardless of environment

MINIO_ROOT_USER=myminioadmin
MINIO_ROOT_PASSWORD=minio-secret-key-change-me

# MINIO_VOLUMES sets the storage volume or path to use for the MinIO server.

MINIO_VOLUMES="/mnt/data"

# MINIO_OPTS sets any additional commandline options to pass to the MinIO server.
# For example, `--console-address :9001` sets the MinIO Console listen port
MINIO_OPTS="--console-address :9001"
```

包括部署所需的任何其他環境變數。

新版本伺服器： RELEASE.2024-03-03T17-50-39Z

如果滿足以下所有條件，MinIO 會自動產生唯一的根憑證：

    KES版本 2024-03-01T18-06-46Z 或更高版本正在運行

    尚未定義：

        MINIO_ROOT_USER多變的

        MINIO_ROOT_PASSWORD多變的

    有：

        使用受支援的 KMS 目標設定 KES

        使用MinIO 環境變數禁用 root 訪問

當啟動時滿足這些條件時，MinIO 使用 KMS 為使用基於雜湊的訊息驗證程式碼 (HMAC) 的部署產生唯一的根憑證。

如果 MinIO 產生此類憑證，則用於產生憑證的金鑰必須保持不變並繼續存在。部署中的所有資料均使用此金鑰加密！

MINIO_KMS_KES_KEY_NAME若要輪換產生的根憑證，請在 KMS 中產生新金鑰，然後使用新金鑰更新 的值。

### 4）啟動MinIO服務

在本機上發出以下命令以將 MinIO SNSD部署作為服務啟動：

```bash
sudo systemctl start minio.service
```

使用以下命令確認服務在線且正常運作：

```bash
sudo systemctl status minio.service
journalctl -f -u minio.service
```

當伺服器進程連接和同步時，MinIO 可能會記錄更多數量的非關鍵警告。這些警告通常是暫時的，應該在部署上線後解決。

版本 RELEASE.2023-02-09T05-16-53Z 中已變更：如果 MinIO 偵測到足夠的磁碟機來滿足部署的寫入仲裁，則它會啟動。

如果啟動 MinIO 後有任何驅動器保持離線狀態，請在開始生產工作負載之前檢查並解決阻礙其功能的任何問題。

MinIO 服務不會在主機重新啟動時自動啟動。您必須使用來啟動該進程作為主機引導的一部分。`systemctl enable minio.service`

```bash
sudo systemctl enable minio.service
```

輸出journalctl應類似以下內容：

```bash
Status:         1 Online, 0 Offline.
API: http://192.168.2.100:9000  http://127.0.0.1:9000
RootUser: myminioadmin
RootPass: minio-secret-key-change-me
Console: http://192.168.2.100:9001 http://127.0.0.1:9001
RootUser: myminioadmin
RootPass: minio-secret-key-change-me

Command-line: https://min.io/docs/minio/linux/reference/minio-mc.html
   $ mc alias set myminio http://10.0.2.100:9000 myminioadmin minio-secret-key-change-me

Documentation: https://min.io/docs/minio/linux/index.html
```

該API區塊列出了客戶端可以存取 MinIO S3 API 的網路介面和連接埠。該Console區塊列出了用戶端可以存取 MinIO Web 控制台的網路介面和連接埠。

### 5）連接到MinIO服務

MinIO 控制台

您可以透過在首選瀏覽器中輸入 MinIO 伺服器區塊中的任何主機名稱或 IP 位址來存取 MinIO 控制台Console，例如`http://localhost:9001`。

使用為容器指定的環境文件中的MINIO_ROOT_USER和配置進行登入。MINIO_ROOT_PASSWORD
MinIO 控制台在全新安裝中顯示儲存桶視圖

您可以使用 MinIO 控制台執行一般管理任務，例如身分識別和存取管理、指標和日誌監控或伺服器設定。每個 MinIO 伺服器都包含自己的嵌入式 MinIO 控制台。

如果您的本機主機防火牆允許外部存取控制台端口，則同一網路上的其他主機可以使用本機的 IP 或主機名稱存取控制台。

## Terminology

### XFS

XFS 是一種高效能的 64 位元日誌檔案系統，最早由 Silicon Graphics, Inc. (SGI) 於 1993 年為其 IRIX 作業系統開發，後來在 Linux 上廣泛使用。XFS 擅長處理大檔案和高吞吐量，特別適合對檔案系統性能要求高的環境，如伺服器、資料庫、和大數據處理工作負載。

#### 主要特點：

1. **高擴展性**：
   XFS 可以支持非常大的檔案系統和檔案，最大可達數百 exabytes 的檔案系統和檔案大小。

2. **效能優化**：
   XFS 以高效能為目標設計，特別是在處理大檔案和高並發 I/O 操作時表現出色。它的設計優化了讀寫大檔案的性能，並且可以很好地處理大量小檔案。

3. **日誌記錄**：
   XFS 使用日誌技術來記錄檔案系統的變更，這樣在系統崩潰或突然斷電後，可以快速恢復檔案系統，減少數據損失的風險。

4. **可即時碎片整理**：
   XFS 支持即時的檔案系統碎片整理，當檔案碎片化時，可以不影響檔案系統的使用進行整理，保持存取性能。

5. **並行 I/O 支援**：
   XFS 擁有卓越的並行 I/O 處理能力，可以充分利用多處理器和多磁碟的系統架構，以提高讀寫效率。

6. **資料擴展與縮減**：
   XFS 支持動態擴展檔案系統大小，這在管理大型存儲池時非常有用。使用者可以隨時擴展檔案系統空間，而無需重新格式化或中斷系統運行。

#### 應用場景：
- **伺服器與企業存儲**：XFS 是 Linux 伺服器和企業存儲環境中的熱門選擇，特別是在需要高效能和高穩定性的場景。
- **資料庫**：由於其出色的高效能處理大檔案和 I/O 操作，XFS 非常適合用於存儲大型資料庫。
- **大數據和高效能計算**：需要處理大量資料和文件的高效能計算環境，通常會使用 XFS 來處理這類高負載。

總的來說，XFS 是一種穩定、高效、功能豐富的檔案系統，特別適合大數據、伺服器、和高效能計算的應用場景。