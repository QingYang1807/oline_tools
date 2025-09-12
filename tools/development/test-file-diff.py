#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能文件对比工具测试脚本
用于验证各种文件格式的解析和对比功能
"""

import os
import sys
import tempfile
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from file_diff_server import FileDiffAPI, FileParser, DiffEngine
    print("✅ 成功导入文件对比模块")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请先安装依赖: pip install -r requirements-diff.txt")
    sys.exit(1)

def create_test_files():
    """创建测试文件"""
    test_dir = tempfile.mkdtemp(prefix="file_diff_test_")
    print(f"📁 创建测试目录: {test_dir}")
    
    # 创建文本文件1
    text1 = """# 项目介绍
这是一个示例项目。

## 功能特性
- 用户管理
- 数据分析
- 报表生成

## 技术栈
- Frontend: React
- Backend: Node.js
- Database: MongoDB

## 安装说明
1. 克隆仓库
2. 安装依赖
3. 启动服务"""

    # 创建文本文件2
    text2 = """# 项目介绍
这是一个示例项目，用于演示文件对比功能。

## 功能特性
- 用户管理系统
- 高级数据分析
- 报表生成工具
- 权限控制

## 技术栈
- Frontend: React + TypeScript
- Backend: Node.js + Express
- Database: PostgreSQL
- Cache: Redis

## 安装说明
1. 克隆仓库到本地
2. 安装项目依赖
3. 配置环境变量
4. 启动开发服务器"""

    file1_path = os.path.join(test_dir, "test1.md")
    file2_path = os.path.join(test_dir, "test2.md")
    
    with open(file1_path, 'w', encoding='utf-8') as f:
        f.write(text1)
    
    with open(file2_path, 'w', encoding='utf-8') as f:
        f.write(text2)
    
    print(f"📝 创建测试文件:")
    print(f"   - {file1_path}")
    print(f"   - {file2_path}")
    
    return file1_path, file2_path, test_dir

def test_file_parsing():
    """测试文件解析功能"""
    print("\n🔍 测试文件解析功能...")
    
    file1_path, file2_path, test_dir = create_test_files()
    
    try:
        # 测试文件1解析
        result1 = FileParser.parse_file(file1_path)
        print(f"📄 文件1解析结果:")
        print(f"   - 成功: {result1['success']}")
        print(f"   - 类型: {result1['file_type']}")
        print(f"   - 大小: {result1['file_size']} 字节")
        print(f"   - 行数: {result1['line_count']}")
        print(f"   - 字符数: {result1['char_count']}")
        
        # 测试文件2解析
        result2 = FileParser.parse_file(file2_path)
        print(f"📄 文件2解析结果:")
        print(f"   - 成功: {result2['success']}")
        print(f"   - 类型: {result2['file_type']}")
        print(f"   - 大小: {result2['file_size']} 字节")
        print(f"   - 行数: {result2['line_count']}")
        print(f"   - 字符数: {result2['char_count']}")
        
        return True, file1_path, file2_path, test_dir
        
    except Exception as e:
        print(f"❌ 文件解析测试失败: {e}")
        return False, None, None, None

def test_diff_engine():
    """测试对比引擎"""
    print("\n⚙️ 测试对比引擎...")
    
    success, file1_path, file2_path, test_dir = test_file_parsing()
    if not success:
        return False
    
    try:
        # 读取文件内容
        with open(file1_path, 'r', encoding='utf-8') as f:
            text1 = f.read()
        
        with open(file2_path, 'r', encoding='utf-8') as f:
            text2 = f.read()
        
        # 测试不同对比模式
        modes = ['line', 'word', 'char', 'semantic']
        
        for mode in modes:
            print(f"\n🔄 测试 {mode} 模式对比:")
            result = DiffEngine.compare_texts(text1, text2, mode=mode)
            
            stats = result['stats']
            print(f"   - 新增: {stats['added']}")
            print(f"   - 删除: {stats['removed']}")
            print(f"   - 修改: {stats['modified']}")
            print(f"   - 总变更: {stats['total_changes']}")
            print(f"   - 相似度: {stats['similarity']}%")
        
        return True, file1_path, file2_path, test_dir
        
    except Exception as e:
        print(f"❌ 对比引擎测试失败: {e}")
        return False, None, None, None

def test_api_integration():
    """测试API集成"""
    print("\n🔗 测试API集成...")
    
    success, file1_path, file2_path, test_dir = test_diff_engine()
    if not success:
        return False
    
    try:
        api = FileDiffAPI()
        
        # 测试文件对比API
        result = api.compare_files(
            file1_path, 
            file2_path,
            mode='line',
            ignore_whitespace=False,
            ignore_case=False,
            notes='API集成测试'
        )
        
        print(f"📊 API对比结果:")
        print(f"   - 成功: {result['success']}")
        print(f"   - 对比ID: {result.get('comparison_id', 'N/A')}")
        print(f"   - 时间戳: {result.get('timestamp', 'N/A')}")
        
        if result['success']:
            stats = result['diff']['stats']
            print(f"   - 统计信息:")
            print(f"     * 相似度: {stats['similarity']}%")
            print(f"     * 总变更: {stats['total_changes']}")
        
        # 测试导出功能
        print(f"\n💾 测试导出功能:")
        
        # 导出为HTML
        html_content = api.export_comparison(result, 'html')
        html_file = os.path.join(test_dir, 'comparison_report.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"   ✅ HTML报告: {html_file}")
        
        # 导出为文本
        text_content = api.export_comparison(result, 'text')
        text_file = os.path.join(test_dir, 'comparison_report.txt')
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text_content)
        print(f"   ✅ 文本报告: {text_file}")
        
        # 导出为JSON
        json_content = api.export_comparison(result, 'json')
        json_file = os.path.join(test_dir, 'comparison_report.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write(json_content)
        print(f"   ✅ JSON数据: {json_file}")
        
        return True, test_dir
        
    except Exception as e:
        print(f"❌ API集成测试失败: {e}")
        return False, None

def test_history_management():
    """测试历史记录管理"""
    print("\n📚 测试历史记录管理...")
    
    try:
        api = FileDiffAPI()
        
        # 获取历史记录
        history_result = api.get_history(limit=10)
        
        print(f"📋 历史记录:")
        print(f"   - 成功: {history_result['success']}")
        
        if history_result['success']:
            history = history_result['history']
            print(f"   - 记录数量: {len(history)}")
            
            for i, record in enumerate(history[:3], 1):
                print(f"   - 记录 {i}:")
                print(f"     * 时间: {record['timestamp']}")
                print(f"     * 文件1: {record['file1_name']}")
                print(f"     * 文件2: {record['file2_name']}")
                if record['stats']:
                    print(f"     * 相似度: {record['stats'].get('similarity', 'N/A')}%")
        
        return True
        
    except Exception as e:
        print(f"❌ 历史记录管理测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始智能文件对比工具测试")
    print("=" * 50)
    
    try:
        # 测试各个组件
        success_parsing = test_file_parsing()[0]
        success_diff = test_diff_engine()[0] if success_parsing else False
        success_api, test_dir = test_api_integration() if success_diff else (False, None)
        success_history = test_history_management() if success_api else False
        
        print("\n" + "=" * 50)
        print("📊 测试结果总结:")
        print(f"   ✅ 文件解析: {'通过' if success_parsing else '失败'}")
        print(f"   ✅ 对比引擎: {'通过' if success_diff else '失败'}")
        print(f"   ✅ API集成: {'通过' if success_api else '失败'}")
        print(f"   ✅ 历史管理: {'通过' if success_history else '失败'}")
        
        if test_dir:
            print(f"\n📁 测试文件位置: {test_dir}")
            print("   可以查看生成的报告文件")
        
        overall_success = all([success_parsing, success_diff, success_api, success_history])
        
        if overall_success:
            print("\n🎉 所有测试通过！文件对比工具运行正常。")
            return 0
        else:
            print("\n⚠️ 部分测试失败，请检查错误信息。")
            return 1
            
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        return 1

if __name__ == "__main__":
    exit(main())