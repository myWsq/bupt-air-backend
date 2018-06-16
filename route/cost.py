import json
from os import path
import pymysql
from flask import Blueprint,request,Response
from concurrent.futures import ThreadPoolExecutor
import time
from model import config

class Costor:
	def __init__(self):
		self.flag=True
		# 读取配置文件
		self.config = config

	#以秒为单位计算每一台从机的能量及消费金额并更新到从机状态
	def run(self):

		self.db = pymysql.connect(**self.config)
		self.cursor = self.db.cursor()

		while self.flag:
			status={'id':[],'speed':[], 'amount':[]}#存放每一台从控机的状态信息

			# 选出每一台从控机的状态信息
			self.cursor.execute("select id,speed, amount from status where speed!=0")
			for sta in self.cursor:
				status['id'].append(sta[0])
				status['speed'].append(sta[1])
				status['amount'].append(sta[2])

			#计算每一台从控机的单位时间消费金额
			for num in range(len(status['id'])):
				if status['speed'][num]==1:#上一次request是低速风，按每分钟0.8标准功率计算能量
					energy=0.8*1/60
				elif status['speed'][num]==3:#上一次request是高速风，按每分钟1.3标准功率计算能量
					energy=1.3*1/60
				else:#上一次request是中速风，按每分钟1.0标准功率计算能量
					energy=1.0*1/60
				cost=5*energy#每标准能量5元

				#更新从控机状态
				self.cursor.execute("update status set energy=energy+%s,amount=amount+%s where id=%s"%(energy,cost,status['id'][num]))

			self.db.commit()#提交
			time.sleep(1)#为实现一秒计算一次

	def exit(self):
		self.flag=False#为退出计算
		self.db.close()


cost = Blueprint('cost', __name__)
costor = Costor()
cost_executor = ThreadPoolExecutor(1)

@cost.route("/open")
def open_cost():
    costor.flag = True
    cost_executor.submit(costor.run)
    return Response('ok',200)

@cost.route("/close")
def close_cost():
    costor.exit()
    return Response('ok',200)

