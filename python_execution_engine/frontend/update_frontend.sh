#!/bin/bash

# 前端部署更新脚本

set -e

echo "更新前端文件..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}请使用root权限运行此脚本${NC}"
    exit 1
fi

# 前端目录
FRONTEND_DIR="/opt/python-execution-engine/frontend"

# 创建前端目录
echo -e "${YELLOW}创建前端目录...${NC}"
mkdir -p $FRONTEND_DIR

# 复制前端文件
echo -e "${YELLOW}复制前端文件...${NC}"
cp -r frontend/* $FRONTEND_DIR/

# 设置权限
echo -e "${YELLOW}设置文件权限...${NC}"
chown -R www-data:www-data $FRONTEND_DIR
chmod -R 755 $FRONTEND_DIR

# 更新nginx配置
echo -e "${YELLOW}更新nginx配置...${NC}"
cp frontend/nginx.conf /etc/nginx/sites-available/python-execution-engine

# 测试nginx配置
nginx -t

# 重启nginx
echo -e "${YELLOW}重启nginx...${NC}"
systemctl restart nginx

echo -e "${GREEN}前端更新完成！${NC}"
echo -e "${GREEN}访问地址: http://101.42.23.49${NC}"