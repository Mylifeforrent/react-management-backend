"""
路由包初始化文件
用于导入和管理所有的路由蓝图
"""

# 这个文件使 routes 目录成为一个 Python 包
# 可以在这里导入所有的路由蓝图，方便其他模块使用

from .auth import auth_bp
from .users import users_bp
from .dashboard import dashboard_bp

# 导出所有蓝图，方便其他模块导入
__all__ = ['auth_bp', 'users_bp', 'dashboard_bp']