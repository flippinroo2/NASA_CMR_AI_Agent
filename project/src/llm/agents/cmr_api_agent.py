import asyncio
import time
from enum import Enum

import httpx

from lib.string_functions import sanitize_llm_output
from src.data.api_manager import CMR_ENDPOINTS, APIManager
from src.llm.agents.agent import Agent
from src.llm.agents.agent_state import AgentState


class CMR_QUERY_INTENTION_ENUM(Enum):
    EXPLORATORY = 1
    SPECIFIC_DATA = 2
    ANALYTICAL = 3


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


class CMRApiAgent(Agent):
    def __init__(self, llm):
        super().__init__(llm)
        self.circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)
        self.session = httpx.AsyncClient()

    def invoke(self, query: str):
        return self.llm.invoke(query)

    async def process(self, state: AgentState):
        _query_intent = state.get(
            "intent", 1
        )  # NOTE: Setting to EXPLORATORY for now because it's the most generic??? (OR do we maybe want intent to be for each sub-query???!!!)
        _sub_queries = state.get(
            "sub_queries", []
        )  # TODO: Check if the list contains entries before moving forward

        _cmr_queries = self.build_cmr_requests_from_subqueries(
            _sub_queries, _query_intent
        )
        _results = await asyncio.gather(*_cmr_queries)
        _cleaned_results = [_result for _result in _results if _result]
        return {**state, "api_responses": _cleaned_results}

    def build_cmr_requests_from_subqueries(self, subqueries, query_intent):
        # TODO: If looping through here it would make sense to have an intent for each sub-query???
        _return_value = []
        for _query in subqueries:
            _return_value.append(
                # self.circuit_breaker.protect(self._fetch_data)(_query)
                self.build_cmr_request_from_query(_query, query_intent)
            )
        return _return_value

    def build_cmr_request_from_query(self, query, query_intent):
        _query_parameters = self.build_cmr_request_parameters(query, query_intent)
        _api_query = APIManager.query_cmr(
            CMR_ENDPOINTS.AUTOCOMPLETE, params={"q": _query_parameters}
        )
        _return_value = _api_query
        return _return_value

    def build_cmr_request_parameters(self, query, query_intent):
        _prompt = f"""Here is a query: {query}
        Break this query down into a search term to use for a single NASA Common Metadata Repository API request.

        ONLY RETURN THE SEARCH TERM! DO NOT PROVIDE ANY OTHER EXPLANATION! DO NOT USE ANY VERBS!"""
        _llm_response = self.invoke(_prompt)
        _return_value = sanitize_llm_output(_llm_response)
        return _return_value

    # @circuit_breaker.protect # TODO: Make this decorator work by using the circuit breaker attached to this object
    async def _fetch_data(self, query):
        params = self.build_cmr_request_parameters(query)
        response = await self.session.get(
            "https://cmr.earthdata.nasa.gov/search", params=params, timeout=30
        )
        return response.json()
