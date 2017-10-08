import datetime
import time


def clocktimer(function):
    def timed(*args, **kargs):
        start_time = time.time()
        result = function(*args, **kargs)
        elapsed_time = time.time() - start_time
        print("--- [%s] [%s] seconds ---" % (function.__name__, elapsed_time))
        return result
    return timed


'@timer.clocktimer'
