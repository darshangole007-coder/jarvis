import time

_last_activity = time.time()

def touch():
    global _last_activity
    _last_activity = time.time()

def idle_for():
    return time.time() - _last_activity
