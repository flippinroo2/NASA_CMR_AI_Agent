from langchain.tools import tool
import time

# This is for failure detection
class CircuitBreaker:
    def __init__(self, failure_threshold, recovery_timeout):
        self.failure_count = 0
        self.last_failure = None
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "closed"

    def protect(self, func):
        async def wrapper(*args, **kwargs):
            if self.state == "open":
                raise Exception("ServiceUnavailableError")
            try:
                result = await func(*args, **kwargs)
                self.state = "closed"
                return result
            except Exception:
                self._record_failure()
                raise

        return wrapper

    def _record_failure(self):
        self.failures += 1
        self.last_failure = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "open"

@tool
async def fetch_nasa_data(query: str):
    """Fetches data from NASA API"""
    # circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.nasa.gov/...?q={query}") as resp:
            return await resp.json()