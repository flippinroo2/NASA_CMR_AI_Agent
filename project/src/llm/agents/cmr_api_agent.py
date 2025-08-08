import asyncio
import time

import httpx

from lib.string_functions import sanitize_llm_output
from src.data.api_manager import CMR_ENDPOINTS, APIManager
from src.llm.agents.agent import Agent
from src.llm.workflow.agent_state import AgentState






class CMRApiAgent(Agent):
    def __init__(self, llm):
        super().__init__(llm)
        self.session = httpx.AsyncClient()

    def _invoke(self, query: str):
        return self.llm.invoke(query)

    async def process(self, state: AgentState):
        _query_intent = state.intent
        _sub_queries = state.sub_queries # TODO: Check if the list contains entries before moving forward
        if len(_sub_queries):
            _cmr_queries = self._build_cmr_requests_from_subqueries(
                _sub_queries, _query_intent
            )
            _results = await asyncio.gather(*_cmr_queries)
            _cleaned_results = [_result for _result in _results if _result]
            return {**state.model_dump(), "api_responses": _cleaned_results}
        return {**state.model_dump(), "api_responses": []}

    def _build_cmr_requests_from_subqueries(self, subqueries, query_intent):
        # TODO: If looping through here it would make sense to have an intent for each sub-query???
        _return_value = []
        for _query in subqueries:
            _return_value.append(
                self._build_cmr_request_from_query(_query, query_intent)
            )
        return _return_value

    def _build_cmr_request_from_query(self, query, query_intent):
        # TODO: Expand this function here to actually handle parameters better.
        _query_parameters = self._build_cmr_request_parameters(query, query_intent)
        _api_query = APIManager.query_cmr(
            CMR_ENDPOINTS.AUTOCOMPLETE, params={"q": _query_parameters}
        )
        _return_value = _api_query
        return _return_value

    def _infer_parameters_from_query(self, query):
        prompt = f"""Extract the following parameters from this query:
        - Temporal range (start/end dates)
        - Spatial bounds (region, coordinates)
        - Data types (satellite, ground-based, etc.)
        - Research purpose

        Query: {query}

        Return as JSON with null values for any missing parameters."""
        response = self.llm.invoke(prompt)
        # return json.loads(response) # NOTE: Commenting out because it was causing errors
        return response

    def _build_cmr_request_parameters(self, query, query_intent):
        _prompt = f"""Here is a query: {query}
        Break this query down into a search term to use for a single NASA Common Metadata Repository API request.

        ONLY RETURN THE SEARCH TERM! DO NOT PROVIDE ANY OTHER EXPLANATION! DO NOT USE ANY VERBS!"""
        _llm_response = self._invoke(_prompt)
        _return_value = sanitize_llm_output(_llm_response)
        return _return_value
