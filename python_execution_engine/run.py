#!/usr/bin/env python3
"""
启动脚本
"""

import os
import sys
from app import app, engine
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    # 确保基础目录存在
    os.makedirs(engine.base_dir, exist_ok=True)
    
    logger.info("=" * 50)
    logger.info("Python执行引擎服务启动中...")
    logger.info(f"工作目录: {engine.base_dir}")
    logger.info(f"最大执行时间: {engine.max_execution_time}秒")
    logger.info(f"最大内存限制: {engine.max_memory_mb}MB")
    logger.info(f"允许的包数量: {len(engine.allowed_packages)}")
    logger.info("=" * 50)
    
    # 获取配置
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    try:
        # 启动服务
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )
    except KeyboardInterrupt:
        logger.info("服务被用户中断")
    except Exception as e:
        logger.error(f"服务启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()