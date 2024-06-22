---
layout: default
title:  CPS 簡介與比較
parent: Codeberg
grand_parent: Static Site Generators
last_modified_date: 2024-06-22 10:21:24
tags: Codeberg 
---

# Codeberg pages-server簡介與比較

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


## 部署

> 警告：一些注意事項適用
> 您需先具備系統管理知識以及程式碼理解和建構知識，以便您最終可以編輯那些原本是不可配置項目、和(或)僅適用於代碼山的特定設定。
> 將來，我們將嘗試減少這些，並使託管 Codeberg 頁面像設定 Gitea 一樣簡單。
> 如果您考慮在實踐中使用頁面，請考慮先聯絡我們，然後我們將嘗試分享一些基本步驟並記錄管理員的當前用法（雖然此一狀態可能會發生變化）。

部署軟體本身非常容易。您可以取得目前版本的二進位檔案或自行構建，按如下所述配置環境，然後就完成了。

困難的部分是添加自訂網域支援（如果您打算使用它）。 SSL 憑證（請求 + 續訂）由 Pages Server 自動處理，但如果您想在共用 IP 位址（而不是獨立的）上執行它，則需要將反向代理設定為不終止 TLS 連接，但將IP 層級的請求轉送到頁面伺服器。

您可以在`examples/haproxy-sni`資料夾中查看概念驗證，尤其是查看`haproxy.cfg` 的這一部分。

如果您想測試更改，可以開啟 PR 並要求build_pr_image新增標籤。這將觸發 PR 的構建，從而建立一個用於測試的 docker 映像。

環境變數
ACME_ACCEPT_TERMS（預設：使用自簽名憑證）：將此設為「true」以接受 ACME 提供者的服務條款。
ACME_API（預設值：https://acme-v02.api.letsencrypt.org/directory）：將其設為https://acme.mock.director以使用無效憑證而不進行任何驗證（非常適合偵錯）。 ZeroSSL 將來可能會更好，因為它沒有速率限制，並且不會與官方 Codeberg 憑證（使用 Let's Encrypt）衝突，但我還無法讓它工作。
ACME_EAB_KID& ACME_EAB_HMAC（預設：不使用 EAB）：EAB 憑證，例如 ZeroSSL。
ACME_EMAIL（預設：noreply@example.email）：設定傳送到 ACME API 伺服器的電子郵件以接收例如續訂提醒。
ACME_USE_RATE_LIMITS（預設值：true）：將此設為 false 以停用速率限制，例如使用 ZeroSSL。
DNS_PROVIDER（預設：使用自簽名憑證）：主網域通配符的 ACME DNS 提供者的程式碼。請參閱https://go-acme.github.io/lego/dns/以了解可用值和其他環境變數。
ENABLE_HTTP_SERVER（預設值：false）：將此設為 true 以啟用 HTTP-01 質詢並將所有其他 HTTP 請求重新導向至 HTTPS。目前僅適用於連接埠 80。
GITEA_API_TOKEN（預設值：空）：Gitea 實例存取非公開（例如有限）儲存庫的 API 令牌。
GITEA_ROOT（預設值：）https://codeberg.org：上游 Gitea 實例的根。
HOST& PORT（預設：[::]& 443）：監聽位址。
LOG_LEVEL（預設值：警告）：設定此項目以指定日誌記錄等級。
NO_DNS_01（預設值false：）：停用 ACME DNS。這意味著通配符憑證是自簽署的，並且所有網域和子網域都將具有不同的憑證。因為這可能會導致 ACME 提供者的速率限制，所以對於開放註冊或大量使用者/組織的 Gitea/Forgejo 實例，不建議使用此選項。
PAGES_DOMAIN（預設值：）codeberg.page：頁面的主域。
RAW_DOMAIN（預設值raw.codeberg.page：）：原始資源的域（必須是 的子域PAGES_DOMAIN）。