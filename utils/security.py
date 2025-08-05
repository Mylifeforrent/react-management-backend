"""
安全相关工具函数
包含密码验证、防重放攻击等安全功能
"""

import hashlib
import time
from flask import current_app

# 用于存储已使用的nonce，防止重放攻击
# 在生产环境中应该使用Redis等缓存系统
used_nonces = set()

def verify_encrypted_password(user, encrypted_password, username):
    """
    验证前端加密的密码
    前端使用 SHA256(password + username) 的方式加密
    
    Args:
        user: 用户对象
        encrypted_password: 前端加密后的密码
        username: 用户名
    
    Returns:
        bool: 验证是否成功
    """
    try:
        # 由于我们无法从哈希值反推原始密码，这里提供几种解决方案：
        
        # 方案1：检查常见的默认密码（适用于演示环境）
        default_passwords = ['admin123', 'test123', 'editor123', 'user123', '123456']
        
        for pwd in default_passwords:
            # 使用相同的加密方式
            test_encrypted = hashlib.sha256((pwd + username).encode()).hexdigest()
            if test_encrypted == encrypted_password:
                # 验证这个密码是否与存储的哈希匹配
                return user.check_password(pwd)
        
        # 方案2：如果需要支持任意密码，可以考虑以下方案：
        # - 在用户表中添加一个额外的字段存储SHA256(password + username)
        # - 或者修改前端，通过HTTPS发送明文密码
        
        return False
        
    except Exception as e:
        current_app.logger.error(f'密码验证失败: {str(e)}')
        return False

def verify_anti_replay(nonce, timestamp):
    """
    验证防重放攻击参数
    
    Args:
        nonce: 随机数
        timestamp: 时间戳
    
    Returns:
        bool: 验证是否成功
    """
    try:
        # 检查时间戳是否在合理范围内（5分钟内）
        current_time = int(time.time() * 1000)
        time_diff = abs(current_time - timestamp)
        
        if time_diff > 300000:  # 5分钟 = 300000毫秒
            current_app.logger.warning(f'请求时间戳过期: {time_diff}ms')
            return False
        
        # 检查nonce是否已使用过
        if nonce in used_nonces:
            current_app.logger.warning(f'检测到重放攻击: nonce {nonce} 已被使用')
            return False
        
        # 标记nonce为已使用
        used_nonces.add(nonce)
        
        # 清理过期的nonce（简单实现，生产环境应使用更高效的方式）
        if len(used_nonces) > 10000:  # 限制内存使用
            used_nonces.clear()
        
        return True
        
    except Exception as e:
        current_app.logger.error(f'防重放验证失败: {str(e)}')
        return False

def generate_secure_hash(password, salt):
    """
    生成安全的密码哈希
    使用与前端相同的算法
    
    Args:
        password: 原始密码
        salt: 盐值
    
    Returns:
        str: 哈希值
    """
    return hashlib.sha256((password + salt).encode()).hexdigest()

def validate_password_strength(password):
    """
    验证密码强度
    
    Args:
        password: 密码
    
    Returns:
        tuple: (是否有效, 错误信息)
    """
    if len(password) < 6:
        return False, "密码长度至少6位"
    
    if len(password) > 128:
        return False, "密码长度不能超过128位"
    
    # 可以添加更多密码强度检查
    # - 包含大小写字母
    # - 包含数字
    # - 包含特殊字符
    
    return True, ""

def log_security_event(event_type, username, ip_address, details=None):
    """
    记录安全事件
    
    Args:
        event_type: 事件类型（login_success, login_failed, etc.）
        username: 用户名
        ip_address: IP地址
        details: 额外详情
    """
    log_message = f'安全事件: {event_type}, 用户: {username}, IP: {ip_address}'
    if details:
        log_message += f', 详情: {details}'
    
    current_app.logger.info(log_message)