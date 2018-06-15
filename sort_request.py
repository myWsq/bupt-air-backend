import random
import json
from os import path
import mysql.connector
# 读取配置文件
def choose_sort(n, choice):
    f = open(path.join(path.dirname(__file__), 'config.json'), 'r')
    config = json.load(f)
    f.close()
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    if(choice == 1):    # 随机
        random_sort(n, cursor)
    elif(choice == 2):  # 先来先服务
        first_sort(n, cursor)
    elif(choice == 3):  # 按风速大小优先
        speed_sort(n, cursor)

    cursor.close()


def random_sort(n, cursor):
    print('Acting requset in random...')
    n = str(n)
    query = (
        'select * from request order by rand() limit '+ n 
    )
    cursor.execute(query)
    randomList = cursor.fetchall() # 将请求列表存储到数组中，每一项格式为(113, 2, 4, 25, datetime.datetime(2018, 6, 10, 17, 42, 16))
    cursor.close()

    return randomList


def first_sort(n, cursor):
    # 因为往请求表中添加数据时，是按照时间顺序添加的，所以无需对时间进行排序,直接取前n条即可
    query = (
        'select * from request limit '+ n 
    )
    cursor.execute(query)
    firstList = cursor.fetchall() # 将请求列表存储到数组中，每一项格式为(113, 2, 4, 25, datetime.datetime(2018, 6, 10, 17, 42, 16))
    cursor.close()

    return firstList
    # time_list = sorted(requestList,key=lambda x:x[4])


def speed_sort(n, cursor):
    return 0

# list1 = random_sort()
# print(list1)