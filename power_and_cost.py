import json
from os import path
import pymysql
import time


critical_energy=[12*3.6*10**6,18*3.6*10**6]#阶梯式计费的能量临界点，将“千瓦时”转化为“焦”
unit_time=1#费用计算时间间隔
unit_price=[0.52,0.55,0.62]#阶梯式计费的不同阶段的单价
# outside_temp=outside_temp

# 读取配置文件
f = open(path.join(path.dirname(__file__), 'config.json'), 'r')
config = json.load(f)
f.close()
db = pymysql.connect(**config)
cursor = db.cursor()

#计算每一台从机的能量及消费金额并实时更新到从机状态
def energy_and_cost():
	#所有开启的从控机的当前状态
	status={"id":[],"target_temp":[],"cur_temp":[],"speed":[],"energy":[],"amount":[]}
	cursor.execute("SELECT id, target_temp, cur_temp, speed,energy,amount FROM status")
	for each in cursor:
		status["id"].append(each[0])
		status["target_temp"].append(each[1])
		status["cur_temp"].append(each[2])
		status["speed"].append(each[3])
		status["energy"].append(each[4])
		status["amount"].append(each[5])
	# print(status)
	for num in range(len(status["id"])):
		#轮询每一台从控机状态
		id, target_temp, cur_temp, speed, energy, amount = status["id"][num],status["target_temp"][num],\
															status["cur_temp"][num],status["speed"][num],\
															status["energy"][num],status["amount"][num]
		print(id, target_temp, cur_temp, speed, energy, amount)

		# if target_temp!=cur_temp:#当前温度未达到目标温度
		# 	temp_sub=abs(target_temp-cur_temp)
		# 	unit_energy=temp_sub
		# else:#当前温度达到目标温度
		# 	unit_energy =
		# if energy<=critical_energy[0]:#消耗能量未超过第一级能量临界值
		# 	unit_amount=unit_energy*unit_price[0]
		# elif energy<=critical_energy[1]:#消耗能量未超过第二级能量临界值
		# 	unit_amount=unit_energy(unit_price[1])
		# else:#进入第三级计费阶段
		# 	unit_amount=unit_energy*unit_price[2]
		# amount=amount+unit_amount
		# energy=energy+unit_energy
		# print(id," ", energy, " ", amount)
		# #更新从控机状态
		# cursor.execute("update status set energy=%s,amount=%s where id=%s",(energy,amount,id,))
		# db.commit()
	print()
	db.close()

if __name__ == '__main__':
	energy_and_cost()
	# while True:
	# 	energy_and_cost()
	# 	time.sleep(1)