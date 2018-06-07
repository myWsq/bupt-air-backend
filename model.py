import json
from os import path
import mysql.connector
# 读取配置文件
f = open(path.join(path.dirname(__file__), 'config.json'), 'r')
config = json.load(f)
f.close()
cnx = mysql.connector.connect(**config)

# 查找全部的从机状态
def find_all_status():
    cursor = cnx.cursor()
    query = (
        'SELECT `id`, `card_id`, `target_temp`, `cur_temp`, `speed`, `energy`, `amount` FROM `status`'
    )
    cursor.execute(query)
    for each in cursor:
        print(each)


if __name__ == '__main__':
    find_all_status()