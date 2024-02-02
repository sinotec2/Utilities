---
layout: default
title:  DNS Server
parent: API Servers
grand_parent: Web Jokers
last_modified_date: 2024-02-02 09:01:27
tags: API_Server 
---

# 自架DNS主機
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

## 自架DNS主機

### 步驟

您可以使用以下步驟來自架DNS主機：

- 獲取一個DNS主機IP地址：您可以使用一些DNS查詢工具，例如nslookup、dig或cuttingspeedtest，來查詢指定域名的DNS主機IP地址。
- 購買一個DNS主機服務：您可以選擇一個DNS主機服務提供商，例如GoDaddy、Namecheap或Cloudflare等，購買一個DNS主機並註冊帳戶。
- 設置DNS記錄：使用DNS主機提供商提供的控制面板或API，設置您要設置的DNS記錄。例如，如果您要設置一個CNAME記錄，您需要將您要設置的CNAME名稱和相應的對應DNS主機IP地址添加到DNS主機控制面板中。
- 測試DNS更改：使用DNS主機提供商提供的測試工具或DNS查詢工具，測試您的DNS更改是否正常工作。
- 請注意，自架DNS主機需要一定的技術知識和步驟，如果您不確定如何進行，建議尋求專業人士的幫助。

### nslookup

nslookup是一個常用的命令行工具，用於查詢DNS記錄，以尋找指定主機名稱或IP地址的相應DNS記錄。NSlookup可以用於Windows和Linux系統上，並且通常預設在Windows系統中。

使用nslookup可以執行以下操作：

- 查詢域名：使用nslookup命令，可以查詢指定的域名，例如查詢google.com的DNS記錄。
- 查詢主機名稱：使用nslookup命令，可以查詢指定的主機名稱，例如查詢127.0.0.1的DNS記錄。
- 查詢IP地址：使用nslookup命令，可以查詢指定的IP地址，例如查詢192.168.1.1的DNS記錄。
- 查詢DNS記錄：使用nslookup命令，可以查詢指定的DNS記錄，例如查詢google.com的CNAME記錄。
- 使用nslookup需要指定域名、主機名稱或IP地址，然後按Enter鍵執行命令。nslookup會即時顯示查詢結果，其中包括DNS記錄的相關資訊，例如DNS名稱、DNS標識符、DNS類型和DNS對應值等。

總之，nslookup是一個強大的命令行工具，可用於查詢DNS記錄，幫助用戶瞭解DNS系統的運作原理。

### macOS solutions

macOS上有免費的自架DNS主機方案。以下是一些常見的方案：

- Pi-hole：Pi-hole是一個基於Raspberry Pi的自架DNS主機解決方案，可用於管理您的家庭或組織的DNS查詢。Pi-hole使用惡意防火牆（NAT）設備（如路由器或交易中心）作為DNS防火牆，並使用您的網絡上的所有設備進行DNS查詢，並轉發到Pi-hole。Pi-hole提供了一個易於使用的Web管理控制台，使您可以輕鬆地設置和管理您的DNS主機。
- dnsmasq：dnsmasq是一個開源的DNS和DHCP伺服器，可用於自架DNS主機。dnsmasq可以在macOS上運行，並提供DNS和DHCP服務，使您可以在自己的網絡中管理DNS查詢。dnsmasq還支持自定義DNS檔案，使您可以自定義您的DNS配置。
- Google DNS：Google DNS是一個免費的DNS服務，可用於自架DNS主機。Google DNS提供快速和可靠的DNS服務，並支持DNSSEC和CNAME解析。在macOS上，您可以透過修改系統的DNS設置，將您的網絡設置為使用Google DNS。

### bingchat

在 macOS 上，有幾種免費的自架 DNS 主機方案：

1. **NOIP DDNS 動態域名服務**¹：這是一種動態域名服務，支援電腦以及多數路由器使用，提供免費與付費選擇。免費方案提供3組動態域名，也有付費方案。

2. **DNS over HTTPS/TLS (DoH/DoT)**²：在 2020 年的 WWDC 中，Apple 為 macOS 添加了系統級的 DNS over HTTPS/TLS 支援。這種方式可以通過系統接口進行全局 DNS 流量加密。

3. **Cloudflare**⁴：Cloudflare 提供免費的 DNS 代管服務，只需要將你的域名指向 Cloudflare 的 DNS 伺服器即可。

請注意，這些方案可能需要一些技術知識來設定和管理。如果你不熟悉這些技術，可能需要找一位熟悉的人來幫忙設定。¹²⁴

來源: 與 Bing 的交談， 2024/2/2

1. 浮動IP照樣架站！NOIP DDNS 動態域名免費服務設定，遠端桌面也好用 、 [老貓測3C]( https://iqmore.tw/no-ip-free-dynamic-dns).
2. 為 iOS 14 和 macOS 11 配置 DNS over HTTPS/TLS - [知乎](https://zhuanlan.zhihu.com/p/351068602).
3. 如何將域名選用 Cloudflare 的免費方案代管DNS教學 (PChome為例) [梅問題．教學網](https://www.minwt.com/website/server/23143.html).
4. iT邦幫忙─怎麼樣架設DNS伺服器，可以簡單、穩定又經濟？ - [iThome](https://www.ithome.com.tw/article/51442).
5. [undefined](https://www.noip.com/).
6. [undefined](https://www.noip.com/download).
7. [undefined](https://gfw.report/blog/gfw_esni_blocking/zh/).

## 免費主機代管服務

### bingchat

以下是一些免費的線上 DNS 主機代管服務：

1. **Cloudmax**¹：提供各式網域申請及免費 DNS 代管服務，主機用戶享網址永久免費。

2. **Linode**²：Linode 是一家知名的 VPS 虛擬主機提供商，他們也有提供免費的 DNS 代管服務，即使不是他們的客戶，也可以在免費註冊後使用這項功能。

3. **freedns.afraid.org**³：這是一個免費的線上 DNS 主機代管服務，他們提供的功能幾乎和一般自行架設的 DNS 伺服器一樣，只要申請帳號就能使用。

請注意，這些服務可能需要一些技術知識來設定和管理。如果你不熟悉這些技術，可能需要找一位熟悉的人來幫忙設定。¹²³

來源: 與 Bing 的交談， 2024/2/2
1. 各式網域申請及免費 DNS 代管服務，主機用戶享網址永久免費 、 Cloudmax [匯智](https://domain.cloudmax.com.tw/index.php).
2. Linode 提供免費 DNS 代管服務，註冊即可使用 - [免費資源網路社群](https://free.com.tw/free-dns-linode/).
3. 免費 線上 DNS 主機 代管 服務 - [bing](https://bing.com/search?q=%e5%85%8d%e8%b2%bb+%e7%b7%9a%e4%b8%8a+DNS+%e4%b8%bb%e6%a9%9f+%e4%bb%a3%e7%ae%a1+%e6%9c%8d%e5%8b%99).
4. [教學]EditDNS 免費DNS代管站，可管理RU網址 - [香腸炒魷魚](https://sofree.cc/editdns/).
5. iT邦幫忙─怎麼樣架設DNS伺服器，可以簡單、穩定又經濟？ - [iThome](https://www.ithome.com.tw/article/51442).
6. [undefined](https://domain.cloudmax.com.tw).
7. [undefined](https://www.linode.com/).
8. [undefined](http://free.editdns.net/).

### ithome建議

- hpc（IT邦初學者10級）發問：
  - 最近申請的網域名稱只接受指定DNS伺服器的設定，所以必須要自己架設DNS伺服器或使用DNS代管服務，請問有哪些解決方案可以選擇？
- vincent118（IT邦初學者2級）：
  - 我用一個免費的DNS服務Everydns（www.everydns.NET）， 如果沒有捐款，可以使用5個網域名稱；假如有，可以用99個網域名稱。我自己捐了10美元，使用時就很方便。
- tibandyli（IT邦初學者9級）：
  - 如果作業系統是Linux，可以考慮使用named來當DNS伺服器，成本比較低；如果是Windows伺服器，可以採用內建的DNS伺服器。想要進階的功能？之前我們用過DNS Plus這套程式，維護工作很簡單，只是要另外花錢購買。
  - 不過，看你的需求，應該可以透過DNS代管就能解決，不用自己架設伺服器，像「網路中文」提供五組名稱解析，一般使用應該足夠。
- kevinhuang（IT邦初學者9級）：
  - 提供一個免費的線上DNS主機代管服務：freedns.afraid.org，它提供的功能，幾乎和一般自行架設的DNS伺服器一樣，只要申請帳號就能使用。
- tom6507（IT邦初學者9級）：
  - 既然你用的是中華電信的ADSL，不需要另外找，直接就用他們的DNS就可以了，將需要設定DNS伺服器的地方，指向為168.95.1.1。

### 中華電信-遠振資訊

- [DNS 與 DNS server 是什麼? 申請免費 DNS 管理設定教學](https://host.com.tw/DNS)
- 需購買該公司提供網域、才能建立託管。

## 類型選擇

### A~TXT

- 類型：A 
  - 將 subdomain.domain.com 指向硬編碼的 IP 位址。 最直接和直接的選項。
  - 也要注意您在 FreeDNS 程式中所做的任何更改都會反映在網路上並立即生效。 您不會立即看到結果的唯一方法是，如果您在 FreeDNS 程式中配置查詢之前透過查找來將查詢快取在電腦上。
- 類型：MX
  - 將 subdomain.domain.com 指向郵件伺服器。 
  - 這些類型的記錄僅適用於郵件伺服器，它們可以與 A 記錄共存，它們的唯一用途是將郵件路由到不同的位置。 
  - 所有郵件實作在嘗試路由電子郵件訊息之前首先檢查此記錄。 如果主機不存在 MX 記錄，則會嘗試直接向主機名稱解析到的 IP 傳送電子郵件。
- 類型：AAAA 
  - 將 subdomain.domain.com 指向 IPv6 位址。 對於在個人網路上使用 IPv6 或在家中使用 IPv4 到 IPv6 隧道的使用者很有用。
- 類型：CNAME
  - 將 subdomain.domain.com 指向另一個主機名稱。 適合使用其他動態 DNS 服務的人。 
  - 您可以為另一台主機建立 CNAME 記錄，您在此處選擇的任何 subdomain.domain.com 將前往 CNAME 主機擁有的任何 IP 位址。
- 類型：NS 
  - 將 subdomain.domain.com 指向另一個 NAMESERVER。 
  - 如果您選擇此選項，則您使用 FreeDNS 選擇的任何 subdomain.domain.com 位址都必須在您選擇的目標位址（名稱伺服器）上進行設定和設定。 
  - 此選項基本上意味著您將 FreeDNS 主機一起委託給另一個 DNS 伺服器，因此當您選擇此選項時，您是在告訴網路上的每台電腦詢問 subdomain.domain.com 所在的「位址」。 
  - 如果您將 NS 記錄指向的主機未配置為應答您在 FreeDNS 中使用的 subdomain.domain.com，則 subdomain.domain.com 主機將無法解析。
- 類型：TXT 
  - 允許您建立TXT 記錄，用於多種不同的用途，最常見的是DKIM 記錄（用於打擊垃圾郵件），以便其他接收郵件伺服器可以透過驗證您公開發布的加密簽章來驗證電子郵件是否是您發送的。 
  - 將您的 TXT“目的地”用引號引起來（不用擔心，如果您忘記了，系統會提醒您）。
- 類型：SPF 
  - 反垃圾郵件記錄，適合您發送電子郵件的任何網域。 請參閱 https://www.spfwizard.net/ 以了解更多詳細資訊。
- 類型：LOC 
  - 在網域名稱系統中表達位置資訊的一種方式。
  - [RFC1876](http://www.faqs.org/rfcs/rfc1876.html)有完整的解釋。
  - 要找到您的緯度/經度位置，您可以使用 Map-O-Rama。

類型：RP - 負責人 RR。

RP 的格式如下：

RP <mbox-dname> <txt-dname>

所有 RP RR 中都需要兩個 RDATA 欄位。

第一個欄位 <mbox-dname> 是一個域名，指定負責人的郵箱。

第二個欄位 <txt-dname> 是存在 TXT RR 的網域名稱。 可以執行後續查詢以擷取 處的關聯 TXT 資源記錄。

RFC1183有完整的解釋。

類型：SRV - “服務”記錄，由會話發起協定 (SIP) 和可擴展訊息傳遞和狀態協定 (XMPP) 使用。 也被《我的世界》使用。

一些例子：

類型：SRV
子網域：_service._protocol.subdomain
目的地：4個字段，以空格分隔（優先權重端口目標）

一些更隨機的例子：

類型：SRV
子網域：_minecraft._tcp.mc
網域：yourdomain.com
目的地： 0 0 25676 dns.yourdomain.com

類型：SRV
子網域：_jabber._tcp
網域：yourdomain.com
目的地：10 0 5269 jabber.yourdomain.com

類型：SRV
子網域：_jabber._tcp
網域：yourdomain.com
目的地：20 0 5269 xmpp-server1.l.google.

### AXFR permission

AXFR 代表“位址區域傳輸協定”(Address Zone Transfer Protoco)，它是網域名稱系統 (DNS) 中使用的一種協議，用於將區域檔案資訊從一個 DNS 伺服器傳輸到另一個 DNS 伺服器。

當 DNS 伺服器收到有關網域名稱資訊的請求時，它會先檢查其本機區域檔案以查看是否有該資訊。 如果沒有，伺服器將向該網域的權威 DNS 伺服器發起 AXFR 請求。 然後，權威伺服器將區域文件資訊傳送到請求伺服器，然後請求伺服器可以使用該資訊來解析網域名稱查詢。

AXFR 通常用於同步不同 DNS 伺服器之間的 DNS 訊息，例如在 DNS 伺服器發生故障或將新的 DNS 伺服器新增至網路時。 它也用於確保所有 DNS 伺服器都擁有有關網域名稱 DNS 記錄的最新資訊。

### ACL access groups

ACL（Access Control Lists）是一種用於控制資源存取權的技術。在它中，對象（例如文件、目錄、檔案、網絡資源等）可以被授予多個存取權限，並且可以對這些權限進行更細粒度的控制。ACLs 通常依賴於一個名為 ACE（Access Control Entry）的結構，每個 ACE 包含了一個主題（SID，安全主題識別符）、一個權限（例如讀取、寫入、執行等）和一個使用者或群組（例如使用者名稱或群組 ID）。

在問題中，ACL access groups 指的是一種對 ACLs 的更細粒度控制，它允許將多個使用者或群組歸納成一個組，並將相同的權限授予組中所有成員。這種授予權限的方式可以更方便地管理和維護 ACLs，並且可以提高系統的安全性。例如，將所有需要訪問特定目錄的使用者歸為一個群組，並將讀取和寫入權限授予該群組，可以確保只有授權的使用者可以訪問該目錄和其中的資源。

### CNAME

- CNAME（Canonical Name）是指一個與主機名稱或IP地址相關聯的名稱。在DNS中，CNAME是一種記錄，可以用於指定一個主機名稱或IP地址的另一個名稱。這種名稱可以是一個別名（例如，www.example.com），也可以是某個其他的主機名稱或IP地址。

- CNAME記錄通常用於解決將多個主機名稱或IP地址映射到同一個物理主機上的問題。例如，如果有兩個網站，它們原本使用相同的主機名稱，但現在想要將其映射到不同的IP地址上，可以使用CNAME記錄來實現這一點。這樣，使用者就可以透過原始的主機名稱訪問網站，而DNS系統會自動將其映射到正確的IP地址上。

- 除了解決主機名稱映射問題外，CNAME記錄還可以用於定義對應關係，將一個名稱映射到另一個名稱。例如，如果有一個公司擁有多個子公司，可以使用CNAME記錄來將子公司的主機名稱映射到公司的主機名稱上。這樣，使用者就可以使用公司的主機名稱訪問所有子公司的網站。
