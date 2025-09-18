# 工具箱门户

一个简约、好用、适配大中小屏的静态门户首页，聚合仓库内各类轻量工具。原先放在根目录的 HTML 预览工具已迁移至开发工具分类目录。

## 访问入口

- 门户首页：打开仓库根目录 `index.html`
- HTML 代码在线预览工具：`tools/development/html-preview/index.html`
- 工具聚合页（旧版视觉）：`tools-portal.html`

## 目录结构

```
/workspace/
├── index.html                         # 全新门户首页（自适应多设备）
├── tools/
│   └── development/
│       └── html-preview/
│           ├── index.html            # HTML 预览工具页面
│           ├── examples.js           # 示例代码
│           ├── README.md             # 工具说明（原根目录）
│           └── 使用说明.md           # 使用说明（原根目录）
├── assets/
│   └── css/
│       └── style.css                 # 门户通用样式
└── tools-portal.html                 # 旧版工具门户（保留，可访问）
```

## 快捷键

- Ctrl/⌘ + K：聚焦搜索框
- ESC：清空搜索并移除焦点

## 说明

- 所有工具均为纯前端实现，无需安装，隐私友好。
- 如果你在 `tools-portal.html` 中使用“HTML预览工具”入口，已自动跳转到新位置。

## 开发

- 样式复用 `assets/css/style.css`，请保持风格一致。
- 新增工具时建议在相应分类目录下创建文件并在首页添加入口。