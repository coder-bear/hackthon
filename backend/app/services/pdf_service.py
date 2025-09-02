import PyPDF2
import os
from io import BytesIO
import re
from typing import Dict, List

class PDFService:
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def extract_text_from_pdf(self, file_content: bytes) -> str:
        """从PDF文件中提取文本"""
        try:
            pdf_file = BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"PDF解析失败: {str(e)}")
    
    def parse_course_description(self, text: str) -> Dict:
        """解析课程描述文本，提取关键信息"""
        course_info = {
            'course_code': '',
            'course_name': '',
            'description': '',
            'objectives': [],
            'topics': [],
            'prerequisites': [],
            'assessment': [],
            'textbooks': []
        }
        
        # 提取课程代码和名称
        course_pattern = r'([A-Z]{2,4}\d{4})\s*[-:]?\s*(.+?)(?:\n|$)'
        course_match = re.search(course_pattern, text, re.IGNORECASE)
        if course_match:
            course_info['course_code'] = course_match.group(1).upper()
            course_info['course_name'] = course_match.group(2).strip()
        
        # 提取课程描述
        desc_patterns = [
            r'(?:Course\s+Description|Description)[:\s]*\n?(.*?)(?=\n\s*(?:[A-Z][a-z]+\s*[:\n]|$))',
            r'(?:课程描述|描述)[：:\s]*\n?(.*?)(?=\n\s*(?:[A-Z][a-z]+\s*[:\n]|$))'
        ]
        for pattern in desc_patterns:
            desc_match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if desc_match:
                course_info['description'] = desc_match.group(1).strip()
                break
        
        # 提取学习目标
        obj_patterns = [
            r'(?:Learning\s+Objectives?|Objectives?)[:\s]*\n?(.*?)(?=\n\s*(?:[A-Z][a-z]+\s*[:\n]|$))',
            r'(?:学习目标|目标)[：:\s]*\n?(.*?)(?=\n\s*(?:[A-Z][a-z]+\s*[:\n]|$))'
        ]
        for pattern in obj_patterns:
            obj_match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if obj_match:
                objectives_text = obj_match.group(1).strip()
                course_info['objectives'] = self._extract_list_items(objectives_text)
                break
        
        # 提取课程主题
        topic_patterns = [
            r'(?:Topics?|Syllabus|Content)[:\s]*\n?(.*?)(?=\n\s*(?:[A-Z][a-z]+\s*[:\n]|$))',
            r'(?:主题|大纲|内容)[：:\s]*\n?(.*?)(?=\n\s*(?:[A-Z][a-z]+\s*[:\n]|$))'
        ]
        for pattern in topic_patterns:
            topic_match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if topic_match:
                topics_text = topic_match.group(1).strip()
                course_info['topics'] = self._extract_list_items(topics_text)
                break
        
        # 提取先修课程
        prereq_patterns = [
            r'(?:Prerequisites?|Pre-requisites?)[:\s]*\n?(.*?)(?=\n\s*(?:[A-Z][a-z]+\s*[:\n]|$))',
            r'(?:先修课程|前置课程)[：:\s]*\n?(.*?)(?=\n\s*(?:[A-Z][a-z]+\s*[:\n]|$))'
        ]
        for pattern in prereq_patterns:
            prereq_match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if prereq_match:
                prereq_text = prereq_match.group(1).strip()
                course_info['prerequisites'] = self._extract_list_items(prereq_text)
                break
        
        # 提取评估方式
        assess_patterns = [
            r'(?:Assessment|Evaluation|Grading)[:\s]*\n?(.*?)(?=\n\s*(?:[A-Z][a-z]+\s*[:\n]|$))',
            r'(?:评估|考核|成绩评定)[：:\s]*\n?(.*?)(?=\n\s*(?:[A-Z][a-z]+\s*[:\n]|$))'
        ]
        for pattern in assess_patterns:
            assess_match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if assess_match:
                assess_text = assess_match.group(1).strip()
                course_info['assessment'] = self._extract_list_items(assess_text)
                break
        
        return course_info
    
    def _extract_list_items(self, text: str) -> List[str]:
        """从文本中提取列表项"""
        if not text:
            return []
        
        # 按行分割并清理
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        items = []
        for line in lines:
            # 移除列表标记
            cleaned_line = re.sub(r'^[-•*]\s*', '', line)
            cleaned_line = re.sub(r'^\d+\.\s*', '', cleaned_line)
            
            if cleaned_line and len(cleaned_line) > 3:
                items.append(cleaned_line)
        
        return items[:10]  # 限制最多10个项目
    
    def validate_pdf_file(self, file_content: bytes) -> bool:
        """验证PDF文件格式"""
        try:
            pdf_file = BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            return len(pdf_reader.pages) > 0
        except:
            return False