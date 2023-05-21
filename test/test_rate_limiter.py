import pytest
from unittest.mock import Mock, patch
from src.rate_limiter import RateLimiter


class TestRateLimiter:
    def test_init_defaults(self):
        limiter = RateLimiter()
        assert limiter.max_calls == 3
        assert limiter.interval == 60
        assert limiter.calls_made == 0

    def test_init_custom(self):
        limiter = RateLimiter(max_calls=5, interval=30)
        assert limiter.max_calls == 5
        assert limiter.interval == 30
        assert limiter.calls_made == 0

    @patch("time.monotonic", Mock(return_value=0))
    def test_enter_valid_call(self):
        limiter = RateLimiter(max_calls=3, interval=60)
        with limiter as rl:
            assert rl == limiter
            assert limiter.calls_made == 1
            assert limiter.last_call == 0

    @patch("time.monotonic", Mock(return_value=0))
    def test_enter_invalid_call(self):
        limiter = RateLimiter(max_calls=3, interval=1)
        limiter.calls_made = 3
        with limiter:
            assert limiter.calls_made == 1
            assert limiter.last_call == 0

    @patch("time.monotonic", Mock(side_effect=[0, 20, 30]))
    @patch("time.sleep", Mock())
    def test_enter_wait(self):
        limiter = RateLimiter(max_calls=3, interval=60)
        limiter.calls_made = 3
        with limiter as rl:
            assert rl == limiter
            assert limiter.calls_made == 1
            assert limiter.last_call == 30

    def test_exit_no_exceptions(self):
        limiter = RateLimiter()
        with limiter:
            pass

    def test_exit_with_keyboardinterrupt(self):
        limiter = RateLimiter()
        try:
            with limiter:
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            pass

        assert limiter.calls_made == 1

    @patch("time.sleep", Mock(side_effect=KeyboardInterrupt))
    def test_enter_wait_keyboardinterrupt(self):
        limiter = RateLimiter()
        limiter.calls_made = 3
        with pytest.raises(KeyboardInterrupt):
            with limiter:
                pass

        assert limiter.calls_made == 3
