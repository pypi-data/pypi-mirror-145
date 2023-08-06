import time
from threading import Thread
from efr.utils.Task import *

class Worker(Thread):
    """
    提供一个循环执行器线程
    """
    def __init__(self, name=None, daemon=True, mindt=0.5):
        super(Worker, self).__init__(name=name, daemon=daemon)
        self.alive = True
        self.mindt = mindt
        self.tasks = []

    def run(self) -> None:
        while self.alive:
            next_point = time.time() + self.mindt

            tasks = []
            for task in self.tasks:
                task()
                if task.left > 0:
                    tasks += [task]
                if not self.alive:
                    break
            self.tasks = tasks

            delta = next_point - time.time()
            if delta > 0:
                time.sleep(delta)


    def addTask(self, task:Task) -> bool:
        self.tasks += [task]
        return True

    def removeTask(self, task:Task) -> bool:
        """
        移除任务
        remove task
        :param task: Task
        :return:
        """
        try:
            self.tasks.remove(task)
        except:
            ...
        return True

    def stop(self):
        """
        停止线程，但是至少需要等待到进行中的任务结束
        Stop the thread, but at least wait until the end of the task in progress
        :return:
        """
        self.alive = False
