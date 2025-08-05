#!/usr/bin/env python3
"""
安全登录功能测试脚本
测试前端加密密码和防重放攻击功能

依赖说明：
- requests: HTTP客户端库，用于发送测试请求
- 其他库为Python标准库，无需额外安装

使用前请确保已安装依赖：
pip install requests
或
pip install -r requirements.txt
"""

import requests
import hashlib
import time
import random
import json

# 测试配置
BASE_URL = 'http://localhost:8088/api'
LOGIN_URL = f'{BASE_URL}/auth/login'

def generate_nonce():
    """生成随机数"""
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=20))

def encrypt_password(password, username):
    """使用与前端相同的方式加密密码"""
    salted_password = password + username
    return hashlib.sha256(salted_password.encode()).hexdigest()

def test_secure_login(username, password):
    """测试安全登录"""
    print(f"\n🔐 测试安全登录: {username}")
    
    # 加密密码
    encrypted_password = encrypt_password(password, username)
    nonce = generate_nonce()
    timestamp = int(time.time() * 1000)
    
    # 构造请求数据
    login_data = {
        'username': username,
        'password': encrypted_password,
        'nonce': nonce,
        'timestamp': timestamp
    }
    
    print(f"📤 发送数据: {json.dumps(login_data, indent=2)}")
    
    try:
        # 发送登录请求
        response = requests.post(LOGIN_URL, json=login_data, timeout=10)
        
        print(f"📥 响应状态: {response.status_code}")
        print(f"📥 响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✅ 登录成功!")
            return response.json()
        else:
            print("❌ 登录失败!")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        return None

def test_replay_attack(username, password):
    """测试重放攻击防护"""
    print(f"\n🛡️ 测试重放攻击防护: {username}")
    
    # 第一次正常登录
    encrypted_password = encrypt_password(password, username)
    nonce = generate_nonce()
    timestamp = int(time.time() * 1000)
    
    login_data = {
        'username': username,
        'password': encrypted_password,
        'nonce': nonce,
        'timestamp': timestamp
    }
    
    print("第一次登录（正常）:")
    response1 = requests.post(LOGIN_URL, json=login_data)
    print(f"状态码: {response1.status_code}")
    
    # 第二次使用相同的nonce（重放攻击）
    print("\n第二次登录（重放攻击）:")
    response2 = requests.post(LOGIN_URL, json=login_data)
    print(f"状态码: {response2.status_code}")
    
    if response2.status_code != 200:
        print("✅ 重放攻击防护生效!")
    else:
        print("❌ 重放攻击防护失败!")

def test_timestamp_expiry():
    """测试时间戳过期"""
    print(f"\n⏰ 测试时间戳过期")
    
    # 使用过期的时间戳（10分钟前）
    expired_timestamp = int(time.time() * 1000) - 600000  # 10分钟前
    
    login_data = {
        'username': 'admin',
        'password': encrypt_password('admin123', 'admin'),
        'nonce': generate_nonce(),
        'timestamp': expired_timestamp
    }
    
    response = requests.post(LOGIN_URL, json=login_data)
    print(f"状态码: {response.status_code}")
    
    if response.status_code != 200:
        print("✅ 时间戳过期检查生效!")
    else:
        print("❌ 时间戳过期检查失败!")

def test_password_encryption():
    """测试密码加密"""
    print(f"\n🔒 测试密码加密")
    
    test_cases = [
        ('admin', 'admin123'),
        ('testuser', 'test123'),
        ('editor', 'editor123')
    ]
    
    for username, password in test_cases:
        encrypted = encrypt_password(password, username)
        print(f"用户: {username}, 原密码: {password}")
        print(f"加密后: {encrypted}")
        print()

def main():
    """主测试函数"""
    print("🚀 开始安全登录测试")
    print("=" * 50)
    
    # 测试密码加密
    test_password_encryption()
    
    # 测试正常登录
    test_secure_login('admin', 'admin123')
    test_secure_login('testuser', 'test123')
    test_secure_login('editor', 'editor123')
    
    # 测试错误密码
    test_secure_login('admin', 'wrongpassword')
    
    # 测试重放攻击防护
    test_replay_attack('admin', 'admin123')
    
    # 测试时间戳过期
    test_timestamp_expiry()
    
    print("\n" + "=" * 50)
    print("🏁 测试完成")

if __name__ == '__main__':
    main()