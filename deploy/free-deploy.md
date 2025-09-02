# 🆓 免费部署方案

## Railway部署（推荐）

### 1. 准备工作
- 注册Railway账号：https://railway.app
- 连接GitHub账号

### 2. 部署步骤
```bash
# 1. 推送代码到GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/rag-system.git
git push -u origin main

# 2. 在Railway中导入项目
# 3. 设置环境变量：GEMINI_API_KEY
# 4. 自动部署完成
```

### 3. 访问地址
- Railway会提供免费域名
- 例如：https://your-app.railway.app

## Render部署

### 1. 注册Render：https://render.com
### 2. 连接GitHub仓库
### 3. 配置构建命令：
```
Build Command: docker-compose build
Start Command: docker-compose up
```

## Heroku替代方案

### 1. Fly.io：https://fly.io
### 2. Cyclic：https://cyclic.sh
### 3. Vercel + PlanetScale

## 成本对比
- Railway：免费额度500小时/月
- Render：免费额度750小时/月
- Fly.io：免费额度2340小时/月