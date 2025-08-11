import time

import aiohttp
from langchain.tools import tool
from pydantic import BaseModel, Field

from src.llm.tools.http import send_http_get_request


# TODO: Maybe put the types of the arguments here to help the API supply the correct arguments
class CMRQueryParameters(BaseModel):
    """
    Arguments for the CMR API

    page_size: Number of results per page

    page_num: The page number to return

    offset: As an alternative to page_num, a 0-based offset of individual results may be specified.

    scroll: A boolean flag (true/false) that allows all results to be retrieved efficiently. page_size is supported with scroll while page_num and offset are not. If scroll is true then the first call of a scroll session sets the page size; page_size is ignored on subsequent calls

    sort_key: Indicates one or more Fields to sort on
    pretty: bool = Field(default=False)  # Return formatted results if set to true

    token: Specifies a user token from EDL or Launchpad for use as authentication. Using the standard Authorization header is the prefered way to supply a token. This parameter may be deprecated in the future
    """

    page_size: int = Field(default=10, description="Number of results per page")
    page_num: int = Field(default=1, description="The page number to return")
    offset: int = Field(
        default=0,
        description="As an alternative to page_num, a 0-based offset of individual results may be specified.",
    )
    scroll: bool = Field(
        default=False,
        description="A boolean flag (true/false) that allows all results to be retrieved efficiently. page_size is supported with scroll while page_num and offset are not. If scroll is true then the first call of a scroll session sets the page size; page_size is ignored on subsequent calls",
    )
    sort_key: str | None = Field(
        default=None, description="Indicates one or more Fields to sort on"
    )
    pretty: bool = Field(
        default=False, description="Return formatted results if set to true"
    )
    token: str | None = Field(
        default=None,
        description="Specifies a user token from EDL or Launchpad for use as authentication. Using the standard Authorization header is the prefered way to supply a token. This parameter may be deprecated in the future",
    )


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
