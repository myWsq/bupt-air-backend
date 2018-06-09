from flask import Blueprint, jsonify, abort, Response
from orm import Status, Request, Log

slave = Blueprint('slave', __name__)


# 通过身份证id获取从机信息
@slave.route("/check/<card_id>")
def check(card_id):
    data = Status.get(Status.card_id == card_id).__data__
    return jsonify(data)


# 通过slave_id获取单个slave信息
@slave.route("/<id>")
def get_slave(id):
    data = Status.get(Status.id == id).__data__
    return jsonify(data)


# slave 设定温度升高/降低一度
@slave.route("/temp/<op>/<id>")
def temp_op(op, id):
    slave = Status.get(Status.id == id)
    if (op == 'high'):
        if slave.target_temp < 30:
            Request(slave_id=id,speed=slave.speed,temp=slave.target_temp+1).save()
            return Response(None, 200)

    elif (op == 'low'):
        if slave.target_temp > 10:
            Request(slave_id=id,speed=slave.speed,temp=slave.target_temp-1).save()
            return Response(None, 200)

    abort(302)


# slave 设定风速升高/降低一档
@slave.route("/speed/<op>/<id>")
def speed_op(op, id):
    slave = Status.get(Status.id == id)
    if (op == 'high'):
        if slave.speed < 5:
            Request(slave_id=id,speed=slave.speed + 1,temp=slave.target_temp).save()
            return Response(None, 200)

    elif (op == 'low'):
        if slave.speed > 0:
            Request(slave_id=id,speed=slave.speed - 1,temp=slave.target_temp).save()
            return Response(None, 200)

    abort(302)


@slave.route("/shutdown/<id>")
def slave_shutdown(id):
    slave = Status.get(Status.id == id)
    Request(slave_id=id,speed=0,temp=slave.target_temp).save()
    return Response(None, 200)
