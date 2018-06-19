import time
from flask import Blueprint, request, Response, jsonify
from concurrent.futures import ThreadPoolExecutor
from orm import Request, Status, Log


# 请求队列超出大小限制将抛出此异常
class RequestException(Exception):
    def __init__(self, err='请求队列超出大小限制'):
        Exception.__init__(self, err)


class mainMachine:
    main_status = 1  # 表示主机状态，制冷1、制热2
    is_standby = 1  # 记录是否待机，待机1、运行0
    num = 3  # 每秒最多处理请求数目，默认为3条
    choice = 1  # 调度算法选择，随机1、先来先服务2、风速优先3

    requestList = []  # 这一秒的请求列表
    flag = True  # 循环标志

    def run(self):
        while self.flag:
            self.judge_status()
            print('待机中..' if self.is_standby else '工作中..')
            self.get_request()
            print([each.temp for each in self.requestList])
            self.resolve_request()
            time.sleep(1)

    def exit(self):
        self.flag = False

    def judge_status(self):  # 判断主机是否应该处于待机状态
        self.is_standby = 0 if Request.select().count() > 0 else 1

    def init(self):  # 初始化
        # 删除所有请求
        Request.delete()
        # 重置从机温度
        for item in Status.select():
            if self.main_status == 1 and item.target_temp > 25:
                item.target_temp = 22
                item.speed = 0
                item.save()
                Log(slave_id=item.id,
                    cur_temp=item.cur_temp,
                    target_temp=22,
                    speed=0).save()
            elif self.main_status == 2 and item.target_temp <= 25:
                item.target_temp = 28
                item.speed = 0
                item.save()
                Log(slave_id=item.id,
                    cur_temp=item.cur_temp,
                    target_temp=28,
                    speed=0).save()

    def push(self, *arg):  # 将请求加入待处理队列,超过上限抛出异常
        for item in arg:
            if len(self.requestList) < self.num:
                # 删除数据库中对应的数据
                Request.delete_by_id(item.id)
                Request.delete().where(Request.slave_id == item.slave_id)
                self.requestList.append(item)
            else:
                raise RequestException

    def get_request(self):  # 获得所有待处理请求队列
        try:
            self.requestList = []  # 清空队列
            self.push(*[item for item in self.power_first()])  # 填入开关机请求
            if self.choice == 1:
                self.push(*[item for item in Request.select()])
            elif self.choice == 2:
                self.push(*[
                    item for item in Request.select().order_by(Request.time)
                ])
            elif self.choice == 3:
                self.push(*[
                   item for item in Request.select().order_by(-Request.speed)
                ])
            else:
                raise ValueError('调度策略超出范围')
        except RequestException:
            return

    def resolve_request(self):  # 处理队列中的请求
        for item in self.requestList:
            status = Status.get(Status.id == item.slave_id)
            if item.speed >= 0 and item.speed <= 3:  # 风速在可调控范围内
                if self.main_status == 1 and item.temp >= 18 and item.temp <= 25:  # 处于制冷模式并且温度在可调控范围内
                    if status.cur_temp < item.temp:  # 从机当前温度低于目标温度则风速调0,等待温度回升
                        status.target_temp = item.temp
                        status.speed = 0
                        status.save()
                        Log(slave_id=item.slave_id,
                            cur_temp=status.cur_temp,
                            target_temp=item.temp,
                            speed=0,
                            req_time=item.time).save()
                    else:
                        status.target_temp = item.temp
                        status.speed = item.speed
                        status.save()
                        Log(slave_id=item.slave_id,
                            cur_temp=status.cur_temp,
                            target_temp=item.temp,
                            speed=item.speed,
                            req_time=item.time).save()
                elif self.main_status == 2 and item.temp >= 25 and item.temp <= 30:
                    if status.cur_temp > item.temp:  # 从机当前温度高于目标温度则风速调0,等待温度下降
                        status.target_temp = item.temp
                        status.speed = 0
                        status.save()
                        Log(slave_id=item.slave_id,
                            cur_temp=status.cur_temp,
                            target_temp=item.temp,
                            speed=0,
                            req_time=item.time).save()
                    else:
                        status.target_temp = item.temp
                        status.speed = item.speed
                        status.save()
                        Log(slave_id=item.slave_id,
                            cur_temp=status.cur_temp,
                            target_temp=item.temp,
                            speed=item.speed,
                            req_time=item.time).save()

    def power_first(self):
        for item in Request.select():
            status = Status.get(Status.id == item.slave_id)
            if status.speed == 0 and item.speed > 0:  # 开机请求
                yield item
            elif status.speed == 3 and item.speed == 0:  # 关机请求
                yield item


machine = Blueprint('machine', __name__)
executor = ThreadPoolExecutor(1)
m = mainMachine()


@machine.route("/open")
def open():
    m.flag = True
    m.init()
    executor.submit(m.run)
    return Response('ok', 200)


@machine.route("/close")
def close():
    m.exit()
    return Response('ok', 200)


@machine.route('/info')
def status():
    return jsonify({
        'status': m.main_status,
        'power': m.num,
        'scheduling': m.choice,
        'standby': m.is_standby
    })


@machine.route('/set', methods=['GET', 'POST'])
def setting():
    if request.method == "POST":
        m.num = int(request.json['power'])
        m.choice = int(request.json['scheduling'])
        m.main_status = int(request.json['status'])
    m.init()
    return 'ok'
