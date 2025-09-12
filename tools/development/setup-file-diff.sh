#!/bin/bash

# 智能文件对比工具安装脚本

echo "🔍 智能文件对比工具安装向导"
echo "=================================="

# 检查Python版本
python_version=$(python3 --version 2>/dev/null | grep -o "[0-9]\+\.[0-9]\+")
if [ -z "$python_version" ]; then
    echo "❌ 错误: 未找到Python 3"
    echo "请先安装Python 3.8或更高版本"
    exit 1
fi

echo "✅ 检测到Python版本: $python_version"

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误: 未找到pip3"
    echo "请先安装pip3"
    exit 1
fi

echo "✅ pip3 已安装"

# 创建虚拟环境（可选）
read -p "是否创建虚拟环境？(推荐) [y/N]: " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "🔧 创建虚拟环境..."
    python3 -m venv file_diff_env
    
    echo "🔧 激活虚拟环境..."
    source file_diff_env/bin/activate
    
    echo "✅ 虚拟环境已创建并激活"
    echo "💡 下次使用时请运行: source file_diff_env/bin/activate"
fi

# 安装基础依赖
echo "📦 安装基础依赖..."
pip3 install flask flask-cors

# 检查是否需要安装文档解析库
echo ""
echo "📄 文档解析库安装选项:"
echo "1. 基础版 - 只支持文本文件"
echo "2. 标准版 - 支持PDF、Word、Excel"
echo "3. 完整版 - 支持所有格式 + 高级功能"

read -p "请选择安装版本 [1/2/3]: " install_option

case $install_option in
    1)
        echo "✅ 基础版安装完成"
        ;;
    2)
        echo "📦 安装标准版依赖..."
        pip3 install PyPDF2 python-docx openpyxl markdown beautifulsoup4
        ;;
    3)
        echo "📦 安装完整版依赖..."
        pip3 install -r requirements-diff.txt
        ;;
    *)
        echo "⚠️ 无效选择，安装基础版"
        ;;
esac

# 运行测试
echo ""
read -p "是否运行功能测试？[y/N]: " run_test
if [[ $run_test =~ ^[Yy]$ ]]; then
    echo "🧪 运行功能测试..."
    python3 test-file-diff.py
fi

echo ""
echo "🎉 安装完成！"
echo ""
echo "📖 使用方法:"
echo "1. 网页版: 在浏览器中打开 advanced-file-diff.html"
echo "2. 命令行: python3 file-diff-server.py file1.txt file2.txt"
echo "3. API服务: python3 -c \"from file_diff_server import *; api = FileDiffAPI(); print('API服务已启动')\""
echo ""
echo "📚 查看详细文档: cat README-FileDiff.md"
echo ""
echo "✨ 享受智能文件对比的便捷体验！"