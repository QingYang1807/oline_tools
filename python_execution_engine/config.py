"""
配置文件
"""

import os

class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'python-execution-engine-secret-key'
    
    # 执行配置
    MAX_EXECUTION_TIME = int(os.environ.get('MAX_EXECUTION_TIME', 30))
    MAX_MEMORY_MB = int(os.environ.get('MAX_MEMORY_MB', 512))
    
    # 服务配置
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # 工作目录
    BASE_DIR = os.environ.get('BASE_DIR', '/tmp/python_execution')
    
    # 安全配置
    ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', '*').split(',')

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}