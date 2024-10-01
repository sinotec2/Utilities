---
layout: default
title:  docker lunchers
parent:   docker system
grand_parent: Parallel Computation
last_modified_date: 2024-06-01 17:41:56
---
# docker lunchers
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

### 結論

- **不需要刻意分配節點**：你可以使用 Kubernetes 的自動調度器來自動分配資源，而不需要手動分配節點。系統會根據資源需求和節點可用資源來決定 Pod 的具體運行位置。
  
- **資源分配根據百分比**：雖然 Kubernetes 不支持直接通過百分比來配置資源，但你可以通過計算節點總資源並設置合適的 `requests` 和 `limits` 來間接實現類似效果。

這樣的配置對於像 **JupyterHub** 這樣的應用場景是合適的，特別是當多用戶同時運行 Notebook，並且你希望 Kubernetes 動態管理資源分配時。
