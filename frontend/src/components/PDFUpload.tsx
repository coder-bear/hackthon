import React, { useState } from 'react';
import { uploadPDF } from '../services/api';

const PDFUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string>('');

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      if (selectedFile.type === 'application/pdf') {
        setFile(selectedFile);
        setError('');
      } else {
        setError('请选择PDF文件');
        setFile(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('请先选择文件');
      return;
    }

    setUploading(true);
    setError('');
    setResult(null);

    try {
      const response = await uploadPDF(file);
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.error || '上传失败');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold mb-4">上传课程描述PDF</h2>
        <p className="text-gray-600 mb-4">
          上传课程描述PDF文件，系统将自动解析课程信息
        </p>
      </div>

      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
        <div className="text-center">
          <div className="text-4xl mb-4">📄</div>
          <div className="mb-4">
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="hidden"
              id="pdf-upload"
            />
            <label
              htmlFor="pdf-upload"
              className="cursor-pointer bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors"
            >
              选择PDF文件
            </label>
          </div>
          {file && (
            <p className="text-sm text-gray-600 mb-4">
              已选择: {file.name}
            </p>
          )}
          <button
            onClick={handleUpload}
            disabled={!file || uploading}
            className="bg-green-500 text-white px-6 py-2 rounded-md hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            {uploading ? '上传中...' : '上传并解析'}
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-red-600">{error}</p>
        </div>
      )}

      {result && (
        <div className="bg-green-50 border border-green-200 rounded-md p-4">
          <h3 className="text-lg font-semibold text-green-800 mb-3">
            解析成功！
          </h3>
          <div className="space-y-3">
            <div>
              <strong>课程代码:</strong> {result.course_info.course_code}
            </div>
            <div>
              <strong>课程名称:</strong> {result.course_info.course_name}
            </div>
            {result.course_info.description && (
              <div>
                <strong>课程描述:</strong>
                <p className="mt-1 text-gray-700">{result.course_info.description}</p>
              </div>
            )}
            {result.course_info.objectives.length > 0 && (
              <div>
                <strong>学习目标:</strong>
                <ul className="mt-1 list-disc list-inside text-gray-700">
                  {result.course_info.objectives.map((obj: string, index: number) => (
                    <li key={index}>{obj}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default PDFUpload;