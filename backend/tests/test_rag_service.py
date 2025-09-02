import pytest
from app.services.rag_service import RAGService

class TestRAGService:
    def setup_method(self):
        self.rag_service = RAGService()
    
    def test_assess_difficulty(self):
        """测试难度评估"""
        # 高分学生
        high_score_student = {
            'grades': [
                {'score': 90}, {'score': 88}, {'score': 92}
            ]
        }
        
        difficulty = self.rag_service._assess_difficulty(high_score_student, {})
        assert difficulty == 'easy'
        
        # 中等分数学生
        medium_score_student = {
            'grades': [
                {'score': 75}, {'score': 78}, {'score': 72}
            ]
        }
        
        difficulty = self.rag_service._assess_difficulty(medium_score_student, {})
        assert difficulty == 'medium'
        
        # 低分学生
        low_score_student = {
            'grades': [
                {'score': 60}, {'score': 65}, {'score': 58}
            ]
        }
        
        difficulty = self.rag_service._assess_difficulty(low_score_student, {})
        assert difficulty == 'hard'
    
    def test_calculate_success_probability(self):
        """测试成功概率计算"""
        student_data = {
            'grades': [
                {'score': 85}, {'score': 88}, {'score': 90}
            ]
        }
        
        probability = self.rag_service._calculate_success_probability(student_data, {})
        
        assert 0.0 <= probability <= 1.0
        assert probability >= 0.8  # 高分学生应该有较高成功概率
    
    def test_generate_study_plan(self):
        """测试学习计划生成"""
        course_data = {
            'topics': [
                'Introduction to AI',
                'Machine Learning Basics',
                'Neural Networks',
                'Deep Learning'
            ]
        }
        
        study_plan = self.rag_service._generate_study_plan({}, course_data)
        
        assert len(study_plan) == 4
        assert study_plan[0]['week'] == 1
        assert study_plan[0]['topic'] == 'Introduction to AI'
        assert 'objectives' in study_plan[0]
        assert 'activities' in study_plan[0]
    
    def test_recommend_resources(self):
        """测试资源推荐"""
        course_data = {
            'course_code': 'CS5187',
            'topics': ['Machine Learning', 'Deep Learning']
        }
        
        resources = self.rag_service._recommend_resources(course_data)
        
        assert len(resources) > 0
        assert any(r['type'] == 'textbook' for r in resources)
        assert any(r['priority'] == 'high' for r in resources)
    
    def test_is_related_course(self):
        """测试相关课程判断"""
        assert self.rag_service._is_related_course('CS3001', 'CS5187') == True
        assert self.rag_service._is_related_course('MATH2001', 'CS5187') == False
        assert self.rag_service._is_related_course('', 'CS5187') == False