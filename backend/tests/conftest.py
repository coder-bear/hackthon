import pytest
import tempfile
import os
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """测试客户端"""
    return TestClient(app)

@pytest.fixture
def temp_file():
    """临时文件"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
        f.write(b"Test content for file upload")
        temp_path = f.name
    
    yield temp_path
    
    # 清理
    if os.path.exists(temp_path):
        os.unlink(temp_path)