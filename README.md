# 🎯 React 管理系统后端 API

一个基于 Flask 的现代化后端 API 服务，为 React 前端提供完整的用户管理、身份认证和数据服务支持。

## ✨ 特性

- 🔐 **JWT 身份认证** - 安全的用户登录和权限管理
- 👥 **用户管理系统** - 完整的用户增删改查功能
- 🛡️ **角色权限控制** - 基于角色的访问控制（RBAC）
- 📊 **仪表板数据** - 丰富的统计数据和图表支持
- 🌐 **RESTful API** - 标准化的 API 接口设计
- 📱 **CORS 支持** - 完美支持前后端分离
- 🗄️ **SQLite 数据库** - 轻量级数据存储，支持扩展到其他数据库
- 🧪 **完整测试** - 内置 API 测试脚本
- 📚 **详细文档** - 新手友好的中文文档

## 🚀 快速开始

### 方法一：一键启动（推荐）

```bash
# 1. 进入项目目录
cd react-management-backend

# 2. 创建虚拟环境
python3 run.py --create-venv

# 3. 激活虚拟环境
source venv/bin/activate  # Mac/Linux
# 或
venv\Scripts\activate     # Windows

# 4. 完整设置项目
python3 run.py --setup

# 5. 启动服务器
python3 run.py
```

### 方法二：手动步骤

```bash
# 1. 安装依赖
pip3 install -r requirements.txt

# 2. 初始化数据库
python3 init_db.py init

# 3. 启动服务器
python3 app.py
```

### 验证启动成功

访问 http://localhost:8081，看到以下响应说明启动成功：

```json
{
  "message": "React 管理系统后端 API",
  "version": "1.0.0",
  "status": "running"
}
```

## 🔑 默认账户

系统预置了以下测试账户：

| 角色 | 用户名 | 密码 | 权限 |
|------|--------|------|------|
| 管理员 | `admin` | `admin123` | 所有权限 |
| 编辑者 | `editor` | `editor123` | 用户管理权限 |
| 普通用户 | `testuser` | `test123` | 基础权限 |

## 📡 API 接口

### 认证接口
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `GET /api/auth/profile` - 获取用户信息
- `POST /api/auth/logout` - 用户登出

### 用户管理接口
- `GET /api/users/` - 获取用户列表
- `POST /api/users/` - 创建用户
- `GET /api/users/{id}` - 获取单个用户
- `PUT /api/users/{id}` - 更新用户
- `DELETE /api/users/{id}` - 删除用户

### 仪表板接口
- `GET /api/dashboard/overview` - 获取概览数据
- `GET /api/dashboard/charts` - 获取图表数据

详细的 API 文档请查看：[API接口文档](./docs/API接口文档.md)

## 🧪 测试

### 运行完整测试
```bash
python3 test_api.py
```

### 运行单个测试
```bash
# 测试服务器健康状态
python3 test_api.py --test health

# 测试用户登录
python3 test_api.py --test login

# 测试用户注册
python3 test_api.py --test register
```

## 📁 项目结构

```
react-management-backend/
├── 📄 app.py                     # 应用入口文件
├── ⚙️ config.py                  # 配置文件
├── 🗄️ init_db.py                 # 数据库初始化
├── 🚀 run.py                     # 启动脚本
├── 🧪 test_api.py                # API测试脚本
├── 📋 requirements.txt           # 依赖列表
├── 🔧 .env.example              # 环境变量示例
├── 📖 README.md                  # 项目说明
├── 📚 docs/                     # 文档目录
│   ├── 新手入门指南.md
│   ├── API接口文档.md
│   ├── 代码结构说明.md
│   └── 快速上手指南.md
├── 🏗️ models/                   # 数据模型
│   ├── __init__.py
│   ├── base.py                  # 基础模型
│   └── user.py                  # 用户模型
├── 🛣️ routes/                   # 路由处理
│   ├── __init__.py
│   ├── auth.py                  # 认证路由
│   ├── users.py                 # 用户管理路由
│   └── dashboard.py             # 仪表板路由
└── 🔧 utils/                    # 工具函数
    ├── __init__.py
    ├── auth.py                  # 认证工具
    ├── decorators.py            # 装饰器
    └── response.py              # 响应格式化
```

## 🛠️ 技术栈

- **Web框架**: Flask 2.3.3
- **数据库ORM**: Flask-SQLAlchemy 3.0.5
- **身份认证**: PyJWT 2.8.0
- **跨域支持**: Flask-CORS 4.0.0
- **密码加密**: Werkzeug 2.3.7
- **数据库**: SQLite（可扩展到 PostgreSQL/MySQL）

## ⚙️ 配置说明

### 环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
# 应用配置
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
FLASK_ENV=development

# 数据库配置
DATABASE_URL=sqlite:///management_system.db

# 服务器配置
HOST=0.0.0.0
PORT=8081
DEBUG=True

# CORS配置
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### 主要配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `SECRET_KEY` | Flask应用密钥 | 随机生成 |
| `JWT_SECRET_KEY` | JWT令牌密钥 | 随机生成 |
| `DATABASE_URL` | 数据库连接URL | SQLite本地文件 |
| `HOST` | 服务器监听地址 | 0.0.0.0 |
| `PORT` | 服务器端口 | 8081 |
| `DEBUG` | 调试模式 | True |

## 🔧 开发指南

### 添加新的API接口

1. **创建路由文件**（如果需要）
2. **定义路由函数**
3. **注册蓝图**
4. **编写测试**

示例：
```python
# routes/example.py
from flask import Blueprint
from utils.response import success_response
from utils.decorators import token_required

example_bp = Blueprint('example', __name__)

@example_bp.route('/hello', methods=['GET'])
@token_required
def hello():
    return success_response('Hello World!')
```

### 添加新的数据模型

1. **继承BaseModel**
2. **定义字段**
3. **添加方法**
4. **更新数据库**

示例：
```python
# models/example.py
from models.base import BaseModel
from models import db

class Example(BaseModel):
    __tablename__ = 'examples'
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }
```

## 📚 文档

- 📖 [新手入门指南](./docs/新手入门指南.md) - 完全不懂Python的新手指南
- ⚡ [快速上手指南](./docs/快速上手指南.md) - 5分钟快速启动项目
- 📡 [API接口文档](./docs/API接口文档.md) - 详细的API接口说明
- 🏗️ [代码结构说明](./docs/代码结构说明.md) - 深入理解项目架构

## 🤝 与前端集成

这个后端完美配合React前端项目：

### 前端配置
确保前端项目的环境变量配置正确：

```javascript
// .env.development
VITE_APP_BASE_URL=http://localhost:8081
```

### API调用示例
```javascript
// 登录示例
const response = await fetch('http://localhost:8081/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'admin',
    password: 'admin123'
  })
});

const result = await response.json();
if (result.success) {
  const token = result.data.token;
  // 存储token用于后续请求
  localStorage.setItem('token', token);
}
```

## 🚀 部署

### 开发环境
```bash
python3 run.py
```

### 生产环境
```bash
# 使用Gunicorn部署
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8081 app:app
```

### Docker部署
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8081
CMD ["python", "app.py"]
```

## 🔍 故障排除

### 常见问题

#### 1. 模块导入错误
```bash
# 确保在虚拟环境中
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. 数据库错误
```bash
# 重新初始化数据库
python3 run.py --init-db
```

#### 3. 端口被占用
```bash
# 使用其他端口
python3 run.py --port 8082
```

#### 4. CORS跨域问题
检查 `config.py` 中的CORS配置是否包含前端地址。

### 获取帮助

1. 查看错误日志
2. 运行测试脚本诊断
3. 检查配置文件
4. 阅读相关文档

## 📈 性能优化

- 使用数据库索引
- 实现查询缓存
- 优化SQL查询
- 使用连接池
- 启用Gzip压缩

## 🔒 安全建议

- 定期更新依赖包
- 使用强密码策略
- 启用HTTPS（生产环境）
- 实现请求限流
- 定期备份数据库

## 🎯 路线图

- [ ] 添加文件上传功能
- [ ] 实现消息通知系统
- [ ] 添加操作日志记录
- [ ] 支持多数据库
- [ ] 实现缓存机制
- [ ] 添加API限流
- [ ] 支持微服务架构

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---

## 📞 联系我们

如果你有任何问题或建议，请：

- 提交 [Issue](https://github.com/your-repo/issues)
- 发送邮件到：your-email@example.com
- 加入我们的讨论群

---

⭐ 如果这个项目对你有帮助，请给我们一个星标！

**Happy Coding! 🎉**