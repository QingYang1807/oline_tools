# Python代码执行引擎服务

一个安全的Python代码执行引擎，提供RESTful API接口，支持自动依赖安装和代码安全检测。

## 功能特性

- ✅ **安全的代码执行**: 内置安全检查，防止危险代码执行
- ✅ **自动依赖管理**: 自动检测和安装Python包依赖
- ✅ **RESTful API**: 提供简洁的HTTP API接口
- ✅ **超时控制**: 防止代码无限执行
- ✅ **资源限制**: 限制内存和CPU使用
- ✅ **Docker支持**: 支持Docker容器化部署
- ✅ **系统服务**: 支持systemd服务管理
- ✅ **Nginx集成**: 支持反向代理和负载均衡

## 快速开始

### 1. 直接运行

```bash
# 克隆或下载代码
cd python_execution_engine

# 安装依赖
pip install -r requirements.txt

# 启动服务
python run.py
```

### 2. Docker部署

```bash
# 构建镜像
docker build -t python-execution-engine .

# 运行容器
docker run -d -p 5000:5000 --name python-engine python-execution-engine

# 或使用docker-compose
docker-compose up -d
```

### 3. Ubuntu服务器部署

```bash
# 使用部署脚本（需要root权限）
sudo ./deploy.sh
```

## API接口

### 健康检查

```http
GET /health
```

响应：
```json
{
    "status": "healthy",
    "service": "Python Execution Engine",
    "version": "1.0.0"
}
```

### 执行Python代码

```http
POST /execute
Content-Type: application/json

{
    "code": "print('Hello, World!')"
}
```

响应：
```json
{
    "success": true,
    "output": "Hello, World!\n",
    "error": "",
    "execution_time": 0.123,
    "imports_used": [],
    "install_message": "无需安装包"
}
```

### 获取允许的包列表

```http
GET /packages
```

响应：
```json
{
    "allowed_packages": ["numpy", "pandas", "matplotlib", ...],
    "total_count": 50
}
```

### 获取服务配置

```http
GET /config
```

响应：
```json
{
    "max_execution_time": 30,
    "max_memory_mb": 512,
    "allowed_packages_count": 50
}
```

## 使用示例

### Python客户端

```python
import requests

# 执行简单代码
response = requests.post('http://localhost:5000/execute', 
                        json={'code': 'print("Hello, World!")'})
result = response.json()
print(result['output'])

# 执行带依赖的代码
code = """
import numpy as np
import matplotlib.pyplot as plt

# 生成数据
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 绘图
plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.title('Sine Wave')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.grid(True)
plt.show()
"""

response = requests.post('http://localhost:5000/execute', json={'code': code})
result = response.json()
print(f"执行成功: {result['success']}")
print(f"输出: {result['output']}")
```

### JavaScript客户端

```javascript
// 执行Python代码
async function executePythonCode(code) {
    const response = await fetch('http://localhost:5000/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: code })
    });
    
    const result = await response.json();
    return result;
}

// 使用示例
executePythonCode('print("Hello from JavaScript!")')
    .then(result => {
        console.log('输出:', result.output);
        console.log('执行时间:', result.execution_time + '秒');
    })
    .catch(error => {
        console.error('执行失败:', error);
    });
```

### cURL命令

```bash
# 健康检查
curl http://localhost:5000/health

# 执行代码
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello, World!\")"}'

# 获取包列表
curl http://localhost:5000/packages
```

## 安全特性

### 代码安全检查

服务会自动检测并阻止以下危险操作：

- 文件写入操作
- 系统命令执行
- 危险模块导入（os, subprocess等）
- 动态代码执行（exec, eval等）

### 资源限制

- **执行时间限制**: 默认30秒
- **内存使用限制**: 默认512MB
- **包安装限制**: 只允许安装预定义的安全包

### 允许的Python包

服务支持以下常用Python包：

- **数据处理**: numpy, pandas, scipy
- **可视化**: matplotlib, seaborn, plotly, bokeh
- **机器学习**: scikit-learn, tensorflow, torch, keras
- **网络请求**: requests, beautifulsoup4
- **图像处理**: pillow, opencv-python
- **Web框架**: flask, django, fastapi
- **数据库**: sqlalchemy, pymongo
- **其他**: jupyter, ipython, sympy等

## 配置选项

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `HOST` | `0.0.0.0` | 服务监听地址 |
| `PORT` | `5000` | 服务监听端口 |
| `DEBUG` | `False` | 调试模式 |
| `MAX_EXECUTION_TIME` | `30` | 最大执行时间（秒） |
| `MAX_MEMORY_MB` | `512` | 最大内存使用（MB） |
| `BASE_DIR` | `/tmp/python_execution` | 工作目录 |

### 配置文件

可以通过修改 `config.py` 文件来自定义配置：

```python
class Config:
    MAX_EXECUTION_TIME = 60  # 增加执行时间限制
    MAX_MEMORY_MB = 1024     # 增加内存限制
    # 添加更多允许的包
    ALLOWED_PACKAGES.add('your_custom_package')
```

## 部署指南

### Ubuntu服务器部署

1. **准备环境**
   ```bash
   # 更新系统
   sudo apt update
   
   # 安装Python 3.11
   sudo apt install python3.11 python3.11-venv python3-pip
   ```

2. **部署服务**
   ```bash
   # 下载代码
   git clone <repository-url>
   cd python_execution_engine
   
   # 运行部署脚本
   sudo ./deploy.sh
   ```

3. **验证部署**
   ```bash
   # 检查服务状态
   sudo systemctl status python-execution-engine
   
   # 测试API
   curl http://localhost/health
   ```

### Docker部署

1. **构建镜像**
   ```bash
   docker build -t python-execution-engine .
   ```

2. **运行容器**
   ```bash
   docker run -d \
     --name python-engine \
     -p 5000:5000 \
     -v /tmp/python_execution:/app/workspace \
     python-execution-engine
   ```

3. **使用docker-compose**
   ```bash
   docker-compose up -d
   ```

### Nginx配置

如果需要使用Nginx作为反向代理：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 监控和日志

### 查看服务日志

```bash
# 查看服务状态
sudo systemctl status python-execution-engine

# 查看实时日志
sudo journalctl -u python-execution-engine -f

# 查看错误日志
sudo journalctl -u python-execution-engine --since "1 hour ago" | grep ERROR
```

### 性能监控

服务提供以下监控接口：

- `/health` - 健康检查
- `/config` - 服务配置信息
- `/packages` - 允许的包列表

## 故障排除

### 常见问题

1. **服务启动失败**
   ```bash
   # 检查端口是否被占用
   sudo netstat -tlnp | grep :5000
   
   # 检查Python版本
   python3 --version
   ```

2. **代码执行超时**
   - 检查代码复杂度
   - 调整 `MAX_EXECUTION_TIME` 配置

3. **包安装失败**
   - 检查网络连接
   - 确认包在允许列表中

4. **权限问题**
   ```bash
   # 检查文件权限
   ls -la /opt/python-execution-engine/
   
   # 修复权限
   sudo chown -R www-data:www-data /opt/python-execution-engine/
   ```

### 调试模式

启用调试模式获取详细日志：

```bash
export DEBUG=True
python run.py
```

## 测试

运行测试脚本验证服务功能：

```bash
# 安装测试依赖
pip install requests

# 运行测试
python test_api.py
```

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

MIT License

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本的Python代码执行
- 实现安全检查和依赖管理
- 提供RESTful API接口
- 支持Docker和systemd部署