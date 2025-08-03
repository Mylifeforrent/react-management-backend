"""
认证工具模块
提供JWT令牌生成、验证等认证相关功能
"""

import jwt
from datetime import datetime, timedelta
from flask import current_app
from models.user import User

def generate_token(user):
    """
    生成JWT访问令牌
    
    Args:
        user (User): 用户对象
        
    Returns:
        str: JWT令牌字符串
    """
    try:
        # 构建令牌载荷
        payload = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=24),  # 24小时后过期
            'iat': datetime.utcnow(),  # 签发时间
            'iss': 'react-management-backend'  # 签发者
        }
        
        # 使用应用密钥签名令牌
        token = jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
        
        return token
        
    except Exception as e:
        current_app.logger.error(f'生成令牌失败: {str(e)}')
        return None

def verify_token(token):
    """
    验证JWT令牌
    
    Args:
        token (str): JWT令牌字符串
        
    Returns:
        dict: 令牌载荷，如果验证失败返回None
    """
    try:
        # 解码并验证令牌
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        
        return payload
        
    except jwt.ExpiredSignatureError:
        current_app.logger.warning('令牌已过期')
        return None
    except jwt.InvalidTokenError:
        current_app.logger.warning('无效的令牌')
        return None
    except Exception as e:
        current_app.logger.error(f'令牌验证失败: {str(e)}')
        return None

def get_current_user(token):
    """
    根据令牌获取当前用户
    
    Args:
        token (str): JWT令牌字符串
        
    Returns:
        User: 用户对象，如果获取失败返回None
    """
    try:
        # 验证令牌
        payload = verify_token(token)
        if not payload:
            return None
        
        # 获取用户ID
        user_id = payload.get('user_id')
        if not user_id:
            return None
        
        # 查找用户
        user = User.find_by_id(user_id)
        if not user:
            current_app.logger.warning(f'令牌中的用户ID {user_id} 不存在')
            return None
        
        # 检查用户状态
        if not user.is_active_user():
            current_app.logger.warning(f'用户 {user.username} 账户已被禁用')
            return None
        
        return user
        
    except Exception as e:
        current_app.logger.error(f'获取当前用户失败: {str(e)}')
        return None

def refresh_token(old_token):
    """
    刷新JWT令牌
    
    Args:
        old_token (str): 旧的JWT令牌
        
    Returns:
        str: 新的JWT令牌，如果刷新失败返回None
    """
    try:
        # 验证旧令牌（即使过期也要能解析出用户信息）
        try:
            payload = jwt.decode(
                old_token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256'],
                options={"verify_exp": False}  # 不验证过期时间
            )
        except jwt.InvalidTokenError:
            return None
        
        # 获取用户
        user_id = payload.get('user_id')
        user = User.find_by_id(user_id)
        
        if not user or not user.is_active_user():
            return None
        
        # 生成新令牌
        return generate_token(user)
        
    except Exception as e:
        current_app.logger.error(f'刷新令牌失败: {str(e)}')
        return None

def extract_token_from_header(auth_header):
    """
    从Authorization头中提取JWT令牌
    
    Args:
        auth_header (str): Authorization头的值
        
    Returns:
        str: JWT令牌，如果提取失败返回None
    """
    if not auth_header:
        return None
    
    # 检查格式是否为 "Bearer <token>"
    if not auth_header.startswith('Bearer '):
        return None
    
    # 提取令牌部分
    try:
        token = auth_header.split(' ')[1]
        return token
    except IndexError:
        return None

def is_token_expired(token):
    """
    检查令牌是否已过期
    
    Args:
        token (str): JWT令牌字符串
        
    Returns:
        bool: True表示已过期，False表示未过期，None表示令牌无效
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        return False  # 如果能正常解码，说明未过期
        
    except jwt.ExpiredSignatureError:
        return True  # 令牌已过期
    except jwt.InvalidTokenError:
        return None  # 令牌无效
    except Exception:
        return None  # 其他错误

def get_token_expiry_time(token):
    """
    获取令牌的过期时间
    
    Args:
        token (str): JWT令牌字符串
        
    Returns:
        datetime: 过期时间，如果获取失败返回None
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=['HS256'],
            options={"verify_exp": False}  # 不验证过期时间
        )
        
        exp_timestamp = payload.get('exp')
        if exp_timestamp:
            return datetime.fromtimestamp(exp_timestamp)
        
        return None
        
    except Exception as e:
        current_app.logger.error(f'获取令牌过期时间失败: {str(e)}')
        return None

def create_password_reset_token(user, expires_in=3600):
    """
    创建密码重置令牌
    
    Args:
        user (User): 用户对象
        expires_in (int): 过期时间（秒），默认1小时
        
    Returns:
        str: 密码重置令牌
    """
    try:
        payload = {
            'user_id': user.id,
            'purpose': 'password_reset',
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
        
        return token
        
    except Exception as e:
        current_app.logger.error(f'创建密码重置令牌失败: {str(e)}')
        return None

def verify_password_reset_token(token):
    """
    验证密码重置令牌
    
    Args:
        token (str): 密码重置令牌
        
    Returns:
        User: 用户对象，如果验证失败返回None
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        
        # 检查令牌用途
        if payload.get('purpose') != 'password_reset':
            return None
        
        # 获取用户
        user_id = payload.get('user_id')
        user = User.find_by_id(user_id)
        
        return user
        
    except jwt.ExpiredSignatureError:
        current_app.logger.warning('密码重置令牌已过期')
        return None
    except jwt.InvalidTokenError:
        current_app.logger.warning('无效的密码重置令牌')
        return None
    except Exception as e:
        current_app.logger.error(f'验证密码重置令牌失败: {str(e)}')
        return None