#!/usr/bin/env python3
"""
RAG学习建议系统测试脚本
测试系统的基本功能，不依赖外部API
"""

import requests
import json
import time
import sys

def test_backend_health():
    """测试后端健康状态"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务正常")
            return True
        else:
            print(f"❌ 后端服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接后端服务: {e}")
        return False

def test_frontend():
    """测试前端服务"""
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务正常")
            return True
        else:
            print(f"❌ 前端服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接前端服务: {e}")
        return False

def test_student_api():
    """测试学生API"""
    try:
        # 创建测试学生
        student_data = {
            "name": "张三",
            "student_id": "2021001",
            "major": "计算机科学与技术",
            "grade": "大三",
            "email": "zhangsan@example.com"
        }
        
        response = requests.post(
            'http://localhost:5000/api/students',
            json=student_data,
            timeout=10
        )
        
        if response.status_code == 201:
            print("✅ 学生创建API正常")
            student_id = response.json().get('student_id')
            
            # 测试获取学生信息
            response = requests.get(f'http://localhost:5000/api/students/{student_id}', timeout=5)
            if response.status_code == 200:
                print("✅ 学生查询API正常")
                return True
            else:
                print(f"❌ 学生查询API异常: {response.status_code}")
                return False
        else:
            print(f"❌ 学生创建API异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 学生API测试失败: {e}")
        return False

def test_pdf_upload():
    """测试PDF上传功能"""
    try:
        # 创建测试文本文件
        test_content = """
CS5187 高级算法设计与分析

课程描述：
本课程深入探讨算法设计的高级技术和分析方法。

学习目标：
1. 掌握动态规划算法设计
2. 理解贪心算法原理
3. 学习图算法应用
4. 分析算法复杂度

主要内容：
- 动态规划
- 贪心算法
- 图论算法
- 网络流算法
- 字符串算法
"""
        
        # 模拟文件上传
        files = {'file': ('test_course.txt', test_content, 'text/plain')}
        response = requests.post(
            'http://localhost:5000/api/pdf/upload',
            files=files,
            timeout=15
        )
        
        if response.status_code == 200:
            print("✅ PDF上传API正常")
            return True
        else:
            print(f"❌ PDF上传API异常: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
    except Exception as e:
        print(f"❌ PDF上传测试失败: {e}")
        return False

def test_rag_advice():
    """测试RAG建议生成"""
    try:
        advice_data = {
            "student_data": {
                "name": "李四",
                "major": "计算机科学",
                "grade": "大三",
                "grades": [
                    {"course": "CS101", "score": 85},
                    {"course": "CS201", "score": 78},
                    {"course": "CS301", "score": 82}
                ]
            },
            "course_data": {
                "course_code": "CS5187",
                "course_name": "高级算法设计与分析",
                "description": "深入学习算法设计与分析的高级技术",
                "topics": ["动态规划", "贪心算法", "图论算法", "网络流"],
                "objectives": ["掌握高级算法设计", "提高问题解决能力"]
            }
        }
        
        response = requests.post(
            'http://localhost:5000/api/rag/advice',
            json=advice_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ RAG建议生成API正常")
            print(f"📝 生成的建议预览: {result.get('advice', '')[:100]}...")
            return True
        else:
            print(f"❌ RAG建议生成API异常: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
    except Exception as e:
        print(f"❌ RAG建议生成测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 开始测试RAG学习建议系统...")
    print("=" * 50)
    
    tests = [
        ("后端健康检查", test_backend_health),
        ("前端服务检查", test_frontend),
        ("学生管理API", test_student_api),
        ("PDF上传功能", test_pdf_upload),
        ("RAG建议生成", test_rag_advice)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 测试: {test_name}")
        try:
            if test_func():
                passed += 1
            time.sleep(1)  # 避免请求过快
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常")
        return 0
    else:
        print("⚠️  部分测试失败，请检查系统配置")
        return 1

if __name__ == "__main__":
    sys.exit(main())