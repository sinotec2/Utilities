---
layout: default
title: 儲存設備的考量 
parent: Kubernetes
grand_parent: Parallel Computation
last_modified_date: 2024-10-02 10:19:38
---
# Storage

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

> k8s儲存設備中所謂的standard是什麼意思？k8s有哪些儲存方案？生產階段佈置的考量有哪些因素？

在 Kubernetes 中，**`standard`** 是一種預設的 **StorageClass** 名稱，通常用來指定叢集中默認的存儲設備。當你創建 **Persistent Volume Claim (PVC)** 而沒有明確指定 **StorageClass** 時，Kubernetes 就會自動將這些 PVC 綁定到被標記為 `standard` 的存儲類別上。

### Kubernetes 的存儲方案

Kubernetes 提供了多種存儲解決方案，支持不同的使用場景和基礎架構需求。以下是常見的 Kubernetes 存儲方案：

1. **HostPath**  
   - **描述**: 直接將節點本地的文件系統目錄掛載到 Pod。
   - **使用場景**: 只在單節點部署中適用，或測試環境。
   - **限制**: 數據無法跨節點共享；節點重啟後數據可能丟失。

2. **NFS（Network File System）**  
   - **描述**: 通過網絡共享文件系統，允許多個節點讀寫同一份數據。
   - **使用場景**: 用於需要跨節點共享數據的場景，如用戶上傳的數據或分析結果。
   - **優勢**: 跨節點數據共享，擴展性高。
   - **限制**: 性能取決於網絡速度和 NFS 服務器的性能。

3. **Ceph**  
   - **描述**: 分布式存儲系統，支持塊存儲、對象存儲和文件系統存儲。
   - **使用場景**: 大型叢集的分布式文件系統，適合需要高可用性、高性能和數據持久化的場景。
   - **優勢**: 分布式、可擴展，支持數據冗餘和自動修復。
   - **限制**: 需要額外的硬件資源和管理工作，複雜性高。

4. **AWS EBS (Elastic Block Store)**  
   - **描述**: AWS 提供的塊存儲服務，適用於在 AWS 上運行的 Kubernetes 叢集。
   - **使用場景**: AWS 環境中的工作負載，適合需要高性能塊存儲的應用。
   - **優勢**: 與 AWS 服務緊密集成，性能穩定。
   - **限制**: 只能綁定到一個節點，跨區域操作較複雜。

5. **Azure Disk / Azure Files**  
   - **描述**: Azure 提供的塊存儲和文件存儲，適合運行在 Azure 上的 Kubernetes 叢集。
   - **使用場景**: 需要塊存儲的應用（Azure Disk），或跨節點共享文件的應用（Azure Files）。
   - **優勢**: 與 Azure 服務緊密集成，適用於各種 Azure 環境。
   - **限制**: Azure Disk 只能掛載到一個節點，Azure Files 性能相對較低。

6. **GCE Persistent Disk (Google Cloud Platform)**  
   - **描述**: Google Cloud 提供的永久性磁盤存儲。
   - **使用場景**: 需要在 Google Cloud 中持久化數據的 Kubernetes 應用。
   - **優勢**: Google Cloud 原生支持，高效且擴展性好。
   - **限制**: 無法跨節點共享，僅適用於 Google Cloud。

7. **CSI（Container Storage Interface）插件**  
   - **描述**: CSI 是一種標準接口，使得 Kubernetes 可以支持各種外部存儲系統，如 Ceph、GlusterFS、Portworx 等。
   - **使用場景**: 需要使用外部存儲服務器的場景。
   - **優勢**: 支持多種存儲系統，靈活擴展。
   - **限制**: 根據具體存儲系統的不同，配置和運行複雜度各異。

### 生產階段部署的考量因素

在生產環境中部署 Kubernetes 存儲系統時，需考慮以下關鍵因素：

1. **可用性與冗餘**
   - 保證數據持久性和高可用性，防止數據丟失或損壞。可以通過分布式存儲（如 Ceph）或數據備份策略來實現數據冗餘。

2. **性能需求**
   - 根據應用的性能需求選擇合適的存儲類型。需要高 I/O 性能的應用應使用高性能塊存儲（如 AWS EBS 或 GCE Persistent Disk），而對於文件共享應用則選擇文件系統存儲（如 NFS 或 Azure Files）。

3. **擴展性**
   - 隨著用戶和數據量的增長，存儲系統需要具備良好的擴展性。分布式存儲系統（如 Ceph 或 GlusterFS）更適合需要動態擴展的大型集群。

4. **備份與恢復**
   - 確保有足夠的備份機制來應對數據丟失或故障。可以使用外部備份工具或分布式存儲自帶的冗餘功能來保障數據安全。

5. **成本效益**
   - 不同的存儲方案會產生不同的成本。需要根據性能需求、數據量和可用資源來選擇最具成本效益的存儲解決方案。高性能存儲通常成本較高，但可用於關鍵應用；低成本的存儲則適合長期備份或冷數據存儲。

6. **數據一致性**
   - 生產環境中，數據一致性是至關重要的。如果多個 Pod 或節點需要共享同一份數據，選擇支持多寫的分布式文件系統或共享存儲是關鍵。

7. **網絡延遲**
   - 網絡存儲的性能取決於網絡的帶寬和延遲。確保節點和存儲之間有足夠的帶寬，尤其是使用 NFS 或其他網絡存儲時，需要有千兆級甚至更高的網絡速度來支持。

### 總結

在 Kubernetes 中，`standard` 是系統預設的存儲類別，通常由基礎設施提供商設置默認存儲類型。生產階段中，你需要考慮高可用性、性能需求、擴展性、備份策略和網絡延遲等因素，選擇合適的存儲解決方案來保障應用穩定運行。

## 跨節點檔案傳輸

> A主機是控制平面、使用者界面是在A主機，如果將計算分配給B主機，上傳檔案是否也會傳給B主機？

在 Kubernetes 叢集中，如果 **A 主機** 作為控制平面並同時提供使用者界面，而計算資源分配給 **B 主機**，那麼具體到文件上傳的情況會取決於以下幾個因素：

### 1. **Pod 和計算的分佈**

   - **Kubernetes Pod** 的調度策略決定了計算在哪個節點上執行。如果計算任務（如 Jupyter Notebook 的 kernel）被分配到 **B 主機** 上，那麼所有與該 Pod 相關的計算和數據處理都會在 **B 主機** 上進行。
   - **A 主機** 上作為控制平面和使用者界面提供服務的部分只處理使用者的接口操作和交互，而不一定處理實際的計算任務。

### 2. **上傳檔案的行為**

   - 當使用者在界面上上傳文件時，文件會首先被傳到與使用者界面相關聯的 Pod。如果這個 Pod 被調度到 **A 主機**，文件最初會存儲在 A 主機的相關路徑中（如某個 Persistent Volume）。
   
   - 如果後續的計算任務分配到了 **B 主機**，那麼依賴該文件的計算過程可能需要從 **A 主機** 將該文件同步或共享給 **B 主機** 上的 Pod。

### 3. **持久性存儲的配置**

   - **Persistent Volume (PV)** 和 **Persistent Volume Claim (PVC)** 的配置對於解決這類情況至關重要。如果使用共享的存儲（例如 NFS 或者雲端存儲），那麼文件上傳後會自動存放在所有節點都能訪問的共享存儲上，無論計算在哪個主機上執行，Pod 都可以訪問到該文件。
   
   - **NFS（網絡文件系統）** 是一種常見的解決方案，這樣所有 Pod（無論是 A 還是 B 主機上的）都可以通過網絡訪問同一個文件系統中的上傳文件。這樣，上傳文件不會局限於單個節點，計算也可以在不同節點上無縫進行。

### 4. **JupyterHub 與存儲配置**

   - 在 JupyterHub 配置中，通常每個用戶會有一個與 Pod 綁定的持久存儲目錄。這些目錄可以通過 NFS 或其他共享存儲來實現，確保無論用戶的計算 Pod 被調度到哪個節點，文件都能夠訪問到。
   
   - 如果你使用了 **Helm 部署 JupyterHub**，你可以在 `config.yaml` 中設置一個共享存儲解決方案，確保所有 Pod 都能訪問同一個存儲資源。

### 總結

如果你將計算分配到 **B 主機**，而上傳文件的過程發生在 **A 主機** 上，文件會存儲在 **A 主機** 上。如果兩者沒有共用存儲，那麼 B 主機上的 Pod 可能無法訪問這些文件。因此，最好的做法是配置一個 **共享存儲（如 NFS）**，這樣所有節點上的 Pod 都可以訪問到上傳的文件，無論計算在哪台主機上執行。

## 速度的配置

> 我有高速、低速2個NAS，這樣會需要高速網路來服務這個叢集比較好，是這樣嗎？

是的，如果你有 **高速** 和 **低速** 兩個 NAS（網絡附加存儲）來服務 Kubernetes 叢集，並且要確保叢集中數據的快速存取、計算效率，使用 **高速網路** 來服務叢集是非常重要的。這是因為 NAS 的性能會直接影響到存儲和計算資源的效率。

以下是為什麼需要高速網路來支持 Kubernetes 叢集的幾個關鍵原因：

### 1. **高效的數據存取**

   - **高速 NAS** 可以顯著提升 Pod 在不同節點間存取數據的速度。當你的計算任務（如 JupyterHub 的 Notebook 工作）需要頻繁讀取和寫入數據時，高速存儲與快速的網路連接能減少數據傳輸的延遲，並提升整體的性能。
   - 如果使用低速網路連接高速 NAS，將會降低 NAS 的潛在性能，並且可能導致讀寫延遲，影響 Pod 的計算效率，尤其是當多個使用者同時操作時。

### 2. **多節點間的數據共享**

   - Kubernetes 叢集通常會依賴共享存儲來保證不同節點之間的數據一致性。如果 NAS 存儲是不同節點之間的唯一共享數據來源，高速網路可以確保每個節點能夠快速讀取和寫入數據。
   - 在高負載情況下，節點間的 I/O 請求可能會迅速累積。如果網路帶寬不足，會導致數據傳輸瓶頸，從而拖慢整個叢集的運行速度。

### 3. **用戶上傳/下載的文件處理**

   - 像 JupyterHub 這樣的應用，經常涉及到用戶上傳和下載大量的文件（如數據集、模型、報告等）。在多節點的環境下，這些操作需要快速的文件傳輸來減少使用者的等待時間。如果文件經過低速網路傳遞，會造成延遲，影響用戶體驗。
   - 尤其當計算任務需要讀取這些上傳的文件時，網路傳輸速度直接影響任務的啟動和執行速度。

### 4. **混合使用高速和低速 NAS 的策略**

   - **高速 NAS** 可以用來存儲那些需要頻繁讀寫、低延遲的文件或數據，如當前正在處理的用戶數據、計算結果等。
   - **低速 NAS** 可以用來存放不常變動或冷數據，如長期存檔的用戶資料、備份文件等。這樣可以根據需求靈活使用兩種存儲資源，最大化資源利用效率。
   
### 5. **網絡架構建議**

   - 你應該考慮部署一個 **千兆級別或更高的網路（如 10Gbps）**，來保證所有節點和 NAS 之間有足夠的帶寬進行數據傳輸。這對於有大量數據處理的應用尤其重要，例如 JupyterHub 的大數據分析和模型訓練。
   - 可以通過 **VLAN** 或 **專用存儲網路（如 iSCSI 或 NFS over RDMA）** 來進一步提高網路效率，確保網路流量不受其他服務器的干擾。

### 結論

在多節點的 Kubernetes 叢集中，如果你依賴 NAS 來進行數據存儲，使用高速網路對於提升存取數據的性能非常重要。尤其是當你同時有高低速的 NAS 時，將計算密集型和 I/O 密集型任務放在高速 NAS 上，並確保網路連接能夠滿足數據傳輸需求，是提高整體系統效率的最佳做法。

## 極大化方案

> 你的建議是2個NAS都做成PV？

是的，將兩個 **NAS（高速與低速）** 都做成 **Persistent Volume (PV)** 是一個非常靈活且合理的策略。這樣的設置能夠讓你根據具體的使用需求選擇使用哪個存儲資源，並根據工作負載自動分配高效或低效存儲來優化成本和性能。

### 為什麼將兩個 NAS 都做成 PV 是合適的：

1. **靈活的存儲選擇**  
   將兩個 NAS 都配置為 PV，Kubernetes 可以根據不同的工作負載需求進行分配：
   - **高速 NAS** 可以配置為存儲需要高頻讀寫、低延遲要求的數據，例如用戶正在運行的 Jupyter Notebook 計算任務和數據集。
   - **低速 NAS** 可以配置為長期存儲不常變動或存取的冷數據，例如歷史備份、使用者長期保存的檔案、或者不會頻繁使用的數據。

2. **擴展性**  
   - 配置多個 PV 可以根據你的需求來擴展不同類型的存儲資源。隨著需求增長，你可以輕鬆地新增 PV 而不必重新設置整個存儲架構。
   
3. **自動分配存儲**  
   - 在 Kubernetes 中，當你創建 **Persistent Volume Claim (PVC)** 時，你可以依據具體需求選擇不同的存儲類別，這樣就可以自動將某些應用程序的數據存儲在高速 NAS 上，而將冷數據存儲在低速 NAS 上。
   - 可以根據 **StorageClass** 來區分高性能和低性能的存儲，例如：
     ```yaml
     apiVersion: storage.k8s.io/v1
     kind: StorageClass
     metadata:
       name: high-performance
     provisioner: nfs
     parameters:
       path: /path/to/high-speed-nas
       server: your-high-speed-nas-ip

     apiVersion: storage.k8s.io/v1
     kind: StorageClass
     metadata:
       name: low-performance
     provisioner: nfs
     parameters:
       path: /path/to/low-speed-nas
       server: your-low-speed-nas-ip
     ```

4. **資源分配的最佳化**  
   - 將高性能需求的計算資源（例如活躍的 JupyterHub 用戶計算工作）分配到高速 NAS，可以保證任務的快速執行。而對於冷數據或不頻繁訪問的文件，使用低速 NAS 可以節省成本和資源，避免浪費寶貴的高速存儲。

5. **數據持久性與數據共享**  
   - 使用 **NAS + PV** 配置能保證所有節點上的 Pod 都可以共享和持久化數據。無論計算工作在哪個節點上運行，都可以通過 Kubernetes 的 PVC 動態綁定到正確的存儲資源上，確保數據一致性。

### 如何設置兩個 NAS 的 PV

你可以為每個 NAS 創建不同的 **Persistent Volume (PV)**，並配置它們的 **StorageClass**。例如：

```yaml
# 高速 NAS PV
apiVersion: v1
kind: PersistentVolume
metadata:
  name: high-speed-pv
spec:
  capacity:
    storage: 500Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  nfs:
    path: /path/to/high-speed-nas
    server: <high-speed-nas-ip>
  storageClassName: high-performance

# 低速 NAS PV
apiVersion: v1
kind: PersistentVolume
metadata:
  name: low-speed-pv
spec:
  capacity:
    storage: 1000Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  nfs:
    path: /path/to/low-speed-nas
    server: <low-speed-nas-ip>
  storageClassName: low-performance
```

然後，當應用程序需要存儲時，創建 **Persistent Volume Claim (PVC)**，並指定它要使用的存儲類型（高速或低速）。例如：

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: high-performance-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 100Gi
  storageClassName: high-performance
```

### 總結

通過將 **高速和低速的 NAS 都配置為 PV**，你可以靈活地根據應用程序的需求自動選擇合適的存儲資源，同時優化性能和成本。這樣的架構能保證 Kubernetes 叢集中的任務可以自動、高效地分配到合適的存儲資源上，無論是在多節點環境還是單節點環境下，都能有效提升系統的可擴展性與效能。

> 在jupyterhub應用中，如何規劃這2個nas的應用？目前我只知道綁定db會需要nas的PVC，如果我使用的是固定IP的mysql 伺服器，似乎沒有固定的儲存需求？

在 JupyterHub 應用中，兩個 NAS 的應用可以根據其性能和用途進行規劃，特別是針對不同類型的數據需求：

1. **高速 NAS 的用途**:
   - **用戶工作空間**: 將用戶的臨時工作數據、代碼和處理中的數據存儲在高速 NAS 上，這樣可以確保更快速的讀寫操作，尤其是在進行數據分析、模型訓練或其他計算密集型任務時。
   - **JupyterHub 的動態卷**: 當用戶啟動時，JupyterHub 可以通過動態 PVC 自動為每個用戶綁定一個高速存儲卷，以提高性能和用戶體驗。

2. **低速 NAS 的用途**:
   - **備份和歸檔**: 可以將長期未使用的數據、已完成的計算結果或備份存儲在低速 NAS 上。這樣可減輕高速 NAS 的壓力並節約成本。
   - **共享資料集**: 若有大型共享資料集，且這些數據不需要頻繁讀取，可以將其放在低速 NAS 上，供所有用戶訪問。

3. **MySQL 伺服器的應用**:
   - 如果你使用的是固定 IP 的 MySQL 伺服器，並且伺服器本身有可靠的數據持久化機制，那麼在 Kubernetes 叢集中不一定需要將它綁定到 PVC 上。MySQL 的數據持久化和備份可以依賴於伺服器自身的存儲解決方案（如本地硬碟或專門的 NAS 系統）。
   - 不過，如果你想在叢集中保持所有組件的可移植性和一致性，還是可以將 MySQL 的數據存儲在 NAS 上，並通過 PVC 來實現數據持久化。

### 總結規劃

- **高速 NAS** 用於用戶臨時工作數據和計算任務。
- **低速 NAS** 用於歸檔、備份和共享不頻繁訪問的數據。
- **MySQL 伺服器** 如果使用固定 IP 和自身的存儲，不需要綁定 PVC，但可以選擇綁定以便於更靈活的存儲管理。

這樣的配置可以最大化利用資源，根據性能需求分配存儲方案。

## mount設定

> helm chart如何設定使用者登入目錄為快速NAS？又如何自動為使用者mount慢速NAS成為儲存目錄？

在 JupyterHub 的 Helm Chart 中，你可以通過配置 `config.yaml` 文件來設定使用者登入的工作目錄到快速 NAS，並自動掛載慢速 NAS 作為儲存目錄。這涉及以下幾個步驟：

### 1. 設定快速 NAS 作為使用者登入目錄

快速 NAS 可以通過 Persistent Volume (PV) 和 Persistent Volume Claim (PVC) 在 JupyterHub 的 Helm Chart 中設置。假設你已有快速 NAS 的 NFS 設定如下：

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: fast-nas-pv
spec:
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteMany
  nfs:
    path: /nas/fast-storage  # 快速NAS目錄
    server: 172.20.31.8      # 快速NAS伺服器IP
  storageClassName: fast-storage-class
```

在 Helm Chart 的 `config.yaml` 文件中，為每個使用者的工作目錄分配這個 PVC。示例配置：

```yaml
singleuser:
  storage:
    dynamic:
      storageClass: fast-storage-class  # 使用快速 NAS 的 storageClass
    capacity: 10Gi                     # 每個使用者的存儲配額
    homeMountPath: /home/jovyan        # 使用者登入的工作目錄
```

這樣，每個使用者登入時，會自動掛載快速 NAS 作為其工作目錄。

### 2. 自動掛載慢速 NAS 作為儲存目錄

慢速 NAS 可以作為額外的卷掛載到使用者的 JupyterHub 容器中，提供用戶用於存儲長期數據。以下是慢速 NAS 的 PVC 和相關 Helm Chart 設定：

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: slow-nas-pv
spec:
  capacity:
    storage: 500Gi
  accessModes:
    - ReadWriteMany
  nfs:
    path: /nas/slow-storage  # 慢速NAS目錄
    server: 172.20.31.9      # 慢速NAS伺服器IP
  storageClassName: slow-storage-class
```

在 `config.yaml` 中設定自動掛載這個慢速 NAS 為 `/mnt/storage` 目錄：

```yaml
singleuser:
  storage:
    extraVolumes:
      - name: slow-nas-storage
        persistentVolumeClaim:
          claimName: slow-nas-pvc
    extraVolumeMounts:
      - name: slow-nas-storage
        mountPath: /mnt/storage   # 掛載慢速NAS的目錄
```

同時還需要創建對應的 PVC：

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: slow-nas-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 500Gi
  storageClassName: slow-storage-class
```

### 3. 完整配置流程

1. **定義 PV 和 PVC**: 對應你的快速 NAS 和慢速 NAS。
2. **設定 `config.yaml`**: 配置 Helm Chart，使得快速 NAS 作為使用者的工作目錄，慢速 NAS 自動掛載成為 `/mnt/storage` 這樣的儲存目錄。
3. **部署 Helm Chart**: 使用 `helm upgrade` 或 `helm install` 來部署這些配置到 JupyterHub。

### 總結

- 快速 NAS 綁定為使用者的工作目錄，以獲得高效性能。
- 慢速 NAS 自動掛載到 `/mnt/storage`，供用戶存儲不頻繁使用的長期數據。

這樣的設置能充分利用兩個不同性能的 NAS，提升 JupyterHub 的使用效率與資源管理。

## 權限設定

> 我需要在叢集上 /mnt/storage目錄下先幫使用者開一個目錄嗎？因為使用者應該沒有權限做這個事？

在 Kubernetes 叢集中，如果你想為每個使用者自動創建一個特定的目錄（如 `/mnt/storage/username`），且使用者本身無法在 NFS 共享目錄中創建目錄，通常可以通過以下方式處理：

### 1. **預先創建目錄（手動或自動腳本）**
你可以通過以下方式在 NAS 上的 `/mnt/storage` 目錄中預先為每個使用者創建對應的子目錄：

- **手動創建**：對於少量用戶，可以手動在 NFS 伺服器上創建 `/mnt/storage/username` 這樣的目錄結構，並設置正確的權限。
  
- **自動腳本**：可以編寫一個簡單的腳本，遍歷當前用戶列表，並在 NFS 上自動創建相應的目錄，確保每個用戶的工作目錄存在並且具有正確的權限。

腳本範例（在 NFS 伺服器上執行）：

```bash
#!/bin/bash

# 使用者列表
users=("user1" "user2" "user3")

# NAS 中的根目錄
base_dir="/mnt/storage"

# 為每個使用者創建目錄
for user in "${users[@]}"; do
  user_dir="$base_dir/$user"
  if [ ! -d "$user_dir" ]; then
    mkdir "$user_dir"
    chown "$user:$user" "$user_dir"
    chmod 700 "$user_dir"
    echo "Created directory for $user at $user_dir"
  fi
done
```

這樣做可以確保每個用戶在 NFS 共享目錄下都有自己的存儲目錄，並且只有該用戶能夠訪問。

### 2. **動態創建卷與目錄**
你也可以通過 **動態卷管理** 的方式來自動為每個使用者創建專屬的 PVC，這樣系統會自動創建和管理對應的目錄。這需要更為複雜的配置，通常會涉及到一些動態存儲控制器或外部存儲插件來處理這樣的需求。

### 3. **配置卷初始化腳本**
在 JupyterHub 的 Helm Chart 中，你可以使用 `initContainers` 在每個用戶的容器啟動時運行一個初始化容器，來為使用者創建專屬目錄。該初始化容器可以有足夠的權限在 `/mnt/storage` 下創建用戶目錄。

`config.yaml` 中的示例配置：

```yaml
singleuser:
  storage:
    extraVolumes:
      - name: slow-nas-storage
        persistentVolumeClaim:
          claimName: slow-nas-pvc
    extraVolumeMounts:
      - name: slow-nas-storage
        mountPath: /mnt/storage

  initContainers:
    - name: create-user-dir
      image: busybox
      command: ["sh", "-c", "mkdir -p /mnt/storage/$(USER) && chown 1000:100 /mnt/storage/$(USER)"]
      volumeMounts:
        - name: slow-nas-storage
          mountPath: /mnt/storage
```

這樣，每次使用者容器啟動時，會先通過 `initContainer` 自動創建對應的使用者目錄，並設置權限。

### 總結
- **手動或腳本創建**：適合靜態環境，可以為每個用戶預先創建目錄。
- **`initContainer` 動態創建**：適合需要自動化的場景，能夠在使用者容器啟動時自動創建和分配目錄。
