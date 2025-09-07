#!/usr/bin/env python3
"""
API测试脚本
"""

import requests
import json
import time

# 服务地址
BASE_URL = "http://localhost:5000"

def test_health():
    """测试健康检查接口"""
    print("测试健康检查接口...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"健康检查失败: {e}")
        return False

def test_execute_simple():
    """测试简单代码执行"""
    print("\n测试简单代码执行...")
    code = """
print("Hello, World!")
result = 2 + 3
print(f"2 + 3 = {result}")
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/execute",
            json={"code": code},
            headers={"Content-Type": "application/json"}
        )
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"执行成功: {result['success']}")
        print(f"输出: {result['output']}")
        if result['error']:
            print(f"错误: {result['error']}")
        print(f"执行时间: {result['execution_time']}秒")
        return result['success']
    except Exception as e:
        print(f"代码执行失败: {e}")
        return False

def test_execute_with_imports():
    """测试带导入的代码执行"""
    print("\n测试带导入的代码执行...")
    code = """
import math
import datetime

print("数学计算:")
print(f"π = {math.pi}")
print(f"√2 = {math.sqrt(2)}")

print("\\n当前时间:")
now = datetime.datetime.now()
print(f"现在时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/execute",
            json={"code": code},
            headers={"Content-Type": "application/json"}
        )
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"执行成功: {result['success']}")
        print(f"输出: {result['output']}")
        if result['error']:
            print(f"错误: {result['error']}")
        print(f"使用的导入: {result.get('imports_used', [])}")
        print(f"安装信息: {result.get('install_message', '')}")
        return result['success']
    except Exception as e:
        print(f"代码执行失败: {e}")
        return False

def test_execute_error():
    """测试错误代码执行"""
    print("\n测试错误代码执行...")
    code = """
print("这行会正常执行")
# 故意制造错误
undefined_variable = some_undefined_function()
print("这行不会执行")
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/execute",
            json={"code": code},
            headers={"Content-Type": "application/json"}
        )
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"执行成功: {result['success']}")
        print(f"输出: {result['output']}")
        if result['error']:
            print(f"错误: {result['error']}")
        return not result['success']  # 期望执行失败
    except Exception as e:
        print(f"代码执行失败: {e}")
        return False

def test_dangerous_code():
    """测试危险代码检测"""
    print("\n测试危险代码检测...")
    code = """
import os
os.system("echo 'This should be blocked'")
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/execute",
            json={"code": code},
            headers={"Content-Type": "application/json"}
        )
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"执行成功: {result['success']}")
        print(f"输出: {result['output']}")
        if result['error']:
            print(f"错误: {result['error']}")
        return not result['success']  # 期望执行失败
    except Exception as e:
        print(f"代码执行失败: {e}")
        return False

def test_packages_list():
    """测试包列表接口"""
    print("\n测试包列表接口...")
    try:
        response = requests.get(f"{BASE_URL}/packages")
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"允许的包数量: {result['total_count']}")
        print(f"前10个包: {result['allowed_packages'][:10]}")
        return response.status_code == 200
    except Exception as e:
        print(f"获取包列表失败: {e}")
        return False

def test_config():
    """测试配置接口"""
    print("\n测试配置接口...")
    try:
        response = requests.get(f"{BASE_URL}/config")
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"最大执行时间: {result['max_execution_time']}秒")
        print(f"最大内存: {result['max_memory_mb']}MB")
        print(f"允许的包数量: {result['allowed_packages_count']}")
        return response.status_code == 200
    except Exception as e:
        print(f"获取配置失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("Python执行引擎API测试")
    print("=" * 50)
    
    tests = [
        ("健康检查", test_health),
        ("简单代码执行", test_execute_simple),
        ("带导入的代码执行", test_execute_with_imports),
        ("错误代码执行", test_execute_error),
        ("危险代码检测", test_dangerous_code),
        ("包列表接口", test_packages_list),
        ("配置接口", test_config),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                print(f"✅ {test_name} 通过")
                passed += 1
            else:
                print(f"❌ {test_name} 失败")
        except Exception as e:
            print(f"❌ {test_name} 异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    print("=" * 50)
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败，请检查服务状态")

if __name__ == "__main__":
    main()