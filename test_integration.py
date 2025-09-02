import requests
import time
import pytest
import os

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

class TestIntegration:
    """集成测试"""
    
    def test_backend_health(self):
        """测试后端健康状态"""
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_frontend_accessibility(self):
        """测试前端可访问性"""
        try:
            response = requests.get(FRONTEND_URL, timeout=10)
            assert response.status_code == 200
        except requests.exceptions.RequestException:
            pytest.skip("Frontend not running")
    
    def test_file_upload_flow(self):
        """测试文件上传流程"""
        # 创建测试文件
        test_content = b"This is a test document for upload testing."
        
        files = {'file': ('test.txt', test_content, 'text/plain')}
        response = requests.post(f"{BASE_URL}/upload", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.txt"
        assert data["size"] == len(test_content)

def test_system_components():
    """测试系统组件"""
    # 检查必要的目录
    assert os.path.exists("backend/app")
    assert os.path.exists("frontend/src")
    assert os.path.exists("data")
    
    # 检查配置文件
    assert os.path.exists("docker-compose.yml")
    assert os.path.exists("backend/requirements.txt")
    assert os.path.exists("frontend/package.json")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])