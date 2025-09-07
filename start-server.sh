#!/bin/bash

echo "🚀 启动二维码解析工具服务器..."
echo ""
echo "选择启动方式："
echo "1) Python 3 (推荐)"
echo "2) Python 2"
echo "3) Node.js (需要安装http-server)"
echo ""

read -p "请选择 (1-3): " choice

case $choice in
    1)
        echo "使用 Python 3 启动服务器..."
        echo "访问地址: http://localhost:8000"
        echo "按 Ctrl+C 停止服务器"
        python3 -m http.server 8000
        ;;
    2)
        echo "使用 Python 2 启动服务器..."
        echo "访问地址: http://localhost:8000"
        echo "按 Ctrl+C 停止服务器"
        python -m SimpleHTTPServer 8000
        ;;
    3)
        echo "使用 Node.js 启动服务器..."
        echo "访问地址: http://localhost:8080"
        echo "按 Ctrl+C 停止服务器"
        npx http-server -p 8080
        ;;
    *)
        echo "无效选择，使用 Python 3 启动..."
        python3 -m http.server 8000
        ;;
esac