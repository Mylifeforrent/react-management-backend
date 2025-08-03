"""
数据库初始化脚本
用于创建数据库表和初始数据
"""

from models.base import db
from models.user import User
from datetime import datetime

def init_database(app=None):
    """
    初始化数据库
    创建所有表并插入初始数据
    
    Args:
        app: Flask应用实例，如果为None则创建新实例
    """
    # 如果没有传入app实例，则创建一个
    if app is None:
        from app import create_app
        app = create_app()
    
    with app.app_context():
        print("正在初始化数据库...")
        
        # 删除所有表（谨慎使用！）
        print("删除现有表...")
        db.drop_all()
        
        # 创建所有表
        print("创建数据库表...")
        db.create_all()
        
        # 创建默认管理员账户
        print("创建默认管理员账户...")
        admin_user = User(
            username='admin',
            email='admin@example.com',
            real_name='系统管理员',
            phone='13800138000',
            role='admin',
            status='active'
        )
        admin_user.set_password('admin123')  # 默认密码，生产环境请修改
        
        # 创建测试用户账户
        print("创建测试用户账户...")
        test_user = User(
            username='testuser',
            email='test@example.com',
            real_name='测试用户',
            phone='13800138001',
            role='user',
            status='active'
        )
        test_user.set_password('test123')
        
        # 创建编辑者账户
        print("创建编辑者账户...")
        editor_user = User(
            username='editor',
            email='editor@example.com',
            real_name='内容编辑',
            phone='13800138002',
            role='editor',
            status='active'
        )
        editor_user.set_password('editor123')
        
        try:
            # 保存用户到数据库
            db.session.add(admin_user)
            db.session.add(test_user)
            db.session.add(editor_user)
            db.session.commit()
            
            print("数据库初始化完成！")
            print("\n默认账户信息：")
            print("=" * 50)
            print("管理员账户:")
            print("  用户名: admin")
            print("  密码: admin123")
            print("  邮箱: admin@example.com")
            print()
            print("测试用户账户:")
            print("  用户名: testuser")
            print("  密码: test123")
            print("  邮箱: test@example.com")
            print()
            print("编辑者账户:")
            print("  用户名: editor")
            print("  密码: editor123")
            print("  邮箱: editor@example.com")
            print("=" * 50)
            print("\n注意：请在生产环境中修改默认密码！")
            
        except Exception as e:
            print(f"数据库初始化失败: {str(e)}")
            db.session.rollback()

def reset_admin_password(app=None):
    """
    重置管理员密码
    用于忘记密码时的紧急恢复
    
    Args:
        app: Flask应用实例，如果为None则创建新实例
    """
    if app is None:
        from app import create_app
        app = create_app()
    
    with app.app_context():
        admin = User.find_by_username('admin')
        if admin:
            new_password = input("请输入新的管理员密码: ")
            if new_password:
                admin.set_password(new_password)
                admin.save()
                print("管理员密码重置成功！")
            else:
                print("密码不能为空！")
        else:
            print("未找到管理员账户！")

def create_sample_users(app=None):
    """
    创建示例用户数据
    用于测试和演示
    
    Args:
        app: Flask应用实例，如果为None则创建新实例
    """
    if app is None:
        from app import create_app
        app = create_app()
    
    with app.app_context():
        print("创建示例用户数据...")
        
        sample_users = [
            {
                'username': 'user1',
                'email': 'user1@example.com',
                'real_name': '张三',
                'phone': '13800138003',
                'role': 'user',
                'status': 'active',
                'password': 'user123'
            },
            {
                'username': 'user2',
                'email': 'user2@example.com',
                'real_name': '李四',
                'phone': '13800138004',
                'role': 'user',
                'status': 'active',
                'password': 'user123'
            },
            {
                'username': 'user3',
                'email': 'user3@example.com',
                'real_name': '王五',
                'phone': '13800138005',
                'role': 'user',
                'status': 'inactive',
                'password': 'user123'
            },
            {
                'username': 'editor2',
                'email': 'editor2@example.com',
                'real_name': '赵六',
                'phone': '13800138006',
                'role': 'editor',
                'status': 'active',
                'password': 'editor123'
            }
        ]
        
        created_count = 0
        for user_data in sample_users:
            # 检查用户是否已存在
            if User.find_by_username(user_data['username']):
                print(f"用户 {user_data['username']} 已存在，跳过...")
                continue
            
            if User.find_by_email(user_data['email']):
                print(f"邮箱 {user_data['email']} 已被使用，跳过...")
                continue
            
            # 创建用户
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                real_name=user_data['real_name'],
                phone=user_data['phone'],
                role=user_data['role'],
                status=user_data['status']
            )
            user.set_password(user_data['password'])
            
            if user.save():
                print(f"创建用户 {user_data['username']} 成功")
                created_count += 1
            else:
                print(f"创建用户 {user_data['username']} 失败")
        
        print(f"示例用户创建完成，共创建 {created_count} 个用户")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'init':
            # 初始化数据库
            init_database()
        elif command == 'reset-admin':
            # 重置管理员密码
            reset_admin_password()
        elif command == 'sample':
            # 创建示例用户
            create_sample_users()
        else:
            print("未知命令！")
            print("可用命令:")
            print("  python init_db.py init        - 初始化数据库")
            print("  python init_db.py reset-admin - 重置管理员密码")
            print("  python init_db.py sample      - 创建示例用户")
    else:
        # 默认执行初始化
        init_database()