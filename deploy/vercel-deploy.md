# Vercel + Railway 部署指南

这是最简单的部署方案，适合快速分享给他人使用。

## 1. 前端部署到Vercel

### 准备工作
1. 注册 [Vercel账号](https://vercel.com)
2. 将代码推送到GitHub

### 部署步骤

#### 创建vercel.json配置
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "https://your-backend-url.railway.app/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

#### 修改前端配置
```bash
# frontend/package.json 添加构建脚本
{
  "scripts": {
    "build": "react-scripts build",
    "vercel-build": "npm run build"
  }
}
```

#### 部署到Vercel
1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 "New Project"
3. 导入GitHub仓库
4. 设置构建配置：
   - Framework Preset: Create React App
   - Root Directory: frontend
   - Build Command: npm run build
   - Output Directory: build

## 2. 后端部署到Railway

### 准备工作
1. 注册 [Railway账号](https://railway.app)
2. 准备后端代码

#### 创建railway.json
```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "python app.py",
    "healthcheckPath": "/health"
  }
}
```

#### 修改后端Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要目录
RUN mkdir -p uploads data

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "app.py"]
```

### 部署步骤
1. 访问 [Railway Dashboard](https://railway.app/dashboard)
2. 点击 "New Project"
3. 选择 "Deploy from GitHub repo"
4. 选择你的仓库
5. 设置环境变量：
   - `GEMINI_API_KEY`: 你的Gemini API密钥
   - `PORT`: 5000
   - `FLASK_ENV`: production

## 3. 数据库部署

### 使用Railway MongoDB
1. 在Railway项目中点击 "New Service"
2. 选择 "Database" → "MongoDB"
3. 复制连接字符串到环境变量 `MONGODB_URI`

### 或使用MongoDB Atlas（推荐）
1. 注册 [MongoDB Atlas](https://www.mongodb.com/atlas)
2. 创建免费集群
3. 获取连接字符串
4. 在Railway中设置 `MONGODB_URI` 环境变量

## 4. 环境变量配置

### Vercel环境变量
```bash
REACT_APP_API_URL=https://your-backend.railway.app
```

### Railway环境变量
```bash
GEMINI_API_KEY=your_gemini_api_key
MONGODB_URI=your_mongodb_connection_string
FLASK_ENV=production
PORT=5000
```

## 5. 自定义域名（可选）

### Vercel域名
1. 在Vercel项目设置中
2. 点击 "Domains"
3. 添加自定义域名

### Railway域名
1. 在Railway项目设置中
2. 点击 "Settings" → "Domains"
3. 添加自定义域名

## 6. 部署脚本

创建自动部署脚本：
```bash
#!/bin/bash
# deploy.sh

echo "🚀 开始部署到云平台..."

# 检查git状态
if [[ -n $(git status -s) ]]; then
    echo "📝 提交代码更改..."
    git add .
    git commit -m "Deploy: $(date)"
fi

# 推送到GitHub
echo "📤 推送代码到GitHub..."
git push origin main

echo "✅ 部署完成！"
echo "🌐 前端地址: https://your-app.vercel.app"
echo "🔧 后端地址: https://your-backend.railway.app"
```

## 7. 监控和维护

### Vercel监控
- 访问Vercel Dashboard查看部署状态
- 查看访问日志和性能指标

### Railway监控
- 访问Railway Dashboard查看服务状态
- 查看日志和资源使用情况

### 成本控制
- Vercel: 免费版有带宽限制
- Railway: 免费版有使用时长限制
- MongoDB Atlas: 免费版有存储限制

## 8. 故障排除

### 常见问题
1. **构建失败**: 检查package.json和依赖
2. **API连接失败**: 检查CORS设置和环境变量
3. **数据库连接失败**: 检查MongoDB连接字符串

### 调试方法
```bash
# 查看Vercel构建日志
vercel logs

# 查看Railway日志
railway logs