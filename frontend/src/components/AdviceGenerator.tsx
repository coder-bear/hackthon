import React, { useState, useEffect } from 'react';
import { getStudents, getCourses, generateAdvice } from '../services/api';

interface Student {
  _id: string;
  name: string;
  student_id: string;
  major: string;
}

interface Course {
  _id: string;
  course_code: string;
  course_name: string;
}

const AdviceGenerator: React.FC = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedStudent, setSelectedStudent] = useState('');
  const [selectedCourse, setSelectedCourse] = useState('');
  const [loading, setLoading] = useState(false);
  const [advice, setAdvice] = useState<any>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [studentsRes, coursesRes] = await Promise.all([
        getStudents(),
        getCourses()
      ]);
      setStudents(studentsRes.data.students || []);
      setCourses(coursesRes.data.courses || []);
    } catch (err) {
      setError('加载数据失败');
    }
  };

  const handleGenerateAdvice = async () => {
    if (!selectedStudent || !selectedCourse) {
      setError('请选择学生和课程');
      return;
    }

    setLoading(true);
    setError('');
    setAdvice(null);

    try {
      const response = await generateAdvice(selectedStudent, selectedCourse);
      setAdvice(response.data);
    } catch (err: any) {
      setError(err.response?.data?.error || '生成建议失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold mb-4">生成学习建议</h2>
        <p className="text-gray-600 mb-4">
          选择学生和课程，系统将基于RAG技术生成个性化学习建议
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="student" className="block text-sm font-medium text-gray-700 mb-1">
            选择学生
          </label>
          <select
            id="student"
            value={selectedStudent}
            onChange={(e) => setSelectedStudent(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">请选择学生</option>
            {students.map((student) => (
              <option key={student._id} value={student._id}>
                {student.name} ({student.student_id}) - {student.major}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="course" className="block text-sm font-medium text-gray-700 mb-1">
            选择课程
          </label>
          <select
            id="course"
            value={selectedCourse}
            onChange={(e) => setSelectedCourse(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">请选择课程</option>
            {courses.map((course) => (
              <option key={course._id} value={course._id}>
                {course.course_code} - {course.course_name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="flex justify-center">
        <button
          onClick={handleGenerateAdvice}
          disabled={loading || !selectedStudent || !selectedCourse}
          className="bg-green-500 text-white px-8 py-3 rounded-md hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors text-lg font-medium"
        >
          {loading ? '生成中...' : '🚀 生成学习建议'}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-red-600">{error}</p>
        </div>
      )}

      {advice && (
        <div className="bg-white border rounded-lg p-6 space-y-6">
          <div className="border-b pb-4">
            <h3 className="text-xl font-semibold text-gray-900">
              📚 {advice.student_name} - {advice.course_name}
            </h3>
          </div>

          {/* 学习建议 */}
          <div>
            <h4 className="text-lg font-semibold mb-3 text-blue-700">💡 个性化学习建议</h4>
            <div className="bg-blue-50 p-4 rounded-md">
              <pre className="whitespace-pre-wrap text-gray-700 font-sans">
                {advice.advice_result.advice}
              </pre>
            </div>
          </div>

          {/* 学习计划 */}
          {advice.advice_result.study_plan && advice.advice_result.study_plan.length > 0 && (
            <div>
              <h4 className="text-lg font-semibold mb-3 text-green-700">📅 学习计划</h4>
              <div className="grid gap-3">
                {advice.advice_result.study_plan.slice(0, 4).map((week: any, index: number) => (
                  <div key={index} className="bg-green-50 p-4 rounded-md border-l-4 border-green-400">
                    <div className="font-medium text-green-800">
                      第{week.week}周: {week.topic}
                    </div>
                    <div className="text-sm text-green-600 mt-1">
                      预计学习时间: {week.estimated_hours}小时
                    </div>
                    <ul className="text-sm text-gray-600 mt-2 list-disc list-inside">
                      {week.activities.slice(0, 3).map((activity: string, i: number) => (
                        <li key={i}>{activity}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 推荐资源 */}
          {advice.advice_result.recommended_resources && advice.advice_result.recommended_resources.length > 0 && (
            <div>
              <h4 className="text-lg font-semibold mb-3 text-purple-700">📖 推荐学习资源</h4>
              <div className="grid md:grid-cols-2 gap-3">
                {advice.advice_result.recommended_resources.slice(0, 4).map((resource: any, index: number) => (
                  <div key={index} className="bg-purple-50 p-3 rounded-md">
                    <div className="font-medium text-purple-800">{resource.title}</div>
                    <div className="text-sm text-purple-600 mt-1">{resource.description}</div>
                    <div className="text-xs text-gray-500 mt-1">
                      类型: {resource.type} | 优先级: {resource.priority}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 学习分析 */}
          <div className="grid md:grid-cols-3 gap-4">
            <div className="bg-yellow-50 p-4 rounded-md text-center">
              <div className="text-2xl font-bold text-yellow-700">
                {advice.advice_result.difficulty_assessment}
              </div>
              <div className="text-sm text-yellow-600">课程难度</div>
            </div>
            
            <div className="bg-blue-50 p-4 rounded-md text-center">
              <div className="text-2xl font-bold text-blue-700">
                {advice.advice_result.estimated_study_time}
              </div>
              <div className="text-sm text-blue-600">建议学习时间</div>
            </div>
            
            <div className="bg-green-50 p-4 rounded-md text-center">
              <div className="text-2xl font-bold text-green-700">
                {Math.round(advice.advice_result.success_probability * 100)}%
              </div>
              <div className="text-sm text-green-600">成功概率</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdviceGenerator;