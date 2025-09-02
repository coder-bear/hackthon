from flask import Blueprint, request, jsonify, current_app
from app.models.student import Student
from bson import ObjectId

student_bp = Blueprint('students', __name__)

@student_bp.route('/', methods=['GET'])
def get_all_students():
    """获取所有学生"""
    try:
        student_model = Student(current_app.db)
        students = student_model.get_all_students()
        return jsonify({'students': students}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_bp.route('/', methods=['POST'])
def create_student():
    """创建新学生"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '缺少学生数据'}), 400
        
        required_fields = ['name', 'student_id', 'major']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必填字段: {field}'}), 400
        
        student_model = Student(current_app.db)
        
        # 检查学号是否已存在
        existing_student = current_app.db.students.find_one({'student_id': data['student_id']})
        if existing_student:
            return jsonify({'error': '学号已存在'}), 400
        
        # 初始化学生数据
        student_data = {
            'name': data['name'],
            'student_id': data['student_id'],
            'major': data['major'],
            'grade': data.get('grade', ''),
            'email': data.get('email', ''),
            'phone': data.get('phone', ''),
            'grades': data.get('grades', [])
        }
        
        student_id = student_model.create_student(student_data)
        return jsonify({
            'message': '学生创建成功',
            'student_id': student_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_bp.route('/<student_id>', methods=['GET'])
def get_student(student_id):
    """获取单个学生信息"""
    try:
        student_model = Student(current_app.db)
        student = student_model.get_student(student_id)
        
        if not student:
            return jsonify({'error': '学生不存在'}), 404
        
        return jsonify({'student': student}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_bp.route('/<student_id>/grades', methods=['POST'])
def add_grade(student_id):
    """添加成绩记录"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '缺少成绩数据'}), 400
        
        required_fields = ['course', 'score']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必填字段: {field}'}), 400
        
        grade_data = {
            'course': data['course'],
            'score': data['score'],
            'semester': data.get('semester', ''),
            'year': data.get('year', '')
        }
        
        student_model = Student(current_app.db)
        success = student_model.add_grade(student_id, grade_data)
        
        if success:
            return jsonify({'message': '成绩添加成功'}), 201
        else:
            return jsonify({'error': '添加成绩失败'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500