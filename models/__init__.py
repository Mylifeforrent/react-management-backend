"""
数据模型包初始化文件
用于导入和管理所有的数据模型
"""

# 这个文件使 models 目录成为一个 Python 包
# 可以在这里导入所有的模型类，方便其他模块使用

from .user import User
from .base import db

# 导出所有模型，方便其他模块导入
__all__ = ['User', 'db']