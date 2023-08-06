# -*- coding: utf-8 -*-
from efr.utils import *

class EventInterface(ABC):
    @property
    @abstractmethod
    # 事件追踪器
    def trace(self): ...

    @property
    @abstractmethod
    # 事件任务
    def task(self): ...

    @property
    @abstractmethod
    # 事件的task的future，这里进行了简化
    def result(self): ...

    @property
    @abstractmethod
    # 事件来源
    def source(self): ...

    @property
    @abstractmethod
    # 事件去向
    def dest(self): ...

    @property
    @abstractmethod
    # 事件具有的tag
    def tags(self): ...

    @property
    @abstractmethod
    # 事件状态
    def state(self): ...

    @property
    @abstractmethod
    # 事件连接数
    def links(self): ...

class EventState:
    def __str__(self):
        return self.__class__.__name__

@singleton
class State_OffLine(EventState): ...
@singleton
class State_Junior (EventState): ...
@singleton
class State_Urgent (EventState): ...
@singleton
class State_Finish (EventState): ...
@singleton
class State_Retired(EventState): ...
@singleton
class State_Except (EventState): ...

STATE_OFFLINE = State_OffLine()
STATE_JUNIOR  = State_Junior()
STATE_URGENT  = State_Urgent()
STATE_FINISH  = State_Finish()
STATE_RETIRED = State_Retired()
STATE_EXCEPT  = State_Except()

EVENT_ONCE = 1
EVENT_ALL = inf

class Event:
    # static const
    STATE_OFFLINE = STATE_OFFLINE
    STATE_JUNIOR  = STATE_JUNIOR
    STATE_URGENT  = STATE_URGENT
    STATE_FINISH  = STATE_FINISH
    STATE_RETIRED = STATE_RETIRED
    STATE_EXCEPT  = STATE_EXCEPT

    EVENT_ONCE = EVENT_ONCE
    EVENT_ALL  = EVENT_ALL

    """
    事件通常有5个状态：
    1.STATE_OFFLINE - 游离态
        刚刚实例化的事件对象，尚未添加到事件框架中。
    2.STATE_JUNIOR - 预备态
        该事件被EventFramework.push()到了事件队列。但尚未被进一步处理的状态
    3.STATE_URGENT - 激发态
        该事件已经被分配到了EventStation中，但尚未被执行的状态
    4.STATE_FINISH - 完成态
        该事件至少被成功执行了一次
        此时的Event可以通过Event.result获取部分结果
    5.STATE_RETIRED - 末态
        该事件被所有工作站成功执行, 并且已经脱离了EventFramework
        此时的Event可以通过Event.result获取所有结果
    *6.STATE_EXCEPT - 异常态
        该事件在任意环节中出错，通过Event.trace获取更多错误信息

    The event generally has four states:
    1.STATE_OFFLINE - free state
        The event object just instantiated has not been added to the EventFramework.
    2.STATE_JUNIOR - ready
        The event was by EventFramework.push() to the event queue. A state that has not yet been further processed
    3.STATE_URGENT - excited state
        The state in which the event has been assigned to an EventStation but has not yet been executed
    4.STATE_FINISH - finish atleast once
        The event was executed successfully atleast once and still in EventFramework
        At this time, the event can be through Event.result get the part of the results
    5.STATE_RETIRED - final state
        The event was executed successfully in all task and has broken away from the EventFramework
        At this time, the event can be through Event.result get the all the results
    *6.STATE_EXCEPT - exception
        The event has an error in any step, which is passed through Event.trace for more error information
    """
    def __init__(self, source:Any=None, dest:Any=None, task:Any=None, tags=(), times:int=EVENT_ALL):
        """

        :param source:
        :param dest:
        :param task:
        :param tags:
        :param times:
        """
        self.efr = None

        self.trace = Trace()
        self.task = task
        self.result = {}
        self.source = source
        self.dest = dest
        self.tags = tags
        self.state = STATE_OFFLINE
        self.times = times
        self.links:int = 0

    def isOffline(self) -> bool:
        """
        检查事件是否处于游离状态
        Check whether the event is offline
        :return: bool
        """
        return self.state is STATE_OFFLINE

    def isJunior(self) -> bool:
        """
        检查事件是否已经被添加到事件队列中或已经处于urgent状态
        Check whether the event has been added to eventQueue
        :return: bool
        """
        return self.state is STATE_JUNIOR or self.state is STATE_URGENT

    def isUrgent(self) -> bool:
        """
        检查事件是否已经被添加到station中
        Check whether the event has been added to station
        :return: bool
        """
        return self.state is STATE_URGENT

    def isFinish(self) -> bool:
        """
        检查事件是否已经结束或完全结束。只有结束的事件才可以获取result
        Check whether the event has finished or retired. Only the finished event can get the result.
        :return: bool
        """
        return self.state is STATE_FINISH or self.state is STATE_RETIRED

    def isRetired(self) -> bool:
        """
        检查事件是否已经完全结束。
        Check whether the event has retired.
        :return: bool
        """
        return self.state is STATE_RETIRED

    def isExcept(self) -> bool:
        """
        检查事件是否出现错误
        Check whether the event has except.
        :return: bool
        """
        return self.state is STATE_EXCEPT

    def getExcepts(self) -> list:
        """
        获取event的错误信息. 尚未出错或失败返回[]
        Get the exception-information of event. No error or failure returned []
        :return: list of Exceptions
        """
        return self.trace.reason

    def waitFor(self, state:EventState=STATE_RETIRED, timeout:float=None, timedt:float=0.1) -> bool:
        """
        等待事件被执行到某种状态。成功返回True，失败返回False
        Wait for the event to be executed to a certain state. Returns true for success and false for failure
        :param state  : EventState, Used to indicate the waiting target
                _: STATE_RETIRED
        :param timeout: float, Wait for more than this time to force the end and return false
                _: None  # mean inf
        :param timedt : float, While waiting, the result is checked every time the 'timedt' elapses(unit: s)
                _: 0.1
        :return: bool
        """
        if timeout:
            end_point:float = timeout if timeout else inf
        while self.state is not state:
            if timeout and time.time() > end_point:
                return False
            time.sleep(timedt)
        return True

    def setResult(self, station_key:object, result:object, syscall=False):
        """
        set the result of event
        (API for outer caller? maybe)
        :param station_key: object
        :param result: object from respond
        :param syscall: bool Whether call from eventframework. If not, it whill auto set it's state.
        :return:
        """
        self.result[station_key] = result
        if not syscall:
            self.links -= 1
            if self.links <= 0:
                self.state = STATE_FINISH
            else:
                self.state = STATE_RETIRED

    def getResult(self, station_key: object)->object:
        """
        get the result of event from station
        :param station_key: object
        :return: object
        """
        return self.result.get(station_key)

    # def record(self):
    #     """
    #     提供该event的当前的路径(用于多线程trace)，推荐用户不操作该函数
    #     Provide the current trace of the event (for multi-threaded trace). It is recommended that users do not operate this function
    #     :return:
    #     """
    #     self.trace.update(traceback.extract_stack())

    def __str__(self):
        txt = "Event[source:{}, dest:{}, task:{}, tags:{}]".format(self.source, self.dest, self.task, self.tags)
        return txt

if __name__ == '__main__':
    s2 = State_OffLine()
    print(s2 is STATE_OFFLINE)

