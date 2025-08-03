# 📡 API接口文档

这份文档详细介绍了后端提供的所有API接口，包括请求方式、参数说明和响应格式。

## 📋 目录
1. [接口概览](#接口概览)
2. [认证相关接口](#认证相关接口)
3. [用户管理接口](#用户管理接口)
4. [仪表板接口](#仪表板接口)
5. [响应格式说明](#响应格式说明)
6. [错误码说明](#错误码说明)
7. [接口测试示例](#接口测试示例)

## 🌐 接口概览

### 基础信息
- **服务器地址**：`http://localhost:8081`
- **API前缀**：`/api`
- **数据格式**：JSON
- **字符编码**：UTF-8
- **认证方式**：JWT Bearer Token

### 接口列表

| 分类 | 接口 | 方法 | 说明 |
|------|------|------|------|
| 系统 | `/` | GET | 服务器健康检查 |
| 认证 | `/api/auth/login` | POST | 用户登录 |
| 认证 | `/api/auth/register` | POST | 用户注册 |
| 认证 | `/api/auth/profile` | GET | 获取用户信息 |
| 认证 | `/api/auth/logout` | POST | 用户登出 |
| 用户 | `/api/users/` | GET | 获取用户列表 |
| 用户 | `/api/users/` | POST | 创建用户 |
| 用户 | `/api/users/{id}` | GET | 获取单个用户 |
| 用户 | `/api/users/{id}` | PUT | 更新用户 |
| 用户 | `/api/users/{id}` | DELETE | 删除用户 |
| 仪表板 | `/api/dashboard/overview` | GET | 获取概览数据 |
| 仪表板 | `/api/dashboard/charts` | GET | 获取图表数据 |

## 🔐 认证相关接口

### 1. 用户登录

**接口地址**：`POST /api/auth/login`

**请求参数**：
```json
{
  "username": "admin",      // 用户名（必填）
  "password": "admin123"    // 密码（必填）
}
```

**成功响应**：
```json
{
  "success": true,
  "message": "登录成功",
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "real_name": "管理员",
      "role": "admin",
      "status": "active",
      "created_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 2. 用户注册

**接口地址**：`POST /api/auth/register`

**请求参数**：
```json
{
  "username": "newuser",           // 用户名（必填，3-20字符）
  "email": "user@example.com",     // 邮箱（必填，有效邮箱格式）
  "password": "password123",       // 密码（必填，6-20字符）
  "real_name": "真实姓名",         // 真实姓名（必填）
  "phone": "13800138000"          // 手机号（可选）
}
```

## 🧪 接口测试示例

### 使用curl测试

#### 1. 测试服务器健康状态
```bash
curl -X GET http://localhost:8081/
```

#### 2. 用户登录
```bash
curl -X POST http://localhost:8081/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

#### 3. 获取用户信息（需要先登录获取token）
```bash
curl -X GET http://localhost:8081/api/auth/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 使用Python requests测试

```python
import requests

# 基础URL
BASE_URL = "http://localhost:8081"

# 1. 登录获取token
login_data = {
    "username": "admin",
    "password": "admin123"
}

response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
result = response.json()

if result["success"]:
    token = result["data"]["token"]
    print(f"登录成功，token: {token}")
    
    # 2. 使用token获取用户信息
    headers = {"Authorization": f"Bearer {token}"}
    profile_response = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers)
    profile_result = profile_response.json()
    
    if profile_result["success"]:
        user = profile_result["data"]["user"]
        print(f"用户信息: {user['username']} - {user['real_name']}")
```

### 使用JavaScript fetch测试

```javascript
// 基础URL
const BASE_URL = 'http://localhost:8081';

// 1. 登录获取token
async function login() {
    const response = await fetch(`${BASE_URL}/api/auth/login`, {
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
        console.log('登录成功，token:', token);
        
        // 2. 使用token获取用户信息
        const profileResponse = await fetch(`${BASE_URL}/api/auth/profile`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const profileResult = await profileResponse.json();
        
        if (profileResult.success) {
            const user = profileResult.data.user;
            console.log('用户信息:', user.username, '-', user.real_name);
        }
    }
}

login();
```

## 📱 前端集成示例

### React + Axios 集成

```javascript
// api/auth.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8081/api';

// 创建axios实例
const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
});

// 请求拦截器 - 添加token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 响应拦截器 - 处理错误
api.interceptors.response.use(
    (response) => {
        return response.data;
    },
    (error) => {
        if (error.response?.status === 401) {
            // token过期，跳转到登录页
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// 认证相关API
export const authAPI = {
    // 登录
    login: (credentials) => api.post('/auth/login', credentials),
    
    // 注册
    register: (userData) => api.post('/auth/register', userData),
    
    // 获取用户信息
    getProfile: () => api.get('/auth/profile'),
    
    // 登出
    logout: () => api.post('/auth/logout')
};

// 用户管理API
export const userAPI = {
    // 获取用户列表
    getUsers: (params) => api.get('/users/', { params }),
    
    // 创建用户
    createUser: (userData) => api.post('/users/', userData),
    
    // 获取单个用户
    getUser: (id) => api.get(`/users/${id}`),
    
    // 更新用户
    updateUser: (id, userData) => api.put(`/users/${id}`, userData),
    
    // 删除用户
    deleteUser: (id) => api.delete(`/users/${id}`)
};

// 仪表板API
export const dashboardAPI = {
    // 获取概览数据
    getOverview: () => api.get('/dashboard/overview'),
    
    // 获取图表数据
    getCharts: (params) => api.get('/dashboard/charts', { params })
};
```

### Vue.js 集成示例

```javascript
// plugins/api.js
import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8081/api',
    timeout: 10000
});

// 请求拦截器
api.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// 响应拦截器
api.interceptors.response.use(
    response => response.data,
    error => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            router.push('/login');
        }
        return Promise.reject(error);
    }
);

export default api;
```

## 🔍 调试技巧

### 1. 查看请求日志

在服务器端，所有请求都会在控制台输出日志：

```
2024-01-01 12:00:00 - INFO - POST /api/auth/login - 200 - 0.123s
2024-01-01 12:00:01 - INFO - GET /api/auth/profile - 200 - 0.045s
```

### 2. 使用浏览器开发者工具

1. 打开浏览器开发者工具（F12）
2. 切换到 Network 标签
3. 发送请求，查看请求和响应详情
4. 检查请求头、响应头和响应体

### 3. 常见问题排查

#### CORS跨域问题
如果遇到跨域错误，检查：
1. 服务器是否正确配置了CORS
2. 前端请求的域名是否在允许列表中

#### 401未授权错误
检查：
1. token是否正确携带
2. token是否已过期
3. 用户权限是否足够

#### 500服务器错误
检查：
1. 服务器控制台的错误日志
2. 数据库连接是否正常
3. 请求参数是否正确

## 📋 接口变更日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 实现基础的认证、用户管理和仪表板功能
- 支持JWT认证
- 统一的响应格式

### 未来计划
- [ ] 添加文件上传接口
- [ ] 实现消息通知功能
- [ ] 添加操作日志记录
- [ ] 支持批量操作
- [ ] 添加数据导出功能

---

📝 **注意事项**：
1. 所有需要认证的接口都必须在请求头中携带有效的JWT token
2. 请求和响应的数据格式都是JSON
3. 时间格式统一使用ISO 8601标准（YYYY-MM-DDTHH:mm:ssZ）
4. 分页从第1页开始计数
5. 建议在生产环境中使用HTTPS协议

如有疑问，请参考项目中的测试脚本或联系开发团队。