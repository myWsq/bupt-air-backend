import json
from os import path
import mysql.connector
import datetime

# 读取配置文件
f = open(path.join(path.dirname(__file__), 'config.json'), 'r')
config = json.load(f)
f.close()
cnx = mysql.connector.connect(**config)


# 查找全部的符合时间限制的记录
def Generate_Report(start, end):
    start_time = datetime.datetime.strptime(str(start), '%Y-%m-%d').strftime("%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(str(end), '%Y-%m-%d').strftime("%Y-%m-%d %H:%M:%S")
    Report = []
    cursor = cnx.cursor()

    # 查询记录表中不同的从机ID
    slave_id = []
    query = (
        'SELECT DISTINCT slave_id FROM `log`'
    )
    cursor.execute(query)
    for m, each in enumerate(cursor):
        Report.append({})
        Report[m]['ID'] = each[0]
        slave_id.append(each[0])

    # 依次统计每个从机
    for n, id in enumerate(slave_id):
        query = (
            'SELECT * FROM `log` WHERE slave_id = "%d" AND res_time >= "%s" AND res_time <= "%s" ORDER BY req_time' % (id, start_time, end_time)
        )
        cursor.execute(query)
        # 统计从机开关机次数
        record = []
        Report[n]['Count'] = 0
        for each in cursor:
            record.append(each)
            if each[3] == 0:
                Report[n]['Count'] = Report[n]['Count'] + 1
        # 整理从机的每一条记录
        Report[n]['Record'] = []

        total_cost = 0.0
        for i in range(len(record) - 1):
            # 记录请求的起止时间、温度、风速
            Report[n]['Record'].append({})
            if record[i][3] != 0:
                Report[n]['Record'][i]['S_time'] = record[i][6].strftime("%Y-%m-%d %H:%M:%S")
                Report[n]['Record'][i]['E_time'] = record[i+1][6].strftime("%Y-%m-%d %H:%M:%S")
                Report[n]['Record'][i]['Speed'] = record[i][3]
                Report[n]['Record'][i]['S_temp'] = record[i][5]
                Report[n]['Record'][i]['E_temp'] = record[i+1][5]
                # 计算每次调节请求的花费
                total_cost = total_cost + Cost(record[i][6], record[i + 1][6], record[i][3])
        Report[n]['Cost'] = '%.2f' % total_cost
        # 删除Record中的空白记录
        for num, each in enumerate(Report[n]['Record']):
            if not each:
                del Report[n]['Record'][num]
    return json.dumps(Report)

def Cost(start, end, speed):
    time = end - start
    cost = 0.0
    if speed == 1:
        cost = (time.total_seconds() / 60) * 0.8 * 5
    elif speed == 2:
        cost = (time.total_seconds() / 60) * 1 * 5
    elif speed == 3:
        cost = (time.total_seconds() / 60) * 1.3 * 5
    # print(str(start) + '  ' + str(end) + '  ' + str(speed) + '  '+ str(time.total_seconds() / 60) + '  ' + str(cost))
    return cost


if __name__ == '__main__':
    Start = datetime.date(2018, 6, 10)
    End = datetime.date(2018, 6, 11)
    Report = Generate_Report(Start, End)
    print(Report)
    cnx.close()

