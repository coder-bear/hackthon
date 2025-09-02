import React, { useState, useEffect } from 'react';
import { getStudents, analyzePerformance } from '../services/api';

interface Student {
  _id: string;
  name: string;
  student_id: string;
  major: string;
}

interface Analysis {
  average_score: number;
  total_courses: number;
  performance_trend: string;
  recent_average: number;
  recommendations: string[];
}

const Analysis: React.FC = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [selectedStudent, setSelectedStudent] = useState('');
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadStudents();
  }, []);

  const loadStudents = async () => {
    try {
      const response = await getStudents();
      setStudents(response.data.students || []);
    } catch (error) {
      console.error('加载学生数据失败:', error);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedStudent) {
      setError('请选择学生');
      return;
    }

    setLoading(true);
    setError('');
    setAnalysis(null);

    try {
      const response = await analyzePerformance(selectedStudent);
      setAnalysis(response.data.analysis);
    } catch (err: any) {
      setError(err.response?.data?.error || '分析失败');
    } finally {
      setLoading(false);
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'improving': return 'text-green-600 bg-green-50';
      case 'declining': return 'text-red-600 bg-red-50';
      case 'stable': return 'text-blue-600 bg-blue-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const getTrendText = (trend: string) => {
    switch (trend) {
      case 'improving': return '📈 上升趋势';
      case 'declining': return '📉 下降趋势';
      case 'stable': return '📊 稳定';
      default: return '❓ 数据不足';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold mb-4">学习表现分析</h1>
        <p className="text-gray-600">
          基于学生历史成绩数据，分析学习表现和趋势
        </p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <div className="flex items-end space-x-4 mb-6">
          <div className="flex-1">
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
          <button
            onClick={handleAnalyze}
            disabled={loading || !selectedStudent}
            className="bg-purple-500 text-white px-6 py-2 rounded-md hover:bg-purple-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? '分析中...' : '🔍 开始分析'}
          </button>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {analysis && (
          <div className="space-y-6">
            <div className="border-b pb-4">
              <h3 className="text-lg font-semibold">📊 学习表现分析报告</h3>
            </div>

            {/* 关键指标 */}
            <div className="grid md:grid-cols-4 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-blue-700">
                  {analysis.average_score}
                </div>
                <div className="text-sm text-blue-600">平均分</div>
              </div>
              
              <div className="bg-green-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-green-700">
                  {analysis.total_courses}
                </div>
                <div className="text-sm text-green-600">总课程数</div>
              </div>
              
              <div className="bg-purple-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-purple-700">
                  {analysis.recent_average}
                </div>
                <div className="text-sm text-purple-600">近期平均分</div>
              </div>
              
              <div className={`p-4 rounded-lg text-center ${getTrendColor(analysis.performance_trend)}`}>
                <div className="text-lg font-bold">
                  {getTrendText(analysis.performance_trend)}
                </div>
                <div className="text-sm">学习趋势</div>
              </div>
            </div>

            {/* 建议 */}
            <div>
              <h4 className="text-lg font-semibold mb-3 text-orange-700">💡 个性化建议</h4>
              <div className="bg-orange-50 p-4 rounded-lg">
                <ul className="space-y-2">
                  {analysis.recommendations.map((rec, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-orange-500 mr-2">•</span>
                      <span className="text-gray-700">{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* 表现等级 */}
            <div>
              <h4 className="text-lg font-semibold mb-3">🏆 表现等级</h4>
              <div className="flex items-center space-x-4">
                <div className="flex-1 bg-gray-200 rounded-full h-4">
                  <div 
                    className={`h-4 rounded-full transition-all duration-500 ${
                      analysis.average_score >= 90 ? 'bg-green-500' :
                      analysis.average_score >= 80 ? 'bg-blue-500' :
                      analysis.average_score >= 70 ? 'bg-yellow-500' :
                      'bg-red-500'
                    }`}
                    style={{ width: `${Math.min(analysis.average_score, 100)}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium">
                  {analysis.average_score >= 90 ? '优秀' :
                   analysis.average_score >= 80 ? '良好' :
                   analysis.average_score >= 70 ? '中等' :
                   '需要改进'}
                </span>
              </div>
            </div>
          </div>
        )}
      </div>

      {students.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-500 text-lg">暂无学生数据</div>
          <p className="text-gray-400 mt-2">请先添加学生信息和成绩数据</p>
        </div>
      )}
    </div>
  );
};

export default Analysis;