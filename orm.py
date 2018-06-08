from peewee import *
from os import path
import json
from datetime import date, datetime

f = open(path.join(path.dirname(__file__), 'config.json'), 'r')
config = json.load(f)
f.close()

db = MySQLDatabase(**config)
db.connect()

class BaseModel(Model):
     class Meta:
        database = db



class Status(BaseModel):
    id = IntegerField(primary_key=True)
    card_id = CharField(18)
    target_temp = IntegerField()
    cur_temp = FloatField()
    speed = IntegerField()
    energy = FloatField()
    amount = FloatField()



class Request(BaseModel):
    id = IntegerField(primary_key=True)
    slave_id = IntegerField()
    temp = FloatField()
    speed = IntegerField()
    time = TimestampField()

class Log(BaseModel):
    id = IntegerField(primary_key=True)
    card_id = CharField(18)
    slave_id = IntegerField()
    speed = IntegerField()
    temp = FloatField()
    req_time = TimestampField()
    res_time = TimestampField()
    



