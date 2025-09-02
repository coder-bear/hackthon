#!/bin/bash

echo "☁️  云服务器部署指南"
echo "==================="

echo "1. 购买云服务器（推荐配置）："
echo "   - 阿里云/腾讯云 2核4G"
echo "   - Ubuntu 20.04"
echo "   - 开放端口：3000, 5000, 27017"
echo ""

echo "2. 服务器部署命令："
echo "   # 安装Docker"
echo "   curl -fsSL https://get.docker.com | sh"
echo "   sudo usermod -aG docker \$USER"
echo ""
echo "   # 上传项目文件"
echo "   scp -r . user@your-server-ip:~/hackthon"
echo ""
echo "   # 启动服务"
echo "   cd ~/hackthon"
echo "   ./start.sh"
echo ""

echo "3. 访问地址："
echo "   http://your-server-ip:3000"
echo ""

echo "💰 成本估算："
echo "   - 阿里云轻量服务器：约60元/月"
echo "   - 腾讯云CVM：约50元/月"