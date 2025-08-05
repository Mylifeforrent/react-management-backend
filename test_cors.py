#!/usr/bin/env python3
"""
CORS配置测试脚本
测试跨域请求是否正常工作
"""

import requests
import json

def test_cors_preflight():
    """测试CORS预检请求"""
    print("🔍 测试CORS预检请求...")
    
    # 模拟浏览器发送的OPTIONS预检请求
    headers = {
        'Origin': 'http://127.0.0.1:5174',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type, Authorization'
    }
    
    try:
        response = requests.options('http://localhost:8088/api/auth/login', headers=headers)
        
        print(f"状态码: {response.status_code}")
        print("响应头:")
        for key, value in response.headers.items():
            if 'access-control' in key.lower():
                print(f"  {key}: {value}")
        
        # 检查必要的CORS头
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials')
        }
        
        print("\n📋 CORS头检查:")
        for header, value in cors_headers.items():
            status = "✅" if value else "❌"
            print(f"  {status} {header}: {value}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def test_actual_request():
    """测试实际的登录请求"""
    print("\n🔐 测试实际登录请求...")
    
    headers = {
        'Origin': 'http://127.0.0.1:5174',
        'Content-Type': 'application/json'
    }
    
    data = {
        'username': 'admin',
        'password': 'test_password'
    }
    
    try:
        response = requests.post(
            'http://localhost:8088/api/auth/login', 
            json=data, 
            headers=headers
        )
        
        print(f"状态码: {response.status_code}")
        print("CORS响应头:")
        for key, value in response.headers.items():
            if 'access-control' in key.lower():
                print(f"  {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始CORS配置测试")
    print("=" * 50)
    
    # 测试预检请求
    preflight_ok = test_cors_preflight()
    
    # 测试实际请求
    actual_ok = test_actual_request()
    
    print("\n" + "=" * 50)
    print("📊 测试结果:")
    print(f"  预检请求: {'✅ 通过' if preflight_ok else '❌ 失败'}")
    print(f"  实际请求: {'✅ 通过' if actual_ok else '❌ 失败'}")
    
    if preflight_ok and actual_ok:
        print("\n🎉 CORS配置正常!")
    else:
        print("\n⚠️  CORS配置需要调整")
        print("\n🔧 建议检查:")
        print("  1. 后端服务器是否正在运行 (http://localhost:8088)")
        print("  2. CORS配置中是否包含正确的源地址")
        print("  3. 是否允许了必要的请求头和方法")

if __name__ == '__main__':
    main()