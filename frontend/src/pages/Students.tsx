import React, { useState, useEffect } from 'react';
import { getStudents, deleteStudent, addGrade } from '../services/api';

interface Student {
  _id: string;
  name: string;
  student_id: string;
  major: string;
  grade: string;
  email: string;
  grades: Array<{
    course: string;
    score: number;
    semester: string;
    year: string;
  }>;
}

const Students: React.FC = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedStudent, setSelectedStudent] = useState<Student | null>(null);
  const [showGradeForm, setShowGradeForm] = useState(false);
  const [gradeForm, setGradeForm] = useState({
    course: '',
    score: '',
    semester: '',
    year: ''
  });

  useEffect(() => {
    loadStudents();
  }, []);

  const loadStudents = async () => {
    try {
      const response = await getStudents();
      setStudents(response.data.students || []);
    } catch (error) {
      console.error('加载学生数据失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteStudent = async (studentId: string) => {
    if (window.confirm('确定要删除这个学生吗？')) {
      try {
        await deleteStudent(studentId);
        setStudents(students.filter(s => s._id !== studentId));
      } catch (error) {
        alert('删除失败');
      }
    }
  };

  const handleAddGrade = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedStudent) return;

    try {
      await addGrade(selectedStudent._id, {
        ...gradeForm,
        score: parseFloat(gradeForm.score)
      });
      
      // 重新加载学生数据
      await loadStudents();
      
      // 重置表单
      setGradeForm({ course: '', score: '', semester: '', year: '' });
      setShowGradeForm(false);
      alert('成绩添加成功');
    } catch (error) {
      alert('添加成绩失败');
    }
  };

  const calculateAverage = (grades: any[]) => {
    if (grades.length === 0) return 0;
    const sum = grades.reduce((acc, grade) => acc + grade.score, 0);
    return (sum / grades.length).toFixed(2);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg">加载中...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">学生管理</h1>
        <div className="text-sm text-gray-600">
          共 {students.length} 名学生
        </div>
      </div>

      <div className="grid gap-6">
        {students.map((student) => (
          <div key={student._id} className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold">{student.name}</h3>
                <p className="text-gray-600">学号: {student.student_id}</p>
                <p className="text-gray-600">专业: {student.major}</p>
                {student.grade && <p className="text-gray-600">年级: {student.grade}</p>}
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => {
                    setSelectedStudent(student);
                    setShowGradeForm(true);
                  }}
                  className="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
                >
                  添加成绩
                </button>
                <button
                  onClick={() => handleDeleteStudent(student._id)}
                  className="bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600"
                >
                  删除
                </button>
              </div>
            </div>

            {student.grades && student.grades.length > 0 && (
              <div>
                <div className="flex justify-between items-center mb-2">
                  <h4 className="font-medium">成绩记录</h4>
                  <span className="text-sm text-gray-600">
                    平均分: {calculateAverage(student.grades)}
                  </span>
                </div>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-2">
                  {student.grades.map((grade, index) => (
                    <div key={index} className="bg-gray-50 p-2 rounded text-sm">
                      <div className="font-medium">{grade.course}</div>
                      <div className="text-gray-600">
                        分数: {grade.score} | {grade.semester} {grade.year}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {students.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-500 text-lg">暂无学生数据</div>
          <p className="text-gray-400 mt-2">请先在首页添加学生信息</p>
        </div>
      )}

      {/* 添加成绩模态框 */}
      {showGradeForm && selectedStudent && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg w-96">
            <h3 className="text-lg font-semibold mb-4">
              为 {selectedStudent.name} 添加成绩
            </h3>
            <form onSubmit={handleAddGrade} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  课程代码
                </label>
                <input
                  type="text"
                  value={gradeForm.course}
                  onChange={(e) => setGradeForm({...gradeForm, course: e.target.value})}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="如: CS5187"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  分数
                </label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={gradeForm.score}
                  onChange={(e) => setGradeForm({...gradeForm, score: e.target.value})}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="0-100"
                />
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    学期
                  </label>
                  <select
                    value={gradeForm.semester}
                    onChange={(e) => setGradeForm({...gradeForm, semester: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">选择学期</option>
                    <option value="春季">春季</option>
                    <option value="夏季">夏季</option>
                    <option value="秋季">秋季</option>
                    <option value="冬季">冬季</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    年份
                  </label>
                  <input
                    type="number"
                    min="2020"
                    max="2030"
                    value={gradeForm.year}
                    onChange={(e) => setGradeForm({...gradeForm, year: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="2024"
                  />
                </div>
              </div>
              <div className="flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setShowGradeForm(false)}
                  className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
                >
                  取消
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                >
                  添加
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Students;