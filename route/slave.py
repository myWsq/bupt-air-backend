from flask import Blueprint,jsonify,abort
from orm import Status,Request,Log

slave = Blueprint('slave',__name__)

# 通过身份证id获取从机信息
@slave.route("/check/<card_id>")
def check(card_id):
    return jsonify(Status.get(Status.card_id==card_id).__data__)

# 通过slave_id获取单个slave信息
@slave.route("/<id>")
def get_slave(id):
    return jsonify(Status.get(Status.id==id).__data__)

# slave 设定温度升高/降低一度
@slave.route("/temp/<op>/<id>")
def temp_op(op,id):
    slave = Status.get(Status.id==id)
    if( op == 'high'):
        if slave.target_temp < 30:
            slave.target_temp += 1
            slave.save()
            abort(200)
    elif (op == 'low'):
        if slave.target_temp > 10:
            slave.target_temp -= 1
            slave.save()
            abort(200)

    abort(302)

# slave 设定风速升高/降低一档          
@slave.route("/speed/<op>/<id>")
def speed_op(op,id):
    slave = Status.get(Status.id==id)
    if( op == 'high'):
        if slave.speed < 5:
            slave.speed += 1
            slave.save()
            abort(200)

    elif(op == 'low'):
        if slave.speed > 0:
            slave.speed -= 1
            slave.save()
            abort(200)

    abort(302)

@slave.route("/shutdown/<id>")
def slave_shutdown(id):
    slave = Status.get(Status.id==id)
    slave.speed = 0
    slave.save()
    abort(200)