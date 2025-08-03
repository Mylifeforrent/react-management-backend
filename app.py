"""
Flask 后端应用主文件
这是整个后端应用的入口点，负责启动 Flask 服务器
"""

from flask import Flask
from flask_cors import CORS
from config import Config
from models.base import db
from routes.auth import auth_bp
from routes.users import users_bp
from routes.dashboard import dashboard_bp

def create_app():
    """
    应用工厂函数
    创建并配置 Flask 应用实例
    
    Returns:
        Flask: 配置好的 Flask 应用实例
    """
    # 创建 Flask 应用实例
    app = Flask(__name__)
    
    # 从配置类加载配置
    app.config.from_object(Config)
    
    # 初始化数据库
    db.init_app(app)
    
    # 启用 CORS（跨域资源共享），允许前端访问后端 API
    # 配置支持凭证传递和预检请求
    CORS(app, 
         origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization', 'icode'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

    # 注册蓝图（Blueprint）- 用于组织路由
    # 蓝图是 Flask 中用来组织相关路由的机制
    app.register_blueprint(auth_bp, url_prefix='/api/auth')      # 认证相关路由
    app.register_blueprint(users_bp, url_prefix='/api/users')    # 用户管理路由
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')  # 仪表板路由
    
    # 根路由 - 用于测试服务器是否正常运行
    @app.route('/')
    def hello():
        """
        根路径处理函数
        返回简单的欢迎信息，用于测试服务器状态
        """
        return {
            'message': '欢迎使用 React 管理系统后端 API',
            'status': 'success',
            'version': '1.0.0'
        }
    
    # 健康检查路由
    @app.route('/api/health')
    def health_check():
        """
        健康检查接口
        用于监控服务器状态
        """
        return {
            'status': 'healthy',
            'message': '服务器运行正常'
        }
    
    return app

# 当直接运行此文件时执行
if __name__ == '__main__':
    # 创建应用实例
    app = create_app()
    
    # 启动开发服务器
    # debug=True 启用调试模式，代码修改后自动重启
    # host='0.0.0.0' 允许外部访问
    # port=8081 设置端口号，与前端配置的 VITE_APP_BASE_URL 保持一致
    app.run(debug=True, host='0.0.0.0', port=8088)