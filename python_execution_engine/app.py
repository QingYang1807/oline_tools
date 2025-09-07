#!/usr/bin/env python3
"""
Python代码执行引擎服务
提供安全的Python代码执行API，支持自动依赖安装
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
import re
import time
import signal
import threading
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class PythonExecutionEngine:
    """Python代码执行引擎"""
    
    def __init__(self, base_dir: str = "/tmp/python_execution"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self.max_execution_time = 30  # 最大执行时间（秒）
        self.max_memory_mb = 512      # 最大内存使用（MB）
        
        # 允许的包列表（安全考虑）
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
        
        # 危险函数和模块黑名单
        self.dangerous_patterns = [
            r'__import__\s*\(',
            r'exec\s*\(',
            r'eval\s*\(',
            r'compile\s*\(',
            r'open\s*\([^)]*[\'"]w[\'"]',
            r'file\s*\(',
            r'input\s*\(',
            r'raw_input\s*\(',
            r'os\.system',
            r'subprocess\.[a-zA-Z_]+',
            r'import\s+os\s*$',
            r'from\s+os\s+import',
            r'import\s+subprocess',
            r'from\s+subprocess\s+import',
            r'import\s+sys\s*$',
            r'from\s+sys\s+import',
            r'import\s+shutil',
            r'from\s+shutil\s+import',
        ]
    
    def _check_code_safety(self, code: str) -> Tuple[bool, str]:
        """检查代码安全性"""
        # 检查危险模式
        for pattern in self.dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
                return False, f"检测到危险代码模式: {pattern}"
        
        # 检查文件操作
        if re.search(r'open\s*\(', code) and not re.search(r'open\s*\([^)]*[\'"]r[\'"]', code):
            return False, "不允许写入文件操作"
        
        return True, "代码安全检查通过"
    
    def _extract_imports(self, code: str) -> List[str]:
        """提取代码中的import语句"""
        imports = []
        
        # 匹配 import 语句
        import_pattern = r'import\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)'
        from_pattern = r'from\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s+import'
        
        for match in re.finditer(import_pattern, code):
            module = match.group(1).split('.')[0]  # 只取主模块名
            imports.append(module)
        
        for match in re.finditer(from_pattern, code):
            module = match.group(1).split('.')[0]  # 只取主模块名
            imports.append(module)
        
        return list(set(imports))  # 去重
    
    def _install_packages(self, packages: List[str], work_dir: Path) -> Tuple[bool, str]:
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
            
            # 安装包
            cmd = [
                sys.executable, "-m", "pip", "install", 
                "-r", str(requirements_file),
                "--user", "--quiet", "--disable-pip-version-check"
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
                return False, f"安装包失败: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, "包安装超时"
        except Exception as e:
            return False, f"安装包时出错: {str(e)}"
    
    def _execute_code(self, code: str, work_dir: Path) -> Tuple[bool, str, str]:
        """执行Python代码"""
        try:
            # 创建执行脚本
            script_file = work_dir / "main.py"
            with open(script_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # 执行代码
            cmd = [sys.executable, str(script_file)]
            
            # 使用超时执行
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.max_execution_time,
                cwd=str(work_dir)
            )
            
            return True, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            return False, "", f"代码执行超时（{self.max_execution_time}秒）"
        except Exception as e:
            return False, "", f"执行代码时出错: {str(e)}"
    
    def execute(self, code: str) -> Dict:
        """执行Python代码的主方法"""
        start_time = time.time()
        
        # 安全检查
        is_safe, safety_msg = self._check_code_safety(code)
        if not is_safe:
            return {
                "success": False,
                "output": "",
                "error": f"安全检查失败: {safety_msg}",
                "execution_time": time.time() - start_time
            }
        
        # 创建临时工作目录
        work_dir = Path(tempfile.mkdtemp(dir=self.base_dir))
        
        try:
            # 提取imports
            imports = self._extract_imports(code)
            logger.info(f"检测到导入: {imports}")
            
            # 安装依赖
            install_success, install_msg = self._install_packages(imports, work_dir)
            if not install_success:
                logger.warning(f"包安装失败: {install_msg}")
                # 继续执行，可能包已经安装
            
            # 执行代码
            exec_success, stdout, stderr = self._execute_code(code, work_dir)
            
            execution_time = time.time() - start_time
            
            return {
                "success": exec_success,
                "output": stdout,
                "error": stderr,
                "execution_time": round(execution_time, 3),
                "imports_used": imports,
                "install_message": install_msg
            }
            
        finally:
            # 清理临时目录
            try:
                shutil.rmtree(work_dir)
            except Exception as e:
                logger.warning(f"清理临时目录失败: {e}")

# 创建执行引擎实例
engine = PythonExecutionEngine()

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "healthy",
        "service": "Python Execution Engine",
        "version": "1.0.0"
    })

@app.route('/execute', methods=['POST'])
def execute_code():
    """执行Python代码接口"""
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({
                "success": False,
                "error": "缺少代码参数",
                "output": ""
            }), 400
        
        code = data['code']
        if not code.strip():
            return jsonify({
                "success": False,
                "error": "代码不能为空",
                "output": ""
            }), 400
        
        logger.info(f"收到执行请求，代码长度: {len(code)}")
        
        # 执行代码
        result = engine.execute(code)
        
        # 记录执行结果
        if result['success']:
            logger.info(f"代码执行成功，耗时: {result['execution_time']}秒")
        else:
            logger.warning(f"代码执行失败: {result['error']}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"执行代码时发生异常: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"服务器内部错误: {str(e)}",
            "output": ""
        }), 500

@app.route('/packages', methods=['GET'])
def list_packages():
    """获取允许的包列表"""
    return jsonify({
        "allowed_packages": sorted(list(engine.allowed_packages)),
        "total_count": len(engine.allowed_packages)
    })

@app.route('/config', methods=['GET'])
def get_config():
    """获取服务配置"""
    return jsonify({
        "max_execution_time": engine.max_execution_time,
        "max_memory_mb": engine.max_memory_mb,
        "allowed_packages_count": len(engine.allowed_packages)
    })

if __name__ == '__main__':
    # 确保基础目录存在
    os.makedirs(engine.base_dir, exist_ok=True)
    
    logger.info("Python执行引擎服务启动中...")
    logger.info(f"工作目录: {engine.base_dir}")
    logger.info(f"最大执行时间: {engine.max_execution_time}秒")
    logger.info(f"允许的包数量: {len(engine.allowed_packages)}")
    
    # 启动服务
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )