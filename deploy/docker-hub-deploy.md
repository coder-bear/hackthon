# Docker Hub 一键部署方案

将应用打包成Docker镜像，用户只需一条命令即可运行。

## 1. 构建Docker镜像

### 创建多阶段Dockerfile
```dockerfile
# Dockerfile.production
FROM node:18-alpine AS frontend-build

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ .
RUN npm run build

FROM python:3.11-slim AS backend-build

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# 复制后端代码
WORKDIR /app
COPY --from=backend-build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-build /usr/local/bin /usr/local/bin
COPY backend/ .

# 复制前端构建文件
COPY --from=frontend-build /app/frontend/build /var/www/html

# 配置Nginx
COPY deploy/nginx-production.conf /etc/nginx/sites-available/default

# 配置Supervisor
COPY deploy/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# 创建必要目录
RUN mkdir -p /app/uploads /app/data /var/log/supervisor

# 暴露端口
EXPOSE 80

# 启动命令
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
```

### 创建Nginx配置
```nginx
# deploy/nginx-production.conf
server {
    listen 80;
    server_name localhost;

    # 前端静态文件
    location / {
        root /var/www/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # API代理
    location /api/ {
        proxy_pass http://localhost:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 健康检查
    location /health {
        proxy_pass http://localhost:5000/health;
    }
}
```

### 创建Supervisor配置
```ini
# deploy/supervisord.conf
[supervisord]
nodaemon=true
user=root

[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/nginx.err.log
stdout_logfile=/var/log/supervisor/nginx.out.log

[program:backend]
command=python app.py
directory=/app
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/backend.err.log
stdout_logfile=/var/log/supervisor/backend.out.log
environment=FLASK_ENV=production,PORT=5000
```

## 2. 构建和推送镜像

### 构建脚本
```bash
#!/bin/bash
# build-docker.sh

IMAGE_NAME="your-username/rag-learning-advisor"
VERSION="latest"

echo "🔨 构建Docker镜像..."
docker build -f Dockerfile.production -t $IMAGE_NAME:$VERSION .

echo "🧪 测试镜像..."
docker run -d --name test-container -p 8080:80 \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  $IMAGE_NAME:$VERSION

sleep 10

if curl -f http://localhost:8080/health; then
    echo "✅ 镜像测试通过"
    docker stop test-container
    docker rm test-container
    
    echo "📤 推送到Docker Hub..."
    docker push $IMAGE_NAME:$VERSION
    
    echo "🎉 镜像发布完成！"
    echo "📋 使用方法："
    echo "docker run -d -p 80:80 -e GEMINI_API_KEY=your_key $IMAGE_NAME:$VERSION"
else
    echo "❌ 镜像测试失败"
    docker stop test-container
    docker rm test-container
    exit 1
fi
```

## 3. 用户使用指南

### 创建用户文档
```markdown
# RAG学习建议系统 - 一键部署

## 快速开始

### 1. 获取Gemini API Key
访问 https://makersuite.google.com/app/apikey 获取免费API密钥

### 2. 运行应用
```bash
docker run -d \
  --name rag-learning-advisor \
  -p 80:80 \
  -e GEMINI_API_KEY=your_gemini_api_key \
  your-username/rag-learning-advisor:latest
```

### 3. 访问应用
打开浏览器访问: http://localhost

## 高级配置

### 使用外部数据库
```bash
docker run -d \
  --name rag-learning-advisor \
  -p 80:80 \
  -e GEMINI_API_KEY=your_gemini_api_key \
  -e MONGODB_URI=mongodb://your-mongodb-url \
  -v /path/to/data:/app/data \
  your-username/rag-learning-advisor:latest
```

### 使用Docker Compose
```yaml
version: '3.8'
services:
  app:
    image: your-username/rag-learning-advisor:latest
    ports:
      - "80:80"
    environment:
      - GEMINI_API_KEY=your_gemini_api_key
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

## 故障排除

### 查看日志
```bash
docker logs rag-learning-advisor
```

### 进入容器调试
```bash
docker exec -it rag-learning-advisor bash
```
```

## 4. GitHub Actions自动构建

### 创建CI/CD配置
```yaml
# .github/workflows/docker-build.yml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      if: github.event_name != 'pull_request'
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: your-username/rag-learning-advisor
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        file: ./Dockerfile.production
        push: ${{ github.event_name != 'pull_request' }}
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

## 5. 分发方式

### 1. Docker Hub分发
```bash
# 用户只需运行
docker run -d -p 80:80 -e GEMINI_API_KEY=xxx your-username/rag-learning-advisor
```

### 2. 一键安装脚本
```bash
#!/bin/bash
# install.sh
curl -fsSL https://raw.githubusercontent.com/your-username/rag-learning-advisor/main/install.sh | bash
```

### 3. 离线安装包
```bash
# 导出镜像
docker save your-username/rag-learning-advisor:latest > rag-app.tar

# 用户导入镜像
docker load < rag-app.tar