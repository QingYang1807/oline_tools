# 工具箱 - 实用工具集合

一个简洁大方的在线工具集合，包含15个精选实用工具，按功能分类整理，提升工作效率。

## 📁 目录结构

```
workspace/
├── index.html                    # 工具门户首页
├── assets/                       # 静态资源
│   └── css/
│       └── style.css            # 统一样式文件
├── tools/                        # 工具分类目录
│   ├── development/              # 开发工具
│   │   ├── api-tester.html      # API接口测试器
│   │   ├── base64-url-encoder.html # Base64/URL编解码
│   │   ├── file-diff.html       # 文件内容对比
│   │   └── python-executor.html # Python代码执行器
│   ├── documentation/            # 文档编辑
│   │   ├── latex-editor.html    # LaTeX公式编辑器
│   │   ├── markdown-editor.html # Markdown编辑器
│   │   ├── mermaid.html         # Mermaid图表渲染器
│   │   ├── mermaid-v2.html      # Mermaid图表渲染器v2
│   │   └── mermaid-history.html # Mermaid历史版本
│   ├── utilities/                # 实用工具
│   │   ├── calendar.html        # 轻量化日历
│   │   ├── data-calculator.html # 数据计算工具
│   │   └── password-generator.html # 密码生成器
│   └── productivity/             # 效率工具
│       ├── pomodoro.html        # 番茄钟待办事项
│       ├── study-checkin.html   # 学习打卡面板
│       └── whiteboard.html      # 极简画板
└── python_execution_engine/      # Python执行引擎后端
```

## 🛠️ 工具分类

### ⚙️ 开发工具 (4个)

| 工具名称 | 文件路径 | 功能描述 |
|---------|---------|---------|
| API接口测试器 | `tools/development/api-tester.html` | 测试HTTP接口，支持GET、POST、PUT、DELETE等方法，可设置请求头、参数等 |
| Base64/URL编解码 | `tools/development/base64-url-encoder.html` | 快速编解码Base64和URL格式，支持文本和文件 |
| 文件内容对比 | `tools/development/file-diff.html` | 对比两个文本文件的差异，高亮显示不同之处 |
| Python代码执行器 | `tools/development/python-executor.html` | 在线运行Python代码，支持常用库和模块 |

### 📝 文档编辑 (5个)

| 工具名称 | 文件路径 | 功能描述 |
|---------|---------|---------|
| Markdown编辑器 | `tools/documentation/markdown-editor.html` | 实时预览的Markdown编辑器，支持导出PDF |
| LaTeX公式编辑器 | `tools/documentation/latex-editor.html` | 数学公式编辑和渲染，支持导出图片 |
| Mermaid图表渲染器 | `tools/documentation/mermaid.html` | 创建流程图、时序图、甘特图等 |
| Mermaid图表渲染器v2 | `tools/documentation/mermaid-v2.html` | 增强版Mermaid渲染器 |
| Mermaid历史版本 | `tools/documentation/mermaid-history.html` | 历史版本Mermaid工具 |

### 🛠️ 实用工具 (3个)

| 工具名称 | 文件路径 | 功能描述 |
|---------|---------|---------|
| 二维码解析工具 | `index.html` | 解析二维码内容，支持粘贴、拖拽、文件上传 |
| 密码生成器 | `tools/utilities/password-generator.html` | 生成安全随机密码，支持自定义规则 |
| 数据计算工具 | `tools/utilities/data-calculator.html` | 进制转换、单位换算、数学计算等 |
| 轻量化日历 | `tools/utilities/calendar.html` | 简洁的日历查看器，支持日期选择 |

### ⚡ 效率工具 (3个)

| 工具名称 | 文件路径 | 功能描述 |
|---------|---------|---------|
| 番茄钟待办事项 | `tools/productivity/pomodoro.html` | 时间管理和任务规划，25分钟专注时间 |
| 学习打卡面板 | `tools/productivity/study-checkin.html` | 学习进度跟踪，连续打卡记录 |
| 极简画板 | `tools/productivity/whiteboard.html` | 在线绘图和标注，支持多种画笔工具 |

## 🚀 快速开始

1. **访问工具门户**：打开 `index.html` 查看所有工具
2. **选择工具**：点击对应工具卡片进入使用
3. **开始使用**：所有工具均为纯前端实现，无需安装

## 🎨 设计特点

- **简洁大方**：采用现代化设计，避免过度装饰
- **分类清晰**：按功能分类，便于查找和使用
- **响应式设计**：支持桌面端和移动端
- **暗色模式**：自动适配系统主题偏好
- **无AI味**：专注于实用性，避免花哨效果

## 🔧 技术栈

- **前端**：纯HTML/CSS/JavaScript
- **样式**：CSS3 + CSS变量 + Flexbox/Grid
- **兼容性**：现代浏览器（Chrome 66+, Firefox 63+, Safari 13.1+, Edge 79+）
- **依赖**：部分工具使用CDN库（MathJax、jsQR、Mermaid等）

## 📱 浏览器支持

- Chrome 66+
- Firefox 63+
- Safari 13.1+
- Edge 79+

## 🔒 隐私保护

- 所有工具均运行在本地浏览器
- 不收集任何用户数据
- 不发送数据到外部服务器
- 保护用户隐私安全

## 📝 使用说明

1. **本地运行**：使用HTTP服务器运行（不能直接打开HTML文件）
2. **推荐服务器**：
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Python 2
   python -m SimpleHTTPServer 8000
   
   # Node.js
   npx http-server
   ```
3. **访问地址**：`http://localhost:8000`

## 🛡️ 安全建议

- 密码生成器：建议生成12位以上密码
- 文件对比：注意保护敏感文件内容
- API测试：避免在生产环境测试
- Python执行：注意代码安全性

## 📊 工具统计

- **总工具数**：15个
- **分类数**：4个
- **开发工具**：4个
- **文档编辑**：5个
- **实用工具**：3个
- **效率工具**：3个

## 🔄 更新日志

### v2.0.0 (当前版本)
- ✅ 重新整理目录结构，按功能分类
- ✅ 创建简洁大方的工具门户首页
- ✅ 统一工具文档和说明
- ✅ 清理冗余和重复文件
- ✅ 优化工具链接和导航

### v1.0.0
- ✅ 初始版本发布
- ✅ 15个实用工具
- ✅ 基础功能实现

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进工具：

1. 报告Bug或建议新功能
2. 优化现有工具性能
3. 添加新的实用工具
4. 改进用户界面设计

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

---

**工具箱** - 让工作更高效，让生活更简单