from src.llm.agents.circuit_breaker import CircuitBreaker, CircuitBreaker2
import httpx
import asyncio

def build_cmr_params(query):
    return {}

class CMRAgent:
    def __init__(self):
        self.circuit_breaker = CircuitBreaker2(
            failure_threshold=5,
            recovery_timeout=60
        )
        self.session = httpx.AsyncClient()
    
    async def process(self, state):
        tasks = [
            self._fetch_data(q) 
            for q in state.validated_queries
        ]
        results = await asyncio.gather(*tasks)
        return {**state, "api_responses": results}
    
    async def _fetch_data(self, query):
        params = build_cmr_params(query)
        response = await self.session.get(
            "https://cmr.earthdata.nasa.gov/search",
            params=params,
            timeout=30
        )
        return response.json()