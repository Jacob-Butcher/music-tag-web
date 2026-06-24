#!/bin/bash
set -e

# Music Tag Web — 本地一键启动
# 用法: bash start.sh

echo "==> 1/4 安装后端依赖"
pip install -q -r requirements/base.txt

echo "==> 2/4 初始化数据库"
python manage.py migrate --run-syncdb

echo "==> 3/4 构建前端"
cd web
npm install --silent
npm run build --silent
cd ..

echo "==> 4/4 启动服务"
python manage.py runserver 0.0.0.0:8001
