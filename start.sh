#!/bin/bash

# 工具箱启动脚本
echo "🚀 启动工具箱..."
echo ""

# 检查Python版本
if command -v python3 &> /dev/null; then
    echo "使用 Python 3 启动服务器..."
    python3 -m http.server 8000
elif command -v python &> /dev/null; then
    echo "使用 Python 2 启动服务器..."
    python -m SimpleHTTPServer 8000
else
    echo "❌ 未找到Python，请安装Python后重试"
    echo ""
    echo "或者使用Node.js:"
    echo "npx http-server"
    exit 1
fi