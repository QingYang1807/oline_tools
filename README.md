# 工具箱

一个简洁大方的在线工具集合，包含15个精选实用工具，按功能分类整理，提升工作效率。

## 🚀 快速开始

1. 使用HTTP服务器运行项目：
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Python 2  
   python -m SimpleHTTPServer 8000
   
   # Node.js
   npx http-server
   ```

2. 访问 `http://localhost:8000` 查看工具门户

## 📁 项目结构

```
workspace/
├── index.html                    # 工具门户首页
├── assets/                       # 静态资源
├── tools/                        # 工具分类目录
│   ├── development/              # 开发工具 (4个)
│   ├── documentation/            # 文档编辑 (5个)  
│   ├── utilities/                # 实用工具 (3个)
│   └── productivity/             # 效率工具 (3个)
├── python_execution_engine/      # Python执行引擎后端
└── TOOLS_README.md              # 详细工具文档
```

## 🛠️ 工具分类

### ⚙️ 开发工具
- API接口测试器
- Base64/URL编解码
- 文件内容对比
- Python代码执行器

### 📝 文档编辑
- Markdown编辑器
- LaTeX公式编辑器
- Mermaid图表渲染器

### 🛠️ 实用工具
- 二维码解析工具
- 密码生成器
- 数据计算工具
- 轻量化日历

### ⚡ 效率工具
- 番茄钟待办事项
- 学习打卡面板
- 极简画板

## 🎨 设计特点

- **简洁大方**：现代化设计，避免过度装饰
- **分类清晰**：按功能分类，便于查找
- **响应式设计**：支持桌面端和移动端
- **暗色模式**：自动适配系统主题
- **无AI味**：专注于实用性

## 🔒 隐私保护

- 所有工具均运行在本地浏览器
- 不收集任何用户数据
- 不发送数据到外部服务器

## 📖 详细文档

查看 [TOOLS_README.md](./TOOLS_README.md) 获取完整的工具列表和使用说明。

## 📄 许可证

MIT License