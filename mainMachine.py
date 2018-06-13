import random
import json
from os import path
import mysql.connector


class mainMachine:
    main_status = 0     # 表示主机状态，待机0、制冷1、制热2
    n = 3       # 每秒最多处理请求数目，默认为3条
    choice = 1  # 调度算法选择，随机1、先来先服务2、风速优先3

    def init(self):
        f = open(path.join(path.dirname(__file__), 'config.json'), 'r')
        config = json.load(f)
        f.close()
        cnx = mysql.connector.connect(**config)
        self.cursor = cnx.cursor()

    def get_request(self):
        query = ( 'SELECT count(*) FROM `request` group by `time` order by `time` limit 4 ')   # 执行该语句判断是否有请求及是否需要调度
        self.cursor.execute(query)
        requestCount = self.cursor.fetchall()
        n_request = requestCount[0][0]
        if(n_request>0):    # 有未响应请求
            if(n_request>3):    # 同一时间有大于3条请求
                self.choose_sort()
            else:
                query2 = ( 'SELECT * FROM `request`')
                self.cursor.execute(query2)
                requestList = self.cursor.fetchall()
                self.cursor.close()
                self.response_request(requestList)

    def choose_sort(self):
        if(self.choice == 1):    # 随机
            self.random_sort(self.n, self.cursor)
        elif(self.choice == 2):  # 先来先服务
            self.first_sort(self.n, self.cursor)
        elif(self.choice == 3):  # 按风速大小优先
            self.speed_sort(self.n, self.cursor)

        self.cursor.close()

    def random_sort(self):
        print('Acting requset in random...')
        n = str(self.n)
        query = (
                'select * from request order by rand() limit ' + n
        )
        self.cursor.execute(query)
        randomList = self.cursor.fetchall()  # 将请求列表存储到数组中，每一项格式为(113, 2, 4, 25, datetime.datetime(2018, 6, 10, 17, 42, 16))
        self.cursor.close()
        self.response_request(randomList)
        # return randomList

    def first_sort(self):
        # 因为往请求表中添加数据时，是按照时间顺序添加的，所以无需对时间进行排序,直接取前n条即可
        print('Acting requset in first_in...')
        n = str(self.n)
        query = (
                'select * from request limit ' + n
        )
        self.cursor.execute(query)
        firstList = self.cursor.fetchall()  # 将请求列表存储到数组中，每一项格式为(113, 2, 4, 25, datetime.datetime(2018, 6, 10, 17, 42, 16))
        self.cursor.close()
        self.response_request(firstList)
        # return firstList
        # time_list = sorted(requestList,key=lambda x:x[4])

    def speed_sort(self):

        # return 0

    def response_request(self, requestList):
        for req in requestList: # 遍历每个请求
            slave_id = req[1]
            tag_speed = req[2]
            tag_temp = req[3]
            req_time = req[4]
            if(tag_speed<=5 and tag_speed>=0 and tag_temp<=30 and tag_temp>=18 and req_time):   # 合法性判断
                query = ('select * from status where slave_id=' + slave_id)
                self.cursor.execute(query)
                
