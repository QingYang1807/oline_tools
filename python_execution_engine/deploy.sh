#!/bin/bash

# Python执行引擎部署脚本
# 适用于Ubuntu服务器

set -e

echo "开始部署Python执行引擎服务..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置变量
SERVICE_NAME="python-execution-engine"
SERVICE_DIR="/opt/python-execution-engine"
SERVICE_USER="www-data"
SERVICE_GROUP="www-data"
PYTHON_VERSION="3.11"

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}请使用root权限运行此脚本${NC}"
    exit 1
fi

# 更新系统包
echo -e "${YELLOW}更新系统包...${NC}"
apt update

# 安装必要的系统依赖
echo -e "${YELLOW}安装系统依赖...${NC}"
apt install -y python3.11 python3.11-venv python3.11-dev python3-pip \
    nginx curl gcc g++ build-essential

# 创建服务目录
echo -e "${YELLOW}创建服务目录...${NC}"
mkdir -p $SERVICE_DIR
mkdir -p $SERVICE_DIR/workspace

# 复制服务文件
echo -e "${YELLOW}复制服务文件...${NC}"
cp -r ./* $SERVICE_DIR/

# 创建虚拟环境
echo -e "${YELLOW}创建Python虚拟环境...${NC}"
cd $SERVICE_DIR
python3.11 -m venv venv
source venv/bin/activate

# 安装Python依赖
echo -e "${YELLOW}安装Python依赖...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# 设置文件权限
echo -e "${YELLOW}设置文件权限...${NC}"
chown -R $SERVICE_USER:$SERVICE_GROUP $SERVICE_DIR
chmod +x $SERVICE_DIR/run.py
chmod +x $SERVICE_DIR/deploy.sh

# 配置systemd服务
echo -e "${YELLOW}配置systemd服务...${NC}"
cp systemd/python-execution-engine.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable $SERVICE_NAME

# 配置nginx
echo -e "${YELLOW}配置nginx...${NC}"
cp nginx.conf /etc/nginx/sites-available/$SERVICE_NAME
ln -sf /etc/nginx/sites-available/$SERVICE_NAME /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 测试nginx配置
nginx -t

# 启动服务
echo -e "${YELLOW}启动服务...${NC}"
systemctl start $SERVICE_NAME
systemctl restart nginx

# 检查服务状态
echo -e "${YELLOW}检查服务状态...${NC}"
sleep 5

if systemctl is-active --quiet $SERVICE_NAME; then
    echo -e "${GREEN}Python执行引擎服务启动成功！${NC}"
else
    echo -e "${RED}Python执行引擎服务启动失败！${NC}"
    systemctl status $SERVICE_NAME
    exit 1
fi

if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}Nginx服务运行正常！${NC}"
else
    echo -e "${RED}Nginx服务启动失败！${NC}"
    systemctl status nginx
    exit 1
fi

# 测试API
echo -e "${YELLOW}测试API接口...${NC}"
sleep 3

if curl -f http://localhost/health > /dev/null 2>&1; then
    echo -e "${GREEN}API接口测试成功！${NC}"
else
    echo -e "${YELLOW}API接口测试失败，请检查服务日志${NC}"
fi

echo ""
echo -e "${GREEN}部署完成！${NC}"
echo -e "${GREEN}服务地址: http://your-server-ip${NC}"
echo -e "${GREEN}健康检查: http://your-server-ip/health${NC}"
echo -e "${GREEN}API文档: http://your-server-ip/execute${NC}"
echo ""
echo "常用命令："
echo "  查看服务状态: systemctl status $SERVICE_NAME"
echo "  查看服务日志: journalctl -u $SERVICE_NAME -f"
echo "  重启服务: systemctl restart $SERVICE_NAME"
echo "  停止服务: systemctl stop $SERVICE_NAME"
echo ""