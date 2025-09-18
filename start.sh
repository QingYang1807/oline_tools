#!/bin/bash

# HTML代码在线预览工具启动脚本

echo "🚀 启动HTML代码在线预览工具..."
echo "📁 工作目录: $(pwd)"
echo "🌐 服务器地址: http://localhost:8000"
echo "📄 主页面: http://localhost:8000/index.html"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "================================"

# 检查Python是否可用
if command -v python3 &> /dev/null; then
    python3 -m http.server 8000
elif command -v python &> /dev/null; then
    python -m http.server 8000
else
    echo "❌ 错误: 未找到Python解释器"
    echo "请安装Python 3.x"
    exit 1
fi