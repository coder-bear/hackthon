import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// PDF相关API
export const uploadPDF = (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/api/pdf/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const extractText = (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/api/pdf/extract-text', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

// 学生相关API
export const createStudent = (studentData: any) => {
  return api.post('/api/students/', studentData);
};

export const getStudents = () => {
  return api.get('/api/students/');
};

export const getStudent = (studentId: string) => {
  return api.get(`/api/students/${studentId}`);
};

export const updateStudent = (studentId: string, studentData: any) => {
  return api.put(`/api/students/${studentId}`, studentData);
};

export const deleteStudent = (studentId: string) => {
  return api.delete(`/api/students/${studentId}`);
};

export const addGrade = (studentId: string, gradeData: any) => {
  return api.post(`/api/students/${studentId}/grades`, gradeData);
};

export const searchStudents = (query: string) => {
  return api.get(`/api/students/search?q=${encodeURIComponent(query)}`);
};

// 课程相关API
export const getCourses = () => {
  return api.get('/api/rag/courses');
};

export const getCourse = (courseId: string) => {
  return api.get(`/api/rag/courses/${courseId}`);
};

// RAG相关API
export const generateAdvice = (studentId: string, courseId: string) => {
  return api.post('/api/rag/advice', {
    student_id: studentId,
    course_id: courseId,
  });
};

export const analyzePerformance = (studentId: string) => {
  return api.post('/api/rag/analyze-performance', {
    student_id: studentId,
  });
};

// 健康检查
export const healthCheck = () => {
  return api.get('/health');
};

export default api;