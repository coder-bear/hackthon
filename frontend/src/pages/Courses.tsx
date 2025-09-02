import React, { useState, useEffect } from 'react';
import { getCourses } from '../services/api';

interface Course {
  _id: string;
  course_code: string;
  course_name: string;
  description: string;
  objectives: string[];
  topics: string[];
  prerequisites: string[];
  assessment: string[];
}

const Courses: React.FC = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);

  useEffect(() => {
    loadCourses();
  }, []);

  const loadCourses = async () => {
    try {
      const response = await getCourses();
      setCourses(response.data.courses || []);
    } catch (error) {
      console.error('加载课程数据失败:', error);
    } finally {
      setLoading(false);
    }
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
        <h1 className="text-2xl font-bold">课程管理</h1>
        <div className="text-sm text-gray-600">
          共 {courses.length} 门课程
        </div>
      </div>

      <div className="grid gap-6">
        {courses.map((course) => (
          <div key={course._id} className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold">
                  {course.course_code} - {course.course_name}
                </h3>
                {course.description && (
                  <p className="text-gray-600 mt-2">{course.description}</p>
                )}
              </div>
              <button
                onClick={() => setSelectedCourse(selectedCourse === course ? null : course)}
                className="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
              >
                {selectedCourse === course ? '收起' : '详情'}
              </button>
            </div>

            {selectedCourse === course && (
              <div className="space-y-4 border-t pt-4">
                {course.objectives.length > 0 && (
                  <div>
                    <h4 className="font-medium mb-2">学习目标</h4>
                    <ul className="list-disc list-inside text-gray-600 space-y-1">
                      {course.objectives.map((obj, index) => (
                        <li key={index}>{obj}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {course.topics.length > 0 && (
                  <div>
                    <h4 className="font-medium mb-2">课程主题</h4>
                    <div className="grid md:grid-cols-2 gap-2">
                      {course.topics.map((topic, index) => (
                        <div key={index} className="bg-gray-50 p-2 rounded text-sm">
                          {topic}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {course.prerequisites.length > 0 && (
                  <div>
                    <h4 className="font-medium mb-2">先修课程</h4>
                    <div className="flex flex-wrap gap-2">
                      {course.prerequisites.map((prereq, index) => (
                        <span key={index} className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm">
                          {prereq}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {course.assessment.length > 0 && (
                  <div>
                    <h4 className="font-medium mb-2">评估方式</h4>
                    <ul className="list-disc list-inside text-gray-600 space-y-1">
                      {course.assessment.map((assess, index) => (
                        <li key={index}>{assess}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      {courses.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-500 text-lg">暂无课程数据</div>
          <p className="text-gray-400 mt-2">请先上传课程描述PDF文件</p>
        </div>
      )}
    </div>
  );
};

export default Courses;