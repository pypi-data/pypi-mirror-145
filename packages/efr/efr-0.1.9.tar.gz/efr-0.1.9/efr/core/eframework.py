# -*- coding: utf-8 -*-
from efr.utils import *
from efr.core.event import Event
from efr.core.equeue import EventQueue
from efr.core.ealloter import EventAlloter
from efr.core.estation import EventStation


class _PARAM_NONE: ...


class _EventFramework:
    def __init__(self):
        self._worker_id = 0
        self._start_flag = False
        self._log_handler = None

    def _newworker(self, name=None, timedt=None):
        self._worker_id += 1
        worker = Worker("worker" + str(self._worker_id - 1) + " of " + self.name if name is None else name, mindt= timedt if timedt else self.timedt)
        if self._start_flag:
            worker.start()
        return worker

    def _initlogger(self):
        self._logger.setLevel(level=self.log_level)
        if self._log_handler:
            self._logger.removeHandler(self._log_handler)
        if self.log_path:
            open(self.log_path, 'w').close()
            self._log_handler = logging.FileHandler(self.log_path)
            self._log_handler.setLevel(level=self.log_level)
            formatter = logging.Formatter(self.log_format)
            self._log_handler.setFormatter(formatter)
            self._logger.addHandler(self._log_handler)

        return self._logger

    def _outputlogs(self):
        for log in self.quit_logs:
            if isinstance(log, Exception):
                self._logger.error(Trace.strError(log))
            elif isinstance(log, Warning):
                self._logger.warn(Trace.strError(log))
            else:
                self._logger.info(log)

    def _log(self, item):
        if self.log_path:
            self._logger.info(item)
        else:
            self.quit_logs += [item]


class EventFramework(_EventFramework):
    def __init__(self, name: str = None, capacity: int = None, step: int = None, timeout=None, timedt=0.1,
                 log_path=None, log_level=logging.INFO, log_immediate=True,
                 log_format='[%(asctime)s][%(levelname)s] - %(message)s'):
        """
        高效事件驱动框架
        Efficient event driven framework

        :param name: str EventFrame's name.
                _: None  # use default name
        :param capacity: int EventQueue's capacity. Mean the max size of eventqueue.
                _: None  # infinite queue capacity.
        :param step: int EventAlloter's step. Mean how many events the eventalloter allote per update.
                _: None
        :param timeout: int EventAlloter's timeout. Mean how long eventalloter wait for eventqueue
                _: None
        :param timedt: int Worker's timedt. Mean how frequency the Worker work
                _: 0.1  # worker do tasks per 0.1s in the quickest case
        :param log_path: str log path.
                _: None  # do not log.
        :param log_level: int log level.
                _: logging.INFO
        :param log_immediate: bool Is log immediatelly written.
                _: False  # only log when .quit()
        :param log_format: str log format.
                _: '[%(asctime)s][%(levelname)s] - %(message)s'
        """
        super(EventFramework, self).__init__()

        self.name = ("efr-" + name) if name else ("efr-" + NewRandomID(8))
        self.timedt = timedt
        self.log_path = log_path
        self.log_level = log_level
        self.log_format = log_format
        self.log_immediate = log_immediate
        self.quit_logs = []  # quit时一起处理

        # workers
        self.workers = []
        self.default_worker = self.addWorker()
        self.workers[0].addTask(Task(self.update, times=Task.CIRCLE))

        # 外部组件
        self.equeue = EventQueue(capacity)
        self.ealloter = EventAlloter(self.equeue, step, timeout)
        self._logger = logging.getLogger(self.name)

        # 启动event组件
        self.equeue.efr = self
        self.ealloter.efr = self
        self._initlogger()

    @property
    def stations(self):
        """
        获取所有已经注册过的station
        """
        return self.ealloter.stations

    def start(self):
        """
        启动事件框架
        start eventframe
        :return:
        """
        self._log(self.name + "start.")
        self._start_flag = True
        for worker in self.workers:
            worker.start()

    def quit(self):
        """
        退出事件框架
        quit eventframework
        :return:
        """
        for worker in self.workers:
            worker.stop()
        self._outputlogs()
        self._log(self.name + "quit.")

    def login(self, station: EventStation, worker: Worker=None) -> bool:
        """
        注册事件工作站。当update时，alloter会用调用station.filter(事件)->bool来判断station是否响应此事件。如果station响应了事件，那么alloter会把事件传入该station的队列.
        成功返回True，失败返回False

        Register the event workstation. When updating, the alloter will call station Filter - > bool to determine whether the station responds to this event. If the station responds to an event, the alloter will pass the event into the queue of the station
        Returns true for success and false for failure
        :param station: EventStation pass through Event Station to login it
        :param worker: Worker assign worker to this station
                _: None  # do not assign.
        :return: bool
        """
        ret = self.ealloter.login(station)
        if ret and worker:
            self.assign(worker, station)
            # print(station._worker)
        return ret

    def logoff(self, station: EventStation) -> bool:
        """
        注销工作站。成功或不存在station返回True，失败返回False
        Log off the eventstation. Successful or non-existent stations return true, while failure returns false
        :param station:
        :return: bool
        """
        ret = self.ealloter.logoff(station)
        if ret:
            self.assign(None, station)
        return ret



    def push(self, event: Event, timeout: float = None) -> Event:
        """
        驱动事件。成功返回该event, 失败返回None
        :param event: Event Event instance.
        :param timeout:float .Wait for more than this time to force the end and return None (if queue refused.)
                _:None  # mean inf
        :return: Event
        """
        return self.equeue.push(event, timeout)

    def config(self, step: int = _PARAM_NONE, timeout: int = _PARAM_NONE, log_path: str = _PARAM_NONE,
               log_immediate: bool = _PARAM_NONE, log_format: str = _PARAM_NONE, log_level: int = _PARAM_NONE):
        """
        配置事件框架
        config it.
        :param step: int EventAlloter's step. Mean how many events the eventalloter allote per update.
                _: None
        :param timeout: int EventAlloter's timeout. Mean how long eventalloter wait for eventqueue
                _: None
        :param timedt: int Worker's timedt. Mean how frequency the Worker work
                _: 0.1  # worker do tasks per 0.1s in the quickest case
        :param log_path: str log path.
                _: None  # do not log.
        :param log_level: int log level.
                _: logging.INFO
        :param log_immediate: bool Is log immediatelly written.
                _: False  # only log when .quit()
        :param log_format: str log format.
                _: '[%(asctime)s][%(levelname)s] - %(message)s'
        :return:
        """

        if step is not _PARAM_NONE:
            self.ealloter.step = step
        if timeout is not _PARAM_NONE:
            self.ealloter.timeout = timeout
        if log_path is not _PARAM_NONE:
            self.log_path = log_path
            self._initlogger()
        if log_immediate is not _PARAM_NONE:
            if self.log_immediate == False and log_immediate == True:
                self._outputlogs()
            self.log_immediate = log_immediate
        if log_format is not _PARAM_NONE:
            self.log_format = log_format
            self._initlogger()
        if log_level is not _PARAM_NONE:
            self.log_level = log_level
            self._initlogger()

    def assign(self, worker: Worker, station: EventStation) -> bool:
        """
        布置任务到worker
        assign task to worker
        :param worker: Worker  If worker is None, mean cancel the station's worker
        :param station: Station
        :return: bool
        """
        # print(worker, station)
        if worker is None :
            if station._worker:
                ret = station._worker.removeTask(station._task)
                station._worker = worker
                station._task = None
                return ret
            return True
        else:
            if station not in self.ealloter.stations:
                self.login(station)
            station._worker = worker
            station._task = Task(station.update, times=Task.CIRCLE)
            return worker.addTask(station._task)


    def addWorker(self, name:str=None, timedt:int=None) -> Worker:
        """
        添加一个工人到事件框架
        add a worker to eventframework.
        :param name: str Worker's name
                _: None  # mean use the default name
        :param timedt: int Worker's timedt. Mean how frequency the Worker work
                _: None  # mean use the default timedt defined in EventFramework.__init__
        :return: Worker
        """
        worker = self._newworker(name, timedt)
        self.workers += [worker]
        return worker

    def removeWorker(self, worker: Worker) -> bool:
        """
        移除指定的工人，对应的工作也会尽可能快地被搁置
        Remove the designated workers and the corresponding work will be put on hold as soon as possible
        :param worker: Worker
        :return: bool
        """
        try:
            self.workers.remove(worker)
            worker.stop()
        except ValueError:
            ...
        return True

    def update(self):
        """
        事件框架更新, 自动添加到worker 0
        efr update， auto added to worker 0
        :return: None
        """
        return self.ealloter.update()


if __name__ == '__main__':
    none = _PARAM_NONE()
    print(none)
