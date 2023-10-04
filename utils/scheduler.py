import sched
import time
from utils.logger import Logger


def scheduler(func, interval_seconds):
    s = sched.scheduler(time.time, time.sleep)
    exec_at= "Function executed at", time.strftime("%Y-%m-%d %H:%M:%S")
    Logger.log_info(exec_at)
    def wrapper():
        func()
        s.enter(interval_seconds, 1, wrapper, ())

    s.enter(interval_seconds, 1, wrapper, ())
    s.run()