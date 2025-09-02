# Google Gemini API 配置指南

## 1. 获取Gemini API Key

### 步骤1：访问Google AI Studio
1. 打开浏览器，访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 使用Google账号登录

### 步骤2：创建API Key
1. 点击 "Create API Key" 按钮
2. 选择一个Google Cloud项目（如果没有会自动创建）
3. 复制生成的API Key

### 步骤3：配置环境变量
1. 在项目根目录找到 `.env` 文件
2. 添加或修改以下配置：
   ```
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

## 2. API使用限制

### 免费额度
- 每分钟15个请求
- 每天1500个请求
- 每个请求最多32K tokens

### 付费计划
- 如需更高配额，可以在Google Cloud Console中启用计费

## 3. 支持的模型

- **gemini-pro**: 文本生成（当前使用）
- **gemini-pro-vision**: 支持图像输入
- **gemini-ultra**: 更强大的模型（需要申请访问）

## 4. 安全注意事项

1. **保护API Key**：
   - 不要将API Key提交到版本控制系统
   - 不要在客户端代码中暴露API Key
   - 定期轮换API Key

2. **使用环境变量**：
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

## 5. 故障排除

### 常见错误

1. **API Key无效**
   ```
   Error: Invalid API key
   ```
   解决方案：检查API Key是否正确复制

2. **配额超限**
   ```
   Error: Quota exceeded
   ```
   解决方案：等待配额重置或升级到付费计划

3. **网络连接问题**
   ```
   Error: Connection timeout
   ```
   解决方案：检查网络连接，可能需要使用代理

### 测试API连接

运行以下命令测试API是否正常工作：

```bash
python -c "
import google.generativeai as genai
import os
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Hello, world!')
print(response.text)
"
```

## 6. 最佳实践

1. **错误处理**：始终包含适当的错误处理
2. **重试机制**：实现指数退避重试
3. **缓存响应**：对相似请求进行缓存
4. **监控使用量**：定期检查API使用情况

## 7. 相关链接

- [Google AI Studio](https://makersuite.google.com/)
- [Gemini API文档](https://ai.google.dev/docs)
- [Python SDK文档](https://ai.google.dev/tutorials/python_quickstart)