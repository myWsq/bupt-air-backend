'''
多线程编程示例
主要思想是在主线程运行时向别的线程抛出一个死循环, 共用内存中的变量.
运行本地服务器后访问 http://loaclhost:5000/test
测试实际运行情况
'''
from flask import Blueprint,request
from concurrent.futures import ThreadPoolExecutor
import threading
import time
from model import cnx

timer = Blueprint(__name__,'test1')

# 进程池,最大允许一个进程后台运行
executor = ThreadPoolExecutor(1)

# 事务类
class Todo:
    counter = 0

    def run(self):
        while True:
            print('current counter: [%s]' %self.counter)
            time.sleep(1)

class mainMachine:
    main_status = 0     # 表示主机状态，待机0、制冷1、制热2
    n = 3       # 每秒最多处理请求数目，默认为3条
    choice = 1  # 调度算法选择，随机1、先来先服务2、风速优先3

    def run(self):
        while True:
            print(self.main_status)
            time.sleep(1)

    def set_status(self, status):
        # self.main_status = status
        self.main_status+=1

    # def print_status(self):
    #     print(self.main_status)
    #
    def set_number_request(self, number):
        self.n = number

    def set_schedule(self, choice):
        self.choice = choice

    def get_request(self):
        cursor = cnx.cursor()
        query = ( 'SELECT count(*) FROM `request` group by `time` order by `time` limit 4 ')   # 执行该语句判断是否有请求及是否需要调度
        cursor.execute(query)
        requestCount = cursor.fetchall()
        n_request = requestCount[0][0]
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
        if(self.choice == 1):    # 随机
            self.random_sort()
        elif(self.choice == 2):  # 先来先服务
            self.first_sort()
        elif(self.choice == 3):  # 按风速大小优先
            self.speed_sort()

    def power_first(self):
        cursor = cnx.cursor()
        query = (
            'select id,speed from status order by speed'
        )
        cursor.execute(query)
        statusList = cursor.fetchall()
        for status in statusList:
            cursor = cnx.cursor()
            query = (
                    'select * from request where slave_id=' + status[0]
            )
            cursor.execute(query)
            requestList = cursor.fetchall()
            if(status[1] == 0):
                if(requestList[2]==1):      # 开机请求
                    self.response_request(requestList)

            if(status[1] == 1):
                if(requestList[2]==1):
                    self.response_request(requestList)


    def random_sort(self):
        print('Acting requset in random...')
        cursor = cnx.cursor()
        n = str(self.n)
        query = (
                'select * from request order by rand() limit ' + n
        )
        cursor.execute(query)
        randomList = cursor.fetchall()  # 将请求列表存储到数组中，每一项格式为(113, 2, 4, 25, datetime.datetime(2018, 6, 10, 17, 42, 16))
        cursor.close()
        self.response_request(randomList)
        # return randomList

    def first_sort(self):
        # 因为往请求表中添加数据时，是按照时间顺序添加的，所以无需对时间进行排序,直接取前n条即可
        print('Acting requset in first_in...')
        cursor = cnx.cursor()
        n = str(self.n)
        query = (
                'select * from request limit ' + n
        )
        cursor.execute(query)
        firstList = cursor.fetchall()  # 将请求列表存储到数组中，每一项格式为(113, 2, 4, 25, datetime.datetime(2018, 6, 10, 17, 42, 16))
        cursor.close()
        self.response_request(firstList)
        # return firstList
        # time_list = sorted(requestList,key=lambda x:x[4])

    def speed_sort(self):
        speedList = []
        cursor = cnx.cursor()
        query = (
                'select id,speed from status order by -speed'
        )
        cursor.execute(query)
        statusList = cursor.fetchall()
        for status in statusList:
            sp = status[1]
            query = (
                'select * from request where speed=' + sp
            )
            cursor.execute(query)
            requestList = cursor.fetchall()
            speedList.append(requestList)
            if(len(speedList)==3):
                cursor.close()
                return speedList
        # return 0

    def response_request(self, requestList):
        cursor = cnx.cursor()
        for req in requestList: # 遍历每个请求
            slave_id = req[1]
            tag_speed = req[2]
            tag_temp = req[3]
            req_time = req[4]
            if(tag_speed<=3 and tag_speed>=0 and tag_temp<=30 and tag_temp>=18 and req_time):   # 合法性判断
                query = ('select id,card_id,cur_temp from status where id=' + slave_id)
                cursor.execute(query)
                status = cursor.fetchall()

                if(status):     # 从机号合法
                    update_query = ('update status set target_temp=' + tag_temp + ' ,speed=' + tag_speed +' where id=' + slave_id)    # 更新相应的从机状态
                    cursor.execute(update_query)
                    cnx.commit()        # 更新status表

                    insert_query = ('insert into log (card_id,slave_id,speed,target_temp,temp,req_time) '
                                    'values (' + status[1] + ',' + status[0] + ',' + req[2] + ',' + req[3] + ',' + status[2] + ',' + req[4] + ')')
                    cursor.execute(insert_query)
                    cnx.commit()        # 添加日志信息

                delete_query = ('delete from request where id=' + req[4])   # 无论该从控机id是否合法，均删除相应的请求信息
                cursor.execute(delete_query)
                cnx.commit()

# todo = Todo()
machine = mainMachine()

@timer.route('/',methods=["GET","POST"])
def index():
    if request.method == "GET":
        # 抛出线程
        # executor.submit(todo.run)
        executor.submit(machine.run())
        return '''
        <h1>Counter was launched in background, Look at your console.<h1>
        <form method="post">
            <button>+1</button>
        </form>
        '''
    else:
        # todo.counter+=1
        machine.set_status()
        return '''
        <h1>counter add<h1>
        <form method="post">
            <button>+1</button>
        </form>
        '''

