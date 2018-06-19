from peewee import *
from playhouse.pool import PooledMySQLDatabase
from os import path
import json
from datetime import date, datetime

f = open(path.join(path.dirname(path.dirname(__file__)), 'config.json'), 'r')
config = json.load(f)
f.close()

db = PooledMySQLDatabase(
    max_connections=None,
    stale_timeout=300,  # 5 minutes.
    **config,
)
db.connect(reuse_if_open=True)


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
    time = DateTimeField()


class Log(BaseModel):
    id = IntegerField(primary_key=True)
    card_id = CharField(18)
    slave_id = IntegerField()
    speed = IntegerField()
    cur_temp = FloatField()
    target_temp = FloatField()
    req_time = DateTimeField()
    res_time = DateTimeField()
