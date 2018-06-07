from flask import Flask, request, abort,jsonify
from flask_cors import CORS
app = Flask(__name__)
# 允许跨域访问
CORS(app)

@app.route("/test")
def connect_test():
    test_str = request.args.get('testStr')
    # 如果收到请求字符串则返回同样的字符串
    if test_str:
        return test_str
    # 否则报错
    else:
        abort(502)
        

