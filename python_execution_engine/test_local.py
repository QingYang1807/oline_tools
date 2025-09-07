#!/usr/bin/env python3
"""
本地测试修复后的Python执行器引擎
"""

import os
import sys
import tempfile
import subprocess
import time
import uuid
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置环境变量
mpl_config_dir = "/tmp/mpl_config"
os.environ["MPLCONFIGDIR"] = mpl_config_dir
os.makedirs(mpl_config_dir, exist_ok=True)
os.chmod(mpl_config_dir, 0o777)

pip_cache_dir = "/tmp/pip_cache"
os.environ["PIP_CACHE_DIR"] = pip_cache_dir
os.makedirs(pip_cache_dir, exist_ok=True)
os.chmod(pip_cache_dir, 0o777)

# 导入我们的执行引擎
from app import PythonExecutionEngine

def test_basic_execution():
    """测试基本代码执行"""
    print("=" * 50)
    print("测试基本代码执行")
    print("=" * 50)
    
    engine = PythonExecutionEngine()
    
    code = """
print("Hello, World!")
print("Python执行器引擎测试成功！")
"""
    
    result = engine.execute(code)
    
    print(f"执行成功: {result['success']}")
    print(f"执行时间: {result['execution_time']}秒")
    print(f"输出: {result['output']}")
    if result['error']:
        print(f"错误: {result['error']}")
    
    return result['success']

def test_import_detection():
    """测试import检测"""
    print("\n" + "=" * 50)
    print("测试import检测")
    print("=" * 50)
    
    engine = PythonExecutionEngine()
    
    code = """
import os
import sys
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

print("导入测试完成")
"""
    
    result = engine.execute(code)
    
    print(f"执行成功: {result['success']}")
    print(f"检测到的导入: {result['imports_used']}")
    print(f"安装消息: {result['install_message']}")
    
    return result['success']

def test_process_management():
    """测试进程管理"""
    print("\n" + "=" * 50)
    print("测试进程管理")
    print("=" * 50)
    
    engine = PythonExecutionEngine()
    
    # 创建一个长时间运行的代码
    code = """
import time
print("开始长时间运行...")
for i in range(10):
    print(f"运行中... {i}")
    time.sleep(0.5)
print("完成")
"""
    
    execution_id = str(uuid.uuid4())
    print(f"执行ID: {execution_id}")
    
    # 在后台启动执行
    import threading
    
    def run_code():
        result = engine.execute(code, execution_id)
        print(f"执行结果: {result['success']}")
        if result['error']:
            print(f"错误: {result['error']}")
    
    thread = threading.Thread(target=run_code)
    thread.start()
    
    # 等待一下然后停止
    time.sleep(1)
    print(f"尝试停止执行: {execution_id}")
    success = engine.stop_execution(execution_id)
    print(f"停止结果: {success}")
    
    thread.join()
    
    return success

def test_directory_permissions():
    """测试目录权限"""
    print("\n" + "=" * 50)
    print("测试目录权限")
    print("=" * 50)
    
    # 检查matplotlib配置目录
    mpl_dir = Path("/tmp/mpl_config")
    if mpl_dir.exists():
        stat = mpl_dir.stat()
        print(f"matplotlib配置目录权限: {oct(stat.st_mode)}")
        print(f"目录可写: {os.access(mpl_dir, os.W_OK)}")
    else:
        print("❌ matplotlib配置目录不存在")
        return False
    
    # 检查pip缓存目录
    pip_dir = Path("/tmp/pip_cache")
    if pip_dir.exists():
        stat = pip_dir.stat()
        print(f"pip缓存目录权限: {oct(stat.st_mode)}")
        print(f"目录可写: {os.access(pip_dir, os.W_OK)}")
    else:
        print("❌ pip缓存目录不存在")
        return False
    
    return True

def main():
    """主测试函数"""
    print("开始本地测试修复后的Python执行器引擎")
    
    tests = [
        ("目录权限", test_directory_permissions),
        ("基本执行", test_basic_execution),
        ("导入检测", test_import_detection),
        ("进程管理", test_process_management),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n正在运行测试: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"测试 {test_name}: {'通过' if result else '失败'}")
        except Exception as e:
            print(f"测试 {test_name} 异常: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "通过" if result else "失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{len(results)} 个测试通过")
    
    if passed == len(results):
        print("🎉 所有测试都通过了！")
    else:
        print("❌ 部分测试失败，请检查日志")

if __name__ == "__main__":
    main()