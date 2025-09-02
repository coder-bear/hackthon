import requests
import os
from typing import List, Dict, Any
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import logging
import google.generativeai as genai

class RAGService:
    def __init__(self):
        # Gemini API配置（主要）
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
        
        # 备用API配置
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.deepseek_base_url = "https://api.deepseek.com/v1"
        self.qwen_api_key = os.getenv('QWEN_API_KEY')
        self.qwen_base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        print(f"RAG服务初始化完成，使用Gemini API")
    
    def generate_learning_advice(self, student_data: Dict, course_data: Dict) -> Dict:
        """生成个性化学习建议"""
        try:
            # 构建上下文信息
            context = self._build_context(student_data, course_data)
            
            # 生成学习建议
            advice = self._generate_advice_with_llm(context)
            
            # 生成学习计划
            study_plan = self._generate_study_plan(student_data, course_data)
            
            # 推荐资源
            resources = self._recommend_resources(course_data)
            
            return {
                'advice': advice,
                'study_plan': study_plan,
                'recommended_resources': resources,
                'difficulty_assessment': self._assess_difficulty(student_data, course_data),
                'estimated_study_time': self._estimate_study_time(course_data),
                'success_probability': self._calculate_success_probability(student_data, course_data)
            }
        except Exception as e:
            logging.error(f"生成学习建议时出错: {str(e)}")
            return {
                'error': f'生成学习建议时出错: {str(e)}',
                'advice': '暂时无法生成个性化建议，请稍后重试。',
                'study_plan': [],
                'recommended_resources': [],
                'difficulty_assessment': 'medium',
                'estimated_study_time': '未知',
                'success_probability': 0.5
            }
    
    def _build_context(self, student_data: Dict, course_data: Dict) -> str:
        """构建RAG上下文"""
        context_parts = []
        
        # 学生信息
        context_parts.append(f"学生姓名: {student_data.get('name', '未知')}")
        context_parts.append(f"专业: {student_data.get('major', '未知')}")
        context_parts.append(f"年级: {student_data.get('grade', '未知')}")
        
        # 历史成绩分析
        grades = student_data.get('grades', [])
        if grades:
            avg_grade = sum([g.get('score', 0) for g in grades]) / len(grades)
            context_parts.append(f"平均成绩: {avg_grade:.2f}")
            
            # 相关课程成绩
            related_grades = [g for g in grades if self._is_related_course(g.get('course', ''), course_data.get('course_code', ''))]
            if related_grades:
                related_avg = sum([g.get('score', 0) for g in related_grades]) / len(related_grades)
                context_parts.append(f"相关课程平均成绩: {related_avg:.2f}")
        
        # 课程信息
        context_parts.append(f"\n课程代码: {course_data.get('course_code', '')}")
        context_parts.append(f"课程名称: {course_data.get('course_name', '')}")
        context_parts.append(f"课程描述: {course_data.get('description', '')}")
        
        if course_data.get('objectives'):
            context_parts.append(f"学习目标: {'; '.join(course_data['objectives'])}")
        
        if course_data.get('topics'):
            context_parts.append(f"主要主题: {'; '.join(course_data['topics'][:5])}")
        
        if course_data.get('prerequisites'):
            context_parts.append(f"先修课程: {'; '.join(course_data['prerequisites'])}")
        
        return '\n'.join(context_parts)
    
    def _generate_advice_with_llm(self, context: str) -> str:
        """使用LLM生成学习建议"""
        # 首先尝试Gemini API
        advice = self._try_gemini_api(context)
        if advice:
            return advice
            
        # 如果Gemini失败，尝试DeepSeek API
        advice = self._try_deepseek_api(context)
        if advice:
            return advice
            
        # 如果DeepSeek失败，尝试通义千问
        advice = self._try_qwen_api(context)
        if advice:
            return advice
            
        # 如果都失败，返回备用建议
        return self._generate_fallback_advice(context)
    
    def _try_gemini_api(self, context: str) -> str:
        """尝试使用Gemini API"""
        if not self.gemini_api_key:
            return None
            
        try:
            prompt = f"""
基于以下学生和课程信息，请生成个性化的学习建议：

{context}

请提供具体、实用的学习建议，包括：
1. 学习重点和难点分析
2. 学习方法建议
3. 时间安排建议
4. 注意事项

请用中文回答，建议要具体且可操作。
"""
            
            response = self.gemini_model.generate_content(prompt)
            
            if response.text:
                return response.text
            else:
                logging.error("Gemini API返回空响应")
                return None
                
        except Exception as e:
            logging.error(f"Gemini API调用失败: {e}")
            return None
    
    def _try_deepseek_api(self, context: str) -> str:
        """尝试使用DeepSeek API"""
        if not self.deepseek_api_key:
            return None
            
        try:
            prompt = f"""
基于以下学生和课程信息，请生成个性化的学习建议：

{context}

请提供具体、实用的学习建议，包括：
1. 学习重点和难点分析
2. 学习方法建议
3. 时间安排建议
4. 注意事项

请用中文回答，建议要具体且可操作。
"""
            
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "你是一位经验丰富的学术顾问，专门为学生提供个性化的学习建议。请用中文回答。"},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 800,
                "temperature": 0.7,
                "stream": False
            }
            
            response = requests.post(
                f"{self.deepseek_base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                logging.error(f"DeepSeek API错误: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logging.error(f"DeepSeek API调用失败: {e}")
            return None
    
    def _try_qwen_api(self, context: str) -> str:
        """尝试使用通义千问API"""
        if not self.qwen_api_key:
            return None
            
        try:
            prompt = f"""
基于以下学生和课程信息，请生成个性化的学习建议：

{context}

请提供具体、实用的学习建议，包括：
1. 学习重点和难点分析
2. 学习方法建议
3. 时间安排建议
4. 注意事项

请用中文回答，建议要具体且可操作。
"""
            
            headers = {
                "Authorization": f"Bearer {self.qwen_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "qwen-turbo",
                "input": {
                    "messages": [
                        {"role": "system", "content": "你是一位经验丰富的学术顾问，专门为学生提供个性化的学习建议。"},
                        {"role": "user", "content": prompt}
                    ]
                },
                "parameters": {
                    "max_tokens": 800,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(
                self.qwen_base_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['output']['text']
            else:
                logging.error(f"通义千问API错误: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logging.error(f"通义千问API调用失败: {e}")
            return None
    
    def _generate_fallback_advice(self, context: str) -> str:
        """生成备用学习建议"""
        return """
基于您的学习背景和课程特点，建议您：

1. **学习重点**：
   - 重点关注课程的核心概念和基础理论
   - 多做练习题巩固理解
   - 定期复习已学内容

2. **学习方法**：
   - 制定详细的学习计划
   - 采用主动学习策略
   - 寻求同学和老师的帮助

3. **时间安排**：
   - 每周安排固定的学习时间
   - 合理分配理论学习和实践练习的时间
   - 留出充足的复习时间

4. **注意事项**：
   - 保持学习的连续性
   - 及时解决学习中的疑问
   - 注意劳逸结合，保持良好的学习状态
"""
    
    def _generate_study_plan(self, student_data: Dict, course_data: Dict) -> List[Dict]:
        """生成学习计划"""
        topics = course_data.get('topics', [])
        if not topics:
            return []
        
        study_plan = []
        weeks = min(len(topics), 12)  # 最多12周的计划
        
        for i, topic in enumerate(topics[:weeks]):
            week_plan = {
                'week': i + 1,
                'topic': topic,
                'objectives': [f"理解{topic}的基本概念", f"掌握{topic}的应用方法"],
                'activities': [
                    "阅读相关教材章节",
                    "完成课后练习",
                    "参与课堂讨论"
                ],
                'estimated_hours': 8
            }
            study_plan.append(week_plan)
        
        return study_plan
    
    def _recommend_resources(self, course_data: Dict) -> List[Dict]:
        """推荐学习资源"""
        resources = []
        
        # 基于课程主题推荐资源
        topics = course_data.get('topics', [])
        course_code = course_data.get('course_code', '')
        
        # 通用资源
        resources.extend([
            {
                'type': 'textbook',
                'title': '课程官方教材',
                'description': '按照课程大纲推荐的主要教材',
                'priority': 'high'
            },
            {
                'type': 'online_course',
                'title': 'B站相关课程',
                'description': '在线学习平台的补充课程',
                'priority': 'medium'
            },
            {
                'type': 'practice',
                'title': '练习题库',
                'description': '相关的练习题和模拟考试',
                'priority': 'high'
            }
        ])
        
        # 基于课程代码的特定资源
        if course_code.startswith('CS'):
            resources.extend([
                {
                    'type': 'platform',
                    'title': 'LeetCode',
                    'description': '编程练习平台',
                    'priority': 'high'
                },
                {
                    'type': 'documentation',
                    'title': '官方文档',
                    'description': '相关技术的官方文档',
                    'priority': 'medium'
                }
            ])
        
        return resources[:6]  # 限制推荐数量
    
    def _assess_difficulty(self, student_data: Dict, course_data: Dict) -> str:
        """评估课程难度"""
        grades = student_data.get('grades', [])
        if not grades:
            return 'medium'
        
        avg_grade = sum([g.get('score', 0) for g in grades]) / len(grades)
        
        # 基于历史成绩评估难度
        if avg_grade >= 85:
            return 'easy'
        elif avg_grade >= 70:
            return 'medium'
        else:
            return 'hard'
    
    def _estimate_study_time(self, course_data: Dict) -> str:
        """估算学习时间"""
        topics_count = len(course_data.get('topics', []))
        
        if topics_count <= 5:
            return '每周6-8小时'
        elif topics_count <= 10:
            return '每周8-12小时'
        else:
            return '每周12-15小时'
    
    def _calculate_success_probability(self, student_data: Dict, course_data: Dict) -> float:
        """计算成功概率"""
        grades = student_data.get('grades', [])
        if not grades:
            return 0.7  # 默认概率
        
        avg_grade = sum([g.get('score', 0) for g in grades]) / len(grades)
        
        # 简单的概率计算
        if avg_grade >= 85:
            return 0.9
        elif avg_grade >= 75:
            return 0.8
        elif avg_grade >= 65:
            return 0.7
        else:
            return 0.6
    
    def _is_related_course(self, course1: str, course2: str) -> bool:
        """判断两个课程是否相关"""
        if not course1 or not course2:
            return False
        
        # 简单的相关性判断：相同的课程前缀
        prefix1 = course1[:2] if len(course1) >= 2 else ''
        prefix2 = course2[:2] if len(course2) >= 2 else ''
        
        return prefix1 == prefix2