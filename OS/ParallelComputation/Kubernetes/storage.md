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

### 以下是為什麼需要高速網路來支持 Kubernetes 叢集的幾個關鍵原因：

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