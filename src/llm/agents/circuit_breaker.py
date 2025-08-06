# This is for failure detection
class CircuitBreaker:
    def __init__(self, max_failures=3, reset_timeout=60):
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure = 0
        self.state = "closed"

    def __enter__(self):
        if self.state == "open":
            if time.time() - self.last_failure > self.reset_timeout:
                self.state = "half-open"
            else:
                raise CircuitBreakerOpenException("Circuit breaker is open")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self._record_failure()
            if isinstance(exc_val, CircuitBreakerOpenException):
                raise exc_val
        else:
            if self.state == "half-open":
                self.state = "closed"
                self.failures = 0

    def _record_failure(self):
        self.failures += 1
        self.last_failure = time.time()
        if self.failures >= self.max_failures:
            self.state = "open"

class CircuitBreaker2:
    def __init__(self, failure_threshold, recovery_timeout):
        self.failure_count = 0
        self.last_failure = None
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
    
    def protect(self, func):
        async def wrapper(*args, **kwargs):
            if self._is_open():
                raise ServiceUnavailableError
            
            try:
                result = await func(*args, **kwargs)
                self._reset()
                return result
            except Exception:
                self._record_failure()
                raise
        return wrapper