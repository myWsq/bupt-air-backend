import json
from os import path
import mysql.connector
import datetime
from flask import Blueprint, jsonify, abort, Response, request
from orm import Status, Request, Log

# 读取配置文件
f = open(path.join(path.dirname(path.dirname(__file__)), 'config.json'), 'r')
config = json.load(f)
f.close()


# 查找全部的符合时间限制的记录
def Generate_Report(start, end):
    cnx = mysql.connector.connect(**config)
    start_time = datetime.datetime.strptime(
        str(start), '%Y-%m-%d').strftime("%Y-%m-%d %H:%M:%S")
    end_time = (datetime.datetime.strptime(str(end), '%Y-%m-%d') +
                datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    Report = []
    cursor = cnx.cursor()
    # 查询记录表中不同的从机ID
    slave_id = []
    query = ('SELECT DISTINCT slave_id FROM `log`')
    cursor.execute(query)
    for m, each in enumerate(cursor):
        Report.append({})
        slave_id.append(each[0])
    slave_id.sort()
    # 依次统计每个从机
    for n, id in enumerate(slave_id):
        query = (
            'SELECT * FROM `log` WHERE slave_id = "%d" AND res_time >= "%s" AND res_time <= "%s" ORDER BY req_time'
            % (id, start_time, end_time))
        cursor.execute(query)
        # 统计从机开关机次数
        record = []
        Report[n]['ID'] = id
        Report[n]['Count'] = 0
        for each in cursor:
            record.append(each)
            if each[3] == 0:
                Report[n]['Count'] = Report[n]['Count'] + 1
        # 整理从机的每一条记录
        Report[n]['Record'] = []
        a = []
        total_cost = 0.0
        for i in range(len(record) - 1):
            # 记录请求的起止时间、温度、风速
            a.append({})
            if record[i][3] != 0:
                a[i]['S_time'] = record[i][6].strftime("%Y-%m-%d %H:%M:%S")
                a[i]['E_time'] = record[i+1][6].strftime("%Y-%m-%d %H:%M:%S")
                a[i]['Speed'] = record[i][3]
                a[i]['S_temp'] = record[i][5]
                a[i]['E_temp'] = record[i+1][5]
                # 计算每次调节请求的花费
                total_cost = total_cost + Cost(record[i][6], record[i + 1][6],
                                               record[i][3])
        Report[n]['Cost'] = '%.2f' % total_cost
        # 删除Record中的空白记录
        for each in a:
            if each:
                Report[n]['Record'].append(each)
    cnx.close()
    return Report


def Cost(start, end, speed):
    time = end - start
    cost = 0.0
    if speed == 1:
        cost = (time.total_seconds() / 60) * 0.8 * 5
    elif speed == 2:
        cost = (time.total_seconds() / 60) * 1 * 5
    elif speed == 3:
        cost = (time.total_seconds() / 60) * 1.3 * 5
    return cost

log = Blueprint('log', __name__)


@log.route('today')
def get_today_log():
    return jsonify(
        Generate_Report(
            datetime.date.today(),
            datetime.date.today()))


@log.route('/', methods=['GET', 'POST'])
def get():
    if request.method == 'POST':
        return jsonify(
            Generate_Report(request.json['startDate'],
                            request.json['endDate']))