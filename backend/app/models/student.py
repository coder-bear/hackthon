from datetime import datetime
from bson import ObjectId

class Student:
    def __init__(self, db):
        self.collection = db.students
    
    def create_student(self, student_data):
        """创建新学生"""
        student_data['created_at'] = datetime.utcnow()
        student_data['updated_at'] = datetime.utcnow()
        result = self.collection.insert_one(student_data)
        return str(result.inserted_id)
    
    def get_student(self, student_id):
        """获取学生信息"""
        try:
            student = self.collection.find_one({'_id': ObjectId(student_id)})
            if student:
                student['_id'] = str(student['_id'])
            return student
        except:
            return None
    
    def get_all_students(self):
        """获取所有学生"""
        students = list(self.collection.find())
        for student in students:
            student['_id'] = str(student['_id'])
        return students
    
    def update_student(self, student_id, update_data):
        """更新学生信息"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {'_id': ObjectId(student_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    def delete_student(self, student_id):
        """删除学生"""
        try:
            result = self.collection.delete_one({'_id': ObjectId(student_id)})
            return result.deleted_count > 0
        except:
            return False
    
    def add_grade(self, student_id, grade_data):
        """添加成绩记录"""
        try:
            grade_data['timestamp'] = datetime.utcnow()
            result = self.collection.update_one(
                {'_id': ObjectId(student_id)},
                {'$push': {'grades': grade_data}}
            )
            return result.modified_count > 0
        except:
            return False