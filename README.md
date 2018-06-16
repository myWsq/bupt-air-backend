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
gunicorn --threads 16 app:app

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


## 主机部分

#### 类名：mainMachine

##### 属性：

```python
	main_status = 0     # 表示主机状态，待机0、制冷1、制热2
    num = 3     # 每秒最多处理请求数目，默认为3条
    n = 3       # 这一秒内还能接收n条请求
    choice = 3  # 调度算法选择，随机1、先来先服务2、风速优先3
    
    requestList = []    # 这一秒的请求列表
    responseList = []   # 这一秒要处理的请求列表
```

##### 不间断处理函数：

```python
run(self)
```

##### 对外方法：

```python
set_status(self, status)      # 设置主机状态

set_number_request(self, number)   # 设置每秒处理的请求数目

set_schedule(self, choice)        # 设置调度类型

```


=======
#计算消费能量及金额
energy_and_cost.py
里面有一个名为coster的类，该类有run()和exit方法
主机启动后实例化一个coster对象，调用run()方法即可一秒更新一次从控机的能量和金额，调用exit()方法即可退出费用计算

=======
#计算消费能量及金额
energy_and_cost.py
里面有一个名为coster的类，该类有run()和exit方法
主机启动后实例化一个coster对象，调用run()方法即可一秒更新一次从控机的能量和金额，调用exit()方法即可退出费用计算
