#!/bin/bash

echo "🌐 本地网络分享"
echo "==============="

# 获取本机IP地址
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

echo "📋 分享信息："
echo "前端地址: http://$LOCAL_IP:3000"
echo "后端API: http://$LOCAL_IP:5000"
echo ""
echo "🔧 使用方法："
echo "1. 确保系统正在运行: ./start.sh"
echo "2. 将上述地址分享给同网络用户"
echo "3. 用户可直接访问使用"
echo ""
echo "⚠️  注意：仅限同一WiFi网络内访问"