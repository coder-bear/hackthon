import React, { useState } from 'react';
import PDFUpload from '../components/PDFUpload';
import StudentForm from '../components/StudentForm';
import AdviceGenerator from '../components/AdviceGenerator';

const Home: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'upload' | 'student' | 'advice'>('upload');

  const tabs = [
    { id: 'upload', label: 'PDF上传', icon: '📄' },
    { id: 'student', label: '学生信息', icon: '👨‍🎓' },
    { id: 'advice', label: '学习建议', icon: '💡' },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          RAG学习建议系统
        </h1>
        <p className="text-lg text-gray-600">
          基于RAG技术的个性化学习建议生成平台
        </p>
      </div>

      {/* 功能特性展示 */}
      <div className="grid md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="text-2xl mb-3">📚</div>
          <h3 className="text-lg font-semibold mb-2">PDF课程解析</h3>
          <p className="text-gray-600">
            自动解析课程描述PDF，提取关键信息和学习要点
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="text-2xl mb-3">🎯</div>
          <h3 className="text-lg font-semibold mb-2">个性化建议</h3>
          <p className="text-gray-600">
            结合学生历史成绩，生成针对性的学习建议和计划
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="text-2xl mb-3">📊</div>
          <h3 className="text-lg font-semibold mb-2">学习分析</h3>
          <p className="text-gray-600">
            深度分析学习表现，预测成功概率和学习难度
          </p>
        </div>
      </div>

      {/* 主要功能区域 */}
      <div className="bg-white rounded-lg shadow-sm border">
        {/* 标签页导航 */}
        <div className="border-b">
          <nav className="flex space-x-8 px-6">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-4 px-2 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* 标签页内容 */}
        <div className="p-6">
          {activeTab === 'upload' && <PDFUpload />}
          {activeTab === 'student' && <StudentForm />}
          {activeTab === 'advice' && <AdviceGenerator />}
        </div>
      </div>
    </div>
  );
};

export default Home;