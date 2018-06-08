# 路由模块(蓝图)

为避免路由过多造成获取信息困难. 相似的子路由应该放到一个py文件内, 再统一注册至app.

## 基本使用

再路由模块中:

```python
# your_route.py

from flask import Blueprint

xxx = Blueprint('xxx',__name__)

xxx.route('/your/route')
def your_handler():
    return 'hello world'

```

在app.py中:

```python
from your_route import xxx

# 直接注册到根路径
app.register_blueprint(xxx)

# 统一加前缀
app.register_blueprint(xxx,url_prefix='/xxx')
.
.
.
```



## 路由说明

> 观察 @/route/slave.py

1. 为避免路由重复, 所有人的路由都应以@/route/*.py下的文件名作为前缀.
2. 频率较少或无前缀路由直接写到app.py里
3. 将自己定义的路由补充至该md文件下, 将作为开发文档使用.

### /slave

1. `/slave/check/<card_id>` 通过身份证id获取从机信息
2. `/slave/<id>` 通过slave_id获取单个从机信息
3. `/slave/temp/<op>/<id>` 设定温度升高/降低一度(op='high' or 'low')
4. `/slave/speed/<op>/<id>` 设定风速升高/降低一档(op='high' or 'low')
5. `/slave/shuwdown/<id>` 关闭从机

