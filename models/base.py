"""
数据库基础配置文件
包含数据库连接和基础模型类
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 创建 SQLAlchemy 实例
# SQLAlchemy 是 Python 中最流行的 ORM（对象关系映射）库
# 它允许我们使用 Python 类来操作数据库，而不需要写 SQL 语句
db = SQLAlchemy()

class BaseModel(db.Model):
    """
    基础模型类
    包含所有模型共有的字段和方法
    其他模型类可以继承这个类来获得基础功能
    """
    
    # 设置为抽象模型，不会在数据库中创建对应的表
    __abstract__ = True
    
    # 主键字段，每个记录的唯一标识符
    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    
    # 创建时间，记录数据创建的时间
    created_at = db.Column(
        db.DateTime, 
        nullable=False, 
        default=datetime.utcnow,
        comment='创建时间'
    )
    
    # 更新时间，记录数据最后修改的时间
    updated_at = db.Column(
        db.DateTime, 
        nullable=False, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        comment='更新时间'
    )
    
    def to_dict(self):
        """
        将模型实例转换为字典格式
        方便序列化为 JSON 返回给前端
        
        Returns:
            dict: 包含模型所有字段的字典
        """
        result = {}
        # 遍历模型的所有列
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            # 如果是日期时间类型，转换为字符串格式
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            result[column.name] = value
        return result
    
    def save(self):
        """
        保存模型实例到数据库
        这是一个便捷方法，封装了添加和提交操作
        """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            # 如果出错，回滚事务
            db.session.rollback()
            print(f"保存数据时出错: {e}")
            return False
    
    def delete(self):
        """
        从数据库中删除模型实例
        这是一个便捷方法，封装了删除和提交操作
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            # 如果出错，回滚事务
            db.session.rollback()
            print(f"删除数据时出错: {e}")
            return False
    
    @classmethod
    def create(cls, **kwargs):
        """
        类方法：创建新的模型实例
        
        Args:
            **kwargs: 模型字段的键值对
            
        Returns:
            模型实例或 None（如果创建失败）
        """
        try:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance
        except Exception as e:
            db.session.rollback()
            print(f"创建数据时出错: {e}")
            return None
    
    def __repr__(self):
        """
        定义模型实例的字符串表示
        用于调试和日志输出
        """
        return f'<{self.__class__.__name__} {self.id}>'