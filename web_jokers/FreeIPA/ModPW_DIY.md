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
  - 因為錯誤可能有很多種(使用者不存在、舊密碼不對、太快修改密碼等等)，傳統引到錯誤訊息html檔的作法太過繁瑣。
  - 還好python-freeipa的錯誤訊息是個html的內容，可以直接寫成error.html讓flask程式呼叫。

## Flask python

- 3個路由
  - 其中第2個`/change_password`，還是回到`index.html`。
  - 還是會需要特別的`/change_password`路由，讓html來呼叫，呼叫`/`感覺會是個endless loop。
  - 沒有特別一個`error`的路由，因為是用現成的python-freeipa error message。
- 是`request.form`、還是`request.get_json`，可以詳見[這一篇](https://stackabuse.com/how-to-get-and-parse-http-post-body-in-flask-json-and-form-data/)，可能跟html的設計有關，如果是分開的空格，還是前者比較方便。

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

## templates資料夾

### index.html

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
    <h1>歡迎來到FreeIPA LDAP密碼更改網站</h1>
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

### success.html

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
