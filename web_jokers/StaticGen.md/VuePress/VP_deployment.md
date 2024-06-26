---
layout: default
title:  VuePress佈建
parent: VuePress
grand_parent: Static Site Generators
nav_order: 99
last_modified_date: 2024-06-26 19:33:39
tags: VuPress
---

# VuePress佈建之限制與考慮
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

- VPH中大量使用了包裹器(wrapper)來保存路徑，經過編譯之後，會形成固定路徑、盤根錯節的html檔案群組，Repo很難更動原有目錄架構。
  - 這項好處讓作者不必擔心路徑丟失的問題、
  - 壞處是更動路徑將造成編譯失敗、即時通過了編譯，很多hyperlink 也會失效，造成閱讀困難。
- 可喜的是找到了`v2`路徑的包裹器，可以作為Repo的替代標籤。檔案如下：

```bash
$ findc "*wrap*.ts"|grep -v module
./docs-shared/lib/theme-wrapper.d.ts
./docs-shared/lib/config-wrapper.d.ts
./docs-shared/src/config-wrapper.ts
./docs-shared/src/theme-wrapper.ts
```

- rebase相關指令

```bash
$ grep v2 $(findc "*wrap*.ts"|grep -v module)
./docs-shared/src/config-wrapper.ts:      ? (`/v2/${base}/` as `/${string}/`)
./docs-shared/src/config-wrapper.ts:      : "/v2/";
./docs-shared/src/theme-wrapper.ts:        indexBase: base ? `/v2/${base}/` : "/v2/",
```

- `v2`：`vuepresshope2/docs/theme/src`
  - 其下可自行開設目錄如：`vuepresshope2/docs/theme/src/zh/kuang`，
  - 將會出現在`https://domain_name/Grp.User.Repo/zh/kuang`（中文版本）
- `v2/shared`：`vuepresshope2/docs/shared/src`
  - 其下可自行開設目錄如：`vuepresshope2/docs/shared/src/kuang`，
  - 將會出現在`https://domain_name/Grp.User.Repo/shared/kuang`(英文版本)
- `v2`路徑必須在workflow中置換成`Grp.User.Repo`，以套用LDAP分組白名單。

## 使用者如何開始運作新的技術文件系統

### Gitea Repo

- 以瀏覽器開啟Gitea 網址
- 註冊或登入會員
- 如果要啟動團隊編輯功能
  - 創設團隊、邀請成員、設定編輯權利
- 找到Vuepress Hope(v2)乾淨版的Repo網址
- 分支(fork)一份 到自己(或團隊)的目錄
  - 在自己或團隊的家目錄、成立新的Repo
  - 在分支空格處貼上前述網址
  - 命名成自己的Repo(按實際的技術內容、不要再出現VPH云云)
- 複製Repo的網址(https://domain_names:3000/Repo.git)，到個人桌機的Github Desktop或VS Code

### 同步桌機與Gitea

- 開啟Github Desktop、在Current Repository右側下拉選單中新增(Add)`Clone Repository...`，選擇URL
- 貼上前述Repo網址、設定本機目錄（LocalPath）
  - 注意：如需研資部協助備份，需存在Y槽。
  - 如為團隊：至少需有1人的作業路徑是在Y槽。
- 按下複製倉儲(`clone`)
- 點選`Open Visual Studio Code`開始編輯
- 編輯完成後，回到Github Desktop執行推送(`push`)，此舉將更新Gitea上的內容，請注意是否會覆蓋別人編輯的檔案。
- 每次編輯完成，都需要執行推送，下次要編輯時，也需要先下載倉儲(`pull`)的最新內容，以避免版本不符，造成衝突。

## workflow tasks

### 整體說明

- workflow task runner: admin level of Gitea
- get the User_name(Team_name) and Repo_name
  - Repo must set to **public** to be read by admin
- **User.Repo.name**:類似個人部落格、團隊部落格的概念（**User**下稱“**作者**”、雖然有可能是個團隊）。
  - apache2需配合以技術組（及/或轄下分組）代號開頭，來套用LDAP分組許可權限。（詳見[apache directory的正則表示](#apache-directory的正則表示)）
  - workflow需判斷**作者**歸屬於哪一個技術組，好在佈建前先在nas上建好目錄、將編譯好的網頁佈建到正確的位置。
  - 判斷方式：
    - 可以利用`bash`的`grep`、`cut`等等指令，從既有的一個csv檔案搜尋。csv檔案必須事先複製到Repo上，check_out to runner。
    - 也可以執行`ldapsearch`指令從LDAP伺服器得到正確的技術組歸屬。（似乎較好、不必一直更新資料庫）
  - future webpage path：https://domain_name/Grp.User.Repo/shared/zh...
- 在workflow中修改包裹器(wrapper)：v2 must be changed to **User_Repo_name**
- mkdir and scp to /nas2/VuePressDist/Grp.User.Repo

### runner docker 佈置

- page build and deployment
  - 偵測任何Depo如有上載活動，隨即檢查，如果確實是VPH的Repo，即開始執行編譯與佈建。
  - 受理期間，將Repo完全控制，不讓別的Runner使用。


## apache directory的正則表示

### LDAP分組

- 開放讀取之白名單
- 全公司(SES)
- 責任中心(GE1/GE2/SUP)
- 部門
- 技術組
- Grp_name == User_name (團隊名稱、共同編輯)
  - 行政分組(技術組轄下、技術組.分組.Repo)
  - 行政跨組(任意組合、SES.分組.Repo、GE1.分組.Repo、EE1.分組.Repo)

### 設定方式

> apache2 `<Directory>` 的設定中，可否設定部分目錄字串的regex條件，如`/nas2/VuePressDist/ICT.*.* `?

是的,在 Apache 的設定檔中,可以使用正規表示式來符合部分目錄字串。

在 Apache 的設定檔中,通常可以在 `<Directory>` 或 `<Location>` 指令中使用正規表示式。

例如,如果您想要設定 `/nas2/VuePressDist/ICT.*.*` 目錄的存取權限,可以使用以下設定:

```bash
<Directory "/nas2/VuePressDist/ICT.*.*">
 # 在這裡設定目錄的存取權限和其他配置
 Options Indexes FollowSymLinks
 AllowOverride None
 Require all granted
</Directory>
```

在這個例子中,`"/nas2/VuePressDist/ICT.*.*"` 是一個正則表達式,它將匹配以 `/nas2/VuePressDist/ICT.` 開頭,後面跟兩個任意字符的目錄路徑。

您也可以使用 `<LocationMatch>` 指令來設定基於正規表示式的 URL 路徑比對:

```bash
<LocationMatch "^/nas2/VuePressDist/ICT.[^/]+.[^/]+/?$">
 # 在這裡設定 URL 路徑的存取權限和其他配置
 Options Indexes FollowSymLinks
 AllowOverride None
 Require all granted
</LocationMatch>
```

這個配置將匹配以 `/nas2/VuePressDist/ICT.` 開頭,後面跟兩個任意字元,最後以斜線結尾的 URL 路徑。

需要注意的是,正規表示式的語法和使用方式可能因 Apache 版本而有所不同,您可能需要查閱 Apache 文件以獲取更多資訊。

### 分隔字元的考量

- LDAP名稱並沒有排除底線underline`_`，如果使用底線將會造成切割錯誤。
- LDAP名稱確實有排除點dot`.`。