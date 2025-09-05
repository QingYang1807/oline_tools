# Mermaid 可视化渲染器

一个功能强大的 Mermaid 图表渲染工具，支持将图表渲染为白色背景的图片并直接复制到剪贴板。

## 功能特性

- 🎨 **实时渲染**: 支持多种 Mermaid 图表类型
- 📋 **一键复制**: 将图表复制为白色背景图片到剪贴板
- 💾 **图片下载**: 支持下载高质量 PNG 图片
- 🚀 **快速示例**: 内置多种图表类型示例
- ⌨️ **快捷键支持**: 提高操作效率
- 📱 **响应式设计**: 支持桌面和移动设备

## 支持的图表类型

- **流程图** (Flowchart)
- **时序图** (Sequence Diagram)
- **甘特图** (Gantt Chart)
- **饼图** (Pie Chart)
- **思维导图** (Mindmap)
- **类图** (Class Diagram)
- **状态图** (State Diagram)
- **用户旅程图** (User Journey)
- **Git 图** (Git Graph)

## 使用方法

### 1. 打开工具
直接在浏览器中打开 `mermaid-renderer.html` 文件。

### 2. 输入代码
在左侧编辑器中输入您的 Mermaid 代码，或点击快速示例按钮加载预设示例。

### 3. 渲染图表
点击"🔄 渲染图表"按钮或使用快捷键 `Ctrl+Enter` 来渲染图表。

### 4. 复制图片
点击"📋 复制为图片"按钮或使用快捷键 `Ctrl+S` 将图表复制为白色背景图片到剪贴板。

### 5. 下载图片
点击"💾 下载图片"按钮将图片保存到本地。

## 快捷键

- `Ctrl+Enter`: 渲染图表
- `Ctrl+S`: 复制为图片

## 示例代码

### 流程图
```mermaid
graph TD
    A[开始] --> B{是否登录?}
    B -->|是| C[显示主页]
    B -->|否| D[显示登录页]
    D --> E[用户登录]
    E --> F{登录成功?}
    F -->|是| C
    F -->|否| G[显示错误信息]
    G --> D
    C --> H[结束]
```

### 时序图
```mermaid
sequenceDiagram
    participant U as 用户
    participant F as 前端
    participant B as 后端
    participant D as 数据库
    
    U->>F: 登录请求
    F->>B: 验证用户信息
    B->>D: 查询用户数据
    D-->>B: 返回用户信息
    B-->>F: 返回验证结果
    F-->>U: 显示登录状态
```

### 甘特图
```mermaid
gantt
    title 项目开发计划
    dateFormat  YYYY-MM-DD
    section 需求分析
    需求收集           :done,    des1, 2024-01-01,2024-01-05
    需求分析           :done,    des2, 2024-01-06, 3d
    section 设计阶段
    系统设计           :active,  des3, 2024-01-10, 5d
    界面设计           :         des4, after des3, 3d
    section 开发阶段
    后端开发           :         des5, 2024-01-20, 10d
    前端开发           :         des6, 2024-01-25, 8d
    测试               :         des7, 2024-02-05, 5d
```

## 技术实现

- **Mermaid.js**: 图表渲染引擎
- **html2canvas**: SVG 转图片转换
- **Clipboard API**: 剪贴板操作
- **响应式 CSS**: 现代化界面设计

## 浏览器兼容性

- Chrome 76+
- Firefox 70+
- Safari 13.1+
- Edge 79+

## 注意事项

1. 复制功能需要 HTTPS 环境或 localhost
2. 某些浏览器可能需要用户授权剪贴板访问
3. 大型图表可能需要较长的渲染时间
4. 建议使用现代浏览器以获得最佳体验

## 故障排除

### 复制功能不工作
- 确保在 HTTPS 环境或 localhost 下运行
- 检查浏览器是否支持 Clipboard API
- 尝试手动授权剪贴板访问权限

### 图表渲染失败
- 检查 Mermaid 语法是否正确
- 确保代码格式符合 Mermaid 规范
- 查看浏览器控制台错误信息

### 图片质量问题
- 工具已自动设置 2x 缩放以提高图片质量
- 对于复杂图表，可能需要调整浏览器缩放级别

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本的 Mermaid 图表渲染
- 实现图片复制和下载功能
- 添加多种图表类型示例
- 响应式界面设计