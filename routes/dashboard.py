"""
仪表板相关路由
处理仪表板数据统计和图表数据
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from models.user import User
from models.base import db
from utils.decorators import require_auth
from utils.response import success_response, error_response
import random

# 创建仪表板蓝图
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/overview', methods=['GET'])
@require_auth
def get_overview():
    """
    获取仪表板概览数据
    包括用户统计、系统状态等基础信息
    """
    try:
        # 用户统计
        total_users = User.query.count()
        active_users = User.query.filter_by(status='active').count()
        admin_users = User.query.filter_by(role='admin').count()
        
        # 最近7天新增用户
        recent_date = datetime.utcnow() - timedelta(days=7)
        recent_users = User.query.filter(User.created_at >= recent_date).count()
        
        # 模拟其他统计数据（实际项目中应该从真实数据源获取）
        overview_data = {
            'user_stats': {
                'total': total_users,
                'active': active_users,
                'admin': admin_users,
                'recent': recent_users
            },
            'system_stats': {
                'total_visits': random.randint(10000, 50000),
                'today_visits': random.randint(100, 1000),
                'total_orders': random.randint(1000, 5000),
                'total_revenue': round(random.uniform(100000, 500000), 2)
            },
            'performance': {
                'cpu_usage': round(random.uniform(20, 80), 1),
                'memory_usage': round(random.uniform(30, 70), 1),
                'disk_usage': round(random.uniform(40, 90), 1)
            }
        }
        
        return success_response(
            message='获取概览数据成功',
            data=overview_data
        )
        
    except Exception as e:
        current_app.logger.error(f'获取概览数据失败: {str(e)}')
        return error_response('获取概览数据失败', code=500)

@dashboard_bp.route('/charts/user-growth', methods=['GET'])
@require_auth
def get_user_growth_chart():
    """
    获取用户增长图表数据
    返回最近30天的用户注册趋势
    """
    try:
        # 获取最近30天的日期范围
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=29)  # 30天数据
        
        # 查询每天的用户注册数量
        daily_data = []
        current_date = start_date
        
        while current_date <= end_date:
            # 查询当天注册的用户数量
            next_date = current_date + timedelta(days=1)
            count = User.query.filter(
                User.created_at >= current_date,
                User.created_at < next_date
            ).count()
            
            daily_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'count': count
            })
            
            current_date = next_date
        
        # 如果没有真实数据，生成一些模拟数据用于演示
        if all(item['count'] == 0 for item in daily_data):
            for item in daily_data:
                item['count'] = random.randint(0, 10)
        
        return success_response(
            message='获取用户增长数据成功',
            data={
                'chart_data': daily_data,
                'total_growth': sum(item['count'] for item in daily_data)
            }
        )
        
    except Exception as e:
        current_app.logger.error(f'获取用户增长数据失败: {str(e)}')
        return error_response('获取用户增长数据失败', code=500)

@dashboard_bp.route('/charts/user-distribution', methods=['GET'])
@require_auth
def get_user_distribution_chart():
    """
    获取用户分布图表数据
    包括角色分布、状态分布等
    """
    try:
        # 角色分布统计
        role_stats = db.session.query(
            User.role,
            db.func.count(User.id).label('count')
        ).group_by(User.role).all()
        
        # 状态分布统计
        status_stats = db.session.query(
            User.status,
            db.func.count(User.id).label('count')
        ).group_by(User.status).all()
        
        # 转换为图表数据格式
        role_data = [
            {'name': role, 'value': count}
            for role, count in role_stats
        ]
        
        status_data = [
            {'name': status, 'value': count}
            for status, count in status_stats
        ]
        
        # 如果没有数据，提供默认数据
        if not role_data:
            role_data = [
                {'name': 'admin', 'value': 1},
                {'name': 'user', 'value': 5},
                {'name': 'editor', 'value': 2}
            ]
        
        if not status_data:
            status_data = [
                {'name': 'active', 'value': 7},
                {'name': 'inactive', 'value': 1}
            ]
        
        return success_response(
            message='获取用户分布数据成功',
            data={
                'role_distribution': role_data,
                'status_distribution': status_data
            }
        )
        
    except Exception as e:
        current_app.logger.error(f'获取用户分布数据失败: {str(e)}')
        return error_response('获取用户分布数据失败', code=500)

@dashboard_bp.route('/charts/activity', methods=['GET'])
@require_auth
def get_activity_chart():
    """
    获取活动统计图表数据
    模拟系统活动数据（访问量、操作次数等）
    """
    try:
        # 生成最近7天的活动数据（模拟数据）
        activity_data = []
        for i in range(7):
            date = (datetime.utcnow() - timedelta(days=6-i)).strftime('%Y-%m-%d')
            activity_data.append({
                'date': date,
                'visits': random.randint(100, 1000),
                'operations': random.randint(50, 500),
                'api_calls': random.randint(200, 2000)
            })
        
        return success_response(
            message='获取活动数据成功',
            data={'activity_data': activity_data}
        )
        
    except Exception as e:
        current_app.logger.error(f'获取活动数据失败: {str(e)}')
        return error_response('获取活动数据失败', code=500)

@dashboard_bp.route('/recent-activities', methods=['GET'])
@require_auth
def get_recent_activities():
    """
    获取最近活动列表
    显示系统中最近发生的重要活动
    """
    try:
        # 获取最近注册的用户作为活动记录
        recent_users = User.query.order_by(
            User.created_at.desc()
        ).limit(10).all()
        
        activities = []
        for user in recent_users:
            activities.append({
                'id': user.id,
                'type': 'user_register',
                'description': f'用户 {user.username} 注册了账户',
                'user': user.username,
                'timestamp': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'success'
            })
        
        # 如果没有真实数据，添加一些模拟活动
        if not activities:
            mock_activities = [
                {
                    'id': 1,
                    'type': 'login',
                    'description': '管理员登录系统',
                    'user': 'admin',
                    'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'success'
                },
                {
                    'id': 2,
                    'type': 'data_export',
                    'description': '导出用户数据',
                    'user': 'admin',
                    'timestamp': (datetime.utcnow() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'success'
                },
                {
                    'id': 3,
                    'type': 'system_backup',
                    'description': '系统自动备份',
                    'user': 'system',
                    'timestamp': (datetime.utcnow() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'success'
                }
            ]
            activities = mock_activities
        
        return success_response(
            message='获取最近活动成功',
            data={'activities': activities}
        )
        
    except Exception as e:
        current_app.logger.error(f'获取最近活动失败: {str(e)}')
        return error_response('获取最近活动失败', code=500)

@dashboard_bp.route('/system-info', methods=['GET'])
@require_auth
def get_system_info():
    """
    获取系统信息
    包括服务器状态、版本信息等
    """
    try:
        import platform
        import psutil
        
        # 获取系统基本信息
        system_info = {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'cpu_count': psutil.cpu_count(),
            'memory_total': round(psutil.virtual_memory().total / (1024**3), 2),  # GB
            'disk_total': round(psutil.disk_usage('/').total / (1024**3), 2),  # GB
            'uptime': 'N/A'  # 可以添加服务器启动时间计算
        }
        
        # 应用信息
        app_info = {
            'name': 'React Management System Backend',
            'version': '1.0.0',
            'environment': current_app.config.get('ENV', 'development'),
            'debug_mode': current_app.debug
        }
        
        return success_response(
            message='获取系统信息成功',
            data={
                'system_info': system_info,
                'app_info': app_info
            }
        )
        
    except ImportError:
        # 如果 psutil 未安装，返回基本信息
        basic_info = {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'message': '需要安装 psutil 库获取详细系统信息'
        }
        
        app_info = {
            'name': 'React Management System Backend',
            'version': '1.0.0',
            'environment': current_app.config.get('ENV', 'development'),
            'debug_mode': current_app.debug
        }
        
        return success_response(
            message='获取系统信息成功',
            data={
                'system_info': basic_info,
                'app_info': app_info
            }
        )
        
    except Exception as e:
        current_app.logger.error(f'获取系统信息失败: {str(e)}')
        return error_response('获取系统信息失败', code=500)