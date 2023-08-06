# -*- coding: utf-8 -*-
import traceback

from efr.core.event import Event
from efr.core.equeue import EventQueue
from efr.core.estation import EventStation

from efr.core.eerrors import SolutionMissing


class EventAlloter:
    """
    事件分配器
    事件分配器会在update函数被调用时工作，取出事件队列中的事件，然后轮询所有已注册的工作站(根据事件的性质可能会提前结束). 最后将事件分配到对应的工作站的队列中

    Event Allocator
    The event allocator will work when the 'update' function is called, take out the events in the event queue, and then poll all registered workstations (depending on the nature of the event, it may end in advance) Finally, the event is allocated to the queue of the corresponding workstation
    """
    def __init__(self, equeue:EventQueue, step:int=None, timeout:int=None):
        """

        :param equeue:
        :param step: int Update amount per update
                _: None  # mean inf
        :param timeout:float .Wait for more than this time when update
                _:None  # mean inf
        """
        self.efr = None

        self.equeue = equeue
        self.step = step
        self.timout = timeout

        self.stations = []

    def login(self, station:EventStation)->bool:
        """
        注册事件工作站。当update时，alloter会用调用station.filter(事件)->bool来判断station是否响应此事件。如果station响应了事件，那么alloter会把事件传入该station的队列.
        成功返回True，失败返回False

        Register the event workstation. When updating, the alloter will call station Filter - > bool to determine whether the station responds to this event. If the station responds to an event, the alloter will pass the event into the queue of the station
        Returns true for success and false for failure
        :param station:
        :return: bool
        """
        if station in self.stations:
            return False

        station.efr = self.efr

        for i in range(len(self.stations)):
            if station.lv > self.stations[i].lv:
                self.stations.insert(i, station)
                return True
        self.stations += [station]
        return True

    def logoff(self, station:EventStation)->bool:
        """
        注销工作站。成功或不存在station返回True，失败返回False
        Log off the eventstation. Successful or non-existent stations return true, while failure returns false
        :param station:
        :return: bool
        """
        try:
            station.etr = None
            self.stations.remove(station)
        except:
            ...

        return True

    def update(self):
        """
        由外部单元执行更新
        Updates are performed by external units
        :return:
        """
        events = self.equeue.release(self.step, self.timout)

        for event in events:
            flag = False
            for station in self.stations:
                # try filter.
                try:
                    get = station.filter(event)
                except Exception as err:
                    event.state = Event.STATE_EXCEPT
                    err.trace = traceback.format_exc()
                    event.trace.update(err, self.efr)
                    continue

                # add to station
                if get:
                    get = station.push(event)
                    if get:
                        flag = True

                    event.times -= 1
                    if event.times <= 0:
                        break

            # set exception
            if not flag:
                event.state = Event.STATE_EXCEPT
                # record except
                try:
                    raise SolutionMissing(event)
                except SolutionMissing as err:
                    err.trace = traceback.format_exc()
                    event.trace.update(err, self.efr)
