---
layout: default
title: MediaWiki 
nav_order: 99
has_children: true
last_modified_date: 2024-01-11 15:58:26
grand_parent: DB_servers 
parent: note_system

tags: DB_servers note_system 
---



太好了，你用的是 MediaWiki，那就更清楚了。
MediaWiki 原生就支援一套很強的「內部連結」與「模板擴充」機制，但若要做到你說的「自動連結自設 wiki 頁面」──也就是當文章中出現某個條目名稱或關鍵字時，自動建立指向該頁的連結──有幾個成熟的方案與擴充外掛可以用。

⸻

🧩 一、現成 MediaWiki 擴充插件選擇

1️⃣ Extension:LinkTitles

🔗 官方頁面：https://www.mediawiki.org/wiki/Extension:LinkTitles￼

功能說明：
這是目前 MediaWiki 上最常用的「自動連結現有頁面」外掛。
	•	會掃描頁面文字，若出現現有頁面的標題（或別名 redirect title），就自動轉成內部連結。
	•	支援配置要掃描哪些 namespace、是否僅在 <autolink> 區塊內啟用等。
	•	可避免過度連結（例如同一詞多次出現，只連第一次）。
	•	能與 Redirect 頁搭配使用，支援別名式連結。

安裝方式：

cd extensions
git clone https://gerrit.wikimedia.org/r/mediawiki/extensions/LinkTitles.git

然後在 LocalSettings.php 加入：

wfLoadExtension( 'LinkTitles' );
$wgLinkTitlesParseAllNamespaces = true;
$wgLinkTitlesFirstOnly = true; // 可選，只自動連結第一次出現

優點：
	•	官方支援且維護中（與 MediaWiki ≥1.35 相容）。
	•	自動掃描、免手動加 link。
	•	可搭配自動更新頁面索引機制。

缺點：
	•	只會匹配與頁面「標題」完全相同的文字。
	•	不支援模糊比對（例如「環保法」不會自動連到《環境保護法》）。
👉 這點可以用 redirect 頁（別名頁）解決，例如建立「環保法」redirect 到「環境保護法」。

⸻

2️⃣ Extension:TextExtracts + 自訂 Hook（建議進階用）

如果你想要「更聰明的連結」（例如自動根據同義詞或分詞結果建立連結），可以搭配 TextExtracts 抓頁面摘要 + 寫一個 Parser Hook 或 Tag Extension 做全文關鍵字掃描。

例如：

$wgHooks['ParserAfterTidy'][] = function( &$parser, &$text ) {
    $titles = array( '環境保護法', '廢棄物清理法' );
    foreach ( $titles as $t ) {
        $link = "[[{$t}|{$t}]]";
        $text = preg_replace("/\b{$t}\b/u", $link, $text);
    }
    return true;
};

這樣可在頁面渲染時動態建立連結。
📦 可再接 RapidFuzz 或中文分詞工具（例如 Jieba + REST API）做模糊比對。

⸻

3️⃣ Extension:Semantic MediaWiki (SMW) + Semantic Internal Objects

若你的 wiki 是知識庫性質（像環保法規系統），可以考慮用 SMW。
它不僅能標註頁面中的實體（Entity），還能讓不同頁面間以語義方式連結。

例如：
頁面 A 提到「環境保護署」，SMW 可自動辨識這是一個已有的「組織」實體，然後自動建立內部連結。
	•	這可以透過「property」與「semantic link」實現，而不只是文字比對。
	•	優點是可以結合查詢語法、視覺化關聯圖譜（Semantic Result Formats）。
	•	缺點是設計門檻較高，但對法規知識庫非常強。

⸻

🧠 二、推薦組合建議（依你的用途）

你提到你的系統要：

「結合關鍵字與全文搜尋、分類選單與問答互動」
「針對法規知識庫、環保規定、百萬級文檔」

我會建議這樣設計：

功能層	建議實作
自動連結	先用 LinkTitles 做基礎自動連結（完全比對）
同義詞／模糊連結	增加 redirect 頁或用自訂 Hook + RapidFuzz
語義連結／多層實體關聯	加上 Semantic MediaWiki 管理法條、條款、主管機關、時間等屬性
查詢強化	搭配 CirrusSearch（ElasticSearch 外掛）提升全文索引與查詢效率
維護工具	加上 Page Forms／Replace Text 外掛，方便批次管理連結與詞條


⸻

🧩 總結建議

情境	推薦
想快速啟用自動連結	安裝 LinkTitles
想要中文模糊比對、自動關聯	LinkTitles + redirect 頁 + 自訂 parser hook
想打造智慧知識庫（像環保法規圖譜）	Semantic MediaWiki 是長期方案
想加搜尋強化	加 CirrusSearch (ElasticSearch backend)


⸻

要不要我幫你列一份 完整 MediaWiki 配置範例（含 LinkTitles、CirrusSearch、Semantic MediaWiki）？
可以直接用在你的環保法規知識庫上，一套設定就能同時有自動連結 + 全文搜尋 + 語義查詢。

