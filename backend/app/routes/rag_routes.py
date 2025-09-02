from flask import Blueprint, request, jsonify, current_app
from app.services.rag_service import RAGService
from app.models.student import Student
from app.models.course import Course

rag_bp = Blueprint('rag', __name__)
rag_service = RAGService()

@rag_bp.route('/advice', methods=['POST'])
def generate_advice():
    """生成个性化学习建议"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '缺少请求数据'}), 400
        
        student_id = data.get('student_id')
        course_id = data.get('course_id')
        
        if not student_id or not course_id:
            return jsonify({'error': '缺少学生ID或课程ID'}), 400
        
        # 获取学生数据
        student_model = Student(current_app.db)
        student_data = student_model.get_student(student_id)
        if not student_data:
            return jsonify({'error': '学生不存在'}), 404
        
        # 获取课程数据
        course_model = Course(current_app.db)
        course_data = course_model.get_course(course_id)
        if not course_data:
            return jsonify({'error': '课程不存在'}), 404
        
        # 生成学习建议
        advice_result = rag_service.generate_learning_advice(student_data, course_data)
        
        return jsonify({
            'student_name': student_data['name'],
            'course_name': course_data.get('course_name', ''),
            'advice_result': advice_result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rag_bp.route('/courses', methods=['GET'])
def get_all_courses():
    """获取所有课程"""
    try:
        course_model = Course(current_app.db)
        courses = course_model.get_all_courses()
        return jsonify({'courses': courses}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rag_bp.route('/courses/<course_id>', methods=['GET'])
def get_course(course_id):
    """获取单个课程信息"""
    try:
        course_model = Course(current_app.db)
        course = course_model.get_course(course_id)
        
        if not course:
            return jsonify({'error': '课程不存在'}), 404
        
        return jsonify({'course': course}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rag_bp.route('/analyze-performance', methods=['POST'])
def analyze_performance():
    """分析学生学习表现"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        
        if not student_id:
            return jsonify({'error': '缺少学生ID'}), 400
        
        student_model = Student(current_app.db)
        student_data = student_model.get_student(student_id)
        
        if not student_data:
            return jsonify({'error': '学生不存在'}), 404
        
        grades = student_data.get('grades', [])
        if not grades:
            return jsonify({
                'analysis': {
                    'average_score': 0,
                    'total_courses': 0,
                    'performance_trend': 'insufficient_data',
                    'recommendations': ['需要更多成绩数据进行分析']
                }
            }), 200
        
        # 计算平均分
        total_score = sum([g.get('score', 0) for g in grades])
        average_score = total_score / len(grades)
        
        # 分析表现趋势
        recent_grades = grades[-3:] if len(grades) >= 3 else grades
        recent_avg = sum([g.get('score', 0) for g in recent_grades]) / len(recent_grades)
        
        if recent_avg > average_score + 5:
            trend = 'improving'
        elif recent_avg < average_score - 5:
            trend = 'declining'
        else:
            trend = 'stable'
        
        # 生成建议
        recommendations = []
        if average_score < 70:
            recommendations.append('建议加强基础知识学习')
            recommendations.append('寻求老师或同学的帮助')
        elif average_score < 85:
            recommendations.append('继续保持学习状态')
            recommendations.append('可以尝试更有挑战性的内容')
        else:
            recommendations.append('学习表现优秀，继续保持')
            recommendations.append('可以考虑帮助其他同学')
        
        analysis = {
            'average_score': round(average_score, 2),
            'total_courses': len(grades),
            'performance_trend': trend,
            'recent_average': round(recent_avg, 2),
            'recommendations': recommendations
        }
        
        return jsonify({'analysis': analysis}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500