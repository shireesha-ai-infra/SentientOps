import concurrent.futures

_executer = concurrent.futures.ThreadPoolExecutor(max_workers=4)

class TimeoutException(Exception):
    pass

def run_with_timeout(func, timeout_seconds):
    future = _executer.submit(func)
    try:
        return future.result(timeout=timeout_seconds)
    except concurrent.futures.TimeoutError:
        raise TimeoutException("Operation timed out")