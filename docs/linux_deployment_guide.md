# ICHTP Linux 伺服器部署指南

本指南提供將 ICHTP 伺服器部署到 Linux 環境的完整步驟，分成「快速測試」及「正式對外營運 (Production)」兩種情境。

## 1. 系統環境準備

首先，登入伺服器，更新系統並安裝必要的套件 (以 Ubuntu/Debian 為例)：

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git nginx -y
```

## 2. 獲取專案與安裝套件

將專案程式碼複製到伺服器上，並建立獨立的 Python 虛擬環境：

```bash
# 1. 複製專案
git clone https://github.com/Kipperii/ICHTP.git ichtp
cd ichtp

# 2. 建立與啟動虛擬環境
python3 -m venv venv
source venv/bin/activate

# 3. 安裝 Python 套件
pip install -r requirements.txt
```

---

## 3. 情境一：快速啟動 (適合內部測試與展示)

如果您只需要短暫啟動伺服器進行測試，可以直接使用專案內建的網頁伺服器。

啟動指令 (需保持終端機開啟)：
```bash
python manage.py run --host 0.0.0.0 --port 5000
```

> **注意**：
> - `--host 0.0.0.0` 允許外部設備透過區網或外網存取。
> - 外部登入請輸入：`http://<伺服器IP>:5000`
> - 請確保伺服器的防火牆或雲端平台的 Security Group 已開放 `5000` TCP port，否則外部無法連線。

---

## 4. 情境二：正式環境部署 (Production)

為了讓網站長期穩定運行，強烈建議使用 **Gunicorn** 作為應用程式伺服器，使用 **Systemd** 管理背景執行與開機自啟，並搭配 **Nginx** 處理網域與連線轉發。

### 4.1 安裝 Gunicorn
在虛擬環境 (venv) 內安裝：
```bash
pip install gunicorn
```

### 4.2 設定 Systemd (背景常駐服務)
建立服務設定檔：
```bash
sudo nano /etc/systemd/system/ichtp.service
```
填入以下內容 (請將 `/path/to/ichtp` 替換為實際的專案路徑，例如 `/home/ubuntu/ichtp`)：
```ini
[Unit]
Description=Gunicorn instance to serve ICHTP
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/path/to/ichtp
Environment="PATH=/path/to/ichtp/venv/bin"
# 以下啟動指令，這裡採用 app:create_app() 作為範例入口，視您的實際啟動寫法而定
ExecStart=/path/to/ichtp/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 "app:create_app()"

[Install]
WantedBy=multi-user.target
```

啟動服務與設定開機自啟：
```bash
sudo systemctl daemon-reload
sudo systemctl start ichtp
sudo systemctl enable ichtp
```

### 4.3 網域 DNS 設定
若您有專屬網域 (例如 `your-domain.com`)：
1. 至您的網域註冊商 (如 GoDaddy、Cloudflare) 控制台。
2. 新增一筆 **A Record**，將記錄名稱 (Host, 例如 `@` 或 `www`) 指向該 Linux 伺服器的 **外部實體 IP (Public IP)**。

### 4.4 設定 Nginx 反向代理
讓 Nginx 接收 80 port (HTTP) 請求並轉發給背景跑在 5000 port 的專案。

建立設定檔：
```bash
sudo nano /etc/nginx/sites-available/ichtp
```
貼上以下內容：
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com; # 填入您的網域，若無網域可用 _ 代替

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
啟用設定並重啟 Nginx：
```bash
sudo ln -s /etc/nginx/sites-available/ichtp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4.5 安裝 SSL 憑證 (開啟 HTTPS 安全連線)
讓您的網站擁有安全鎖頭 (`https://`)。

```bash
# 安裝 Let's Encrypt Certbot
sudo apt install certbot python3-certbot-nginx -y

# 自動化申請憑證並設定 Nginx 
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```
按照畫面提示輸入 Email，完成後，Nginx 就會自動載入 SSL 憑證，並將一般 HTTP 流量重新導向至安全的 HTTPS 線路。