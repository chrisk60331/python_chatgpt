import time


class RateLimiter:
    def __init__(self, max_calls=3, interval=60):
        self.max_calls = max_calls
        self.interval = interval
        self.calls_made = 0
        self.last_call = time.monotonic()

    def __enter__(self):
        if self.calls_made < self.max_calls:
            self.calls_made += 1
            if self.last_call is None:
                self.last_call = time.monotonic()
            return self

        time_since_last_call = time.monotonic() - self.last_call
        time_to_wait = self.interval - time_since_last_call
        if time_to_wait > 0:
            time.sleep(time_to_wait)

        self.calls_made = 1
        self.last_call = time.monotonic()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
