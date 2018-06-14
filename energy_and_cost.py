import json
from os import path
import pymysql

#计算每一台从机的能量及消费金额并实时更新到从机状态
def cost(card_id,slave_id):
	# 读取配置文件
	f = open(path.join(path.dirname(__file__), 'config.json'), 'r')
	config = json.load(f)
	f.close()
	db = pymysql.connect(**config)
	cursor = db.cursor()
	logs={'res_time':[],'speed':[]}#存放该从控机最近两次的日志
	
	# 选出该从控机最近两次的日志
	cursor.execute("select speed,res_time from log where card_id=%s and slave_id=%s order by res_time desc limit 2"%(card_id,slave_id))
	for log in cursor:
		logs['res_time'].append(log[1])
		logs['speed'].append(log[0])

	sub_time=(logs['res_time'][0]-logs['res_time'][1]).total_seconds()#最近两次request的时间差(以秒为单位)
	if logs['speed'][1]==1:#上一次request是低速风，按每分钟0.8标准功率计算能量
		energy=0.8*sub_time/60
	elif logs['speed'][1]==3:#上一次request是高速风，按每分钟1.3标准功率计算能量
		energy=1.3*sub_time/60
	else:#上一次request是中速风，按每分钟1.0标准功率计算能量
		energy=1.0*sub_time/60
	cost=5*energy#每标准能量5元

	cursor.execute("update status set energy=energy+%s,amount=amount+%s where id=%s"%(energy,cost,slave_id))
	db.commit()
	db.close()
