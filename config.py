"""
Flask 应用配置文件
包含应用的各种配置参数，如数据库连接、密钥等
"""

import os
from datetime import timedelta

class Config:
    """
    应用配置类
    包含 Flask 应用运行所需的各种配置参数
    """
    
    # Flask 应用密钥，用于会话加密和安全功能
    # 在生产环境中应该使用环境变量设置，这里为了演示使用固定值
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    # JWT (JSON Web Token) 配置
    # JWT 用于用户认证，生成和验证用户登录令牌
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # 访问令牌有效期 24 小时
    
    # 数据库配置
    # 这里使用 SQLite 作为示例，生产环境建议使用 PostgreSQL 或 MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///management_system.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭对象修改跟踪，节省内存
    
    # 文件上传配置
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大上传文件大小 16MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    
    # 分页配置
    POSTS_PER_PAGE = 10  # 每页显示的记录数
    
    # 邮件配置（如果需要发送邮件功能）
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    
    @staticmethod
    def init_app(app):
        """
        应用初始化方法
        可以在这里添加一些应用启动时需要执行的初始化代码
        
        Args:
            app: Flask 应用实例
        """
        # 确保上传目录存在
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

class DevelopmentConfig(Config):
    """
    开发环境配置
    继承基础配置，添加开发环境特有的配置
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///dev_management_system.db'

class ProductionConfig(Config):
    """
    生产环境配置
    继承基础配置，添加生产环境特有的配置
    """
    DEBUG = False
    # 生产环境应该使用更安全的数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///management_system.db'

class TestingConfig(Config):
    """
    测试环境配置
    继承基础配置，添加测试环境特有的配置
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # 使用内存数据库进行测试

# 配置字典，根据环境变量选择不同的配置
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}