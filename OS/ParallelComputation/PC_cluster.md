---
layout: default
title:  PC計算叢集的相應設定
parent:   Parallel Computation
grand_parent: Operation Systems
last_modified_date: 2022-04-25 12:20:36
---
# PC計算叢集的相應設定
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

## 使用者設定

- 可否設定特定的window使用者名稱，當以其登入window是，設定可接受Guacamole的遠端遙控，而以其他人登入時，則否？

Guacamole本身並沒有直接的機制來限制特定Windows使用者名稱的遠程遙控訪問權限。Guacamole的身份驗證機制通常是基於用戶提供的憑據（例如用戶名和密碼）。

然而，你可以在Windows系統上使用相應的權限和安全設置來達到類似的目標。具體來說，你可以配置Windows使用者帳戶的權限，確保只有特定的使用者擁有遠程桌面訪問的權限，而其他使用者則沒有。這可以在Windows的"遠程桌面使用者"組或類似的組織單位中進行配置。

在Guacamole方面，你仍然需要提供這些Windows使用者的憑據，以便Guacamole能夠進行LDAP身份驗證或其他支援的身份驗證方法。確保設定Guacamole的LDAP或其他身份驗證方式，以與Windows上的使用者管理系統協同工作。

## 內部化

### 連線使用者上Internet權限

在資安的考量下，確實有可能限制特定使用者在Windows系統上的Internet連接權限。這可以透過Windows系統的一些內建功能來實現。

一種方法是使用Windows的防火牆（Firewall）設置，你可以配置防火牆規則，僅允許特定使用者或應用程式訪問Internet。這可以通過「Windows Defender 防火牆」等工具來實現。

另一種方法是通過Windows的群組原則（Group Policy）來限制特定使用者的網路訪問權限。你可以配置群組原則以禁用或限制特定使用者的網路訪問權限，以確保他們無法連接到Internet。

請注意，確保在實施這些限制之前，你深入了解相關設置的影響，以防止不必要的中斷或阻礙。此外，這僅限於Windows系統的控制，Guacamole伺服器和其它可能使用的系統也需要單獨考慮和配置。

### 與Anydesk方案的比較

讓我們更深入比較Apache Guacamole和AnyDesk在資訊安全、Internet連線、地端方案、速度等方面的差異：

**1. 資訊安全:**
   - **Guacamole:** Guacamole的開源性質意味著可以進行更深入的安全審查，並提供多種身份驗證方法，如LDAP。它的開源特點也允許使用者檢查代碼，加強安全性。
   - **AnyDesk:** AnyDesk提供TLS加密連接，但由於是封閉的商業產品，其安全性細節可能不如開源軟體透明。

**2. Internet連線:**
   - **Guacamole:** 透過Web瀏覽器訪問，並在互聯網上使用。連線的穩定性和速度受到伺服器和客戶端之間的網絡環境的影響。
   - **AnyDesk:** 提供直觀的用戶界面，支援在不同網絡環境下的實時遠程連接。

**3. 地端方案:**
   - **Guacamole:** 提供開源且可自定製的遠程桌面解決方案，伺服器端可在Linux上運行。
   - **AnyDesk:** 為商業解決方案，提供各種操作系統的桌面客戶端。

**4. 速度:**
   - **Guacamole:** 速度取決於伺服器和客戶端之間的帶寬和延遲。由於使用Web瀏覽器，可能受到瀏覽器性能的影響。
   - **AnyDesk:** 通常提供快速的實時遠程控制，採用先進的編碼和優化技術。

總的來說，Guacamole更注重開源和自定製性，而AnyDesk更注重商業用途，提供簡單易用的界面。在選擇之前，需考慮你的特定需求、安全性要求、使用環境以及是否需要商業支援。


