#!/usr/bin/env python3
"""
测试核心功能（不依赖Flask）
"""

import os
import sys
import tempfile
import subprocess
import time
import uuid
import re
import shutil
from pathlib import Path

# 设置环境变量
mpl_config_dir = "/tmp/mpl_config"
os.environ["MPLCONFIGDIR"] = mpl_config_dir
os.makedirs(mpl_config_dir, exist_ok=True)
os.chmod(mpl_config_dir, 0o777)

pip_cache_dir = "/tmp/pip_cache"
os.environ["PIP_CACHE_DIR"] = pip_cache_dir
os.makedirs(pip_cache_dir, exist_ok=True)
os.chmod(pip_cache_dir, 0o777)

class SimplePythonExecutionEngine:
    """简化的Python执行引擎（用于测试）"""
    
    def __init__(self, base_dir: str = "/tmp/python_execution"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self.max_execution_time = 30
        self.running_processes = {}
        
        # 允许的包列表
        self.allowed_packages = {
            'numpy', 'pandas', 'matplotlib', 'seaborn', 'scipy', 'sklearn',
            'requests', 'beautifulsoup4', 'lxml', 'pillow', 'opencv-python',
            'flask', 'django', 'fastapi', 'sqlalchemy', 'pymongo',
            'jupyter', 'ipython', 'sympy', 'plotly', 'bokeh',
            'tensorflow', 'torch', 'keras', 'xgboost', 'lightgbm',
            'pytest', 'unittest', 'datetime', 'json', 'csv', 'xml',
            'hashlib', 'base64', 'urllib', 'http', 'socket', 'threading',
            'multiprocessing', 'queue', 'collections', 'itertools',
            'functools', 'operator', 'math', 'random', 'statistics',
            'os', 'sys', 'pathlib', 'shutil', 'tempfile', 'glob',
            're', 'string', 'time', 'datetime', 'calendar', 'locale'
        }
    
    def _extract_imports(self, code: str):
        """提取代码中的import语句"""
        imports = []
        
        # 匹配 import 语句
        import_pattern = r'import\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)'
        from_pattern = r'from\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s+import'
        
        for match in re.finditer(import_pattern, code):
            module = match.group(1).split('.')[0]
            imports.append(module)
        
        for match in re.finditer(from_pattern, code):
            module = match.group(1).split('.')[0]
            imports.append(module)
        
        return list(set(imports))
    
    def _install_packages(self, packages, work_dir):
        """安装Python包"""
        if not packages:
            return True, "无需安装包"
        
        # 过滤允许的包
        allowed_packages = [pkg for pkg in packages if pkg in self.allowed_packages]
        if not allowed_packages:
            return True, "所有包都在允许列表中"
        
        try:
            # 创建requirements.txt
            requirements_file = work_dir / "requirements.txt"
            with open(requirements_file, 'w') as f:
                for pkg in allowed_packages:
                    f.write(f"{pkg}\n")
            
            # 设置pip缓存目录为可写目录
            pip_cache_dir = "/tmp/pip_cache"
            os.makedirs(pip_cache_dir, exist_ok=True)
            os.chmod(pip_cache_dir, 0o777)
            
            # 安装包 - 使用root权限和可写缓存目录
            cmd = [
                "sudo", sys.executable, "-m", "pip", "install", 
                "-r", str(requirements_file),
                "--quiet", "--disable-pip-version-check",
                "--cache-dir", pip_cache_dir,
                "--no-user"
            ]
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=60,
                cwd=str(work_dir)
            )
            
            if result.returncode == 0:
                return True, f"成功安装包: {', '.join(allowed_packages)}"
            else:
                # 如果sudo失败，尝试不使用sudo
                print(f"sudo安装失败，尝试普通安装: {result.stderr}")
                cmd_no_sudo = [
                    sys.executable, "-m", "pip", "install", 
                    "-r", str(requirements_file),
                    "--quiet", "--disable-pip-version-check",
                    "--cache-dir", pip_cache_dir,
                    "--no-user"
                ]
                
                result_no_sudo = subprocess.run(
                    cmd_no_sudo, 
                    capture_output=True, 
                    text=True, 
                    timeout=60,
                    cwd=str(work_dir)
                )
                
                if result_no_sudo.returncode == 0:
                    return True, f"成功安装包: {', '.join(allowed_packages)}"
                else:
                    return False, f"安装包失败: {result_no_sudo.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, "包安装超时"
        except Exception as e:
            return False, f"安装包时出错: {str(e)}"
    
    def _execute_code(self, code: str, work_dir: Path, execution_id: str = None):
        """执行Python代码"""
        try:
            # 创建执行脚本
            script_file = work_dir / "main.py"
            with open(script_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # 执行代码
            cmd = [sys.executable, str(script_file)]
            
            # 使用Popen启动进程，以便可以管理
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(work_dir)
            )
            
            # 如果有execution_id，存储进程信息
            if execution_id:
                self.running_processes[execution_id] = process
            
            try:
                # 等待进程完成或超时
                stdout, stderr = process.communicate(timeout=self.max_execution_time)
                
                # 从运行进程列表中移除
                if execution_id and execution_id in self.running_processes:
                    del self.running_processes[execution_id]
                
                return True, stdout, stderr
                
            except subprocess.TimeoutExpired:
                # 超时时终止进程
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                
                # 从运行进程列表中移除
                if execution_id and execution_id in self.running_processes:
                    del self.running_processes[execution_id]
                
                return False, "", f"代码执行超时（{self.max_execution_time}秒）"
            
        except Exception as e:
            # 从运行进程列表中移除
            if execution_id and execution_id in self.running_processes:
                del self.running_processes[execution_id]
            return False, "", f"执行代码时出错: {str(e)}"
    
    def stop_execution(self, execution_id: str):
        """停止正在执行的代码"""
        if execution_id in self.running_processes:
            process = self.running_processes[execution_id]
            try:
                process.terminate()
                process.wait(timeout=5)
                del self.running_processes[execution_id]
                return True
            except subprocess.TimeoutExpired:
                process.kill()
                del self.running_processes[execution_id]
                return True
            except Exception as e:
                print(f"停止进程时出错: {e}")
                return False
        return False
    
    def execute(self, code: str, execution_id: str = None):
        """执行Python代码的主方法"""
        start_time = time.time()
        
        # 如果没有提供execution_id，生成一个
        if not execution_id:
            execution_id = str(uuid.uuid4())
        
        # 创建临时工作目录
        work_dir = Path(tempfile.mkdtemp(dir=self.base_dir))
        
        try:
            # 提取imports
            imports = self._extract_imports(code)
            print(f"检测到导入: {imports}")
            
            # 安装依赖
            install_success, install_msg = self._install_packages(imports, work_dir)
            if not install_success:
                print(f"包安装失败: {install_msg}")
                # 继续执行，可能包已经安装
            
            # 执行代码
            exec_success, stdout, stderr = self._execute_code(code, work_dir, execution_id)
            
            execution_time = time.time() - start_time
            
            return {
                "success": exec_success,
                "output": stdout,
                "error": stderr,
                "execution_time": round(execution_time, 3),
                "imports_used": imports,
                "install_message": install_msg,
                "execution_id": execution_id
            }
            
        finally:
            # 清理临时目录
            try:
                shutil.rmtree(work_dir)
            except Exception as e:
                print(f"清理临时目录失败: {e}")

def test_basic_execution():
    """测试基本代码执行"""
    print("=" * 50)
    print("测试基本代码执行")
    print("=" * 50)
    
    engine = SimplePythonExecutionEngine()
    
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
    
    engine = SimplePythonExecutionEngine()
    
    code = """
import os
import sys
import json
from pathlib import Path

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
    
    engine = SimplePythonExecutionEngine()
    
    # 创建一个长时间运行的代码
    code = """
import time
print("开始长时间运行...")
for i in range(5):
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
    print("开始本地测试修复后的Python执行器引擎核心功能")
    
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