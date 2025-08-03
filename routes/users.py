"""
用户管理相关路由
处理用户的增删改查等管理功能
"""

from flask import Blueprint, request, jsonify, current_app
from models.user import User
from models.base import db
from utils.decorators import validate_json, require_auth, require_admin
from utils.response import success_response, error_response

# 创建用户管理蓝图
users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@require_auth
def get_users():
    """
    获取用户列表接口（分页）
    
    查询参数:
    - page: 页码（默认1）
    - per_page: 每页数量（默认10）
    - search: 搜索关键词（可选）
    - role: 角色筛选（可选）
    - status: 状态筛选（可选）
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        role = request.args.get('role', '')
        status = request.args.get('status', '')
        
        # 构建查询
        query = User.query
        
        # 搜索功能：根据用户名、邮箱、真实姓名搜索
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                db.or_(
                    User.username.like(search_pattern),
                    User.email.like(search_pattern),
                    User.real_name.like(search_pattern)
                )
            )
        
        # 角色筛选
        if role:
            query = query.filter(User.role == role)
        
        # 状态筛选
        if status:
            query = query.filter(User.status == status)
        
        # 按创建时间倒序排列
        query = query.order_by(User.created_at.desc())
        
        # 执行分页查询
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # 构建返回数据
        users_data = [user.to_dict() for user in pagination.items]
        
        return success_response(
            message='获取用户列表成功',
            data={
                'users': users_data,
                'pagination': {
                    'page': pagination.page,
                    'pages': pagination.pages,
                    'per_page': pagination.per_page,
                    'total': pagination.total,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
        )
        
    except Exception as e:
        current_app.logger.error(f'获取用户列表失败: {str(e)}')
        return error_response('获取用户列表失败', code=500)

@users_bp.route('/<int:user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    """
    获取单个用户详情
    
    路径参数:
    - user_id: 用户ID
    """
    try:
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

@users_bp.route('/', methods=['POST'])
@require_admin  # 只有管理员可以创建用户
@validate_json(['username', 'email', 'password'])
def create_user():
    """
    创建新用户接口（管理员功能）
    
    请求体格式:
    {
        "username": "用户名",
        "email": "邮箱",
        "password": "密码",
        "real_name": "真实姓名",
        "phone": "手机号",
        "role": "角色",
        "status": "状态"
    }
    """
    try:
        data = request.get_json()
        
        # 验证用户名是否已存在
        if User.find_by_username(data['username']):
            return error_response('用户名已存在', code=400)
        
        # 验证邮箱是否已存在
        if User.find_by_email(data['email']):
            return error_response('邮箱已被注册', code=400)
        
        # 创建新用户
        user = User(
            username=data['username'],
            email=data['email'],
            real_name=data.get('real_name', ''),
            phone=data.get('phone', ''),
            role=data.get('role', 'user'),
            status=data.get('status', 'active')
        )
        
        # 设置密码
        user.set_password(data['password'])
        
        # 保存到数据库
        if user.save():
            return success_response(
                message='用户创建成功',
                data={'user': user.to_dict()}
            )
        else:
            return error_response('用户创建失败', code=500)
            
    except Exception as e:
        current_app.logger.error(f'创建用户失败: {str(e)}')
        return error_response('创建用户失败', code=500)

@users_bp.route('/<int:user_id>', methods=['PUT'])
@require_admin  # 只有管理员可以编辑用户
def update_user(user_id):
    """
    更新用户信息接口（管理员功能）
    
    路径参数:
    - user_id: 用户ID
    
    请求体格式:
    {
        "username": "用户名",
        "email": "邮箱",
        "real_name": "真实姓名",
        "phone": "手机号",
        "role": "角色",
        "status": "状态"
    }
    """
    try:
        user = User.find_by_id(user_id)
        if not user:
            return error_response('用户不存在', code=404)
        
        data = request.get_json()
        
        # 检查用户名是否被其他用户使用
        if 'username' in data and data['username'] != user.username:
            existing_user = User.find_by_username(data['username'])
            if existing_user and existing_user.id != user_id:
                return error_response('用户名已存在', code=400)
        
        # 检查邮箱是否被其他用户使用
        if 'email' in data and data['email'] != user.email:
            existing_user = User.find_by_email(data['email'])
            if existing_user and existing_user.id != user_id:
                return error_response('邮箱已被注册', code=400)
        
        # 更新用户信息
        for field in ['username', 'email', 'real_name', 'phone', 'role', 'status']:
            if field in data:
                setattr(user, field, data[field])
        
        # 如果提供了新密码，则更新密码
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        # 保存到数据库
        if user.save():
            return success_response(
                message='用户信息更新成功',
                data={'user': user.to_dict()}
            )
        else:
            return error_response('用户信息更新失败', code=500)
            
    except Exception as e:
        current_app.logger.error(f'更新用户信息失败: {str(e)}')
        return error_response('更新用户信息失败', code=500)

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@require_admin  # 只有管理员可以删除用户
def delete_user(user_id):
    """
    删除用户接口（管理员功能）
    
    路径参数:
    - user_id: 用户ID
    """
    try:
        user = User.find_by_id(user_id)
        if not user:
            return error_response('用户不存在', code=404)
        
        # 防止删除管理员账户（可选的安全措施）
        if user.is_admin():
            return error_response('不能删除管理员账户', code=403)
        
        # 删除用户
        if user.delete():
            return success_response(message='用户删除成功')
        else:
            return error_response('用户删除失败', code=500)
            
    except Exception as e:
        current_app.logger.error(f'删除用户失败: {str(e)}')
        return error_response('删除用户失败', code=500)

@users_bp.route('/<int:user_id>/status', methods=['PATCH'])
@require_admin  # 只有管理员可以修改用户状态
def update_user_status(user_id):
    """
    更新用户状态接口（管理员功能）
    
    路径参数:
    - user_id: 用户ID
    
    请求体格式:
    {
        "status": "active|inactive|banned"
    }
    """
    try:
        user = User.find_by_id(user_id)
        if not user:
            return error_response('用户不存在', code=404)
        
        data = request.get_json()
        new_status = data.get('status')
        
        # 验证状态值
        valid_statuses = ['active', 'inactive', 'banned']
        if new_status not in valid_statuses:
            return error_response(f'无效的状态值，必须是: {", ".join(valid_statuses)}', code=400)
        
        # 更新状态
        user.status = new_status
        
        # 保存到数据库
        if user.save():
            return success_response(
                message='用户状态更新成功',
                data={'user': user.to_dict()}
            )
        else:
            return error_response('用户状态更新失败', code=500)
            
    except Exception as e:
        current_app.logger.error(f'更新用户状态失败: {str(e)}')
        return error_response('更新用户状态失败', code=500)

@users_bp.route('/stats', methods=['GET'])
@require_admin  # 只有管理员可以查看统计信息
def get_user_stats():
    """
    获取用户统计信息接口（管理员功能）
    
    返回用户总数、各角色用户数、各状态用户数等统计信息
    """
    try:
        # 总用户数
        total_users = User.query.count()
        
        # 各角色用户数
        role_stats = db.session.query(
            User.role, 
            db.func.count(User.id)
        ).group_by(User.role).all()
        
        # 各状态用户数
        status_stats = db.session.query(
            User.status, 
            db.func.count(User.id)
        ).group_by(User.status).all()
        
        # 最近注册的用户（最近7天）
        from datetime import datetime, timedelta
        recent_date = datetime.utcnow() - timedelta(days=7)
        recent_users = User.query.filter(
            User.created_at >= recent_date
        ).count()
        
        return success_response(
            message='获取用户统计信息成功',
            data={
                'total_users': total_users,
                'role_stats': dict(role_stats),
                'status_stats': dict(status_stats),
                'recent_users': recent_users
            }
        )
        
    except Exception as e:
        current_app.logger.error(f'获取用户统计信息失败: {str(e)}')
        return error_response('获取用户统计信息失败', code=500)