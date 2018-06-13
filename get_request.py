import json
from os import path
import mysql.connector
import sort_request
# 读取配置文件
f = open(path.join(path.dirname(__file__), 'config.json'), 'r')
config = json.load(f)
f.close()
cnx = mysql.connector.connect(**config)

# 查找全部的请求信息
def find_all_request():
    cursor = cnx.cursor()
    query = (
        'SELECT * FROM `request` group by `time` order by `time` limit 4 '
    )
    cursor.execute(query)
    requestList = cursor.fetchall() # 将请求列表存储到数组中，每一项格式为(113, 2, 4, 25, datetime.datetime(2018, 6, 10, 17, 42, 16))
    cursor.close()
    print(requestList)

    return requestList

n = 3       # 默认一秒最多响应三个请求
choice = 1  # 默认随机算法

if __name__ == '__main__':
    # find_all_request()
    req_list = find_all_request()
    if(req_list == None):
        print('there is not any request')
    else:
        print(req_list)
        print(req_list[0][0])
