---
layout: default
title:  superset_config.py
parent: apache_superset
grand_parent: Graphics
last_modified_date: 2024-06-15 11:00:11
tags: apache_superset graphics
---

# 設定生產階段的superset_config.py
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

此處簡介superset生產階段的設定方式。主要集中在環境變數與superset_config.py的修改。

## 背景

- [official website](https://superset.apache.org/docs/configuration/configuring-superset)
- Superset透過其`config.py`模組公開了數百個可設定參數、公開的變數和物件可作為您可能想要配置、變更和連接的大部分內容的公共介面。
  - 在此 python 模組中，您將找到所有這些參數、合理的預設值以及註釋形式的豐富文檔。
- 要配置您的應用程序，您需要創建自己的配置模組，這將允許您覆蓋其中的一些或許多參數。
  - 您不需要更改核心模組，而是需要定義自己的模組（通常是一個名為`superset_config.py`的文件。
  - 將此文件添加到您的`PYTHONPATH`或創建另一個環境變量`SUPERSET_CONFIG_PATH`，指定到特定的`superset_config.py`。

### 路徑環境變數

- 例如，如果直接在基於 Linux 的系統（您所在的目錄superset_config.py下）上部署 Superset /app，您可以執行：

```bash
export SUPERSET_CONFIG_PATH=/app/superset_config.py
```

### Dockerfile

- 如果您使用自己的自訂 Dockerfile，並以官方 Superset 映像作為基礎映像，那麼您可以新增您設定檔來覆蓋原來的路徑，如下所示：

```yml
COPY --chown=superset superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py
```

### docker-compose

- 部署生產階段的docker-compose 需特別約定以不同方式來處理應用程式的配置。以下是您可以在`superset_config.py`文件中設定的範例：

```yml
# Superset specific config
ROW_LIMIT = 5000

# Flask App Builder configuration
# Your App secret key will be used for securely signing the session cookie
# and encrypting sensitive information on the database
# Make sure you are changing this key for your deployment with a strong key.
# Alternatively you can set it with `SUPERSET_SECRET_KEY` environment variable.
# You MUST set this for production environments or the server will refuse
# to start and you will see an error in the logs accordingly.
SECRET_KEY = 'YOUR_OWN_RANDOM_GENERATED_SECRET_KEY'

# The SQLAlchemy connection string to your database backend
# This connection defines the path to the database that stores your
# superset metadata (slices, connections, tables, dashboards, ...).
# Note that the connection information to connect to the datasources
# you want to explore are managed directly in the web UI
# The check_same_thread=false property ensures the sqlite client does not attempt
# to enforce single-threaded access, which may be problematic in some edge cases
SQLALCHEMY_DATABASE_URI = 'sqlite:////path/to/superset.db?check_same_thread=false'

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = []
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = ''
```

> 提示
> 請注意，通常[僅需]將要變更的核心superset/config.py部分以及相關註解複製並貼上到您自己的`superset_config.py`檔案中即可。

- `superset/config.py`中定義的所有參數和預設值，都可以在本機的`superset_config.py`中更改覆蓋。
- 管理員需要通讀該文件以了解配置的可能內容及其預設值。
- 由於`superset_config.py`充當 Flask 配置模組，它可用於更改 Flask 本身的設置，以及 Superset 綁定的 Flask 擴展，如`flask-wtf`、`flask-caching`、flask-migrate和flask-appbuilder。這些擴充中的每一個都提供了複雜的可配置性。 Superset 使用的 Web 框架 Flask App Builder 也提供了許多設定。請參閱Flask App Builder 文件以取得有關如何配置它的詳細資訊。

你會想要改變：

- `SECRET_KEY`: 一個長的隨機字串
- `SQLALCHEMY_DATABASE_URI`：預設指向位於 ~/.superset/superset.db 的 sqlite 資料庫

```python
 WTF_CSRF_EXEMPT_LIST = [‘’]
```

## 指定SECRET_KEY

### 新增初始SECRET_KEY

Superset 需要使用者指定的 `SECRET_KEY` 才能啟動。此要求是在 2.1.0 版本中新增的，以強制進行安全性配置。將強 `SECRET_KEY` 新增至您的superset_config.py檔案中，例如：

```python
SECRET_KEY = 'YOUR_OWN_RANDOM_GENERATED_SECRET_KEY'
```

您可以使用 產生強大的安全金鑰`openssl rand -base64 42`。

> 使用強密鑰：
> 此金鑰將用於簽署會話的 cookie，以保證安全性，並以加密方式存進 Superset 的應用程式，放在元資料資料庫中的敏感資訊區。
> 確認您的生產部署必須使用複雜、且唯一的金鑰。

### 輪調到更新的SECRET_KEY

- 如果您希望更改現有的 `SECRET_KEY`，請將現有的 `SECRET_KEY` 新增至您的`superset_config.py`檔案中，`PREVIOUS_SECRET_KEY = `並提供新密鑰作為`SECRET_KEY =`。
- 您可以使用以下命令找到目前的 `SECRET_KEY` 
  - 如果使用 Docker 運行 Superset，請從 Superset 應用程式容器內執行

```bash
superset shell
from flask import current_app; print(current_app.config["SECRET_KEY"])
```

保存`superset_config.py`這些值，然後運行`superset re-encrypt-secrets`。

## 設定生產階段之元資料庫

- Superset 需要一個資料庫來儲存它所管理的信息，例如圖表、儀表板和許多其他內容的定義。

預設情況下，Superset 配置為使用SQLite，這是一個獨立的單檔案資料庫，提供簡單快速的入門方法（無需任何安裝）。然而，對於生產環境，由於安全性、可擴展性和資料完整性的原因，強烈建議不要使用 SQLite。僅使用受支援的資料庫引擎並考慮在單獨的主機或容器上使用不同的資料庫引擎非常重要。

Superset 支援以下資料庫引擎/版本：

資料庫引擎	支援的版本
PostgreSQL	10.X、11.X、12.X、13.X、14.X、15.X
MySQL	5.7、8.X
使用以下資料庫驅動程式和連接字串：

資料庫	PyPI包	連接字串
PostgreSQL	pip install psycopg2	postgresql://<UserName>:<DBPassword>@<Database Host>/<Database Name>
MySQL	pip install mysqlclient	mysql://<UserName>:<DBPassword>@<Database Host>/<Database Name>
提示
正確設定元資料儲存超出了本文檔的範圍。我們建議使用託管託管服務（例如Amazon RDS或Google 雲端資料庫）來處理服務並支援基礎架構和備份策略。

若要設定 Superset Metastore，請將SQLALCHEMY_DATABASE_URI組態鍵設定superset_config為適當的連接字串。

在 WSGI HTTP
雖然您可以在 NGINX 或 Apache 上執行 Superset，但我們建議在非同步模式下使用 Gunicorn。這甚至可以實現令人印象深刻的並發性，並且相當容易安裝和配置。請參閱您首選技術的文檔，以適合您的環境的方式設定此 Flask WSGI 應用程式。這是一個在生產中運作良好的非同步設定：

      -w 10 \
      -k gevent \
      --worker-connections 1000 \
      --timeout 120 \
      -b  0.0.0.0:6666 \
      --limit-request-line 0 \
      --limit-request-field_size 0 \
      --statsd-host localhost:8125 \
      "superset.app:create_app()"

請參閱Gunicorn 文件以獲取更多資訊。請注意，開發 Web 伺服器（superset run或flask run）不適用於生產用途。

如果您不使用 Gunicorn，您可能需要flask-compress通過COMPRESS_REGISTER = False在superset_config.py.

目前，Google BigQuery python sdk 與 不相容gevent，因為gevent.因此，當您BigQuery在 Superset 上使用資料來源時，您必須使用gunicorn除了 之外的工作類型gevent。

## HTTPS配置

- 您可以透過負載平衡器或反向代理（例如 nginx）配置 HTTPS 上游，並在流量到達 Superset 應用程式之前執行 SSL/TLS 卸載。
- 在此設定中，來自為警報和報告產生圖表快照的 Celery 工作線程的本機流量可以http://從入口點後面的 URL 存取 Superset。
- 如果您使用官方 Superset Docker 映像，您也可以在 Gunicorn（Python Web 伺服器）中配置 SSL 。

### 負載平衡器

- 如果您在負載平衡器或反向代理程式（例如 AWS 上的 NGINX 或 ELB）後面執行超集，您可能需要利用執行狀況檢查端點，以便負載平衡器知道您的超集執行個體是否正在執行。
- 如果網頁伺服器正在運行，則將/health傳回包含「OK」的 200 回應。
- 如果負載平衡器插入X-Forwarded-For/X-Forwarded-Proto標頭，您應該ENABLE_PROXY_FIX = True在超集設定檔 ( superset_config.py) 中設定以提取和使用標頭。
- 如果反向代理用於提供 SSL 加密，則X-Forwarded-Proto可能需要明確定義。對於 Apache Web 伺服器，可以如下設定：

```bash
RequestHeader set X-Forwarded-Proto "https"
```

### 自訂 OAuth2 配置

- Superset 建構於 Flask-AppBuilder (FAB) 之上，它支援許多開箱即用的供應商（GitHub、Twitter、LinkedIn、Google、Azure 等）。
- 除此之外，Superset 還可以設定為與其他支援「代碼」授權的 OAuth2 授權伺服器實作連線。

確保 pip 套件Authlib已安裝在網路伺服器上。

首先，在 Superset 中配置授權superset_config.py。

```python
from flask_appbuilder.security.manager import AUTH_OAUTH

# Set the authentication type to OAuth
AUTH_TYPE = AUTH_OAUTH

OAUTH_PROVIDERS = [
    {   'name':'egaSSO',
        'token_key':'access_token', # Name of the token in the response of access_token_url
        'icon':'fa-address-card',   # Icon for the provider
        'remote_app': {
            'client_id':'myClientId',  # Client Id (Identify Superset application)
            'client_secret':'MySecret', # Secret for this Client Id (Identify Superset application)
            'client_kwargs':{
                'scope': 'read'               # Scope for the Authorization
            },
            'access_token_method':'POST',    # HTTP Method to call access_token_url
            'access_token_params':{        # Additional parameters for calls to access_token_url
                'client_id':'myClientId'
            },
            'jwks_uri':'https://myAuthorizationServe/adfs/discovery/keys', # may be required to generate token
            'access_token_headers':{    # Additional headers for calls to access_token_url
                'Authorization': 'Basic Base64EncodedClientIdAndSecret'
            },
            'api_base_url':'https://myAuthorizationServer/oauth2AuthorizationServer/',
            'access_token_url':'https://myAuthorizationServer/oauth2AuthorizationServer/token',
            'authorize_url':'https://myAuthorizationServer/oauth2AuthorizationServer/authorize'
        }
    }
]

# Will allow user self registration, allowing to create Flask users from Authorized User
AUTH_USER_REGISTRATION = True

# The default user self registration role
AUTH_USER_REGISTRATION_ROLE = "Public"
```

- 然後，創建一個CustomSsoSecurityManager擴展SupersetSecurityManager並覆蓋的oauth_user_info：

```python
import logging
from superset.security import SupersetSecurityManager

class CustomSsoSecurityManager(SupersetSecurityManager):

    def oauth_user_info(self, provider, response=None):
        logging.debug("Oauth2 provider: {0}.".format(provider))
        if provider == 'egaSSO':
            # As example, this line request a GET to base_url + '/' + userDetails with Bearer  Authentication,
    # and expects that authorization server checks the token, and response with user details
            me = self.appbuilder.sm.oauth_remotes[provider].get('userDetails').data
            logging.debug("user_data: {0}".format(me))
            return { 'name' : me['name'], 'email' : me['email'], 'id' : me['user_name'], 'username' : me['user_name'], 'first_name':'', 'last_name':''}
    ...
```

- 該檔案必須位於superset_config.py與名稱相同的目錄中custom_sso_security_manager.py。最後，將以下兩行加入superset_config.py：

```python
from custom_sso_security_manager import CustomSsoSecurityManager
CUSTOM_SECURITY_MANAGER = CustomSsoSecurityManager
```

> 筆記
如果需要，重定向 URL 將是https://<superset-webserver>/oauth-authorized/<provider-name>設定 OAuth2 授權提供者時。例如，重定向 URL 將https://<superset-webserver>/oauth-authorized/egaSSO用於上述配置。

- 如果 OAuth2 授權伺服器支援 OpenID Connect 1.0，您可以僅設定其設定文件 URL，而無需提供、api_base_url和其他必要選項（如使用者資訊端點、jwks uri 等）。access_token_urlauthorize_url

```python
OAUTH_PROVIDERS = [
  {   'name':'egaSSO',
      'token_key':'access_token', # Name of the token in the response of access_token_url
      'icon':'fa-address-card',   # Icon for the provider
      'remote_app': {
          'client_id':'myClientId',  # Client Id (Identify Superset application)
          'client_secret':'MySecret', # Secret for this Client Id (Identify Superset application)
          'server_metadata_url': 'https://myAuthorizationServer/.well-known/openid-configuration'
      }
  }
]
```

### LDAP身分驗證

FAB(Flask-AppBuilder) 支援根據 LDAP 伺服器驗證使用者憑證。要使用 LDAP，您必須安裝[python-ldap套件](https://www.python-ldap.org/en/latest/installing.html)。有關詳細信息，請參閱[FAB 的 LDAP 文件](https://flask-appbuilder.readthedocs.io/en/latest/security.html#authentication-ldap)。

## Superset角色對應

- 此處討論將 LDAP 或 OAUTH 群組對應到 Superset角色。
- FAB(Flask-AppBuilder) 中的 `AUTH_ROLES_MAPPING` 是從 LDAP/OAUTH 群組名稱對應到 FAB 角色的字典。
- 它用於為使用 LDAP 或 OAuth 進行身份驗證的使用者指派角色。
- 實例在[8082](http://eng06.sinotech-eng.com:8082/login/)(未成功)
  - `export SUPERSET_CONFIG_PATH=/nas2/kuang/MyPrograms/superset/superset_config_LDAP.py`
  - 設定詳見[2024-07-11筆記](http://eng06.sinotech-eng.com:3000/kuang/ITnotes/src/branch/main/_posts/2024-07-11.md)

### 將 OAUTH 群組映射到 Superset角色

以下AUTH_ROLES_MAPPING字典將 OAUTH 群組“superset_users”對應到 Superset 角色“Gamma”和“Alpha”，並將 OAUTH 群組“superset_admins”對應到 Superset 角色“Admin”。

```python
AUTH_ROLES_MAPPING = {
"superset_users": ["Gamma","Alpha"],
"superset_admins": ["Admin"],
}
```

### 將 LDAP 群組對應到超集

以下AUTH_ROLES_MAPPING字典將 LDAP DN“cn=superset_users,ou=groups,dc=example,dc=com”對應到超級集角色“Gamma”和“Alpha”，以及 LDAP DN“cn=superset_admins,ou=” groups,dc= example,dc=com” 到超級集角色「Admin」。

```python
AUTH_ROLES_MAPPING = {
"cn=superset_users,ou=groups,dc=example,dc=com": ["Gamma","Alpha"],
"cn=superset_admins,ou=groups,dc=example,dc=com": ["Admin"],
}
```

注意：這個需要`AUTH_LDAP_SEARCH`設定。有關更多詳細信息，請參閱[FAB 安全文件](https://flask-appbuilder.readthedocs.io/en/latest/security.html)。

### 登入時同步角色

您也可以使用AUTH_ROLES_SYNC_AT_LOGIN設定變數來控制 Flask-AppBuilder 將使用者角色與 LDAP/OAUTH 群組同步的頻率。如果AUTH_ROLES_SYNC_AT_LOGIN設定為 True，Flask-AppBuilder 將在使用者每次登入時同步使用者的角色AUTH_ROLES_SYNC_AT_LOGIN。

Flask 應用程式配置
FLASK_APP_MUTATOR是可以在您的環境中提供的配置函數，接收應用程式物件並可以以任何方式更改它。例如，將會話 cookie 過期時間新增FLASK_APP_MUTATOR至superset_config.py24 小時：

```python
from flask import session
from flask import Flask


def make_session_permanent():
    '''
    Enable maxAge for the cookie 'session'
    '''
    session.permanent = True

# Set up max age of session to 24 hours
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
def FLASK_APP_MUTATOR(app: Flask) -> None:
    app.before_request_funcs.setdefault(None, []).append(make_session_permanent)
```

### 特色啟用開關

- 為了支援不同的使用者群組，Superset 具有一些預設未啟用的特色功能。
  - 例如，某些用戶具有更強的安全限制，而另一些用戶則可能沒有。因此 Superset 允許使用者透過配置來啟用或停用某些功能。
  - 對於功能擁有者，您可以在 Superset 中新增可選功能，但只會受到一小部分使用者的影響。
- 您可以在`superset_config.py`中使用以下dict來切換特色功能是啟用或停用狀態：

```python
FEATURE_FLAGS = {
    'PRESTO_EXPAND_DATA': False, #or True
}
```

- 目前的功能標誌清單可以在[RESOURCES/FEATURE_FLAGS.md](https://github.com/apache/superset/blob/master/RESOURCES/FEATURE_FLAGS.md)中找到。

#### 開發與測試階段不穩定設定

- 開發階段

Flags|function|ref
-|-|-
ALERT_REPORT_TABS|使用者可以設定自動警報和報告，以將儀表板或圖表傳送給電子郵件收件人或 Slack 頻道。|[Alerts and Reports](https://superset.apache.org/docs/configuration/alerts-reports)
ENABLE_ADVANCED_DATA_TYPES|將執行`from superset.advanced_data_type.types import AdvancedDataType`|在`./superset/config.py`中進一步指定
  PRESTO_EXPAND_DATA
  SHARE_QUERIES_VIA_KV_STORE
  TAGGING_SYSTEM
  CHART_PLUGINS_EXPERIMENTAL

- 測試階段

Flags|function|ref
-|-|-
ALERT_REPORTS|(同上) |[docs](https://superset.apache.org/docs/configuration/alerts-reports)
ALLOW_FULL_CSV_EXPORT
CACHE_IMPERSONATION
CONFIRM_DASHBOARD_DIFF
DRILL_TO_DETAIL
DYNAMIC_PLUGINS|k8s上執行插件|[docs](https://superset.apache.org/docs/configuration/running-on-kubernetes)
ENABLE_SUPERSET_META_DB|在db間查找|[docs](https://superset.apache.org/docs/configuration/databases/#querying-across-databases)
ESTIMATE_QUERY_COST
GLOBAL_ASYNC_QUERIES|查找結果全域同步|[docs](https://github.com/apache/superset/blob/master/CONTRIBUTING.md#async-chart-queries)
HORIZONTAL_FILTER_BAR
IMPERSONATE_WITH_EMAIL_PREFIX
PLAYWRIGHT_REPORTS_AND_THUMBNAILS
RLS_IN_SQLLAB
SSH_TUNNELING|登入主機以利查找不同db|[docs](https://superset.apache.org/docs/configuration/databases/#querying-across-databases)
USE_ANALAGOUS_COLORS

#### 開發階段穩定功能

- 路徑與停用去除

Flags|function|ref
-|-|-
DASHBOARD_VIRTUALIZATION
DRILL_BY
DISABLE_LEGACY_DATASOURCE_EDITOR

- 執行階段保留的設定項目

Flags|function|ref
-|-|-
ALERTS_ATTACH_REPORTS
ALLOW_ADHOC_SUBQUERY
DASHBOARD_RBAC|開放存取[許可](https://superset.apache.org/docs/using-superset/creating-your-first-dashboard/#manage-access-to-dashboards)|see also [docs](https://github.com/apache/superset/blob/master/RESOURCES/STANDARD_ROLES.md)
DATAPANEL_CLOSED_BY_DEFAULT
DRUID_JOINS
EMBEDDABLE_CHARTS
EMBEDDED_SUPERSET
ENABLE_TEMPLATE_PROCESSING
ESCAPE_MARKDOWN_HTML
LISTVIEWS_DEFAULT_CARD_VIEW
SCHEDULED_QUERIES|查找排程的報告格式|[docs](https://superset.apache.org/docs/configuration/alerts-reports)
SQLLAB_BACKEND_PERSISTENCE
SQL_VALIDATORS_BY_ENGINE|SQL模板|[docs](https://superset.apache.org/docs/configuration/sql-templating)
THUMBNAILS|快取記憶體之縮圖|[docs](https://superset.apache.org/docs/configuration/cache)


## docker image startup

- [apache/superset](https://hub.docker.com/r/apache/superset)
- 一次性測試

```bash
docker run -d -p "200.200.32.153:8080":8088 -e "SUPERSET_SECRET_KEY=oXbM6bfa1aO6zHyAGSjc7Ajq5tyhjILTmGjXttQnJe4G" -e "MAPBOX_API_KEY=pk.eyJ1IjoieWNrdWFuZyIsImEiOiJjbHd6dTV3d24wMHI5MmlzY2xrOWthbDZkIn0.1ylBvXKdivGsaLXbE80MrA" --name superset  apache/superset
docker exec -it superset superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password admin
docker exec -it superset superset db upgrade
docker exec -it superset superset load_examples
docker exec -it superset superset init
```

-  to stop and remove：`docker stop <id>; docker rm superset`

## superset 中文化

[](https://blog.csdn.net/jiangnianwangluo/article/details/130379493)

```python

```

### 中文簡介安裝

- [devlive.org](https://docs.devlive.org/read/apache-superset-zh-20240427/Introduction)
