---
layout: default
title: HPA in k8s 
parent: Kubernetes
grand_parent: Parallel Computation
last_modified_date: 2024-10-02 10:19:38
---

# Horizontal  Pods Autoscaling 

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

> 可不可以用本機系統資源的百分比為量度，直接交付kubeadm來管理，也不刻意分節點，可能有這種設定方式嗎？

- minikube可以將主機上的部分資源定義成節點以供pod來使用、而生產階段的kubeadm則是將主機所有資源納入分配，所以需要知道每個pod可以使用的資源上限、總體的上限在哪裡？等等問題討論。

## Ans 

是的，Kubernetes 支持根據資源的 **百分比** 來配置 Pod 的資源需求和限制，而不是只使用固定的 CPU 和內存數量。這意味著你可以在 **kubeadm** 部署的叢集中配置資源限制，讓每個 Pod 根據系統資源的相對百分比來進行分配，而不需要刻意手動分配到具體的節點。

### 使用資源請求和限制進行百分比量度

在 Kubernetes 中，通過 `resource requests` 和 `resource limits` 來設定 Pod 需要多少資源。這可以根據每個 Pod 的需求動態分配系統資源。雖然 Kubernetes 不能直接使用 "百分比" 來指定資源，但你可以通過計算每個 Pod 的請求相對於節點總資源的比例，來達成類似的效果。

### 1. **資源請求與限制**

- **資源請求（requests）**：Pod 需要的最小資源量，Kubernetes 調度器會基於這個請求來確保 Pod 能在節點上正常運行。
- **資源限制（limits）**：Pod 能使用的最大資源量，即使節點還有空閒資源，Pod 也無法超過這個上限。

例如，你可以為一個 Pod 設置 CPU 和內存的資源請求和限制：

```yaml
resources:
  requests:
    cpu: "500m"  # 表示 0.5 個 CPU
    memory: "1Gi"  # 表示 1GB 內存
  limits:
    cpu: "1"  # 表示最多使用 1 個 CPU
    memory: "2Gi"  # 表示最多使用 2GB 內存
```

### 2. **根據系統資源百分比進行分配**

雖然 Kubernetes 不能直接通過百分比來分配資源，但你可以根據節點的總資源來設置 Pod 的請求。例如，如果一個節點有 8 個 CPU，你可以讓某些 Pod 的 CPU 請求為 `500m`（即 0.5 個 CPU，相當於 6.25%），而限制為 `2`（即 25% 的總 CPU 資源）。

- **Node 的資源總量**：每個節點的 CPU 和內存資源可以通過 Kubernetes 資源查詢來獲取，這樣你就可以計算出每個 Pod 應該佔用的資源百分比。
  - 查看節點資源情況：`kubectl describe node <node-name>`。
  
### 3. **允許 Kubernetes 自動負載平衡**

Kubernetes 支持自動調度器，它會根據每個節點的資源狀態，將 Pod 自動調度到資源充裕的節點上。這樣你不必手動指定每個 Pod 要運行在哪個節點。Kubernetes 會根據你配置的資源請求和限制，將 Pod 分佈到不同的節點，達到資源的自動分配和平衡。

### 4. **不刻意分節點的方案**

- **不強制指定節點**：如果不想刻意將 Pod 分配到特定節點，可以不設置 `nodeSelector` 或 `affinity` 等約束條件，這樣 Kubernetes 會自動根據資源負載情況在不同的節點之間分配 Pod。
  
- **讓 Kubernetes 自動管理**：Kubernetes 的調度器會根據節點的當前資源利用率和 Pod 的資源請求來進行調度。因此，Kubernetes 會自動選擇一個有足夠資源的節點來運行 Pod，而你不必手動管理具體的節點資源分配。

### 5. **Horizontal Pod Autoscaler（HPA）**

你還可以使用 **Horizontal Pod Autoscaler（HPA）** 根據 CPU 或內存的使用情況，自動增加或減少 Pod 的數量。HPA 會根據系統資源的實際使用情況動態調整應用負載，這樣你可以在不分配固定節點的情況下，根據負載情況擴展應用。

配置 HPA 示例：

```yaml
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50  # 當 CPU 利用率超過 50% 時擴展 Pod
```

## 工作節點的準備與加入

> 工作節點是否只要啟動kubelet、打開防火牆，就能接受主節點的連結？

是的，**工作節點** 要能加入 Kubernetes 叢集，接受主節點（控制平面節點）的連結，基本條件包括：

### 1. **啟動 `kubelet`**：

   - `kubelet` 是 Kubernetes 的核心組件之一，負責管理和執行在工作節點上的 Pod。每個工作節點必須運行 `kubelet`，才能與 Kubernetes 控制平面互動。
   - 當工作節點成功加入叢集後，`kubelet` 會定期向主節點的 API Server 報告節點狀態。

### 2. **防火牆配置**：

   - 要讓工作節點與主節點正常通信，需要確保防火牆打開所需的端口，尤其是以下常見端口：

     **工作節點需要開放的端口：**
     - **10250**：`kubelet` API，用於主節點和 `kubelet` 之間的通信。
     - **30000-32767**：Kubernetes 預設的 NodePort 範圍，用於服務之間的通信。
   
     **主節點需要開放的端口（從工作節點連接）**：
     - **6443**：Kubernetes API Server 的端口，用於所有控制平面與工作節點之間的通信。

   具體配置可以根據使用的防火牆工具（如 `iptables`、`firewalld` 等）來調整。確保主節點和工作節點之間的必要端口是開放的，以便節點之間能順利通信。

### 3. **加入 Kubernetes 叢集**

   - 在工作節點上啟動 `kubelet` 並打開防火牆後，還需要將工作節點加入 Kubernetes 叢集。這通常是通過以下步驟完成的：
   
   1. **在主節點上生成加入指令**：
      - 使用 `kubeadm` 工具生成加入工作節點的 token。這個 token 是用來讓工作節點加入控制平面的憑證。
      ```bash
      kubeadm token create --print-join-command
      ```

   2. **在工作節點上執行加入命令**：
      - 在每個工作節點上執行由主節點生成的 `kubeadm join` 命令，這將讓該工作節點連接到控制平面並正式成為 Kubernetes 叢集的一部分。
      - 例如：
      ```bash
      kubeadm join <control-plane-ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
      ```

### 4. **檢查連接狀態**

   - 完成以上步驟後，可以通過主節點使用 `kubectl get nodes` 檢查工作節點是否已成功加入叢集。
   - 如果節點狀態顯示為 "Ready"，則表明工作節點已正常運行，並能夠接受主節點的調度。

### 總結

要讓工作節點接受主節點的連結，基本步驟是：

1. **啟動 `kubelet`**：這是每個工作節點必須運行的核心進程。
2. **打開防火牆**：確保主節點和工作節點之間的必要端口（如 10250 和 6443）是開放的。
3. **使用 `kubeadm` 將工作節點加入 Kubernetes 叢集**。
4. **檢查節點狀態**：確認節點加入並處於 "Ready" 狀態。

### 結論

- **不需要刻意分配節點**：你可以使用 Kubernetes 的自動調度器來自動分配資源，而不需要手動分配節點。系統會根據資源需求和節點可用資源來決定 Pod 的具體運行位置。
  
- **資源分配根據百分比**：雖然 Kubernetes 不支持直接通過百分比來配置資源，但你可以通過計算節點總資源並設置合適的 `requests` 和 `limits` 來間接實現類似效果。

這樣的配置對於像 **JupyterHub** 這樣的應用場景是合適的，特別是當多用戶同時運行 Notebook，並且你希望 Kubernetes 動態管理資源分配時。

## 有centos 版本的kubelet嗎？

是的，**`kubelet`** 支援 **CentOS**，並且可以在 CentOS 上安裝 Kubernetes 的相關工具，包括 `kubelet`、`kubeadm` 和 `kubectl`。這些軟件可以通過 Kubernetes 的官方 YUM 軟件庫來安裝。

### 在 CentOS 上安裝 `kubelet` 的步驟

#### 1. **更新系統**

首先，確保你的 CentOS 系統是最新的：
```bash
sudo yum update -y
```

#### 2. **關閉 SELinux**

Kubernetes 需要禁用 SELinux，否則可能會導致許多權限相關的問題：

```bash
sudo setenforce 0
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
```

#### 3. **禁用 Swap**

Kubernetes 要求禁用 Swap，這是因為 Swap 可能會影響調度器的行為：

```bash
sudo swapoff -a
sudo sed -i '/swap/d' /etc/fstab
```

#### 4. **配置 Kubernetes 軟件庫**

將 Kubernetes 的 YUM 軟件庫添加到 CentOS 的軟件源中：

```bash
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF
```

#### 5. **安裝 `kubelet`、`kubeadm` 和 `kubectl`**

一旦設置了 Kubernetes 軟件庫，你可以安裝 `kubelet`、`kubeadm` 和 `kubectl`：

```bash
sudo yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
```

#### 6. **啟動並啟用 `kubelet`**

安裝完成後，啟動並設置 `kubelet` 隨系統啟動：

```bash
sudo systemctl enable --now kubelet
```

#### 7. **配置防火牆**

確保 CentOS 上的防火牆允許 Kubernetes 所需的端口流量：

```bash
sudo firewall-cmd --permanent --add-port=6443/tcp   # Kubernetes API 端口
sudo firewall-cmd --permanent --add-port=10250/tcp  # Kubelet API 端口
sudo firewall-cmd --reload
```

### 總結

你可以在 CentOS 上安裝和運行 `kubelet`。透過配置官方的 Kubernetes 軟件庫來安裝 `kubelet`、`kubeadm` 和 `kubectl`，並確保禁用 SELinux 和 Swap，然後啟動並啟用 `kubelet`，就能讓你的 CentOS 系統成為 Kubernetes 叢集的一部分。

## docker as a worker ?

> 要關閉selinux/swap?我可以在一個docker裡面準備這些條件，這樣control-plan可以連結嗎？

你可以在 Docker 容器中準備 Kubernetes 組件（如 `kubelet` 和 `kubeadm`），但是會有一些限制和挑戰。這種設置方式不是 Kubernetes 的常見做法，主要原因是 `kubelet` 和容器技術如 Docker 本身的運作邏輯有所重疊。此外，`kubelet` 需要直接訪問主機的系統資源（如 Cgroups、網絡設備和文件系統），這些資源通常無法輕易在容器中完全模擬。

### 運行在 Docker 容器中的挑戰

1. **關閉 SELinux 和 Swap**：
   - **SELinux** 和 **Swap** 是在宿主機上管理的，關閉這些功能主要是為了確保 Kubernetes 正常運行。如果你想在 Docker 容器中運行 `kubelet`，你可以不在容器中進行這些操作，因為這些設定會由宿主機進行管理。
   
2. **容器的系統訪問**：
   - `kubelet` 需要訪問宿主機的資源，而 Docker 容器是隔離的。因此，你需要使用 Docker 的一些選項來突破這些限制，比如使用 `--privileged` 標誌來運行容器，允許它訪問更多的系統資源。
   
3. **網絡連接問題**：
   - 由於容器和宿主機之間有網絡隔離，確保容器中的 Kubernetes 組件可以與外部網絡（如控制平面節點）進行通信是非常重要的。你需要配置 Docker 容器的網絡，並確保所有必要的端口（如 6443、10250）都可以在容器內外部通行。

### 實現方式

1. **準備 Docker 容器**：
   - 構建一個 Docker 容器映像，包含 Kubernetes 組件（如 `kubeadm`、`kubelet` 和 `kubectl`），並允許 `kubelet` 和主機系統進行交互。
   - Dockerfile 示例：
     ```Dockerfile
     FROM centos:7

     # 安裝依賴
     RUN yum update -y && \
         yum install -y kubelet kubeadm kubectl

     # 啟用 kubelet
     CMD ["kubelet"]
     ```

2. **啟動 Docker 容器**：
   - 使用 `--privileged` 和正確的網絡配置來運行容器：
     ```bash
     docker run --privileged --network=host -d your-kubernetes-image
     ```

   - 這樣可以允許容器訪問主機的系統資源，並使它能夠與控制平面節點進行通信。

3. **添加到 Kubernetes 叢集**：
   - 當容器運行起來後，你可以使用 `kubeadm` 在宿主機上生成 `kubeadm join` 命令，並將容器中的工作節點加入 Kubernetes 叢集。
   - 在容器內運行 `kubeadm join` 命令來連接控制平面。

### 注意事項

- **不建議在生產環境中**：將 Kubernetes 工作節點運行在 Docker 容器內，僅適合測試和開發環境。在生產環境中，最好將 Kubernetes 直接運行在虛擬機或裸機上，確保可靠性和性能。
  
- **Docker 的限制**：即使使用 `--privileged` 模式，某些系統資源的完全訪問權限仍可能存在限制，因此你可能需要進行大量的配置和調試。

### 替代方案

如果你想要輕量化測試 Kubernetes，可以考慮使用像 **kind (Kubernetes in Docker)** 這樣的工具，這些工具設計用來在 Docker 中模擬 Kubernetes 多節點叢集，並已經處理了許多兼容性問題。

## minikube vskubeadm

> 我有3台主機，CPU核心各有20核、目前也都有低量的其他服務任務，jupyterhub生產階段的服務你會建議3台個別執行Minikube？還是用kubeadm串連？

對於 JupyterHub 的生產環境部署，在你的三台主機上，我強烈建議使用 **kubeadm** 來串連三台主機，而不是在每台主機上分別運行 Minikube。以下是兩者的比較和建議：

### 1. **使用 kubeadm 串連 (推薦)**

- **彈性和擴展性**：`kubeadm` 是設計用於生產環境的工具，可以將多台主機（工作節點）串連在一起，形成一個高彈性的多節點 Kubernetes 叢集。這樣的架構適合需要在多台主機間分配負載的應用，特別是像 JupyterHub 這樣的多用戶應用。
  
- **資源利用效率**：通過 `kubeadm`，你可以將三台主機組成一個統一的 Kubernetes 叢集，允許 Pod 在不同的節點之間根據資源使用情況進行分配。這樣可以更好地利用每台主機的 CPU 和內存資源，並且減少某些節點過載的情況。

- **高可用性**：如果你使用 `kubeadm`，可以實現多節點高可用。假設其中一台主機出現問題，其他節點可以繼續提供服務，而不會影響整個 JupyterHub 的運行。

- **簡化管理**：在生產環境中，將所有的節點統一管理和監控會更容易。`kubeadm` 使得你能夠統一管理多個工作節點，並且支持更多的生產工具，比如備份、監控和自動擴展。

### 2. **使用 Minikube**

- **單節點環境**：Minikube 本質上是為本地開發和測試設計的單節點 Kubernetes 叢集。每個 Minikube 叢集都是孤立的，無法將不同主機的 Minikube 互相串連。
  
- **資源利用問題**：如果你在每台主機上分別運行 Minikube，它們會各自為政，無法共享資源，這可能會導致某些主機過載，而其他主機的資源空閒。

- **缺乏擴展能力**：Minikube 不支持生產級的多節點部署，並且缺乏 Kubernetes 在多節點部署中的強大調度能力。

### 建議

由於你有多台主機並且準備部署生產環境的 JupyterHub，**使用 `kubeadm` 串連三台主機形成一個完整的多節點 Kubernetes 叢集** 是最合適的選擇。這樣你可以將資源統一管理，並根據需求分配任務，獲得更高的彈性和可擴展性。

## 實務討論

### 最大應用時節點功能分配

- 以infiniband網路為實體網域。
- 方案一：master 負責control-plan、其餘node1~3作為workers
  - 檢討master轉換OS的困難與必要性
  - node03 FreeIPA似乎必須保持是CENTOS。
- 方案二：node02自己是control and worker、另聯合node01甚至其他ubuntu工作站做workers。
  - 跨節點的傳輸需求似乎不是考慮重點？！