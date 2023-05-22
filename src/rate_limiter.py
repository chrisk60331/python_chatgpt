import time


class RateLimiter:
    def __init__(self, max_calls=3, interval=60):
        self.max_calls = max_calls
        self.interval = interval
        self.calls_made = 0
        self.last_call = time.monotonic()

    def __enter__(self):
        if self.calls_made >= self.max_calls:
            time.sleep(1)
        if time.monotonic() - self.last_call < self.interval:
            time.sleep(1)
        self.last_call = time.monotonic()
        self.calls_made += 1

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
