#!/bin/bash

# 测试脚本
set -e

echo "🧪 开始运行测试..."

# 后端测试
echo "📋 运行后端测试..."
cd backend
python -m pytest tests/ -v --tb=short
cd ..

# 前端测试
echo "🎨 运行前端测试..."
cd frontend
npm test -- --watchAll=false
cd ..

# 集成测试
echo "🔗 运行集成测试..."
python test_integration.py

echo "✅ 所有测试通过！"