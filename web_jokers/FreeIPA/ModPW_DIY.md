---
layout: default
title:  FreeIPA自助重置密码
parent: Security And Authentication
grand_parent: Web Jokers
last_modified_date: 2024-03-11 11:11:54
tags: OAuth
---

# FreeIPA自助重置密码
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

- ref: 
  - [Python FreeIPA client](https://python-freeipa.readthedocs.io/en/latest/)
  - [API documentation]( https://ipa.demo1.freeipa.org/ipa/ui/#/p/apibrowser/)
- source:[FreeIPA自助重置密码](https://www.volcengine.com/theme/3968715-F-7-1)
- GPT's
    > 試用python-ipa 與Flask模組，寫一個讓使用者登入FreeIPA自行修改密碼的網頁程式。

### 安裝

- pip install 三個名稱，結果都是一樣：python-freeipa(官網)、ipapython、python-ipa(GPT's)

### python-freeipa測試

- python-freeipa與新版FreeIPA的CA管理並未銜接得很好，因此需要在ipython中逐一詳細測試，確定可以連接、登入、並執行密碼修改。
- 有關url的設定：不需要前綴(http或https)、domain name與ip的效果式一樣。
- 有關CA認證與SSL設定
  - FreeIPA需使用https才能連接。目前公司並未開放個人電腦自己新增證書。
  - 傳統apache是用`/etc/httpd/alias/httpd.crt`及`/etc/httpd/alias/httpd.key`，
  - 但是新版的FreeIPA的alias(設定如下)是使用db形式來授權，因此須關閉SSL的驗證，這在python-freeipa默認是True，需要在python中更改：`verify_ssl=False`。

```bash
sudo ls /etc/httpd/alias
lrwxrwxrwx. 1 root root     24 Feb  5 14:20 libnssckbi.so -> /usr/lib64/libnssckbi.so*
-rw-------. 1 root root   5.2K Feb  5 14:20 install.log
-rw-------. 1 root root     32 Feb  5 17:56 ipasession.key
-rw-------. 1 root apache   41 Feb  8 15:38 pwdfile.txt
-rw-r-----. 1 root apache  16K Feb  8 15:38 secmod.db
-rw-r-----. 1 root apache  16K Feb  8 15:38 key3.db
-rw-r-----. 1 root apache  64K Feb  8 15:38 cert8.db
```

- 是否需先登入：
  - 傳統GPT與claude都建議先以admin或使用者自己舊的帳密先登入，確認無誤再開放密碼的修改。前者沒有必要、且有帳密暴露之虞。
  - 事實上，`client.change_password()`函式的錯誤訊息包括了登入錯誤，因此似乎不需要先登入、確認後再接受密碼修改。
- 如何呈現錯誤訊息
  - 因為錯誤可能有很多種(使用者不存在、舊密碼不對、)

## Flask python

```python
from flask import Flask, request, render_template, redirect, url_for
from python_freeipa import ClientMeta

app = Flask(__name__)
url='node03.sinotech-eng.com'

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/change_password", methods=["GET","POST"])
def change_password():
    if request.method == 'POST':
        client = ClientMeta(url,verify_ssl=False)
        username = request.form['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        try:
            client.change_password(username, new_password, old_password)
            return redirect(url_for('success'))
        except Exception as e:
            with open('templates/error.html','w') as f:
                f.write(str(e))
            return render_template('error.html', error=str(e))
    return render_template("index.html")

# 密碼更改成功路由
@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == "__main__":
    app.run(debug=True, host=url, port=5000)

```

接著，創建一個 `templates` 資料夾，其中包含一個 `index.html` 檔案：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Change Password</title>
</head>
<body>
    <h1>Change Password</h1>
    \{\% with messages = get_flashed_messages() \%\}
        \{\% if messages \%\}
            <ul>
                \{\% for message in messages \%\}
                    <li>{{ message }}</li>
                \{\% endfor \%\}
            </ul>
        \{\% endif \%\}
    \{\% endwith \%\}
    <form action="{{ url_for('change_password') }}" method="post">
        <label for="username">Username:</label>
        <input type="text" name="username" required><br>
        <label for="old_password">Old Password:</label>
        <input type="password" name="old_password" required><br>
        <label for="new_password">New Password:</label>
        <input type="password" name="new_password" required><br>
        <button type="submit">Change Password</button>
    </form>
</body>
</html>
```

請注意替換程式碼中的 `your-ipa-server`、`admin` 和 `your-password` 部分為你的 FreeIPA 伺服器地址、管理員帳號和密碼。此程式碼提供了一個簡單的 Web 頁面，用戶可以輸入用戶名、舊密碼和新密碼，然後修改密碼。

請確保在實際應用中採取適當的安全措施，例如使用 HTTPS 來保護通信，以及妥善處理錯誤和例外情況。

## Claude2 solution

很好,以下是一個使用Python的Flask框架和python-ipa模組建立的網頁應用程式,允許使用者修改自己的密碼。

```python
from flask import Flask, request, render_template, redirect, url_for
import ipa  # python-ipa模組

app = Flask(__name__)

# 初始化使用者密碼字典
users = {'user1': 'password1', 'user2': 'password2'}

# 首頁路由
@app.route('/')
def index():
    return render_template('index.html')

# 更改密碼路由
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        username = request.form['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        # 檢查舊密碼是否正確
        if username in users and users[username] == old_password:
            # 更新密碼
            users[username] = new_password
            return redirect(url_for('success'))
        else:
            error = '無效的使用者名稱或舊密碼'
            return render_template('change_password.html', error=error)

    return render_template('change_password.html')

# 密碼更改成功路由
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
```

在這個範例中,我們首先導入所需的模組和初始化Flask應用程式。然後定義一個簡單的使用者密碼字典,用於模擬用戶驗證。

接下來,我們定義三個路由:

1. `index()`路由渲染主頁模板。
2. `change_password()`路由處理密碼更改請求。如果是GET請求,它渲染密碼更改表單模板。如果是POST請求,它會檢查舊密碼是否正確,如果正確就更新密碼字典中的密碼,否則返回錯誤信息。
3. `success()`路由渲染密碼更改成功模板。

您還需要創建三個HTML模板文件:

`index.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>首頁</title>
</head>
<body>
    <h1>歡迎來到密碼更改網站</h1>
    <a href="{{ url_for('change_password') }}">更改密碼</a>
</body>
</html>
```

`change_password.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>更改密碼</title>
</head>
<body>
    <h1>更改密碼</h1>
    \{\% if error \%\}
        <p style="color: red;">{{ error }}</p>
    \{\% endif \%\}
    <form method="post" action="{{ url_for('change_password') }}">
        <label for="username">使用者名稱:</label>
        <input type="text" id="username" name="username" required><br>

        <label for="old_password">舊密碼:</label>
        <input type="password" id="old_password" name="old_password" required><br>

        <label for="new_password">新密碼:</label>
        <input type="password" id="new_password" name="new_password" required><br>

        <input type="submit" value="更改密碼">
    </form>
</body>
</html>
```

`success.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>密碼更改成功</title>
</head>
<body>
    <h1>密碼更改成功!</h1>
    <a href="{{ url_for('index') }}">返回首頁</a>
</body>
</html>
```

請確保將這些HTML文件放置在與Flask應用程式相同的目錄下的`templates`子目錄中。

啟動Flask應用程式後,您可以在瀏覽器中訪問`http://localhost:5000`來查看首頁。從首頁,您可以點擊"更改密碼"鏈接來訪問密碼更改表單。填寫表單後,如果舊密碼正確,密碼就會被更新,並重定向到成功頁面。

請注意,這只是一個簡單的示例,在生產環境中,您應該採取額外的安全措施,如散列密碼、使用安全的會話管理等。

## 綜合版本

### template 

- `change_password.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>更改密碼</title>
</head>
<body>
    <h1>更改密碼</h1>
    \{\% if error \%\}
        <p style="color: red;">{{ error }}</p>
    \{\% endif \%\}
    \{\% with messages = get_flashed_messages() \%\}
        \{\% if messages \%\}
            <ul>
                \{\% for message in messages \%\}
                    <li>{{ message }}</li>
                \{\% endfor \%\}
            </ul>
        \{\% endif \%\}
    \{\% endwith \%\}
    <form action="{{ url_for('change_password') }}" method="post">
        <label for="username">使用者名稱:</label>
        <input type="text" name="username" required><br>
        <label for="old_password">舊密碼:</label>
        <input type="password" name="old_password" required><br>
        <label for="new_password">新密碼:</label>
        <input type="password" name="new_password" required><br>
        <button type="submit">Change Password</button>
    </form>
</body>
</html>
```

`success.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>密碼更改成功</title>
</head>
<body>
    <h1>密碼更改成功!</h1>
    <a href="{{ url_for('index') }}">返回首頁</a>
</body>
</html>
```
