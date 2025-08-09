import time

import aiohttp
from langchain.tools import tool

from src.llm.tools.http import send_http_get_request


@tool(
    name_or_callable="query_cmr_autocomplete_endpoint",
    description="Use this tool when you want to send an HTTP request to the /autocomplete endpoint of the NASA Common Metadata Repository API.",
    return_direct=True,
    args_schema={},
    infer_schema=False,
    response_format="content",
)
async def query_cmr_autocomplete_endpoint(query: str):
    """
    Sends an HTTP request to the /autocomplete endpoint of the NASA Common Metadata Repository API and returns the response.
    """
    # circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.nasa.gov/...?q={query}") as resp:
            return await resp.json()


@tool(
    name_or_callable="query_cmr_collections_endpoint",
    description="Use this tool when you want to send an HTTP request to the /collections endpoint of the NASA Common Metadata Repository API.",
    return_direct=True,
    args_schema={},
    infer_schema=False,
    response_format="content",
)
async def query_cmr_collections_endpoint(query: str):
    """
    Sends an HTTP request to the /collections endpoint of the NASA Common Metadata Repository API and returns the response.
    """
    # circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.nasa.gov/...?q={query}") as resp:
            return await resp.json()


@tool(
    name_or_callable="query_cmr_granules_endpoint",
    description="Use this tool when you want to send an HTTP request to the /granules endpoint of the NASA Common Metadata Repository API.",
    return_direct=True,
    args_schema={},
    infer_schema=False,
    response_format="content",
)
async def query_cmr_granules_endpoint(query: str):
    """
    Sends an HTTP request to the /granules endpoint of the NASA Common Metadata Repository API and returns the response.
    """
    # circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.nasa.gov/...?q={query}") as resp:
            return await resp.json()
