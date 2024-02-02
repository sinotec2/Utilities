

### macOS set-up

要在 macOS 上架設一個外部可連結的 HTTPS 網站伺服器，您可以使用內建的 Apache 伺服器並使用 Let's Encrypt 提供的免費 SSL/TLS 憑證。以下是一個簡單的步驟：

1. **安裝 Homebrew：**
   如果您尚未安裝 Homebrew，您可以使用以下指令安裝它：

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **安裝 Apache：**
   使用 Homebrew 安裝 Apache：

   ```bash
   brew install httpd
   ```

3. **啟動 Apache：**
   使用以下指令啟動 Apache 伺服器：

   ```bash
   sudo apachectl start
   ```

4. **安裝 Certbot：**
   使用 Homebrew 安裝 Certbot：

   ```bash
   brew install certbot
   ```

5. **取得 Let's Encrypt 憑證：**
   使用 Certbot 取得免費的 Let's Encrypt SSL/TLS 憑證。請將 `your_domain.com` 替換為您實際的網域名稱。

   ```bash
   sudo certbot certonly --webroot -w /usr/local/var/www -d your_domain.com
   ```

   這個指令會在 `/usr/local/var/www` 資料夾中創建一個暫時的檔案，以證明您對網域的控制權。

6. **設定 Apache 支援 HTTPS：**
   編輯 Apache 的設定檔，通常在 `/usr/local/etc/httpd/httpd.conf`(yes) 或 `/etc/apache2/httpd.conf`。確保以下模組被啟用：

   ```apache
   LoadModule socache_shmcb_module lib/httpd/modules/mod_socache_shmcb.so
   LoadModule ssl_module lib/httpd/modules/mod_ssl.so
   ```

   添加以下設定：

   ```apache
<VirtualHost *:80>
    ServerName your_domain.com
    DocumentRoot "/usr/local/var/www"
    Redirect permanent "/" "https://your_domain.com/"
</VirtualHost>

<VirtualHost *:443>
    ServerName your_domain.com
    DocumentRoot "/usr/local/var/www"

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/your_domain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/your_domain.com/privkey.pem

    <Directory "/usr/local/var/www">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
   ```

   請替換 `your_domain.com` 為您實際的網域名稱。

7. **重新啟動 Apache：**
   使用以下指令重新啟動 Apache：

   ```bash
   sudo apachectl restart
   ```

現在，您的 Apache 伺服器應該支援 HTTPS 了，而且使用 Let's Encrypt 提供的免費憑證。请注意，這僅為基本的設定，您可能需要進一步調整以符合您的實際需求。

### 取消GoDaddy指定到網域的免費網站

- 將免費網站指定到其他免費網域的url
