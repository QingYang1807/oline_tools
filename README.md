# 工具箱门户与实用工具集合

一个简洁现代的工具门户与前端实用工具集合，涵盖开发、文档、实用与效率四大类，共 20 个工具；同时包含 `python_execution_engine` 服务端模块。

## 📁 仓库结构

```
/workspace/
├── index.html                     # 首页门户（工具目录与搜索）
├── tools-portal.html              # 门户备份页面（与首页一致，可保留）
├── assets/
│   └── css/
│       ├── style.css             # 通用样式
│       └── markdown-editor.css   # Markdown编辑器样式
├── tools/
│   ├── development/              # 开发类
│   │   ├── api-tester.html
│   │   ├── base64-url-encoder.html
│   │   ├── file-diff.html
│   │   ├── advanced-file-diff.html
│   │   ├── python-executor.html
│   │   ├── sql-rollback-generator.html
│   │   └── html-preview.html     # 原首页的HTML在线预览工具（迁移至此）
│   ├── documentation/            # 文档类
│   │   ├── latex-editor.html
│   │   ├── markdown-editor.html
│   │   ├── mermaid.html
│   │   ├── mermaid-v2.html
│   │   └── mermaid-history.html
│   ├── utilities/                # 实用类
│   │   ├── calendar.html
│   │   ├── data-calculator.html
│   │   ├── password-generator.html
│   │   └── qr-decoder.html
│   └── productivity/             # 效率类
│       ├── markdown_clean.html
│       ├── pomodoro.html
│       ├── study-checkin.html
│       └── whiteboard.html
├── python_execution_engine/       # Python执行引擎服务端
│   ├── app.py, run.py, wsgi.py, config.py 等
│   ├── requirements.txt, Dockerfile, docker-compose.yml
│   ├── frontend/ (前端交互界面)
│   └── README.md, README_FRONTEND.md
├── TOOLS_README.md                # 工具集合说明
├── 使用说明.md                     # 中文使用说明（旧）
├── examples.js                    # HTML预览工具示例数据
├── start.sh                       # 本地静态服务器启动脚本
└── README.md                      # 当前文档
```

## 🛠️ 工具目录

### ⚙️ 开发工具（7）
- API接口测试器: `tools/development/api-tester.html`
- Base64/URL编解码: `tools/development/base64-url-encoder.html`
- 文件内容对比: `tools/development/file-diff.html`
- 高级文件对比: `tools/development/advanced-file-diff.html`
- Python代码执行器: `tools/development/python-executor.html`
- SQL回滚生成工具: `tools/development/sql-rollback-generator.html`
- HTML在线预览工具: `tools/development/html-preview.html`

### 📝 文档编辑（5）
- Markdown编辑器: `tools/documentation/markdown-editor.html`
- LaTeX公式编辑器: `tools/documentation/latex-editor.html`
- Mermaid图表渲染器: `tools/documentation/mermaid.html`
- Mermaid图表渲染器v2: `tools/documentation/mermaid-v2.html`
- Mermaid历史版本: `tools/documentation/mermaid-history.html`

### 🛠️ 实用工具（4）
- 轻量化日历: `tools/utilities/calendar.html`
- 数据计算工具: `tools/utilities/data-calculator.html`
- 密码生成器: `tools/utilities/password-generator.html`
- 二维码解析工具: `tools/utilities/qr-decoder.html`

### ⚡ 效率工具（4）
- 番茄钟待办事项: `tools/productivity/pomodoro.html`
- 学习打卡面板: `tools/productivity/study-checkin.html`
- 极简画板: `tools/productivity/whiteboard.html`
- Markdown清理工具: `tools/productivity/markdown_clean.html`

## 🚀 快速开始

1. 打开首页门户 `index.html`，浏览与搜索所有工具
2. 点击任意工具卡片进入使用（纯前端，无需安装）
3. 如需本地静态服务，可运行：

```bash
./start.sh
# 打开浏览器访问 http://localhost:8000
```

## 🔧 服务端模块：python_execution_engine

一个安全的Python代码执行引擎，支持依赖安装、资源限制、Docker与systemd部署。详见：
- `python_execution_engine/README.md`
- `python_execution_engine/README_FRONTEND.md`

核心接口：`/health`、`/execute`、`/packages`、`/config`。

## 🎨 设计与技术

- 前端：原生 HTML/CSS/JavaScript，CSS变量与响应式布局
- 主题：自动适配暗色/浅色模式
- 门户：搜索过滤、分类统计、快捷访问

## 🔒 隐私

- 所有前端工具均本地运行，不收集、不上传数据

## 🔄 变更记录

### v2.2.0
- 新增首页门户 `index.html`，集中展示全部工具
- 将 HTML 在线预览工具迁移至 `tools/development/html-preview.html`
- 更新 `TOOLS_README.md`/`README.md` 统一工具清单与路径

### v2.1.0
- 新增 SQL 回滚生成工具与多模型支持

### v2.0.0
- 目录重构，分类清晰；统一工具文档

## 🤝 贡献

欢迎提交 Issue 与 PR 来完善工具或新增工具。

## 📄 许可证

MIT License