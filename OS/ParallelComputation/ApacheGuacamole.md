---
layout: default
title:  Apache Guacamole
parent:   Parallel Computation
grand_parent: Operation Systems
last_modified_date: 2022-04-25 12:20:36
---
# Apache Guacamole
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

[Apache Guacamole](https://guacamole.apache.org/)是一個開源的遠端桌面網頁應用程式，它允許用戶透過瀏覽器訪問和控制遠端桌面。以下是有關 Apache Guacamole 的一些更多介紹：

### 特點：

1. **支援協議：**
   - Guacamole 支援多種遠端協議，包括 VNC、RDP 和 SSH。這意味著您可以透過同一個介面訪問不同協議的遠端桌面。

2. **無需客戶端安裝：**
   - Guacamole 是一個基於 Web 的應用程式，不需要在用戶端安裝任何客戶端軟體。用戶只需要一個支援 HTML5 的瀏覽器即可。

3. **多用戶支援：**
   - Guacamole 具有多用戶支援，可以設定不同用戶的權限和訪問控制。

4. **整合驗證機制：**
   - Guacamole 支援多種身份驗證方式，包括 LDAP、MySQL、PostgreSQL、以及本地的 XML 驗證。這使得與現有的身份驗證系統（如 Active Directory）整合變得容易。

5. **多語言支援：**
   - Guacamole 提供多語言支援，使得用戶可以選擇自己熟悉的語言進行操作。

### AD 整合：

Guacamole支援與Active Directory（AD）整合，這使得用戶可以使用他們在 AD 中的憑據來登入 Guacamole。這提供了單一登入（Single Sign-On，SSO）的能力，使得管理和使用更加方便。

整合 AD 的步驟通常包括配置 Guacamole 的 LDAP 身份驗證以連接到 AD 伺服器，並確保 Guacamole 中的用戶帳戶映射到 AD 中的用戶。具體的步驟可能會根據您的環境和需求而有所不同，建議查閱 Guacamole 官方文檔以獲得最新和詳細的整合指南。

### 其他開源方案

在 Windows 環境下，有一些開源（opensource）或免費的遠端控制和遠端桌面軟體，其中一些可能適合您的需求。以下是一些常見的開源或免費遠端控制軟體：

1. **[RealVNC](https://www.realvnc.com/):**
   - RealVNC 提供了免費版本，允許您在 Windows 系統之間進行遠端控制。它也提供了商業版本，具有更多功能。

2. **[TightVNC](https://www.tightvnc.com/):**
   - TightVNC 是 VNC（Virtual Network Computing）的一個衍生版本，提供免費的遠端控制功能。它支援 Windows 平台。

3. **[UltraVNC](https://www.uvnc.com/):**
   - UltraVNC 是 VNC 的另一個分支，提供免費的遠端控制和支援 Windows。它具有快速的更新速度和較低的延遲。

4. **[Apache Guacamole](https://guacamole.apache.org/):**
   - Apache Guacamole 是一個基於 Web 的遠端桌面網頁應用程式，支援 VNC、RDP 和 SSH。它是開源的，並可以在 Windows 平台上使用。

5. **[AnyDesk](https://anydesk.com/):**
   - AnyDesk 不是完全開源，但提供免費版本，支援 Windows 平台。它以高性能和低延遲為特點。

請確保在使用這些工具之前仔細閱讀其使用條款，並遵守相關法律法規。選擇一個適合您需求的遠端控制軟體可能會取決於您的使用情境、安全需求和個人喜好。

## 硬體設備

- 在公司網路區分出4台個人電腦架設內部網路，需要甚麼樣的軟硬體，可以達成叢集的效能?
架設內部網路上的集群需要考慮軟硬體和網路配置，以實現效能和高可用性。以下是建議的硬體和軟體元件：

### 硬體要求：

1. **伺服器：**
   - 至少 4 台伺服器，每台配備相當於您的應用程式需求的適當硬體，包括 CPU、RAM 和儲存容量。
   - 選擇支援虛擬化和叢集的伺服器硬體，以確保更好的效能。

2. **網路交換機：**
   - 高效能的網路交換機，以確保伺服器之間的高速連接。
   - 選擇支援 1 Gbps 或 10 Gbps 以及支援 VLAN 的交換機。

3. **網路連接：**
   - 每台伺服器需要至少一個網路介面卡（NIC）。
   - 如果可能，使用雙連接（Dual NIC）以實現冗餘和高可用性。

4. **電源供應器：**
   - 確保伺服器的電源供應器具有冗餘性，以防止單點故障。

### 軟體要求：

1. **作業系統：**
   - 選擇支援叢集和虛擬化技術的作業系統，例如 Linux 的 CentOS、Ubuntu Server，或者 Windows Server。
   - 保持所有伺服器上的作業系統版本和補丁保持一致。

2. **虛擬化平台：**
   - 使用虛擬化平台來管理和部署虛擬機（VM），例如 KVM/QEMU、VMware、或 Hyper-V。

3. **叢集管理工具：**
   - 選擇合適的叢集管理工具，例如 Kubernetes（適用於容器化應用程式）、Apache Hadoop（適用於分散式運算），或者 Pacemaker（適用於 HA 叢集）。

4. **網路設定：**
   - 配置正確的 IP 地址、子網掩碼和網關，確保伺服器能夠正確通信。
   - 考慮使用虛擬 IP 地址和 Load Balancer 以實現負載均衡。

5. **安全性工具：**
   - 實施適當的防火牆和安全性措施。
   - 使用適當的存取控制和身份驗證來保護內部網路。

6. **監控工具：**
   - 安裝監控工具以實時監視伺服器性能和狀態。
   - 使用日誌管理工具來記錄系統事件和錯誤。

7. **儲存：**
   - 確保您有足夠的儲存容量，並使用 RAID 或其他冗餘技術以防止資料損失。

8. **備份和復原：**
   - 設定定期備份和復原計劃，以保護數據並快速復原系統。

以上只是一個概觀，實際需求可能會根據您的應用程式、預算和性能要求而有所不同。在進行任何部署之前，建議進行仔細的需求分析和規劃。


## 安裝

