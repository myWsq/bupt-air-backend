# Bupt-air 后台
> Flask + MySQL

#### Installation

1. fork项目至本地目录并随时更新进度.
2. 配置Python3.6环境, 推荐使用Miniconda. [配置教程](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)

#### Build Setup

```bash

cd bupt-air-backend

# 安装依赖
pip install -r requirements.txt

# 测试数据库连接情况
python model.py

# 运行开发服务器
export FLASK_ENV=development
flask run