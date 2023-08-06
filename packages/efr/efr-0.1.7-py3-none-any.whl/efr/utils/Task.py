# -*- coding: utf-8 -*-
from efr.utils import inf
from efr.utils.Functions import EmptyFunction

ONCE = 1
CIRCLE = inf

class Task:
    ONCE = ONCE
    CIRCLE = CIRCLE
    def __init__(self, target=EmptyFunction, args=(), kwargs={}, times=ONCE):
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.left = times

    def __call__(self, *args, **kwargs):
        self.left -= 1
        return self.target(*args, *self.args, **kwargs, **self.kwargs)

if __name__ == '__main__':
    task = Task(lambda a: print(a))
    task("hello, world!")
