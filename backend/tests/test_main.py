import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Document Analysis API is running"}

def test_health_check():
    """测试健康检查"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_upload_no_file():
    """测试无文件上传"""
    response = client.post("/upload")
    assert response.status_code == 422  # Validation error

def test_upload_with_file():
    """测试文件上传"""
    test_file = ("test.txt", b"test content", "text/plain")
    response = client.post("/upload", files={"file": test_file})
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.txt"
    assert data["size"] > 0