#!/usr/bin/env python3
"""
测试脚本：模拟PDF上传和系统功能测试
"""

import requests
import json
import time

API_BASE = "http://localhost:5000"

def test_health():
    """测试健康检查"""
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ 后端服务健康检查通过")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到后端服务: {e}")
        return False

def test_create_student():
    """测试创建学生"""
    student_data = {
        "name": "张三",
        "student_id": "2021001",
        "major": "计算机科学",
        "grade": "大三",
        "email": "zhangsan@example.com"
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/students/", json=student_data)
        if response.status_code == 201:
            result = response.json()
            print(f"✅ 学生创建成功: {result['student_id']}")
            return result['student_id']
        else:
            print(f"❌ 学生创建失败: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 创建学生时出错: {e}")
        return None

def test_add_grade(student_id):
    """测试添加成绩"""
    grade_data = {
        "course": "CS3001",
        "score": 85,
        "semester": "2023春",
        "year": "2023"
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/students/{student_id}/grades", json=grade_data)
        if response.status_code == 201:
            print("✅ 成绩添加成功")
            return True
        else:
            print(f"❌ 成绩添加失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 添加成绩时出错: {e}")
        return False

def test_parse_course():
    """测试课程解析"""
    with open('data/sample_pdfs/CS5187_sample.txt', 'r', encoding='utf-8') as f:
        course_text = f.read()
    
    try:
        response = requests.post(f"{API_BASE}/api/pdf/parse-course", json={"text": course_text})
        if response.status_code == 200:
            result = response.json()
            print("✅ 课程解析成功")
            print(f"   课程代码: {result['course_info']['course_code']}")
            print(f"   课程名称: {result['course_info']['course_name']}")
            return result['course_info']
        else:
            print(f"❌ 课程解析失败: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 解析课程时出错: {e}")
        return None

def main():
    print("🧪 开始系统功能测试...")
    print()
    
    # 1. 健康检查
    if not test_health():
        print("请确保后端服务正在运行")
        return
    
    print()
    
    # 2. 创建学生
    print("📝 测试学生创建...")
    student_id = test_create_student()
    if not student_id:
        return
    
    print()
    
    # 3. 添加成绩
    print("📊 测试成绩添加...")
    test_add_grade(student_id)
    
    print()
    
    # 4. 解析课程
    print("📚 测试课程解析...")
    course_info = test_parse_course()
    
    print()
    print("🎉 基础功能测试完成！")
    print()
    print("💡 接下来您可以：")
    print("   1. 访问 http://localhost:3000 使用Web界面")
    print("   2. 在界面中生成学习建议")
    print("   3. 查看学习分析报告")

if __name__ == "__main__":
    main()