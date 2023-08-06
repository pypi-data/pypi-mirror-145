# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import random
import time

from efr import EventFramework, EventStation, Event, Task

class Calculator(EventStation):
    def filter(self, event) -> bool:
        return event.dest == 'calc'

class Adder(Calculator):
    def respond(self, event) -> object:
        a, b = event.task
        return a + b

class Subber(Calculator):
    def respond(self, event) -> object:
        a, b = event.task
        return a - b

class Multipler(Calculator):
    def respond(self, event) -> object:
        a, b = event.task
        return a * b

class Divver(Calculator):
    def respond(self, event) -> object:
        a, b = event.task
        return a / b

"""
主线程承担Producer，负责产生event
在事件框架中添加+-*/, 他们均对calc事件敏感
"""

efr = EventFramework(log_path='test.log')

# 添加stations
calcs = [Adder('+'), Subber('-'), Multipler('*'), Divver('/')]
# calcs = [Adder('+'), Subber('-'), Multipler('*'), Divver('/', lv = 1)]  # 指定lv可以改变顺序(默认都是0, 越大越优先)
worker = efr.addWorker()  # 新建一个worker用于处理这四个station的工作任务
for station in calcs:
    efr.login(station)  # 注册到事件框架
    efr.assign(worker, station)  # 为这些station提供一个Worker用于更新

efr.start()  # 启动事件框架

events = []
for i in range(10):
    # 发送事件
    a, b = random.randint(0, 50), random.randint(0, 50)
    event = efr.push( Event(source="main", dest='calc', task=[a, b]) )  # 推动事件进入事件循环(被多个事件处理)
    # event = efr.push( Event(source="main", dest='calc', task=[a, b], times=1) )  # 指定times可以限制event被处理的次数

    events += [event]

    # join;
    time.sleep(0.5)

    # 读取返回值、更新events
    temp = []
    for event in events:
        if event.isRetired():  # 判断事件是否完全结束
            print( '{:^4} + {:^4} = {:^4}'.format(*event.task, event.getResult('+')) )
            print( '{:^4} - {:^4} = {:^4}'.format(*event.task, event.getResult('-')) )
            print( '{:^4} * {:^4} = {:^4}'.format(*event.task, event.getResult('*')) )
            print( '{:^4} / {:^4} = {:^4}'.format(*event.task, event.getResult('/')) )
            print()
        else:
            temp += [event]
    events = temp


# 退出框架
efr.quit()

