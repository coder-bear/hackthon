from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # 启用CORS
    CORS(app)
    
    # MongoDB连接
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/rag_learning_advisor')
    app.config['MONGODB_URI'] = mongodb_uri
    
    # 初始化数据库连接
    try:
        client = MongoClient(mongodb_uri)
        db = client[os.getenv('MONGODB_DB_NAME', 'rag_learning_advisor')]
        app.db = db
        print("MongoDB连接成功")
    except Exception as e:
        print(f"MongoDB连接失败: {e}")
    
    # 注册蓝图
    from app.routes.pdf_routes import pdf_bp
    from app.routes.student_routes import student_bp
    from app.routes.rag_routes import rag_bp
    
    app.register_blueprint(pdf_bp, url_prefix='/api/pdf')
    app.register_blueprint(student_bp, url_prefix='/api/students')
    app.register_blueprint(rag_bp, url_prefix='/api/rag')
    
    # 健康检查路由
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'RAG学习建议系统运行正常'}
    
    return app