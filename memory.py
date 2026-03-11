import time

_last_activity = time.time()

def touch():
    """Updates the last activity timestamp."""
    global _last_activity
    _last_activity = time.time()

def idle_for():
    """Returns seconds since last activity."""
    return time.time() - _last_activity