// MongoDB初始化脚本
db = db.getSiblingDB('rag_learning_advisor');

// 创建用户
db.createUser({
  user: 'app_user',
  pwd: 'app_password',
  roles: [
    {
      role: 'readWrite',
      db: 'rag_learning_advisor'
    }
  ]
});

// 创建集合和索引
db.createCollection('students');
db.createCollection('courses');

// 学生集合索引
db.students.createIndex({ "student_id": 1 }, { unique: true });
db.students.createIndex({ "name": 1 });
db.students.createIndex({ "major": 1 });

// 课程集合索引
db.courses.createIndex({ "course_code": 1 }, { unique: true });
db.courses.createIndex({ "course_name": 1 });

// 插入示例数据
db.students.insertMany([
  {
    name: "张三",
    student_id: "2021001",
    major: "计算机科学",
    grade: "大三",
    email: "zhangsan@example.com",
    grades: [
      {
        course: "CS3001",
        score: 85,
        semester: "2023春",
        year: "2023"
      },
      {
        course: "CS3002",
        score: 78,
        semester: "2023春",
        year: "2023"
      }
    ],
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    name: "李四",
    student_id: "2021002",
    major: "软件工程",
    grade: "大三",
    email: "lisi@example.com",
    grades: [
      {
        course: "CS3001",
        score: 92,
        semester: "2023春",
        year: "2023"
      }
    ],
    created_at: new Date(),
    updated_at: new Date()
  }
]);

print('数据库初始化完成');