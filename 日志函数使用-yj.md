### 函数原型：Generate_Report(Start_time ，end_time)

#### 参数类型说明：

Start_time: (datatime.date) 	//2018-6-10

Start_time: (datatime.date)	//2018-6-11

```python
if __name__ == '__main__':
    Start = datetime.date(2018, 6, 10)
    End = datetime.date(2018, 6, 11)
    Report = Generate_Report(Start, End)
```

#### 返回值类型说明：

##### 字段描述

| ID                 | Count        | Cost   | Record   |
| ------------------ | ------------ | ------ | -------- |
| 从控机ID，房间号码 | 开关机的次数 | 总花费 | 详细记录 |

#####Record详细字段：

| S_time             | E_time             | Speed    | S_temp             | E_temp             |
| ------------------ | ------------------ | -------- | ------------------ | ------------------ |
| 一次调节的开始时间 | 一次调节的结束时间 | 期间风速 | 一次调节的开始温度 | 一次调节的结束温度 |

```js
[
    {
        "ID":1,
        "Count":2,
        "Record":[
            {
                "E_time":"2018-06-10 13:00:00",
                "Speed":1,
                "E_temp":25,
                "S_temp":26,
                "S_time":"2018-06-10 12:00:00"
            },
            {
                "E_time":"2018-06-10 13:10:00",
                "Speed":3,
                "E_temp":20,
                "S_temp":25,
                "S_time":"2018-06-10 13:00:00"
            },
            {
                "E_time":"2018-06-10 13:30:00",
                "Speed":2,
                "E_temp":22,
                "S_temp":26,
                "S_time":"2018-06-10 13:20:00"
            },
            {
                "E_time":"2018-06-10 13:35:00",
                "Speed":1,
                "E_temp":18,
                "S_temp":22,
                "S_time":"2018-06-10 13:30:00"
            }
        ],
        "Cost":"375.00"
    },
    {
        "ID":2,
        "Count":1,
        "Record":[
            {
                "E_time":"2018-06-10 13:15:01",
                "Speed":3,
                "E_temp":18,
                "S_temp":26,
                "S_time":"2018-06-10 13:10:00"
            }
        ],
        "Cost":"32.61"
    }
]
```
