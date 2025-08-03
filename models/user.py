"""
用户数据模型
定义用户表结构和相关的数据库操作方法
"""

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .base import db, BaseModel

class User(BaseModel, UserMixin):
    """
    用户模型类
    继承 BaseModel 获得基础字段（id, created_at, updated_at）
    继承 UserMixin 获得 Flask-Login 需要的方法
    """
    
    # 定义数据库表名
    __tablename__ = 'users'
    
    # 用户名字段，唯一且不能为空
    username = db.Column(
        db.String(80), 
        unique=True, 
        nullable=False, 
        index=True,  # 创建索引提高查询性能
        comment='用户名'
    )
    
    # 邮箱字段，唯一且不能为空
    email = db.Column(
        db.String(120), 
        unique=True, 
        nullable=False, 
        index=True,
        comment='邮箱地址'
    )
    
    # 密码哈希值，不存储明文密码
    password_hash = db.Column(
        db.String(255), 
        nullable=False,
        comment='密码哈希值'
    )
    
    # 真实姓名
    real_name = db.Column(
        db.String(100), 
        nullable=True,
        comment='真实姓名'
    )
    
    # 手机号码
    phone = db.Column(
        db.String(20), 
        nullable=True,
        comment='手机号码'
    )
    
    # 用户角色：admin(管理员), user(普通用户), editor(编辑者)
    role = db.Column(
        db.String(20), 
        nullable=False, 
        default='user',
        comment='用户角色'
    )
    
    # 用户状态：active(激活), inactive(未激活), banned(被禁用)
    status = db.Column(
        db.String(20), 
        nullable=False, 
        default='active',
        comment='用户状态'
    )
    
    # 头像URL
    avatar = db.Column(
        db.String(255), 
        nullable=True,
        comment='头像URL'
    )
    
    # 最后登录时间
    last_login = db.Column(
        db.DateTime, 
        nullable=True,
        comment='最后登录时间'
    )
    
    def set_password(self, password):
        """
        设置用户密码
        将明文密码转换为哈希值存储，提高安全性
        
        Args:
            password (str): 明文密码
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        验证用户密码
        将输入的明文密码与存储的哈希值进行比较
        
        Args:
            password (str): 要验证的明文密码
            
        Returns:
            bool: 密码是否正确
        """
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """
        检查用户是否为管理员
        
        Returns:
            bool: 是否为管理员
        """
        return self.role == 'admin'
    
    def is_active_user(self):
        """
        检查用户是否为激活状态
        
        Returns:
            bool: 用户是否激活
        """
        return self.status == 'active'
    
    def to_dict(self, include_sensitive=False):
        """
        将用户对象转换为字典
        重写父类方法，可以选择是否包含敏感信息
        
        Args:
            include_sensitive (bool): 是否包含敏感信息（如密码哈希）
            
        Returns:
            dict: 用户信息字典
        """
        # 调用父类的 to_dict 方法
        result = super().to_dict()
        
        # 如果不包含敏感信息，移除密码哈希
        if not include_sensitive:
            result.pop('password_hash', None)
        
        return result
    
    @classmethod
    def find_by_username(cls, username):
        """
        根据用户名查找用户
        
        Args:
            username (str): 用户名
            
        Returns:
            User: 用户对象或 None
        """
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls, email):
        """
        根据邮箱查找用户
        
        Args:
            email (str): 邮箱地址
            
        Returns:
            User: 用户对象或 None
        """
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, user_id):
        """
        根据ID查找用户
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            User: 用户对象或 None
        """
        return cls.query.get(user_id)
    
    @classmethod
    def get_all_users(cls, page=1, per_page=10):
        """
        获取所有用户（分页）
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            Pagination: 分页对象
        """
        return cls.query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
    
    def __repr__(self):
        """
        定义用户对象的字符串表示
        用于调试和日志输出
        """
        return f'<User {self.username}>'