from datetime import datetime
from bson import ObjectId

class Course:
    def __init__(self, db):
        self.collection = db.courses
    
    def create_course(self, course_data):
        """创建新课程"""
        course_data['created_at'] = datetime.utcnow()
        course_data['updated_at'] = datetime.utcnow()
        result = self.collection.insert_one(course_data)
        return str(result.inserted_id)
    
    def get_course(self, course_id):
        """获取课程信息"""
        try:
            course = self.collection.find_one({'_id': ObjectId(course_id)})
            if course:
                course['_id'] = str(course['_id'])
            return course
        except:
            return None
    
    def get_course_by_code(self, course_code):
        """根据课程代码获取课程"""
        course = self.collection.find_one({'course_code': course_code})
        if course:
            course['_id'] = str(course['_id'])
        return course
    
    def get_all_courses(self):
        """获取所有课程"""
        courses = list(self.collection.find())
        for course in courses:
            course['_id'] = str(course['_id'])
        return courses
    
    def update_course(self, course_id, update_data):
        """更新课程信息"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {'_id': ObjectId(course_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    def delete_course(self, course_id):
        """删除课程"""
        try:
            result = self.collection.delete_one({'_id': ObjectId(course_id)})
            return result.deleted_count > 0
        except:
            return False