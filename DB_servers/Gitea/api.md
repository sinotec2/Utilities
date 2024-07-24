
## API token

- 有很多登入方式

### Personal Access Token 

- 在設定頁面中，找到並點擊 "Applications"（應用程式）。在該頁面，您可以看到 "Generate New Token"（產生新令牌）的選項。點擊它。
- 設定令牌名稱和權限：
  - 在產生令牌頁面，您可以為令牌設定一個名稱，以資識別。
  - 選擇所需的權限。根據作業需求、選擇合適的權限，
  - 然後點擊 "Generate Token"（產生令牌）。
- 複製令牌
  - 產生的令牌將顯示在頁面上。請務必將令牌複製並儲存到安全的地方，因為之後任何人都將無法再次查看該令牌。
- 注意
  - `token and access_token API authentication is deprecated and will be removed in gitea 1.23.`
  - `Please use AuthorizationHeaderToken instead. Existing queries will continue to work but without authorization. `

## create organization

### model

- 創建者的`username`是必要項目（*）。名稱不能跟現有的其他名稱相同。

```java
CreateOrgOption{
description:	CreateOrgOption options for creating an organization
description	[...]
email	[...]
full_name	[...]
location	[...]
repo_admin_change_team_access	[...]
username*	[...]
visibility	[...]
website	[...]
}
```

### 範例

- json檔案內容 

```json
{
  "description": "org1",
  "email": "sinotec2@gmail.com",
  "full_name": "organization number one",
  "location": "same as company",
  "repo_admin_change_team_access": true,
  "username": "grp1_admin",
  "visibility": "public",
  "website": "https://sinotech-eng.com"
}
```

- curl指令
  ```bash
  curl -X 'POST' \
  'http://localhost:3000/api/v1/orgs?access_token=***' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  ...
  }
  ```
- 
