'''
多线程编程示例
主要思想是在主线程运行时向别的线程抛出一个死循环, 共用内存中的变量.
运行本地服务器后访问 http://loaclhost:5000/timer 
'''
from flask import Blueprint,request
from concurrent.futures import ThreadPoolExecutor
import threading
import time


timer = Blueprint(__name__,'timer')

# 进程池,最大允许一个进程后台运行
executor = ThreadPoolExecutor(1)

# 事务类
class Todo:
    counter = 0 1

    def run(self):
        while True:
            print('current counter: [%s]' %self.counter)
            time.sleep(1)


todo = Todo()


@timer.route('/',methods=["GET","POST"])
def index():
    if request.method == "GET":
        # 抛出线程
        executor.submit(todo.run)
        return '''
        <h1>Counter was launched in background, Look at your console.<h1>
        <form method="post">
            <button>+1</button>
        </form>
        '''
    else:
        todo.counter+=1
        return '''
        <h1>counter add<h1>
        <form method="post">
            <button>+1</button>
        </form>
        '''
