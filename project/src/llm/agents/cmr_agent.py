import asyncio
import time

import httpx

from src.llm.agents.agent_state import AgentState


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


class CMRAgent:
    def __init__(self, llm):
        self.llm = llm
        self.circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)
        self.session = httpx.AsyncClient()

    async def process(self, state: AgentState):
        tasks = [self._fetch_data(q) for q in state.validated_queries]
        results = await asyncio.gather(*tasks)
        return {**state, "api_responses": results}

    def build_cmr_params(query):
        return {}

    # @circuit_breaker.protect # TODO: Make this work by using the circuit breaker attached to this object
    async def _fetch_data(self, query):
        params = self.build_cmr_params(query)
        response = await self.session.get(
            "https://cmr.earthdata.nasa.gov/search", params=params, timeout=30
        )
        return response.json()
