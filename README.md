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

```

#### 生产环境部署

```bash

cd bupt-air-backend

# gunicorn
gunicorn -w 4 app:app

# Nginx

server {
    listen 80;
    server_name example.org;
    access_log  /var/log/nginx/example.log;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
  }

```


#### Tip

1. Flask [官方教程](http://flask.pocoo.org/)
2. 负基础Flask[入门](https://wsq.cool/article/9.html)

#### ORM

>peewee is a small, expressive orm -- supports postgresql, mysql and sqlite 

[官方文档](http://docs.peewee-orm.com/en/latest/peewee/quickstart.html)

减少重复轮子

#计算消费能量及金额
energy_and_cost.py
里面有一个名为coster的类，该类有run()和exit方法
主机启动后实例化一个coster对象，调用run()方法即可一秒更新一次从控机的能量和金额，调用exit()方法即可退出费用计算