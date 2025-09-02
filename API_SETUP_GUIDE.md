# API配置指南

## 支持的AI服务提供商

本系统支持多个AI服务提供商，您可以选择其中任意一个：

### 1. Google Gemini API（推荐）

**优势**：
- 免费使用（有配额限制）
- Google官方支持
- 响应速度快
- 中文支持好

**获取步骤**：
1. 访问 https://makersuite.google.com/app/apikey
2. 使用Google账号登录
3. 点击 "Create API Key" 创建新的API密钥
4. 复制API Key到`.env`文件中的`GEMINI_API_KEY`

**免费配额**：
- 每分钟15个请求
- 每天1500个请求

### 2. DeepSeek API（备用）

**优势**：
- 国内访问速度快
- 价格便宜
- 中文支持好

**获取步骤**：
1. 访问 https://platform.deepseek.com/
2. 注册账号并登录
3. 进入API Keys页面
4. 创建新的API Key
5. 复制API Key到`.env`文件中的`DEEPSEEK_API_KEY`

**定价**：约0.14元/1M tokens

### 2. 通义千问API（备用）

**优势**：
- 阿里云服务，稳定可靠
- 中文理解能力强
- 企业级支持

**获取步骤**：
1. 访问 https://dashscope.aliyuncs.com/
2. 使用阿里云账号登录
3. 开通灵积模型服务
4. 获取API Key
5. 复制API Key到`.env`文件中的`QWEN_API_KEY`

**定价**：约0.12元/1K tokens

### 3. 其他可选API

如果您有其他AI服务的API Key，也可以联系我们添加支持：
- 百度文心一言
- 腾讯混元
- 智谱GLM
- Moonshot AI

## 配置步骤

1. **复制环境变量文件**：
   ```bash
   cp .env.example .env
   ```

2. **编辑.env文件**：
   ```bash
   nano .env
   ```

3. **设置API Key**（至少设置一个）：
   ```env
   # Google Gemini API配置（推荐）
   GEMINI_API_KEY=your-gemini-api-key-here
   
   # DeepSeek API配置（备用）
   DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here
   
   # 通义千问API配置（备用）
   QWEN_API_KEY=your-qwen-api-key-here
   ```

4. **保存文件并启动系统**：
   ```bash
   ./start.sh
   ```

## 测试API连接

启动系统后，可以通过以下方式测试API是否正常工作：

```bash
# 测试API连接
curl -X POST http://localhost:5000/api/rag/advice \
  -H "Content-Type: application/json" \
  -d '{
    "student_data": {
      "name": "测试学生",
      "major": "计算机科学",
      "grade": "大三",
      "grades": [{"course": "CS101", "score": 85}]
    },
    "course_data": {
      "course_code": "CS5187",
      "course_name": "高级算法",
      "description": "深入学习算法设计与分析"
    }
  }'
```

## 故障排除

### 1. API Key无效
- 检查API Key是否正确复制
- 确认API Key是否已激活
- 检查账户余额是否充足

### 2. 网络连接问题
- 确认网络可以访问对应的API服务
- 检查防火墙设置
- 尝试使用代理（如需要）

### 3. 服务降级
如果所有API都无法使用，系统会自动使用内置的备用建议生成器，确保基本功能可用。

## 成本控制

为了控制API使用成本，系统已实现：
- 请求缓存机制
- 智能重试策略
- 备用方案降级
- 请求频率限制

建议设置月度预算提醒，避免意外产生高额费用。