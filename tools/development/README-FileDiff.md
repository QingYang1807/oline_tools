# 🔍 智能文件对比工具

一个功能强大、支持多种文件格式的智能文件对比工具，提供直观的差异展示和丰富的导出选项。

## ✨ 核心特性

### 📄 多格式文件支持
- **PDF文档** - 自动提取文本内容进行对比
- **Word文档** (.doc, .docx) - 支持复杂格式文档
- **Excel表格** (.xls, .xlsx) - 按工作表对比数据
- **Markdown文件** - 保持格式的智能对比
- **代码文件** - 支持各种编程语言
- **纯文本文件** - 通用文本文件支持

### 🎯 智能对比模式
- **逐行对比** - 传统的行级别差异分析
- **单词对比** - 更细粒度的词汇级别对比
- **字符对比** - 最精确的字符级别对比
- **语义对比** - 基于句子的语义级别对比

### 🎨 直观的差异展示
- **颜色标记** - 新增、删除、修改内容用不同颜色标识
- **行号显示** - 可选的行号显示功能
- **统计信息** - 详细的变更统计和相似度分析
- **响应式设计** - 适配各种屏幕尺寸

### 💾 强大的导出功能
- **HTML报告** - 带样式的完整对比报告
- **纯文本** - 简洁的文本格式导出
- **JSON数据** - 结构化数据格式
- **PDF报告** - 专业的PDF格式报告（开发中）

### 🔧 高级功能
- **拖拽上传** - 支持文件拖拽上传
- **文件夹对比** - 批量对比整个文件夹
- **版本历史** - 保存和管理对比历史
- **自定义设置** - 丰富的对比选项配置

## 🚀 快速开始

### 在线使用
直接打开 `advanced-file-diff.html` 文件即可在浏览器中使用。

### 本地部署
1. 下载所有文件到本地
2. 在浏览器中打开 `advanced-file-diff.html`
3. 开始使用！

### 命令行使用
如需使用高级功能（文件夹对比、版本历史等），需要安装Python依赖：

```bash
# 安装依赖
pip install -r requirements-diff.txt

# 命令行对比两个文件
python file-diff-server.py file1.txt file2.txt

# 指定对比模式和输出格式
python file-diff-server.py file1.txt file2.txt --mode word --format html --output report.html

# 忽略空白字符和大小写
python file-diff-server.py file1.txt file2.txt --ignore-whitespace --ignore-case
```

## 📖 使用指南

### 基本使用步骤

1. **上传文件**
   - 点击"选择文件"按钮或直接拖拽文件到上传区域
   - 支持同时上传两个不同格式的文件

2. **配置对比选项**
   - 选择对比模式（逐行、单词、字符、语义）
   - 设置忽略选项（空白字符、大小写）
   - 选择显示选项（行号、自动换行等）

3. **执行对比**
   - 点击"开始对比"按钮
   - 系统自动解析文件并生成对比结果

4. **查看结果**
   - 查看详细的统计信息
   - 浏览彩色标记的差异内容
   - 使用控制按钮调整显示效果

5. **导出结果**
   - 选择合适的导出格式
   - 下载对比报告到本地

### 高级功能使用

#### 文件夹对比
```python
from file_diff_server import FileDiffAPI

api = FileDiffAPI()
result = api.compare_folders(
    'folder1', 
    'folder2',
    recursive=True,
    include_patterns=['*.py', '*.js'],
    exclude_patterns=['__pycache__', 'node_modules']
)
```

#### 版本历史管理
```python
# 保存对比历史
comparison_id = api.history.save_comparison(
    'file1.txt', 
    'file2.txt', 
    diff_result, 
    notes='重要的功能更新对比'
)

# 查看历史记录
history = api.history.get_comparison_history(limit=20)
```

## 🎯 支持的文件类型

| 文件类型 | 扩展名 | 解析方式 | 特殊功能 |
|---------|--------|----------|----------|
| PDF | .pdf | 文本提取 | 自动处理多页内容 |
| Word | .doc, .docx | 段落解析 | 保持文档结构 |
| Excel | .xls, .xlsx | 工作表解析 | 按表格对比数据 |
| Markdown | .md | 原始格式 | 保持标记语法 |
| 代码文件 | .py, .js, .java等 | 语法高亮 | 代码结构感知 |
| 文本文件 | .txt, .log等 | 直接读取 | 自动编码检测 |

## ⚙️ 配置选项

### 对比模式说明
- **逐行对比**: 适合大多数文本文件，性能最佳
- **单词对比**: 适合文档内容对比，能发现词汇级变化
- **字符对比**: 最精确的对比，适合代码文件
- **语义对比**: 基于句子的对比，适合自然语言文本

### 忽略选项
- **忽略空白字符**: 忽略空格、制表符、换行符的差异
- **忽略大小写**: 不区分大小写进行对比

### 显示选项
- **显示行号**: 在差异展示中显示行号
- **自动换行**: 长行内容自动换行显示

## 🔧 技术架构

### 前端技术栈
- **HTML5** - 现代化的网页结构
- **CSS3** - 响应式设计和动画效果
- **JavaScript ES6+** - 交互逻辑和文件处理
- **外部库**:
  - PDF.js - PDF文件解析
  - Mammoth.js - Word文档解析
  - SheetJS - Excel文件解析
  - Marked.js - Markdown解析
  - Diff.js - 文本对比算法

### 后端技术栈（可选）
- **Python 3.8+** - 核心处理引擎
- **Flask** - Web框架（用于API服务）
- **SQLite** - 历史记录存储
- **文档解析库**:
  - PyPDF2 - PDF解析
  - python-docx - Word文档
  - openpyxl - Excel表格

## 🎨 界面特色

### 现代化设计
- **深色/浅色主题** - 支持主题切换
- **渐变色彩** - 美观的视觉效果
- **卡片式布局** - 清晰的信息层次
- **动画过渡** - 流畅的交互体验

### 用户体验优化
- **拖拽上传** - 直观的文件上传方式
- **实时预览** - 文件信息即时显示
- **进度指示** - 处理状态实时反馈
- **错误处理** - 友好的错误提示信息

## 📊 性能优化

### 文件处理优化
- **流式读取** - 大文件分块处理
- **缓存机制** - 避免重复解析
- **异步处理** - 不阻塞用户界面
- **内存管理** - 及时释放资源

### 对比算法优化
- **增量对比** - 只对比变化部分
- **并行处理** - 多线程加速计算
- **结果缓存** - 相同文件复用结果
- **智能匹配** - 优化的相似度算法

## 🛠️ 扩展开发

### 添加新的文件格式支持
```python
def parse_custom_format(file_path: str) -> str:
    """解析自定义格式文件"""
    # 实现解析逻辑
    return extracted_text

# 注册到解析器
FileParser.register_parser('.custom', parse_custom_format)
```

### 自定义对比算法
```python
def custom_diff_algorithm(text1: str, text2: str) -> List[str]:
    """自定义对比算法"""
    # 实现对比逻辑
    return diff_result

# 注册到引擎
DiffEngine.register_algorithm('custom', custom_diff_algorithm)
```

## 🤝 贡献指南

欢迎提交问题报告、功能请求和代码贡献！

### 开发环境设置
```bash
# 克隆项目
git clone <repository-url>

# 安装依赖
pip install -r requirements-diff.txt

# 运行测试
pytest tests/

# 代码格式化
black file-diff-server.py
```

## 📄 许可证

本项目采用 MIT 许可证，详情请查看 LICENSE 文件。

## 🔗 相关链接

- [在线演示](./advanced-file-diff.html)
- [问题反馈](https://github.com/your-repo/issues)
- [功能请求](https://github.com/your-repo/discussions)

---

**🎉 享受智能文件对比的便捷体验！**