# -*- coding: utf-8 -*-
from efr.utils import *
from efr.core.event import Event
"""
事件队列
"""

class EventQueue:
    """
    事件队列，事件框架的事件入口

    EventQueue, event entry of EventFramework
    """
    def __init__(self, capacity=None):
        """

        :param capacity: capacity of QventQueue
                _: None  # mean inf
        """
        self.efr = None
        self._capacity = capacity if capacity else inf
        self.equeue = Queue(0 if capacity is None else capacity)

    def push(self, event:Event, timeout:float=None) -> Event:
        """
        驱动事件。成功返回该event, 失败返回None
        :param event: Event Event instance.
        :param timeout:float .Wait for more than this time to force the end and return None (if queue refused.)
                _:None  # mean inf
        :return: Event
        """
        get = self.equeue.put(event, block=True, timeout=timeout)
        event.efr = self.efr
        if get is not QFull:
            if event.state is Event.STATE_OFFLINE:
                event.state = Event.STATE_JUNIOR
            return event
        return None

    def getSize(self):
        """
        Get how many event in queue.
        equal to len(self)
        :return: int
        """
        return self.equeue.qsize()

    def getMaxSize(self):
        """
        Get the capacity of EventQueue
        :return:
        """
        return self._capacity

    def release(self, num:int=None, timeout:float=None):
        """
        获取事件队列中的事件, 该函数不推荐用户使用。用户调用会导致EventFramework工作异常
        Get events in the event queue. This function is not recommended for users. User calls will cause the EventFramework to work abnormally
        :param num: int Get the number of events at one time. The number of returned events will not exceed this value.
                _: None  # mean inf
        :param timeout:float .Wait for more than this time to force the end and return list early (if queue refused.)
                _:None  # mean inf
        :return:
        """
        if num is None:
            num = inf

        _len:int = len(self)
        num = _len if _len < num else num
        ret: list = []
        while num:
            get = self.equeue.get(block=True, timeout=timeout)
            if get is QEmpty:
                return ret
            ret += [get]
            num -= 1
        return ret

    def __len__(self):
        return self.equeue.qsize()