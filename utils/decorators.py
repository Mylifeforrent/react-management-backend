"""
装饰器工具模块
包含各种用于路由保护和数据验证的装饰器
"""

from functools import wraps
from flask import request, jsonify, current_app
import jwt
from models.user import User
from .response import error_response

def validate_json(required_fields):
    """
    JSON数据验证装饰器
    验证请求体是否包含必需的字段
    
    Args:
        required_fields (list): 必需字段列表
        
    Usage:
        @validate_json(['username', 'password'])
        def login():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 检查请求是否包含JSON数据
            if not request.is_json:
                return error_response('请求必须包含JSON数据', code=400)
            
            data = request.get_json()
            if not data:
                return error_response('请求体不能为空', code=400)
            
            # 检查必需字段
            missing_fields = []
            for field in required_fields:
                if field not in data or not data[field]:
                    missing_fields.append(field)
            
            if missing_fields:
                return error_response(
                    f'缺少必需字段: {", ".join(missing_fields)}', 
                    code=400
                )
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_auth(f):
    """
    身份认证装饰器
    验证用户是否已登录（检查JWT令牌）
    
    Usage:
        @require_auth
        def protected_route():
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头获取令牌
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return error_response('缺少认证令牌', code=401)
        
        # 检查令牌格式
        if not auth_header.startswith('Bearer '):
            return error_response('令牌格式错误', code=401)
        
        # 提取令牌
        token = auth_header.split(' ')[1]
        
        try:
            # 验证令牌
            payload = jwt.decode(
                token, 
                current_app.config['JWT_SECRET_KEY'], 
                algorithms=['HS256']
            )
            
            # 获取用户信息
            user_id = payload.get('user_id')
            user = User.find_by_id(user_id)
            
            if not user:
                return error_response('用户不存在', code=401)
            
            if not user.is_active_user():
                return error_response('账户已被禁用', code=403)
            
            # 将用户信息添加到请求上下文中
            request.current_user = user
            
        except jwt.ExpiredSignatureError:
            return error_response('令牌已过期', code=401)
        except jwt.InvalidTokenError:
            return error_response('无效的令牌', code=401)
        except Exception as e:
            current_app.logger.error(f'令牌验证失败: {str(e)}')
            return error_response('令牌验证失败', code=401)
        
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    """
    管理员权限装饰器
    验证用户是否为管理员
    
    Usage:
        @require_admin
        def admin_only_route():
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 首先进行身份认证
        auth_result = require_auth(f)(*args, **kwargs)
        
        # 如果认证失败，直接返回错误
        if hasattr(auth_result, 'status_code') and auth_result.status_code != 200:
            return auth_result
        
        # 检查用户是否为管理员
        user = getattr(request, 'current_user', None)
        if not user or not user.is_admin():
            return error_response('需要管理员权限', code=403)
        
        return f(*args, **kwargs)
    return decorated_function

def require_role(required_role):
    """
    角色权限装饰器
    验证用户是否具有指定角色
    
    Args:
        required_role (str): 需要的角色
        
    Usage:
        @require_role('editor')
        def editor_route():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 首先进行身份认证
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return error_response('缺少认证令牌', code=401)
            
            token = auth_header.split(' ')[1]
            
            try:
                payload = jwt.decode(
                    token, 
                    current_app.config['JWT_SECRET_KEY'], 
                    algorithms=['HS256']
                )
                
                user_id = payload.get('user_id')
                user = User.find_by_id(user_id)
                
                if not user:
                    return error_response('用户不存在', code=401)
                
                if not user.is_active_user():
                    return error_response('账户已被禁用', code=403)
                
                # 检查角色权限
                if user.role != required_role and not user.is_admin():
                    return error_response(f'需要{required_role}权限', code=403)
                
                request.current_user = user
                
            except jwt.ExpiredSignatureError:
                return error_response('令牌已过期', code=401)
            except jwt.InvalidTokenError:
                return error_response('无效的令牌', code=401)
            except Exception as e:
                current_app.logger.error(f'权限验证失败: {str(e)}')
                return error_response('权限验证失败', code=401)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def rate_limit(max_requests=100, window=3600):
    """
    速率限制装饰器
    限制用户在指定时间窗口内的请求次数
    
    Args:
        max_requests (int): 最大请求次数
        window (int): 时间窗口（秒）
        
    Usage:
        @rate_limit(max_requests=10, window=60)  # 每分钟最多10次请求
        def limited_route():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 这里可以实现基于Redis或内存的速率限制
            # 为了简化，这里只是一个示例框架
            
            # 获取客户端IP
            client_ip = request.remote_addr
            
            # 实际实现中，你需要：
            # 1. 使用Redis或内存存储来跟踪请求次数
            # 2. 检查当前IP在时间窗口内的请求次数
            # 3. 如果超过限制，返回429错误
            
            # 这里暂时跳过实际的限制检查
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def log_activity(activity_type):
    """
    活动日志装饰器
    记录用户的操作活动
    
    Args:
        activity_type (str): 活动类型
        
    Usage:
        @log_activity('user_login')
        def login():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 执行原函数
            result = f(*args, **kwargs)
            
            try:
                # 记录活动日志
                user = getattr(request, 'current_user', None)
                user_info = user.username if user else 'anonymous'
                
                current_app.logger.info(
                    f'Activity: {activity_type} by {user_info} '
                    f'from {request.remote_addr}'
                )
                
                # 这里可以将活动记录保存到数据库
                # 实际项目中可能需要创建一个Activity模型来存储这些信息
                
            except Exception as e:
                current_app.logger.error(f'记录活动日志失败: {str(e)}')
            
            return result
        return decorated_function
    return decorator