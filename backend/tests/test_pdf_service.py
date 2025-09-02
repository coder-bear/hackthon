import pytest
import os
from app.services.pdf_service import PDFService

class TestPDFService:
    def setup_method(self):
        self.pdf_service = PDFService()
    
    def test_parse_course_description(self):
        """测试课程描述解析"""
        sample_text = """
        CS5187: Advanced Machine Learning
        
        Course Description:
        This course covers advanced topics in machine learning including deep learning,
        reinforcement learning, and neural networks.
        
        Learning Objectives:
        - Understand deep learning fundamentals
        - Implement neural network architectures
        - Apply reinforcement learning algorithms
        
        Topics:
        1. Neural Networks
        2. Deep Learning
        3. Reinforcement Learning
        4. Computer Vision
        
        Prerequisites:
        - CS3001: Data Structures
        - MATH2001: Linear Algebra
        
        Assessment:
        - Assignments: 40%
        - Midterm: 30%
        - Final Project: 30%
        """
        
        result = self.pdf_service.parse_course_description(sample_text)
        
        assert result['course_code'] == 'CS5187'
        assert 'Advanced Machine Learning' in result['course_name']
        assert 'machine learning' in result['description'].lower()
        assert len(result['objectives']) > 0
        assert len(result['topics']) > 0
        assert len(result['prerequisites']) > 0
        assert len(result['assessment']) > 0
    
    def test_extract_list_items(self):
        """测试列表项提取"""
        text = """
        - Item 1
        - Item 2
        • Item 3
        1. Item 4
        2. Item 5
        """
        
        items = self.pdf_service._extract_list_items(text)
        
        assert len(items) == 5
        assert 'Item 1' in items
        assert 'Item 5' in items
    
    def test_validate_pdf_file_invalid(self):
        """测试无效PDF文件验证"""
        invalid_content = b"This is not a PDF file"
        
        result = self.pdf_service.validate_pdf_file(invalid_content)
        
        assert result == False