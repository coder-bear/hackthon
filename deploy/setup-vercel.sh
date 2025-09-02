#!/bin/bash

echo "🚀 Vercel + Railway 快速部署脚本"
echo "=================================="

# 检查必要工具
if ! command -v git &> /dev/null; then
    echo "❌ 请先安装Git"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ 请先安装Node.js和npm"
    exit 1
fi

# 安装Vercel CLI
echo "📦 安装Vercel CLI..."
npm install -g vercel

# 安装Railway CLI
echo "📦 安装Railway CLI..."
npm install -g @railway/cli

# 检查环境变量
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  请设置GEMINI_API_KEY环境变量"
    read -p "请输入您的Gemini API Key: " GEMINI_API_KEY
    export GEMINI_API_KEY=$GEMINI_API_KEY
fi

# 创建vercel.json
echo "📝 创建Vercel配置..."
cat > vercel.json << EOF
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
      "dest": "https://\$RAILWAY_DOMAIN/api/\$1"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/\$1"
    }
  ]
}
EOF

# 部署前端到Vercel
echo "🚀 部署前端到Vercel..."
cd frontend
vercel --prod
cd ..

# 部署后端到Railway
echo "🚀 部署后端到Railway..."
cd backend
railway login
railway new
railway add
railway deploy
cd ..

echo "✅ 部署完成！"
echo "🌐 前端地址: 查看Vercel控制台"
echo "🔧 后端地址: 查看Railway控制台"
echo "📝 请在Vercel中设置环境变量REACT_APP_API_URL"