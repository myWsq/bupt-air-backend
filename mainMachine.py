import random
import json
from os import path
import mysql.connector
from model import cnx
import time

class mainMachine:
    main_status = 0     # 表示主机状态，待机0、制冷1、制热2
    num = 3     # 每秒最多处理请求数目，默认为3条
    n = 3       # 这一秒内还能接收n条请求
    choice = 1  # 调度算法选择，随机1、先来先服务2、风速优先3

    responseList = []   # 这一秒要处理的请求列表

    def run(self):
        # while True:
            # print(self.main_status)
        self.n = self.num           # 初始化参数
        self.responseList = []      # 初始化请求列表
        self.judge_status()
        self.get_request()
        time.sleep(1)

    def set_status(self, status):       # 设置主机状态
        self.main_status = status
        # self.main_status+=1

    def print_status(self):
        print(self.main_status)

    def set_number_request(self, number):   # 设置每秒处理的请求数目
        self.num = number

    def set_schedule(self, choice):         # 设置调度类型
        self.choice = choice

    def judge_status(self):
        cursor = cnx.cursor()
        query = 'SELECT * FROM `status` where speed<>0 '  # 执行该语句判断有无正在送风的从机
        cursor.execute(query)
        statusList = cursor.fetchall()
        if(statusList is None):     # 从机状态均为关机，主机进行待机操作
            self.main_status = 0

    def get_request(self):
        print('get request and act')
        cursor = cnx.cursor()
        query = ( 'SELECT count(time) FROM `request` ')   # 执行该语句判断是否有请求及是否需要调度
        cursor.execute(query)
        requestCount = cursor.fetchall()
        n_request = requestCount[0][0]
        print(n_request)
        if(n_request>0):    # 有未响应请求
            if(n_request>3):    # 同一时间有大于3条请求
                self.choose_sort()
            else:
                query2 = ( 'SELECT * FROM `request`')
                cursor.execute(query2)
                requestList = cursor.fetchall()
                cursor.close()
                self.response_request(requestList)

    def choose_sort(self):
        self.power_first()
        if(self.choice == 1):    # 随机
            self.random_sort()
        elif(self.choice == 2):  # 先来先服务
            self.first_sort()
        elif(self.choice == 3):  # 按风速大小优先
            self.speed_sort()

    def power_first(self):
        cursor = cnx.cursor()
        query = (
            'select id,speed from status'
        )
        cursor.execute(query)
        statusList = cursor.fetchall()
        for status in statusList:
            cursor = cnx.cursor()
            query = (
                    'select * from request where slave_id=%s'%status[0]
            )
            cursor.execute(query)
            requestList = cursor.fetchall()
            # print(requestList)
            # print(status[1])
            if(status[1] == 0):
                if(requestList[0][2]==1):      # 开机请求
                    print('power on request')
                    # self.response_request(requestList)
                    self.n -= 1
                    self.responseList.append(requestList[0])

                    # print(requestList[0][2])
                    # print(status[1])
                    # print(self.responseList)

            if(status[1] == 1):
                if(requestList[0][2]==0):
                    print('power off request')
                    # self.response_request(requestList)
                    self.n -= 1
                    self.responseList.append(requestList[0])

                    # print(requestList[0][2])
                    # print(status[1])
                    print(self.responseList)
        return


    def random_sort(self):
        print('Acting requset in random...')
        cursor = cnx.cursor()
        query = (  'select * from request order by rand() limit %s' %self.n)
        cursor.execute(query)
        randomList = cursor.fetchall()  # 将请求列表存储到数组中，每一项格式为(113, 2, 4, 25, datetime.datetime(2018, 6, 10, 17, 42, 16))

        cursor.close()
        print(randomList)
        print(self.responseList)
        self.responseList.append(randomList)
        print(self.responseList)
        self.response_request(self.responseList[0])

        # return randomList

    def first_sort(self):
        # 因为往请求表中添加数据时，是按照时间顺序添加的，所以无需对时间进行排序,直接取前n条即可
        print('Acting requset in first_in...')
        cursor = cnx.cursor()
        query = ('select * from request limit %s' %self.n)
        cursor.execute(query)
        firstList = cursor.fetchall()  # 将请求列表存储到数组中，每一项格式为(113, 2, 4, 25, datetime.datetime(2018, 6, 10, 17, 42, 16))
        cursor.close()
        self.responseList.append(firstList)
        self.response_request(self.responseList[0])
        print(self.responseList)
        # return firstList
        # time_list = sorted(requestList,key=lambda x:x[4])

    def speed_sort(self):
        print('Acting requset in speed_first...')
        speedList = []
        cursor = cnx.cursor()
        query = (
                'select id,speed from status order by -speed'
        )
        cursor.execute(query)
        statusList = cursor.fetchall()
        # print(statusList)
        for status in statusList:
            s_id = status[0]
            query = ( 'select * from request where slave_id=%s' %s_id)
            cursor.execute(query)
            requestList = cursor.fetchall()
            speedList.append(requestList[0])
            # print(speedList)
            # print(speedList)
            # print(speedList)
            print(len(speedList))
            if(len(speedList)>=self.n):
                cursor.close()
                self.responseList.append(speedList)
                self.response_request(self.responseList[0])
                # print(self.responseList[0])
                return
        # return 0

    def response_request(self, requestList):
        print('response request!\n')
        cursor = cnx.cursor()
        print(requestList)
        for req in requestList:     # 遍历每个请求
            slave_id = req[1]
            tag_speed = req[2]
            tag_temp = req[3]
            req_time = req[4]
            # if(tag_speed<=3 and tag_speed>=0 and tag_temp<=30 and tag_temp>=18 and req_time):   # 合法性判断
            #     query = ('select id,card_id,cur_temp from status where id=%s'%slave_id )     # 在状态表里读取响应从机信息
            #     cursor.execute(query)
            #     the_status = cursor.fetchall()
            #     status = the_status[0]
            #     # print('status list: \n')
            #     # print(req[4].strftime("%Y-%m-%d %H:%M:%S"))
            #     # print(status)
            #
            #     if(status):     # 从机号合法
            #         update_query = ('update status set target_temp=%s, speed=%s where id=%s ' %(tag_temp,tag_speed,slave_id))    # 更新相应的从机状态
            #         cursor.execute(update_query)
            #         cnx.commit()        # 更新status表
            #
            #         insert_query = ("insert into log (card_id,slave_id,speed,target_temp,temp,req_time) "
            #                         "values (%s,%s,%s,%s,%s,'%s')" %(status[1], status[0], req[2], req[3], status[2], req[4].strftime("%Y-%m-%d %H:%M:%S")))
            #         #   ,%s,%s,%s,%s,%s
            #         cursor.execute(insert_query)
            #         cnx.commit()        # 添加日志信息
            #     else:
            #         print('request log is not legal!\n')
            #
            #     # delete_query = ('delete from request where id=%s' %req[0])   # 无论该从控机id是否合法，均删除相应的请求信息
            #     # cursor.execute(delete_query)
            #     # cnx.commit()
            #     print('delete request id is: %s\n' %req[0])

            print('delete request id is: %s\n' % req[0])


machine = mainMachine()
machine.run()

