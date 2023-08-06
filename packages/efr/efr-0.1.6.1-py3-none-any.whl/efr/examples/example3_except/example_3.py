# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import random
import time

from efr import EventFramework, EventStation, Event, Task

class ExceptTest(EventStation):
    def filter(self, event:Event) -> bool:
        if event.dest == 'except':
            if event.task % 3 == 0:
                raise Exception("Error hanpen in filter")
            return True
    def respond(self, event) -> object:
        if event.task % 3 == 1:
            raise Exception("Error hanpen in respond")
        return "正常执行"

"""
主线程承担Producer，负责产生event
在事件框架中测试异常处理

事件框架执行中如果出现错误，并不会直接报错，而是由对应的event记录

"""

efr = EventFramework(log_path='test.log')

except_test = ExceptTest( 'err' )  # 新建工作站
efr.login(except_test)  # 注册到事件框架
efr.assign(efr.default_worker, except_test)  # 为test提供一个Worker用于更新

efr.start()  # 启动事件框架

events = []
for i in range(10):
    # 发送事件
    event = efr.push( Event(source="main", dest='except', task=i) )  # 推动事件进入事件循环
    events += [event]

    # join;
    time.sleep(0.5)

    # 读取返回值、更新events
    temp = []
    for event in events:
        if event.isFinish():  # 判断事件是否结束
            print( event.getResult('err') )
        elif event.isExcept():
            print("event except.", event.task)
            for err in event.getExcepts():
                print(event.trace.strError(err))
                # 可以在程序和日志中看到错误信息
                # 隐藏错误: SolutionMissing:
                #       当filter错误时，会继续寻找其他station去filter这个事件
                #       当没有任何station接受此event时抛给event错误:SolutionMissing. 然后抛弃该event
            print()
        else:
            temp += [event]
    events = temp


# 退出框架
efr.quit()
