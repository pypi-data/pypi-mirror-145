# -*- coding: utf-8 -*-
from efr.utils import *
from efr.core.event import Event
from efr.core.equeue import EventQueue


class EventStation(EventQueue):
    def __init__(self, key:str=None, filter:callable=None, respond:callable=None, lv:int=0, step:int=None, timeout:int=None):
        """

        :param key:
        :param lv:
        :param step:
        """
        super(EventStation, self).__init__()
        self.efr = None

        self.key = key if key else self.__class__.__name__
        self.lv = lv

        self._worker = None
        self._task = None
        self._filter = filter
        self._respond = respond

        self.step = step
        self.timeout = timeout

    # @abstractmethod
    def filter(self, event:Event) -> bool:
        """
        如果初始化时未传入filter则需要用户覆盖此方法
        If filter is not passed in during initialization, you need to override this method

        定义工作站对事件的筛选方法. 筛选通过返回True, 失败返回False
        Defines how the workstation filters events. The filter returns true if passed and false if failed

        默认筛选方法是: 判断事件的dest是否和工作站的key匹配
        The default filtering method is to judge whether the dest of the event matches the workstation.key

        :param event: Event
        :return: bool
        """
        if self._filter:
            return self._filter(event)
        return self.key == event.dest

    # @abstractmethod
    def respond(self, event:Event) -> object:
        """
        如果初始化时未传入filter则需要用户覆盖此方法
        If filter is not passed in during initialization, you need to override this method

        :param event: Event
        :return: object
        """
        if self._respond:
            return self._respond(event)
        return

    def __eq__(self, other):
        return isinstance(other, EventStation) and self.key == other.key and self._filter == other._filter and self._respond == other._respond \
               and self.filter == other.filter and self.respond == other.respond

    def __str__(self):
        txt = f"estation: {self.key}<worker={self._worker}>"
        return txt

    def __repr__(self):
        txt = f'estation({self.key})...'
        return txt

    def push(self, event:Event, timeout=1) -> bool:
        """

        :param event:
        :return: bool
        """
        event = super(EventStation, self).push(event, timeout)
        if event:
            event.result[self.key] = None
            if event.state is Event.STATE_JUNIOR:
                event.state = Event.STATE_URGENT
            event.links += 1
            return True
        return False

    def update(self):
        events = self.release(self.step, self.timeout)
        for event in events:
            if event.state is not Event.STATE_EXCEPT:
                try:
                    ret = self.respond(event)
                except Exception as err:
                    event.state = Event.STATE_EXCEPT
                    err.trace = traceback.format_exc()
                    event.trace.update(err, self.efr)

                if event.state is not Event.STATE_EXCEPT:
                    event.setResult(self.key, ret, syscall=True)
                    event.links -= 1
                    if event.links <= 0:
                        event.state = Event.STATE_RETIRED
                    else:
                        event.state = Event.STATE_FINISH
