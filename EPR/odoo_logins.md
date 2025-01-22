---
layout: default
title:  odoo login and connections
parent: ERPs
last_modified_date: 2025-01-02 10:29:34
tags: ERP
---

# 登入、權限、連線相關問題

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

### LDAP 登入 Odoo

> 使用者經由Ldap帳密登入Odoo後修改密碼，請問Ldap的密碼會改變嗎？之後登入Odoo就不必由Ldap 轉介？

在 Odoo 與 LDAP 整合的情況下，使用者修改密碼時，是否影響 LDAP 密碼及後續行為，取決於以下幾個因素：

1. LDAP 密碼是否會改變
- 不會改變：
  - Odoo 的 LDAP 整合通常只是進行身份驗證，當使用者在 Odoo 內部修改密碼時，該操作通常只影響 Odoo 本地用戶的記錄，而不會同步修改 LDAP 伺服器上的密碼。
  - Odoo 通常不具有直接寫入或更改 LDAP 密碼的權限，這是為了安全性考量，避免意外覆寫 LDAP 中的憑證。

2. 之後登入是否仍需經由 LDAP 轉介、依情境而定：

- 如果 Odoo 內部存儲了修改後的本地密碼（例如，啟用了本地驗證機制），則使用者在後續登入時可以選擇不使用 LDAP，直接使用 Odoo 本地密碼登入。
- 如果未啟用本地驗證或強制 LDAP 驗證，則仍需透過 LDAP 密碼登入。

3. 如何確認行為
- 檢查 LDAP 設定：
  - 在 Odoo 中檢查是否允許本地密碼登入，設定路徑為：
  - 設定 > 使用者和公司 > LDAP 驗證
  - 若設定中強制啟用了「僅允許 LDAP 驗證」，則即使密碼修改，也需要透過 LDAP 進行身份驗證。
- 測試操作：
  - 可以嘗試修改密碼後，分別使用本地密碼及 LDAP 密碼測試登入行為，以確認設定是否允許繞過 LDAP。

4. 建議的最佳實踐

若希望確保所有登入操作都由 LDAP 統一管理，建議：

- 禁止 Odoo 本地密碼驗證功能。
- 明確告知使用者，若需修改密碼，應透過 LDAP 伺服器或其他外部工具，而非 Odoo 界面。
- 若允許混合驗證（LDAP + 本地密碼），則需要清楚管理密碼更新與同步的政策，避免混亂。

## odoo https 

> Odoo可否以https 型態運作！

是的，Odoo 可以以 HTTPS 型態運作。這是常見的需求，尤其是在保護敏感資料或進行內部與外部訪問時需要加密連線。以下是如何設置 Odoo 以 HTTPS 型態運作的詳細步驟：

### 設置 HTTPS 的方式

您可以選擇以下幾種方式來實現 Odoo 的 HTTPS：

### 1. 使用反向代理（推薦方式）

這是最常用且高效的方式，您可以使用 Nginx 或 Apache 作為反向代理，處理 HTTPS 的流量並將請求轉發給 Odoo 的服務。

步驟：

	1.	準備 SSL 憑證
	•	您可以使用免費的 Let’s Encrypt 生成 SSL 憑證，或購買商業 SSL 憑證。
	•	使用 Certbot 工具可以快速生成 Let’s Encrypt 憑證。
	2.	安裝 Nginx 或 Apache
	•	安裝 Nginx：
  ```bash
  sudo apt update
  sudo apt install nginx
  ```

	•	安裝 Apache：
  ```bash
  sudo apt update
  sudo apt install apache2
  ```

	3.	配置反向代理
	•	以 Nginx 為例，編輯配置檔案：sudo nano /etc/nginx/sites-available/odoo

添加以下內容：

  ```js
  server {
      listen 80;
      server_name your_domain.com;

      # Redirect HTTP to HTTPS
      return 301 https://$host$request_uri;
  }

  server {
      listen 443 ssl;
      server_name your_domain.com;

      ssl_certificate /path/to/fullchain.pem;
      ssl_certificate_key /path/to/privkey.pem;

      location / {
          proxy_pass http://127.0.0.1:8069;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto https;
      }
  }
  ```

	•	啟用配置並重新啟動 Nginx：

  ```bash
  sudo ln -s /etc/nginx/sites-available/odoo /etc/nginx/sites-enabled/
  sudo nginx -t
  sudo systemctl restart nginx
  ```

	4.	測試 HTTPS
確保您的網站可以通過 https://your_domain.com 訪問。

### 2. 使用 Odoo 自帶的 HTTPS 支援

Odoo 本身可以啟用 SSL，但通常不推薦直接使用，因為它缺乏更高級的功能，例如負載平衡或高效能管理。

步驟

	1.	準備 SSL 憑證
	•	同樣需要準備 SSL 憑證，可以使用 Let’s Encrypt 或商業憑證。
	2.	修改 Odoo 配置檔案
	•	編輯 Odoo 的配置檔案 odoo.conf：

  ```bash
  [options]
  ssl_certificate = /path/to/fullchain.pem
  ssl_private_key = /path/to/privkey.pem
```

	3.	重新啟動 Odoo

`sudo systemctl restart odoo`

	4.	訪問 HTTPS
Odoo 現在可以通過 HTTPS 運行，例如` https://your_domain.com:8069`。

### 3. 配合 Docker 部署

如果您的 Odoo 是通過 Docker 部署的，可以使用 Docker Compose 與 Nginx 配合實現 HTTPS。

步驟：

	1.	準備 Nginx 配置檔案
	•	創建一個 Nginx 容器，與 Odoo 容器組合運行。
	•	在 Nginx 配置中添加 HTTPS 支援（類似上述 Nginx 配置）。
	2.	更新 Docker Compose 文件
	•	確保 Odoo 和 Nginx 的容器都正確連線，並且 Odoo 的 HTTP 流量由 Nginx 處理。

### 注意事項

	1.	域名需求
	•	確保您有有效的域名，並將其指向您的伺服器 IP。
	2.	防火牆設置
	•	開啟伺服器的 80（HTTP）和 443（HTTPS）端口，確保外部流量可達。
	3.	自動更新 SSL 憑證
	•	若使用 Let’s Encrypt，設置自動更新憑證的排程任務（例如使用 certbot renew）。
	4.	安全性優化
	•	使用強加密協議（例如 TLS 1.2 或以上），並禁用過時的加密算法。

### 結論

建議使用 Nginx 作為反向代理處理 HTTPS，因為這種方式簡單高效，並且可以輕鬆實現負載平衡和其他高級功能。如果需要更多的指導或特定環境的配置建議，可以告訴我，我會提供更詳細的方案！

## 外部登入

> 如果我使用Ldap帳密讓同仁可以從手機登入雲端 Odoo.com，Ldap伺服器是不是必須能由外部存取得到？

是的，如果您希望使用 LDAP 帳密 讓同仁從手機登入雲端 Odoo（如在 odoo.com 上部署的版本），您的 LDAP 伺服器需要能夠被 Odoo 的伺服器（也就是外部網路）存取到。以下是詳細的解釋和解決方案：

### 原因

	1.	LDAP 認證原理
	•	當使用者嘗試登入 Odoo 並輸入 LDAP 帳密時，Odoo 會向您設定的 LDAP 伺服器發出請求，驗證該帳密的正確性。
	•	如果 Odoo 無法從其伺服器連接到 LDAP 伺服器，認證將無法完成，導致用戶無法登入。
	2.	雲端 Odoo 的網路架構
	•	雲端 Odoo 位於外部網路（Internet），因此，為了讓它與您的內部 LDAP 伺服器通信，LDAP 伺服器需要對外部網路開放存取。

### 解決方案

如果您希望在不降低安全性的情況下實現此功能，可以考慮以下幾種方式：

#### 1. 直接開放 LDAP 伺服器對外存取

	•	在防火牆中允許雲端 Odoo 的伺服器 IP 存取 LDAP 伺服器。
	•	通常，LDAP 使用的通訊埠為 389（明文）或 636（加密 LDAPS）。
	•	建議使用 LDAPS（LDAP over SSL）以確保傳輸安全。

優勢：
	•	設定簡單直接，無需額外的基礎設施。

缺點：
	•	如果配置不當，可能存在安全風險（例如暴露 LDAP 伺服器給未授權的外部存取）。

#### 2. 設置 VPN

	•	將 Odoo 的雲端伺服器與您內部的 LDAP 伺服器通過 VPN 連接，這樣 LDAP 伺服器不需要對外開放，僅允許來自 VPN 的連接。
	•	常見的 VPN 解決方案包括 OpenVPN、IPSec 或 WireGuard。

優勢：
	•	高安全性，避免直接暴露 LDAP 伺服器。

缺點：
	•	設置較為複雜，可能需要管理多個 VPN 設定。

#### 3. 設置 LDAP Proxy 或中繼伺服器

	•	在內部網路中設置一個 LDAP Proxy（例如 Apache Directory Studio 或 OpenLDAP Proxy），並將 Proxy 對外公開，而實際的 LDAP 伺服器依然保持在內部。
	•	Proxy 可以控制哪些外部請求可以通過，並提供額外的安全性層。

優勢：
	•	進一步提升安全性，並提供更靈活的存取控制。

缺點：
	•	設置需要額外的伺服器和配置工作。

#### 4. 考慮使用雲端身份驗證服務

	•	如果您的內部 LDAP 伺服器無法安全地開放給外部存取，可以考慮將 LDAP 整合到雲端身份驗證服務（如 Azure AD 或 Okta）。
	•	這些服務通常支援 LDAP 整合，並可以安全地與 Odoo 進行身份驗證。

優勢：
	•	減少內部基礎設施的負擔。
	•	高可用性和安全性。

缺點：
	•	可能需要支付額外的雲端服務費用。

安全性考量
	•	啟用加密傳輸：無論是直接開放 LDAP 還是使用 Proxy/VPN，確保使用 LDAPS 或者在 VPN 隧道內傳輸資料。
	•	限制存取來源：在防火牆或 LDAP 配置中，僅允許 Odoo 伺服器的 IP 存取。
	•	定期審查配置：監控外部存取的日誌，確保僅有授權的存取請求。

### 結論

如果您希望同仁從手機使用 LDAP 登入雲端 Odoo，您需要使 Odoo 能夠存取 LDAP 伺服器。最簡單的方式是開放 LDAP 伺服器對外網的存取，但建議優先考慮更安全的方案，例如使用 VPN 或 LDAP Proxy，以保護內部網路的安全性。

## App 與內部伺服器的連結

> 手機App是不是只能連到雲端Odoo.com? 可能連到我開放的公司特定伺服器嗎？

Odoo 的手機 App（iOS 和 Android）既可以連接到 雲端 Odoo.com，也可以連接到您公司自己部署的 Odoo 伺服器（自託管版本，Self-Hosted）。這取決於您如何設置伺服器的網路存取。以下是詳細解釋：

### 情況 1：連接到雲端 Odoo.com

•	如果您使用的是 Odoo Online（SaaS 版本），手機 App 會直接連接到 Odoo 的雲端伺服器。這是 Odoo 提供的標準服務。
•	您只需在手機 App 中輸入您的雲端 Odoo 域名（如 mycompany.odoo.com）即可登入。
•	優勢：
•	無需額外設定網路，Odoo 已經幫您處理伺服器的可用性和安全性。
•	適合不需要自行管理伺服器的公司。

### 情況 2：連接到公司自建的 Odoo 伺服器

如果您希望讓手機 App 連接到您公司特定的 Odoo 伺服器，需要確保以下幾點：

1. Odoo 伺服器必須對外網可存取
	•	方法 1：直接開放伺服器對外存取
	•	在公司內部網路中設置 Odoo 伺服器，並通過防火牆將其公開到互聯網（例如配置公共 IP 或動態域名）。
	•	確保 Odoo 伺服器的 URL 可被外部網路上的手機存取，例如 https://odoo.mycompany.com。
	•	建議使用 HTTPS 以確保傳輸安全。
	•	方法 2：使用 VPN
	•	若您不希望伺服器直接暴露在互聯網上，可要求手機通過 VPN 連接到公司內部網路，再訪問內部 Odoo 伺服器。
	•	適合對安全性要求較高的環境。
	•	方法 3：使用反向代理
	•	配置 Nginx 或 Apache 作為反向代理，將內部伺服器暴露給外部網路。
	•	這樣可以控制外部訪問的權限，同時實現更高的安全性。

2. 配置手機 App 的伺服器地址
	•	手機 App 啟動時，輸入您公司伺服器的網址，例如：
	•	局域網：http://192.168.1.100:8069
	•	外部網路：https://odoo.mycompany.com

3. 確保伺服器資源充足
	•	如果大量員工通過手機 App 訪問，請確保 Odoo 伺服器具備足夠的資源來處理額外的請求。

4. 檢查防火牆和路由器設置
	•	如果伺服器部署在內部網路中，需要在路由器和防火牆中開放必要的通訊埠（通常是 8069 或代理服務的 HTTPS 埠 443）。

5. 測試訪問
	•	測試手機是否能夠通過輸入伺服器地址成功登入您的 Odoo。
	•	如果使用 VPN，需要先連接 VPN，然後再測試登入。

### 比較：雲端 Odoo.com 與自建伺服器

特性|雲端Odoo.com	|自建伺服器
-|-|-
配置難度	|無需配置	|需要手動設置外網存取或 VPN
成本	|按需付費	|伺服器硬體和維護成本
訪問控制	|由 Odoo 管理	|完全由公司控制，靈活性更高
性能和擴展性	|由 Odoo 提供，隨使用量自動調整	|需要自行調整伺服器資源
安全性	|Odoo 提供 HTTPS 和基本安全保護	|可選擇使用 VPN、反向代理等高級保護

### 建議

•	如果您不想自行處理伺服器的部署和網路配置，可以選擇使用 Odoo Online。
•	如果您的公司已有內部 IT 基礎設施或對數據保密性要求較高，則可以考慮自行部署 Odoo，並確保伺服器對外網可安全存取。
  