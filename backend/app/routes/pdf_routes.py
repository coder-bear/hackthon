from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.services.pdf_service import PDFService
from app.models.course import Course
import os

pdf_bp = Blueprint('pdf', __name__)
pdf_service = PDFService()

@pdf_bp.route('/upload', methods=['POST'])
def upload_pdf():
    """上传并解析PDF文件"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': '只支持PDF文件'}), 400
        
        # 读取文件内容
        file_content = file.read()
        
        # 验证PDF文件
        if not pdf_service.validate_pdf_file(file_content):
            return jsonify({'error': 'PDF文件格式无效'}), 400
        
        # 提取文本
        text = pdf_service.extract_text_from_pdf(file_content)
        
        # 解析课程信息
        course_info = pdf_service.parse_course_description(text)
        
        # 保存到数据库
        course_model = Course(current_app.db)
        
        # 检查课程是否已存在
        existing_course = course_model.get_course_by_code(course_info['course_code'])
        if existing_course:
            # 更新现有课程
            course_id = existing_course['_id']
            course_model.update_course(course_id, course_info)
        else:
            # 创建新课程
            course_id = course_model.create_course(course_info)
        
        return jsonify({
            'message': 'PDF解析成功',
            'course_id': course_id,
            'course_info': course_info
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pdf_bp.route('/extract-text', methods=['POST'])
def extract_text():
    """仅提取PDF文本内容"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        file = request.files['file']
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': '只支持PDF文件'}), 400
        
        file_content = file.read()
        text = pdf_service.extract_text_from_pdf(file_content)
        
        return jsonify({
            'text': text,
            'filename': secure_filename(file.filename)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pdf_bp.route('/parse-course', methods=['POST'])
def parse_course():
    """解析课程描述文本"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': '缺少文本内容'}), 400
        
        text = data['text']
        course_info = pdf_service.parse_course_description(text)
        
        return jsonify({
            'course_info': course_info
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500