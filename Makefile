.PHONY: install migrate build run start

install:  ## 安装后端依赖
	pip install -r requirements/base.txt

migrate:  ## 初始化/迁移数据库
	python manage.py migrate --run-syncdb

build:  ## 构建前端
	cd web && npm install && npm run build

run:  ## 启动开发服务器
	python manage.py runserver 0.0.0.0:8001

start: install migrate build run  ## 一键启动
