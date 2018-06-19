import time
import math
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, jsonify, abort, Response
from orm import Status, Request


class monitor:
    status = None
    out_temp = 0  #外部温度
    rate = 50  # 变化速率
    cur_temp = 0
    target_temp = 0
    speed = 0

    switch = False
    time = 0

    last_req = 0

    def syntax(self):
        self.status = Status.get(Status.id == self.status.id)
        self.target_temp = self.status.target_temp
        self.speed = self.status.speed

    def update(self):
        self.status.cur_temp = round(self.cur_temp)
        if self.cur_temp == self.target_temp: self.status.speed = 0
        self.status.save()

    def request(self):
        req,_ = Request.get_or_create(slave_id=self.status.id)
        req.speed=1
        req.temp=round(self.target_temp)
        req.save()

    def init(self, id, out_temp):
        self.status = Status.get(Status.id == id)
        self.syntax()
        self.cur_temp = self.out_temp = out_temp
        self.update()
        self.time = time.time()

    def run(self):
        while True:
            if (time.time() - self.time > 1e-5):
                self.syntax()
                if (self.speed != 0):
                    a = self.speed * self.rate
                    if (self.target_temp > self.cur_temp):
                        x = a * math.log(
                            (3 * self.target_temp + self.cur_temp) /
                            (3 * self.target_temp - self.cur_temp))
                        during = time.time() - self.time
                        self.cur_temp = min(3 * self.target_temp *
                                            (1 - math.exp(-(x + during) / a)) /
                                            (1 + math.exp(-(x + during) / a)),
                                            self.target_temp)
                    elif (self.target_temp < self.cur_temp):
                        x = a * math.log(
                            (6 * self.out_temp - self.cur_temp - 5 +
                             self.target_temp) /
                            (self.cur_temp + 5 - self.target_temp))
                        during = time.time() - self.time
                        self.cur_temp = max(
                            self.target_temp, 3 * self.out_temp *
                            (math.exp(-(x + during) / a) - 1) /
                            (math.exp(-(x + during) / a) + 1) +
                            self.target_temp - 5 + 3 * self.out_temp)
                        print(self.cur_temp)

                elif (self.cur_temp != self.out_temp):
                    a = self.rate
                    if (self.out_temp > self.cur_temp):
                        x = a * math.log(
                            (1.5 * self.out_temp + self.cur_temp) /
                            (1.5 * self.out_temp - self.cur_temp))
                        during = time.time() - self.time
                        self.cur_temp = min(1.5 * self.out_temp *
                                            (1 - math.exp(-(x + during) / a)) /
                                            (1 + math.exp(-(x + during) / a)),
                                            self.out_temp)

                    if (self.out_temp < self.cur_temp):
                        x = a * math.log((3 * self.out_temp - self.cur_temp -
                                          5 + self.out_temp) /
                                         (self.cur_temp + 5 - self.out_temp))
                        during = time.time() - self.time
                        self.cur_temp = max(
                            self.out_temp, 1.5 * self.out_temp *
                            (math.exp(-(x + during) / a) - 1) /
                            (math.exp(-(x + during) / a) + 1) + self.out_temp -
                            5 + 1.5 * self.out_temp)
                        print(self.cur_temp)
                    if (self.switch):
                        if (abs(self.cur_temp - self.target_temp) > 1
                                and time.time() - self.last_req > 1):
                            self.last_req = time.time()
                            self.request()

                elif (self.cur_temp == self.out_temp and self.switch):
                    if (time.time() - self.last_req > 1):
                        self.last_req = time.time()
                        self.request()

                self.time = time.time()
                self.update()


ac = monitor()

executor = ThreadPoolExecutor(1)

monitor = Blueprint('monitor', __name__)


@monitor.route('/init/<id>/<init>')
def init(id, init):
    ac.init(int(id), int(init))
    executor.submit(ac.run)
    return 'ok'


@monitor.route('/open')
def open():
    ac.switch = True
    return 'ok'


@monitor.route('/close')
def close():
    ac.switch = False
    return 'ok'
