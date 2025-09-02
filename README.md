# 文档分析系统

一个基于AI的文档分析和处理系统，支持PDF、Word等多种格式文档的智能分析。

## 🚀 快速开始

### 环境要求

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

### 一键部署

```bash
# 克隆项目
git clone <repository-url>
cd hackthon

# 运行部署脚本
chmod +x deploy/deploy.sh
./deploy/deploy.sh
```

### 手动部署

#### 后端部署

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# 编辑.env文件配置环境变量
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### 前端部署

```bash
cd frontend
npm install
npm run build
npm start
```

## 🧪 测试

### 运行所有测试

```bash
chmod +x deploy/test.sh
./deploy/test.sh
```

### 单独测试

```bash
# 后端测试
cd backend && python -m pytest tests/ -v

# 前端测试
cd frontend && npm test

# 集成测试
python test_integration.py
```

## 📁 项目结构

```
hackthon/
├── backend/           # 后端API服务
│   ├── app/          # 应用代码
│   ├── tests/        # 测试文件
│   └── requirements.txt
├── frontend/         # 前端界面
│   ├── src/         # 源代码
│   └── package.json
├── data/            # 数据文件
├── deploy/          # 部署配置
└── docker-compose.yml
```

## 🔧 配置

### 环境变量

复制 `backend/.env.example` 到 `backend/.env` 并配置：

- `OPENAI_API_KEY`: OpenAI API密钥
- `DATABASE_URL`: 数据库连接字符串
- `UPLOAD_DIR`: 文件上传目录

## 📊 API文档

启动后端服务后访问：http://localhost:8000/docs

## 🌐 访问地址

- 前端界面: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 🐛 故障排除

### 常见问题

1. **端口占用**: 修改docker-compose.yml中的端口映射
2. **权限问题**: 确保有Docker执行权限
3. **依赖安装失败**: 检查网络连接和包管理器配置

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend
docker-compose logs frontend
```

## 📝 开发指南

### 添加新功能

1. 后端: 在 `backend/app/routes/` 添加新路由
2. 前端: 在 `frontend/src/components/` 添加新组件
3. 测试: 在对应的 `tests/` 目录添加测试

### 代码规范

- 后端: 遵循PEP 8规范
- 前端: 使用ESLint和Prettier
- 提交前运行测试确保代码质量

## 🤝 贡献

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request