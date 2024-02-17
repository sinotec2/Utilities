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

### 硬體設備

- 在公司網路區分出4台個人電腦架設內部網路，需要甚麼樣的軟硬體，可以達成叢集的效能?



## 安裝

