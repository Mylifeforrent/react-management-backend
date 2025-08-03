#!/usr/bin/env python3
"""
项目启动脚本
提供便捷的项目启动和管理功能
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 错误：需要Python 3.8或更高版本")
        print(f"当前版本：{sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python版本检查通过：{sys.version.split()[0]}")

def check_virtual_env():
    """检查是否在虚拟环境中"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ 检测到虚拟环境")
        return True
    else:
        print("⚠️  警告：未检测到虚拟环境，建议使用虚拟环境")
        return False

def install_dependencies():
    """安装项目依赖"""
    print("📦 正在安装项目依赖...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败：{e}")
        return False

def init_database():
    """初始化数据库"""
    print("🗄️  正在初始化数据库...")
    try:
        subprocess.check_call([sys.executable, "init_db.py", "init"])
        print("✅ 数据库初始化完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 数据库初始化失败：{e}")
        return False

def start_server(host="0.0.0.0", port=8088, debug=True):
    """启动Flask服务器"""
    print(f"🚀 正在启动服务器...")
    print(f"   地址：http://{host}:{port}")
    print(f"   调试模式：{'开启' if debug else '关闭'}")
    print("   按 Ctrl+C 停止服务器")
    print("-" * 50)
    
    try:
        # 设置环境变量
        env = os.environ.copy()
        env['FLASK_APP'] = 'app.py'
        env['FLASK_ENV'] = 'development' if debug else 'production'
        
        # 启动服务器
        subprocess.check_call([sys.executable, "app.py"], env=env)
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except subprocess.CalledProcessError as e:
        print(f"❌ 服务器启动失败：{e}")

def create_virtual_env():
    """创建虚拟环境"""
    venv_path = Path("venv")
    if venv_path.exists():
        print("⚠️  虚拟环境已存在")
        return True
    
    print("🔧 正在创建虚拟环境...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print("✅ 虚拟环境创建完成")
        print("请运行以下命令激活虚拟环境：")
        if os.name == 'nt':  # Windows
            print("   venv\\Scripts\\activate")
        else:  # macOS/Linux
            print("   source venv/bin/activate")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 虚拟环境创建失败：{e}")
        return False

def show_project_info():
    """显示项目信息"""
    print("=" * 60)
    print("🎯 React 管理系统后端 API")
    print("=" * 60)
    print("📋 项目信息：")
    print("   - 基于 Flask 框架")
    print("   - 支持 JWT 身份认证")
    print("   - 用户管理和权限控制")
    print("   - RESTful API 设计")
    print("   - SQLite 数据库")
    print()
    print("🔗 默认账户：")
    print("   管理员 - 用户名: admin, 密码: admin123")
    print("   测试用户 - 用户名: testuser, 密码: test123")
    print("   编辑者 - 用户名: editor, 密码: editor123")
    print()
    print("🌐 API 地址：")
    print("   - 服务器: http://localhost:8088")
    print("   - 健康检查: http://localhost:8088/api/health")
    print("   - API 文档: 查看 README.md")
    print("=" * 60)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="React 管理系统后端启动脚本")
    parser.add_argument("--host", default="0.0.0.0", help="服务器地址 (默认: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8088, help="服务器端口 (默认: 8088)")
    parser.add_argument("--no-debug", action="store_true", help="关闭调试模式")
    parser.add_argument("--setup", action="store_true", help="执行完整的项目设置")
    parser.add_argument("--init-db", action="store_true", help="仅初始化数据库")
    parser.add_argument("--install", action="store_true", help="仅安装依赖")
    parser.add_argument("--create-venv", action="store_true", help="创建虚拟环境")
    parser.add_argument("--info", action="store_true", help="显示项目信息")
    
    args = parser.parse_args()
    
    # 显示项目信息
    if args.info:
        show_project_info()
        return
    
    # 创建虚拟环境
    if args.create_venv:
        create_virtual_env()
        return
    
    # 检查Python版本
    check_python_version()
    
    # 检查虚拟环境
    check_virtual_env()
    
    # 仅安装依赖
    if args.install:
        install_dependencies()
        return
    
    # 仅初始化数据库
    if args.init_db:
        init_database()
        return
    
    # 完整设置
    if args.setup:
        print("🔧 开始项目设置...")
        
        # 安装依赖
        if not install_dependencies():
            return
        
        # 初始化数据库
        if not init_database():
            return
        
        print("✅ 项目设置完成！")
        print("现在可以运行 'python run.py' 启动服务器")
        return
    
    # 检查依赖文件是否存在
    if not Path("requirements.txt").exists():
        print("❌ 未找到 requirements.txt 文件")
        return
    
    # 检查是否已安装依赖（简单检查）
    try:
        import flask
        print("✅ 依赖检查通过")
    except ImportError:
        print("⚠️  未检测到Flask，正在安装依赖...")
        if not install_dependencies():
            return
    
    # 检查数据库是否存在
    db_files = list(Path(".").glob("*.db"))
    if not db_files:
        print("⚠️  未检测到数据库文件，正在初始化...")
        if not init_database():
            return
    
    # 启动服务器
    debug_mode = not args.no_debug
    start_server(args.host, args.port, debug_mode)

if __name__ == "__main__":
    main()