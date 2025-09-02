#!/bin/bash

echo "🚀 Gemini API 快速配置脚本"
echo "=" * 40

# 检查.env文件
if [ ! -f .env ]; then
    echo "📋 创建.env文件..."
    cp .env.example .env
fi

# 检查是否已配置Gemini API Key
if grep -q "GEMINI_API_KEY=your_gemini_api_key_here" .env || ! grep -q "GEMINI_API_KEY=" .env; then
    echo ""
    echo "🔑 请配置Gemini API Key："
    echo ""
    echo "1. 访问: https://makersuite.google.com/app/apikey"
    echo "2. 使用Google账号登录"
    echo "3. 点击 'Create API Key' 创建API密钥"
    echo "4. 复制API Key"
    echo ""
    read -p "请输入您的Gemini API Key: " api_key
    
    if [ ! -z "$api_key" ]; then
        # 更新.env文件
        if grep -q "GEMINI_API_KEY=" .env; then
            sed -i.bak "s/GEMINI_API_KEY=.*/GEMINI_API_KEY=$api_key/" .env
        else
            echo "GEMINI_API_KEY=$api_key" >> .env
        fi
        echo "✅ API Key已保存到.env文件"
    else
        echo "⚠️  未输入API Key，请手动编辑.env文件"
    fi
else
    echo "✅ 已找到Gemini API Key配置"
fi

# 安装依赖
echo ""
echo "📦 安装Python依赖..."
cd backend
pip install -r requirements.txt
cd ..

# 测试API连接
echo ""
echo "🧪 测试API连接..."
python test_gemini_api.py

echo ""
echo "🎉 配置完成！"
echo ""
echo "📱 启动系统: ./start.sh"
echo "📚 查看文档: cat GEMINI_SETUP_GUIDE.md"