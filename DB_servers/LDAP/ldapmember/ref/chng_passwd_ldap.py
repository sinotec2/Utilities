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
