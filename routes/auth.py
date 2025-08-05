"""
认证相关路由
处理用户登录、注册、登出等认证功能
支持前端加密密码和防重放攻击验证
"""

from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
import jwt
from models.user import User
from models.base import db
from utils.decorators import validate_json
from utils.response import success_response, error_response
from utils.security import verify_encrypted_password, verify_anti_replay, log_security_event

# 创建认证蓝图
# Blueprint 是 Flask 中用于组织路由的机制
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@validate_json(['username', 'password'])
def login():
    """
    安全用户登录接口
    支持前端加密密码和防重放攻击验证
    
    请求体格式:
    {
        "username": "用户名或邮箱",
        "password": "SHA256加密后的密码",
        "nonce": "随机数字符串",
        "timestamp": 时间戳
    }
    
    返回格式:
    {
        "code": 200,
        "message": "登录成功",
        "data": {
            "token": "JWT令牌",
            "user": {用户信息}
        }
    }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        username = data.get('username')
        encrypted_password = data.get('password')  # 前端加密后的密码
        nonce = data.get('nonce')
        timestamp = data.get('timestamp')
        
        # 记录登录尝试（不记录密码）
        current_app.logger.info(f'登录尝试: 用户名={username}, IP={request.remote_addr}')
        
        # 验证必要参数
        if not all([username, encrypted_password]):
            return error_response('用户名和密码不能为空', code=400)
        
        # 如果提供了防重放参数，进行验证
        if nonce and timestamp:
            if not verify_anti_replay(nonce, timestamp):
                return error_response('请求验证失败，请重新登录', code=400)
        
        # 查找用户（支持用户名或邮箱登录）
        user = User.find_by_username(username) or User.find_by_email(username)
        
        # 验证用户是否存在
        if not user:
            current_app.logger.warning(f'登录失败: 用户不存在 - {username}')
            return error_response('用户名或密码错误', code=401)  # 不透露具体错误信息
        
        # 验证加密密码
        if not verify_encrypted_password(user, encrypted_password, username):
            log_security_event('login_failed', username, request.remote_addr, '密码错误')
            return error_response('用户名或密码错误', code=401)
        
        # 检查用户状态
        if not user.is_active_user():
            current_app.logger.warning(f'登录失败: 账户被禁用 - {username}')
            return error_response('账户已被禁用，请联系管理员', code=403)
        
        # 生成 JWT 令牌
        # JWT 包含用户ID、用户名、角色等信息，用于后续请求的身份验证
        payload = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=24),  # 令牌24小时后过期
            'iat': datetime.utcnow()  # 令牌签发时间
        }
        
        # 使用应用密钥签名令牌
        token = jwt.encode(
            payload, 
            current_app.config['JWT_SECRET_KEY'], 
            algorithm='HS256'
        )
        
        # 更新用户最后登录时间
        user.last_login = datetime.utcnow()
        user.save()
        
        # 记录成功登录
        log_security_event('login_success', username, request.remote_addr)
        
        # 返回成功响应
        return success_response(
            message='登录成功',
            data={
                'token': token,
                'user': user.to_dict()
            }
        )
        
    except Exception as e:
        current_app.logger.error(f'登录失败: {str(e)}')
        return error_response('登录失败，请稍后重试', code=500)

@auth_bp.route('/register', methods=['POST'])
@validate_json(['username', 'email', 'password'])
def register():
    """
    用户注册接口
    
    请求体格式:
    {
        "username": "用户名",
        "email": "邮箱",
        "password": "密码",
        "real_name": "真实姓名（可选）",
        "phone": "手机号（可选）"
    }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        real_name = data.get('real_name', '')
        phone = data.get('phone', '')
        
        # 验证用户名是否已存在
        if User.find_by_username(username):
            return error_response('用户名已存在', code=400)
        
        # 验证邮箱是否已存在
        if User.find_by_email(email):
            return error_response('邮箱已被注册', code=400)
        
        # 创建新用户
        user = User(
            username=username,
            email=email,
            real_name=real_name,
            phone=phone,
            role='user',  # 默认为普通用户
            status='active'  # 默认激活状态
        )
        
        # 设置密码（会自动进行哈希处理）
        user.set_password(password)
        
        # 保存到数据库
        if user.save():
            return success_response(
                message='注册成功',
                data={'user': user.to_dict()}
            )
        else:
            return error_response('注册失败，请稍后重试', code=500)
            
    except Exception as e:
        current_app.logger.error(f'注册失败: {str(e)}')
        return error_response('注册失败，请稍后重试', code=500)

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    用户登出接口
    
    注意：JWT 是无状态的，服务端无法主动使令牌失效
    实际的登出逻辑主要在前端进行（删除本地存储的令牌）
    这个接口主要用于记录登出日志或执行其他清理操作
    """
    try:
        # 这里可以添加登出日志记录
        # 或者将令牌加入黑名单（需要额外的存储机制）
        
        return success_response(message='登出成功')
        
    except Exception as e:
        current_app.logger.error(f'登出失败: {str(e)}')
        return error_response('登出失败', code=500)

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    获取当前用户信息接口
    需要在请求头中包含有效的 JWT 令牌
    
    请求头格式:
    Authorization: Bearer <JWT令牌>
    """
    try:
        # 从请求头获取令牌
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return error_response('缺少认证令牌', code=401)
        
        # 提取令牌
        token = auth_header.split(' ')[1]
        
        # 验证令牌
        try:
            payload = jwt.decode(
                token, 
                current_app.config['JWT_SECRET_KEY'], 
                algorithms=['HS256']
            )
            user_id = payload.get('user_id')
        except jwt.ExpiredSignatureError:
            return error_response('令牌已过期', code=401)
        except jwt.InvalidTokenError:
            return error_response('无效的令牌', code=401)
        
        # 查找用户
        user = User.find_by_id(user_id)
        if not user:
            return error_response('用户不存在', code=404)
        
        return success_response(
            message='获取用户信息成功',
            data={'user': user.to_dict()}
        )
        
    except Exception as e:
        current_app.logger.error(f'获取用户信息失败: {str(e)}')
        return error_response('获取用户信息失败', code=500)

@auth_bp.route('/change-password', methods=['POST'])
@validate_json(['old_password', 'new_password'])
def change_password():
    """
    修改密码接口
    需要提供旧密码和新密码
    """
    try:
        # 验证用户身份（这里简化处理，实际应该使用装饰器）
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return error_response('缺少认证令牌', code=401)
        
        token = auth_header.split(' ')[1]
        payload = jwt.decode(
            token, 
            current_app.config['JWT_SECRET_KEY'], 
            algorithms=['HS256']
        )
        user_id = payload.get('user_id')
        
        # 获取请求数据
        data = request.get_json()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        # 查找用户
        user = User.find_by_id(user_id)
        if not user:
            return error_response('用户不存在', code=404)
        
        # 验证旧密码
        if not user.check_password(old_password):
            return error_response('原密码错误', code=400)
        
        # 设置新密码
        user.set_password(new_password)
        
        # 保存到数据库
        if user.save():
            return success_response(message='密码修改成功')
        else:
            return error_response('密码修改失败', code=500)
            
    except jwt.ExpiredSignatureError:
        return error_response('令牌已过期', code=401)
    except jwt.InvalidTokenError:
        return error_response('无效的令牌', code=401)
    except Exception as e:
        current_app.logger.error(f'修改密码失败: {str(e)}')
        return error_response('修改密码失败', code=500)