# AWS部署指南

本文档详细说明如何在AWS上部署RAG学习建议系统。

## 前置条件

1. AWS账户和适当的权限
2. AWS CLI已安装并配置
3. Docker和Docker Compose已安装
4. 域名（可选，用于HTTPS）

## 部署步骤

### 1. 创建EC2实例

```bash
# 创建安全组
aws ec2 create-security-group \
    --group-name rag-learning-advisor-sg \
    --description "Security group for RAG Learning Advisor"

# 添加安全组规则
aws ec2 authorize-security-group-ingress \
    --group-name rag-learning-advisor-sg \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-name rag-learning-advisor-sg \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-name rag-learning-advisor-sg \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0

# 启动EC2实例
aws ec2 run-instances \
    --image-id ami-0c02fb55956c7d316 \
    --count 1 \
    --instance-type t3.medium \
    --key-name your-key-pair \
    --security-groups rag-learning-advisor-sg \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=rag-learning-advisor}]'
```

### 2. 连接到EC2实例

```bash
# 获取实例公网IP
INSTANCE_IP=$(aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=rag-learning-advisor" \
    --query "Reservations[0].Instances[0].PublicIpAddress" \
    --output text)

# SSH连接
ssh -i your-key-pair.pem ubuntu@$INSTANCE_IP
```

### 3. 安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 安装其他工具
sudo apt install -y git nginx certbot python3-certbot-nginx
```

### 4. 部署应用

```bash
# 克隆代码
git clone <your-repository-url>
cd rag-learning-advisor

# 配置环境变量
cp .env.example .env
nano .env  # 编辑配置

# 部署应用
chmod +x deploy/deploy.sh
./deploy/deploy.sh
```

### 5. 配置Nginx和SSL

```bash
# 备份默认配置
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup

# 创建新的Nginx配置
sudo tee /etc/nginx/sites-available/rag-learning-advisor << 'EOF'
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
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# 启用站点
sudo ln -s /etc/nginx/sites-available/rag-learning-advisor /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx

# 获取SSL证书
sudo certbot --nginx -d your-domain.com
```

### 6. 设置自动启动

```bash
# 创建systemd服务
sudo tee /etc/systemd/system/rag-learning-advisor.service << 'EOF'
[Unit]
Description=RAG Learning Advisor
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/rag-learning-advisor
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# 启用服务
sudo systemctl enable rag-learning-advisor.service
sudo systemctl start rag-learning-advisor.service
```

## 监控和维护

### 日志查看

```bash
# 查看应用日志
docker-compose logs -f

# 查看Nginx日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# 查看系统日志
sudo journalctl -u rag-learning-advisor.service -f
```

### 备份策略

```bash
# 创建备份脚本
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/ubuntu/backups"

mkdir -p $BACKUP_DIR

# 备份MongoDB数据
docker-compose exec -T mongodb mongodump --archive | gzip > $BACKUP_DIR/mongodb_$DATE.gz

# 备份应用配置
tar -czf $BACKUP_DIR/config_$DATE.tar.gz .env docker-compose.yml

# 清理旧备份（保留7天）
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
EOF

chmod +x backup.sh

# 设置定时备份
(crontab -l 2>/dev/null; echo "0 2 * * * /home/ubuntu/rag-learning-advisor/backup.sh") | crontab -
```

### 更新部署

```bash
# 拉取最新代码
git pull origin main

# 重新构建和部署
./deploy/deploy.sh

# 验证部署
./deploy/deploy.sh health
```

## 故障排除

### 常见问题

1. **服务无法启动**
   ```bash
   # 检查Docker状态
   sudo systemctl status docker
   
   # 检查端口占用
   sudo netstat -tlnp | grep :5000
   sudo netstat -tlnp | grep :3000
   ```

2. **数据库连接失败**
   ```bash
   # 检查MongoDB容器
   docker-compose ps mongodb
   docker-compose logs mongodb
   ```

3. **SSL证书问题**
   ```bash
   # 续期证书
   sudo certbot renew --dry-run
   ```

### 性能优化

1. **启用缓存**
   - 配置Redis缓存
   - 启用Nginx缓存

2. **数据库优化**
   - 创建适当的索引
   - 配置MongoDB副本集

3. **负载均衡**
   - 使用AWS Application Load Balancer
   - 配置多个后端实例

## 成本估算

基于AWS t3.medium实例的月度成本估算：

- EC2实例: ~$30/月
- EBS存储: ~$10/月
- 数据传输: ~$5/月
- 总计: ~$45/月

## 安全建议

1. 定期更新系统和依赖
2. 使用IAM角色而非访问密钥
3. 启用CloudTrail日志
4. 配置VPC和安全组
5. 定期备份数据
6. 监控异常访问