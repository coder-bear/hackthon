#!/usr/bin/env python3
"""
测试Gemini API连接
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_gemini_api():
    """测试Gemini API连接"""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ 未找到GEMINI_API_KEY环境变量")
            print("请在.env文件中设置GEMINI_API_KEY")
            return False
        
        # 配置API
        genai.configure(api_key=api_key)
        
        # 创建模型
        model = genai.GenerativeModel('gemini-pro')
        
        # 测试简单请求
        print("🧪 测试Gemini API连接...")
        response = model.generate_content("请用中文说'Hello, World!'")
        
        if response.text:
            print("✅ Gemini API连接成功")
            print(f"📝 测试响应: {response.text}")
            return True
        else:
            print("❌ Gemini API返回空响应")
            return False
            
    except ImportError:
        print("❌ 未安装google-generativeai包")
        print("请运行: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"❌ Gemini API测试失败: {e}")
        return False

def test_rag_service():
    """测试RAG服务的Gemini集成"""
    try:
        sys.path.append('backend')
        from app.services.rag_service import RAGService
        
        rag_service = RAGService()
        
        # 测试数据
        student_data = {
            "name": "测试学生",
            "major": "计算机科学",
            "grade": "大三",
            "grades": [
                {"course": "CS101", "score": 85},
                {"course": "CS201", "score": 78}
            ]
        }
        
        course_data = {
            "course_code": "CS5187",
            "course_name": "高级算法设计与分析",
            "description": "深入学习算法设计与分析的高级技术",
            "topics": ["动态规划", "贪心算法", "图论算法"],
            "objectives": ["掌握高级算法设计", "提高问题解决能力"]
        }
        
        print("🧪 测试RAG服务...")
        result = rag_service.generate_learning_advice(student_data, course_data)
        
        if result and 'advice' in result:
            print("✅ RAG服务测试成功")
            print(f"📝 生成的建议预览: {result['advice'][:100]}...")
            return True
        else:
            print("❌ RAG服务测试失败")
            return False
            
    except Exception as e:
        print(f"❌ RAG服务测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 测试Gemini API集成...")
    print("=" * 50)
    
    tests = [
        ("Gemini API连接", test_gemini_api),
        ("RAG服务集成", test_rag_service)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 测试: {test_name}")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 Gemini API集成测试通过！")
        return 0
    else:
        print("⚠️  部分测试失败，请检查配置")
        return 1

if __name__ == "__main__":
    sys.exit(main())