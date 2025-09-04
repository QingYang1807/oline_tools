# 网页工具箱

一个轻量的静态网页工具集合。当前内置：

- Mermaid 可视化渲染器：`/tools/mermaid.html`
- Markdown 在线编辑器：`/tools/markdown-editor.html`

## 使用

- 直接用任意静态服务器打开此目录，或拖入浏览器打开 `index.html`。
- Mermaid 页面支持把内容与主题编码到 URL Hash，便于分享。

## 功能

- 目录首页：列出所有工具
- 单页工具：每个工具都有独立 URL
- 护眼黄主题（自动适配系统暗色）
- Mermaid 实时渲染、下载 PNG / SVG / PDF
- Markdown 编辑器：实时预览、PDF 导出、本地保存

## 部署

任意静态托管均可：

- Nginx/Apache 静态目录
- GitHub Pages / Vercel / Netlify

将仓库发布为静态站点即可，入口为 `index.html`。

## 结构

```
/ (根目录)
├── index.html                # 首页（目录）
├── tools/
│   ├── mermaid.html          # Mermaid 工具页面
│   └── markdown-editor.html  # Markdown 编辑器
└── assets/
    └── css/
        ├── style.css         # 主题与样式
        └── markdown-editor.css # Markdown 编辑器样式
```

## 开发

- 采用原生 HTML/CSS/JS，无构建依赖。
- 如需本地预览，可用 Python 简单起一个静态服务器：

```bash
python3 -m http.server 8080 --directory .
```

然后访问 `http://localhost:8080/`。

## 后续扩展建议

- 为每个新工具新增 `tools/xxx.html`，并在 `index.html` 的目录中添加卡片链接。
- 如需共享样式或脚本，放置于 `assets/` 下按需复用。
- 可添加 Service Worker 以支持离线使用。