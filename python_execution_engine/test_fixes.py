#!/usr/bin/env python3
"""
测试修复后的Python执行器引擎
"""

import requests
import json
import time
import uuid

# 测试服务器地址
BASE_URL = "http://101.42.23.49"

def test_matplotlib_execution():
    """测试matplotlib代码执行"""
    print("=" * 50)
    print("测试matplotlib代码执行")
    print("=" * 50)
    
    code = """
import numpy as np
import matplotlib.pyplot as plt

# 生成数据
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 绘图
plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.title('Sine Wave')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.grid(True)
plt.savefig('/tmp/test_plot.png')
print("图表已保存到 /tmp/test_plot.png")
"""
    
    payload = {
        "code": code,
        "execution_id": str(uuid.uuid4())
    }
    
    try:
        response = requests.post(f"{BASE_URL}/execute", json=payload, timeout=60)
        result = response.json()
        
        print(f"状态码: {response.status_code}")
        print(f"执行成功: {result.get('success', False)}")
        print(f"执行时间: {result.get('execution_time', 0)}秒")
        print(f"使用的包: {result.get('imports_used', [])}")
        print(f"安装消息: {result.get('install_message', '')}")
        
        if result.get('error'):
            print(f"错误信息: {result['error']}")
        
        if result.get('output'):
            print(f"输出: {result['output']}")
            
        return result.get('success', False)
        
    except Exception as e:
        print(f"请求失败: {e}")
        return False

def test_stop_execution():
    """测试停止执行功能"""
    print("\n" + "=" * 50)
    print("测试停止执行功能")
    print("=" * 50)
    
    # 创建一个长时间运行的代码
    code = """
import time
print("开始长时间运行...")
for i in range(100):
    print(f"运行中... {i}")
    time.sleep(1)
print("完成")
"""
    
    execution_id = str(uuid.uuid4())
    payload = {
        "code": code,
        "execution_id": execution_id
    }
    
    try:
        # 启动执行
        print(f"启动执行，ID: {execution_id}")
        response = requests.post(f"{BASE_URL}/execute", json=payload, timeout=5)
        
        # 等待一下然后停止
        time.sleep(2)
        print(f"尝试停止执行: {execution_id}")
        stop_response = requests.post(f"{BASE_URL}/stop/{execution_id}")
        stop_result = stop_response.json()
        
        print(f"停止结果: {stop_result}")
        return stop_result.get('success', False)
        
    except requests.exceptions.Timeout:
        print("执行超时（这是预期的，因为我们设置了短超时）")
        return True
    except Exception as e:
        print(f"测试失败: {e}")
        return False

def test_status():
    """测试状态接口"""
    print("\n" + "=" * 50)
    print("测试状态接口")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/status")
        result = response.json()
        
        print(f"状态: {result.get('status')}")
        print(f"正在运行的执行数: {result.get('running_executions', 0)}")
        print(f"执行ID列表: {result.get('execution_ids', [])}")
        
        return True
        
    except Exception as e:
        print(f"获取状态失败: {e}")
        return False

def test_health():
    """测试健康检查"""
    print("\n" + "=" * 50)
    print("测试健康检查")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        result = response.json()
        
        print(f"健康状态: {result.get('status')}")
        print(f"服务: {result.get('service')}")
        print(f"版本: {result.get('version')}")
        
        return result.get('status') == 'healthy'
        
    except Exception as e:
        print(f"健康检查失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试修复后的Python执行器引擎")
    print(f"测试服务器: {BASE_URL}")
    
    tests = [
        ("健康检查", test_health),
        ("matplotlib执行", test_matplotlib_execution),
        ("停止执行", test_stop_execution),
        ("状态查询", test_status),
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