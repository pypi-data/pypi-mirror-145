# -*- coding: utf-8 -*-
import random
import time

from efr import EventFramework, EventStation, Event, Task

def respond(event) -> object:
    a, b = event.task
    return a + b

"""
主线程承担Producer，负责产生event
在事件框架中添加一个Comsumer负责消耗event
    comsumer负责进行加法，然后返回
"""

efr = EventFramework(log_path='test.log')

# 添加comsumer
comsumer = EventStation( 'comsumer', respond = respond )  # 新建工作站
efr.login(comsumer)  # 注册到事件框架
efr.assign(efr.default_worker, comsumer)  # 为comsumer提供一个Worker用于更新

efr.start()  # 启动事件框架

events = []
for i in range(10):
    # 发送事件
    a, b = random.randint(0, 50), random.randint(0, 50)
    event = efr.push( Event(source="main", dest='comsumer', task=[a, b]) )  # 推动事件进入事件循环
    events += [event]

    # join;
    time.sleep(0.5)

    # 读取返回值、更新events
    temp = []
    for event in events:
        if event.isFinish():  # 判断事件是否结束
            print( '{:^4d} + {:^4d} = {:^4d}'.format(*event.task, event.getResult('comsumer')) )
        else:
            temp += [event]
    events = temp

# 退出框架
efr.quit()
