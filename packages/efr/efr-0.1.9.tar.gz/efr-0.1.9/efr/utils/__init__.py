import time
import logging
import inspect
import traceback
from math import inf
from typing import Any
from queue import Queue, Empty as QEmpty, Full as QFull
from abc import ABC, abstractmethod


# inner
from efr.utils.IdGenerator import NewRandomID, NewRandom
from efr.utils.Functions import EmptyFunction, singleton
from efr.utils.Trace import Trace
from efr.utils.Worker import Worker
from efr.utils.Task import Task

if __name__ == '__main__':
    print(inf > inf)
    print(inf < inf)
