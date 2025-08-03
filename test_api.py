#!/usr/bin/env python3
"""
API 测试脚本
用于测试后端API接口的基本功能
"""

import requests
import json
import sys
from datetime import datetime

# API基础URL
BASE_URL = "http://localhost:8088"

class APITester:
    """API测试类"""
    
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.token = None
        self.session = requests.Session()
        
    def print_result(self, test_name, success, message="", data=None):
        """打印测试结果"""
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{status} {test_name}")
        if message:
            print(f"   {message}")
        if data and isinstance(data, dict):
            print(f"   响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print()
    
    def test_server_health(self):
        """测试服务器健康状态"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                self.print_result(
                    "服务器健康检查", 
                    True, 
                    f"服务器正常运行，版本: {data.get('version', 'N/A')}"
                )
                return True
            else:
                self.print_result("服务器健康检查", False, f"状态码: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            self.print_result("服务器健康检查", False, "无法连接到服务器，请确保服务器已启动")
            return False
        except Exception as e:
            self.print_result("服务器健康检查", False, f"错误: {str(e)}")
            return False
    
    def test_login(self, username="admin", password="admin123"):
        """测试用户登录"""
        try:
            login_data = {
                "username": username,
                "password": password
            }
            
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "data" in data and "token" in data["data"]:
                    self.token = data["data"]["token"]
                    user_info = data["data"]["user"]
                    self.print_result(
                        "用户登录", 
                        True, 
                        f"用户 {user_info.get('username')} 登录成功，角色: {user_info.get('role')}"
                    )
                    return True
                else:
                    self.print_result("用户登录", False, data.get("message", "登录失败"))
                    return False
            else:
                try:
                    error_data = response.json()
                    self.print_result("用户登录", False, error_data.get("message", "登录失败"))
                except:
                    self.print_result("用户登录", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.print_result("用户登录", False, f"错误: {str(e)}")
            return False
    
    def test_get_profile(self):
        """测试获取用户信息"""
        if not self.token:
            self.print_result("获取用户信息", False, "需要先登录")
            return False
        
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            response = self.session.get(
                f"{self.base_url}/api/auth/profile",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    user_info = data["data"]["user"]
                    self.print_result(
                        "获取用户信息", 
                        True, 
                        f"用户: {user_info.get('username')}, 邮箱: {user_info.get('email')}"
                    )
                    return True
                else:
                    self.print_result("获取用户信息", False, data.get("message"))
                    return False
            else:
                self.print_result("获取用户信息", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.print_result("获取用户信息", False, f"错误: {str(e)}")
            return False
    
    def test_get_users(self):
        """测试获取用户列表"""
        if not self.token:
            self.print_result("获取用户列表", False, "需要先登录")
            return False
        
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            response = self.session.get(
                f"{self.base_url}/api/users/?page=1&per_page=5",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    users = data["data"]["users"]
                    pagination = data["data"]["pagination"]
                    self.print_result(
                        "获取用户列表", 
                        True, 
                        f"获取到 {len(users)} 个用户，总计 {pagination.get('total')} 个用户"
                    )
                    return True
                else:
                    self.print_result("获取用户列表", False, data.get("message"))
                    return False
            else:
                self.print_result("获取用户列表", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.print_result("获取用户列表", False, f"错误: {str(e)}")
            return False
    
    def test_dashboard_overview(self):
        """测试仪表板概览"""
        if not self.token:
            self.print_result("仪表板概览", False, "需要先登录")
            return False
        
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            response = self.session.get(
                f"{self.base_url}/api/dashboard/overview",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    overview = data["data"]
                    user_stats = overview.get("user_stats", {})
                    self.print_result(
                        "仪表板概览", 
                        True, 
                        f"总用户数: {user_stats.get('total')}, 活跃用户: {user_stats.get('active')}"
                    )
                    return True
                else:
                    self.print_result("仪表板概览", False, data.get("message"))
                    return False
            else:
                self.print_result("仪表板概览", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.print_result("仪表板概览", False, f"错误: {str(e)}")
            return False
    
    def test_register_user(self):
        """测试用户注册"""
        try:
            # 生成唯一的测试用户名
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            test_user = {
                "username": f"testuser_{timestamp}",
                "email": f"test_{timestamp}@example.com",
                "password": "test123456",
                "real_name": "测试用户",
                "phone": "13800138000"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/auth/register",
                json=test_user,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    user_info = data["data"]["user"]
                    self.print_result(
                        "用户注册", 
                        True, 
                        f"用户 {user_info.get('username')} 注册成功"
                    )
                    return True
                else:
                    self.print_result("用户注册", False, data.get("message"))
                    return False
            else:
                try:
                    error_data = response.json()
                    self.print_result("用户注册", False, error_data.get("message"))
                except:
                    self.print_result("用户注册", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.print_result("用户注册", False, f"错误: {str(e)}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🧪 开始API测试")
        print("=" * 50)
        
        # 测试计数
        total_tests = 0
        passed_tests = 0
        
        # 1. 测试服务器健康状态
        total_tests += 1
        if self.test_server_health():
            passed_tests += 1
        else:
            print("❌ 服务器未启动，停止测试")
            return
        
        # 2. 测试用户注册
        total_tests += 1
        if self.test_register_user():
            passed_tests += 1
        
        # 3. 测试用户登录
        total_tests += 1
        if self.test_login():
            passed_tests += 1
        else:
            print("❌ 登录失败，跳过需要认证的测试")
            self.print_summary(total_tests, passed_tests)
            return
        
        # 4. 测试获取用户信息
        total_tests += 1
        if self.test_get_profile():
            passed_tests += 1
        
        # 5. 测试获取用户列表
        total_tests += 1
        if self.test_get_users():
            passed_tests += 1
        
        # 6. 测试仪表板概览
        total_tests += 1
        if self.test_dashboard_overview():
            passed_tests += 1
        
        # 打印测试总结
        self.print_summary(total_tests, passed_tests)
    
    def print_summary(self, total, passed):
        """打印测试总结"""
        print("=" * 50)
        print("📊 测试总结")
        print(f"总测试数: {total}")
        print(f"通过测试: {passed}")
        print(f"失败测试: {total - passed}")
        print(f"通过率: {(passed/total*100):.1f}%")
        
        if passed == total:
            print("🎉 所有测试通过！")
        else:
            print("⚠️  部分测试失败，请检查服务器状态和配置")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="API测试脚本")
    parser.add_argument("--url", default=BASE_URL, help=f"API基础URL (默认: {BASE_URL})")
    parser.add_argument("--username", default="admin", help="登录用户名 (默认: admin)")
    parser.add_argument("--password", default="admin123", help="登录密码 (默认: admin123)")
    parser.add_argument("--test", choices=["health", "login", "profile", "users", "dashboard", "register"], 
                       help="运行单个测试")
    
    args = parser.parse_args()
    
    # 创建测试实例
    tester = APITester(args.url)
    
    print(f"🔗 测试目标: {args.url}")
    print(f"👤 测试账户: {args.username}")
    print()
    
    # 运行指定测试
    if args.test:
        if args.test == "health":
            tester.test_server_health()
        elif args.test == "login":
            tester.test_login(args.username, args.password)
        elif args.test == "profile":
            tester.test_login(args.username, args.password)
            tester.test_get_profile()
        elif args.test == "users":
            tester.test_login(args.username, args.password)
            tester.test_get_users()
        elif args.test == "dashboard":
            tester.test_login(args.username, args.password)
            tester.test_dashboard_overview()
        elif args.test == "register":
            tester.test_register_user()
    else:
        # 运行所有测试
        tester.run_all_tests()

if __name__ == "__main__":
    main()