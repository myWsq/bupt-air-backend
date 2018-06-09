import json
from os import path
import mysql.connector
import time



class Energy_And_Cost:
	def __init__(self,critical_energy,unit_price,over_price):
		self.critical_energy=critical_energy#能量临界点，临界点内和临界点外采取不同计费方式
		self.unit_time=1#费用计算时间间隔
		self.unit_price=unit_price
		self.over_price=over_price
		self.start_over_time=[0,0,0,0]

		# 读取配置文件
		f = open(path.join(path.dirname(__file__), 'config.json'), 'r')
		config = json.load(f)
		f.close()
		self.db = mysql.connector.connect(**config)
		self.cursor = self.db.cursor()

	#计算每一台从机的能量及消费金额并实时更新到从机状态
	def calculate(self):
		#所有从控机的当前状态
		status={"id":[],"target_temp":[],"cur_temp":[],"speed":[],"energy":[],"amount":[]}
		self.cursor.execute("SELECT id, target_temp, cur_temp, speed,energy,amount FROM status")
		for each in self.cursor:
			status["id"].append(each[0])
			status["target_temp"].append(each[1])
			status["cur_temp"].append(each[2])
			status["speed"].append(each[3])
			status["energy"].append(each[4])
			status["amount"].append(each[5])

		for num in range(len(status["id"])):
			#轮询每一台从控机状态
			id, target_temp, cur_temp, speed, energy, amount = status["id"][num],status["target_temp"][num],\
																status["cur_temp"][num],status["speed"][num],\
																status["energy"][num],status["amount"][num]

			if speed!=0:#
				if target_temp!=cur_temp:#当前温度未达到目标温度
					temp_sub=abs(target_temp-cur_temp)
					unit_energy=temp_sub*speed*self.unit_time*0.001#计算每单位时间消耗的能量
				else:#当前温度达到目标温度
					unit_energy = 0.001 * speed * self.unit_time
				if energy<=self.critical_energy:#消耗能量未超过第一计费阶段能量临界值
					unit_amount=unit_energy*self.unit_price
					if energy>=self.critical_energy:
						self.start_over_time[id-1]=time.time()#记录超过能量临界值的时刻
				else:#进入第二计费阶段
					unit_amount=unit_energy*(self.unit_price+(time.time()-self.start_over_time[id-1])*self.over_price)
				amount=amount+unit_amount
				energy=energy+unit_energy
				print(id," ", energy, " ", amount)
				#更新从控机状态
				self.cursor.execute("update status set energy=%s,amount=%s where id=%s",(energy,amount,id,))
				self.db.commit()
		print()

if __name__ == '__main__':
	energy_and_cost=Energy_And_Cost(10,0.01,0.02)
	while True:
		energy_and_cost.calculate()
		time.sleep(1)