import time

import aiohttp
from langchain.tools import tool


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


@tool(
    name_or_callable="send_http_get_request",
    description="Use this tool when you want to send an HTTP GET request.",
    return_direct=True,
    infer_schema=False,
    response_format="content",
)
async def send_http_get_request(query: str):
    """
    Sends an HTTP GET request to the provided url and returns an HTTP response.
    """
    return await aiohttp.ClientSession().get(query)
