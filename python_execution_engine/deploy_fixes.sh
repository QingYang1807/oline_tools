#!/bin/bash

echo "开始部署修复后的Python执行器引擎..."

# 停止现有服务
echo "停止现有服务..."
docker-compose down

# 清理旧的镜像
echo "清理旧的镜像..."
docker rmi python_execution_engine_python-execution-engine 2>/dev/null || true

# 重新构建镜像
echo "重新构建镜像..."
docker-compose build --no-cache

# 启动服务
echo "启动服务..."
docker-compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 检查服务状态
echo "检查服务状态..."
docker-compose ps

# 检查健康状态
echo "检查健康状态..."
for i in {1..5}; do
    if curl -f http://localhost:5000/health >/dev/null 2>&1; then
        echo "✅ 服务健康检查通过"
        break
    else
        echo "⏳ 等待服务启动... ($i/5)"
        sleep 5
    fi
done

# 显示日志
echo "显示最近的日志..."
docker-compose logs --tail=20

echo "部署完成！"
echo "服务地址: http://localhost:5000"
echo "健康检查: http://localhost:5000/health"
echo "状态查询: http://localhost:5000/status"