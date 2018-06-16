from flask import Blueprint, jsonify, abort, Response
from orm import Status, Request, Log

import datetime
master = Blueprint('master', __name__)


@master.route('temp/<op>/<id>')
def temp_op(op, id):
    slave = Status.get(Status.id == id)
    if (op == 'high'):
        if slave.target_temp < 30:
            slave.target_temp += 1
            slave.save()
            return Response(None, 200)

    elif (op == 'low'):
        if slave.target_temp > 10:
            slave.target_temp -= 1
            slave.save()
            return Response(None, 200)

    abort(302)


@master.route("/speed/<op>/<id>")
def speed_op(op, id):
    slave = Status.get(Status.id == id)
    if (op == 'high'):
        if slave.speed < 5:
            slave.speed += 1
            slave.save()
            return Response(None, 200)

    elif (op == 'low'):
        if slave.speed > 0:
            slave.speed -= 1
            slave.save()
            return Response(None, 200)

    abort(302)


# 获取当前的请求列表
@master.route("/request/all")
def all_requests():
    data = [each.__data__ for each in Request.select()]
    return jsonify(data)
