from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from route import *

app = Flask(__name__)
# 允许跨域访问
CORS(app)
# 注册子路由
app.register_blueprint(slave, url_prefix='/slave')
app.register_blueprint(master, url_prefix='/master')
app.register_blueprint(timer, url_prefix='/timer')
app.register_blueprint(cost, url_prefix='/cost')
app.register_blueprint(machine, url_prefix='/machine')
app.register_blueprint(monitor, url_prefix='/monitor')


@app.route("/test")
def connect_test():
    test_str = request.args.get('testStr')
    # 如果收到请求字符串则返回同样的字符串
    if test_str:
        return test_str
    # 否则报错
    else:
        abort(502)


@app.route('/')
def index():
    return 'hello world'
