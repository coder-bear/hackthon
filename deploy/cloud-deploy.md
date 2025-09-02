# 云服务器部署指南

## 1. 服务器选择

### 推荐配置
- **CPU**: 2核心以上
- **内存**: 4GB以上
- **存储**: 20GB以上
- **带宽**: 5Mbps以上

### 云服务商推荐
- **阿里云ECS**（国内用户）
- **腾讯云CVM**（国内用户）
- **AWS EC2**（国际用户）
- **Google Cloud**（国际用户）

## 2. 服务器环境配置

### 连接服务器
```bash
ssh root@your_server_ip
```

### 安装Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

### 配置防火墙
```bash
# 开放必要端口
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw allow 3000  # 前端
sudo ufw allow 5000  # 后端
sudo ufw enable
```

## 3. 部署应用

### 上传代码
```bash
# 方法1：使用git
git clone https://github.com/your-username/rag-learning-advisor.git
cd rag-learning-advisor

# 方法2：使用scp上传
scp -r ./rag-learning-advisor root@your_server_ip:/root/
```

### 配置环境变量
```bash
cp .env.example .env
nano .env
```

配置内容：
```env
# Gemini API配置
GEMINI_API_KEY=your_actual_gemini_api_key

# 生产环境配置
FLASK_ENV=production
FLASK_DEBUG=False

# 域名配置
DOMAIN=your-domain.com
```

### 启动服务
```bash
chmod +x start.sh
./start.sh
```

## 4. 域名和SSL配置

### 购买域名
1. 在阿里云、腾讯云等购买域名
2. 将域名解析到服务器IP

### 配置Nginx反向代理
```bash
sudo apt install nginx

# 创建配置文件
sudo nano /etc/nginx/sites-available/rag-app
```

Nginx配置：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://localhost:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/rag-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 配置SSL证书（免费）
```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加：0 12 * * * /usr/bin/certbot renew --quiet
```

## 5. 系统服务配置

创建systemd服务：
```bash
sudo nano /etc/systemd/system/rag-app.service
```

服务配置：
```ini
[Unit]
Description=RAG Learning Advisor
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/root/rag-learning-advisor
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable rag-app
sudo systemctl start rag-app
```

## 6. 监控和维护

### 查看服务状态
```bash
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 查看系统资源
htop
df -h
```

### 备份数据
```bash
# 创建备份脚本
nano backup.sh
```

备份脚本：
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/root/backups"

mkdir -p $BACKUP_DIR

# 备份MongoDB数据
docker-compose exec -T mongodb mongodump --archive | gzip > $BACKUP_DIR/mongodb_$DATE.gz

# 备份配置文件
tar -czf $BACKUP_DIR/config_$DATE.tar.gz .env docker-compose.yml

# 清理旧备份（保留7天）
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "备份完成: $DATE"
```

设置定时备份：
```bash
chmod +x backup.sh
crontab -e
# 添加：0 2 * * * /root/rag-learning-advisor/backup.sh
```

## 7. 性能优化

### Docker优化
```yaml
# docker-compose.yml 添加资源限制
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

### 数据库优化
```bash
# MongoDB配置优化
docker-compose exec mongodb mongosh
db.adminCommand({setParameter: 1, internalQueryExecMaxBlockingSortBytes: 335544320})
```

## 8. 故障排除

### 常见问题
1. **端口被占用**：`sudo netstat -tulpn | grep :端口号`
2. **内存不足**：增加swap空间或升级服务器
3. **磁盘空间不足**：清理Docker镜像 `docker system prune -a`

### 日志查看
```bash
# 系统日志
sudo journalctl -u rag-app -f

# 应用日志
docker-compose logs backend
docker-compose logs frontend