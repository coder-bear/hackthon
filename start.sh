#!/bin/bash

echo "🚀 启动RAG学习建议系统..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 检查API配置
if [ ! -f .env ]; then
    echo "⚠️  未找到.env文件，正在创建..."
    cp .env.example .env
    echo "📝 请编辑.env文件，设置您的API Key："
    echo "   - GEMINI_API_KEY（推荐，免费）"
    echo "   - DEEPSEEK_API_KEY（备用）"
    echo "   - QWEN_API_KEY（备用）"
    echo ""
    echo "💡 查看GEMINI_SETUP_GUIDE.md获取Gemini API配置指南"
    echo "💡 查看API_SETUP_GUIDE.md获取其他API配置指南"
    echo ""
    read -p "按Enter键继续（系统将使用备用建议生成器）..."
fi

# 检查环境变量文件
echo "📋 检查环境配置..."

# 停止现有容器
echo "🛑 停止现有容器..."
docker-compose down

# 构建并启动服务
echo "🔨 构建并启动服务..."
docker-compose up -d --build

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose ps

# 检查服务健康状态
echo "🏥 检查服务健康状态..."
for i in {1..10}; do
    if curl -s http://localhost:5000/health > /dev/null; then
        echo "✅ 后端服务启动成功"
        break
    else
        echo "⏳ 等待后端服务启动... ($i/10)"
        sleep 3
    fi
done

for i in {1..10}; do
    if curl -s http://localhost:3000 > /dev/null; then
        echo "✅ 前端服务启动成功"
        break
    else
        echo "⏳ 等待前端服务启动... ($i/10)"
        sleep 3
    fi
done

echo ""
echo "🎉 系统启动完成！"
echo ""
echo "📱 访问地址："
echo "   前端界面: http://localhost:3000"
echo "   后端API:  http://localhost:5000"
echo "   API文档:  http://localhost:5000/docs"
echo ""
echo "🧪 测试系统："
echo "   python test_gemini_api.py  # 测试Gemini API"
echo "   python test_system.py      # 完整系统测试"
echo "   python test_upload.py      # 文件上传测试"
echo ""
echo "📚 使用指南："
echo "   - 查看 README.md 了解系统功能"
echo "   - 查看 API_SETUP_GUIDE.md 配置AI服务"
echo "   - 查看 DEPLOYMENT_GUIDE.md 了解部署详情"
echo ""
echo "🛠️  管理命令："
echo "   查看日志: docker-compose logs -f"
echo "   停止服务: docker-compose down"
echo "   重启服务: docker-compose restart"