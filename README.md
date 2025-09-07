# 二维码解析工具

一个简单易用的二维码解析工具，支持通过粘贴（Ctrl+V / Cmd+V）或上传图片来解析二维码内容。

## 功能特性

- 🔍 **多种输入方式**：支持粘贴、拖拽、文件选择
- ⌨️ **快捷键支持**：Ctrl+V（Windows/Linux）或 Cmd+V（Mac）
- 📱 **智能识别**：自动识别URL链接并提供打开功能
- 📋 **一键复制**：解析结果可一键复制到剪贴板
- 🎨 **现代界面**：响应式设计，支持移动端
- ⚡ **快速解析**：使用高效的jsQR库进行解析

## 使用方法

### 1. 粘贴二维码图片
- 复制二维码图片到剪贴板
- 在页面上按 `Ctrl+V`（Windows/Linux）或 `Cmd+V`（Mac）
- 工具会自动解析并显示结果

### 2. 拖拽上传
- 直接将二维码图片拖拽到上传区域
- 松开鼠标即可开始解析

### 3. 文件选择
- 点击"选择文件"按钮
- 从文件管理器中选择二维码图片

## 支持的格式

- 常见图片格式：PNG、JPG、JPEG、GIF、BMP、WebP
- 文件大小限制：最大10MB
- 二维码类型：URL链接、纯文本、WiFi信息等

## 快捷键

- `Ctrl+V` / `Cmd+V`：粘贴剪贴板中的图片
- `Enter`：在结果区域时打开链接
- `Esc`：清除所有内容

## 技术实现

- **前端框架**：原生JavaScript（ES6+）
- **二维码解析**：jsQR库
- **样式**：CSS3 with Flexbox/Grid
- **兼容性**：现代浏览器（支持Clipboard API）

## 浏览器兼容性

- Chrome 66+
- Firefox 63+
- Safari 13.1+
- Edge 79+

## 本地运行

1. 下载所有文件到本地目录
2. 使用HTTP服务器运行（不能直接打开HTML文件）
3. 推荐使用Live Server或Python简单服务器：

```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000

# Node.js (需要安装http-server)
npx http-server
```

然后访问 `http://localhost:8000`

## 文件结构

```
├── index.html          # 主页面
├── styles.css          # 样式文件
├── script.js           # JavaScript逻辑
└── README.md           # 说明文档
```

## 注意事项

1. 需要HTTPS环境或localhost才能使用剪贴板API
2. 图片质量会影响解析成功率
3. 建议使用清晰的二维码图片以获得最佳效果

## 更新日志

### v1.0.0
- 初始版本发布
- 支持粘贴、拖拽、文件上传
- 集成jsQR解析库
- 响应式设计
- 错误处理和用户反馈