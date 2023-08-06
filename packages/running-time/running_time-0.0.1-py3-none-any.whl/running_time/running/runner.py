def run_func(func, params=(), log=False):
    from time import time, ctime
    from ..logging import LogMachine

    start = time()
    result = func(*params)
    end = time()

    result_time = end - start
    if log:
        LogMachine.add_log(ctime(), result_time, result)

    return result_time, result
