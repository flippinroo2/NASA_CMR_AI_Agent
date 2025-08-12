from time import time
from typing import Any, Optional

from langchain.tools import tool
from pydantic import BaseModel, Field

from config import Configuration
from lib.http_functions import get_request
from lib.string_functions import replace_double_newline
from src.ENUMS import CMR_ENDPOINTS


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
        self.failure_count += 1
        self.last_failure = time()
        if self.failure_count >= self.failure_threshold:
            self.state = "open"


class AutocompleteEntry(BaseModel):
    score: float
    type: str
    value: str
    fields: str


class CollectionEntry(BaseModel):
    processing_level_id: Optional[str] = None
    boxes: Optional[list[str]] = None
    time_start: str
    entry_id: str
    short_name: str
    data_center: str
    title: str
    summary: str
    coordinate_system: Optional[str] = None
    id: str
    score: float
    original_format: str
    links: list[dict[str, str]] = Field(default_factory=list[dict[str, str]])


class FeedItem(BaseModel):
    updated: str | None = Field(default=None)
    id: str | None = Field(default=None)
    title: str | None = Field(default=None)
    entry: list[dict[str, Any]] = Field(default_factory=list[dict[str, Any]])


class SearchResponse(BaseModel):
    feed: FeedItem


class CMRSearchParameters(BaseModel):
    entry_title: str | None = Field(default=None)
    entry_id: str | None = Field(default=None)
    data_center: str | None = Field(default=None)
    project: str | None = Field(default=None)
    consortium: str | None = Field(default=None)
    platform: str | None = Field(default=None)
    instrument: str | None = Field(default=None)
    sensor: str | None = Field(default=None)
    browsable: str | None = Field(default=None)
    keyword: str | None = Field(default=None)
    provider: str | None = Field(default=None)
    short_name: str | None = Field(default=None)
    tag_parameters: str | None = Field(default=None)
    service_parameters: str | None = Field(default=None)
    author: str | None = Field(default=None)
    standard_product: str | None = Field(default=None)


# TODO: Maybe put the types of the arguments here to help the API supply the correct arguments
class CMRQueryParameters(BaseModel):
    """
    Arguments for the CMR API

    keyword: The search term used to query the CMR API

    page_size: Number of results per page

    page_num: The page number to return

    offset: As an alternative to page_num, a 0-based offset of individual results may be specified.

    scroll: A boolean flag (true/false) that allows all results to be retrieved efficiently. page_size is supported with scroll while page_num and offset are not. If scroll is true then the first call of a scroll session sets the page size; page_size is ignored on subsequent calls

    sort_key: Indicates one or more Fields to sort on

    pretty: Return formatted results if set to true

    token: Specifies a user token from EDL or Launchpad for use as authentication. Using the standard Authorization header is the prefered way to supply a token. This parameter may be deprecated in the future
    """

    keyword: str | None = Field(
        default=None, description="The search term used to query the CMR API"
    )
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


class CMRAutocompleteEndpointParameters(BaseModel):
    query: str


@tool(
    name_or_callable="query_cmr_autocomplete_endpoint",
    description=(
        "Use this tool when you want to send an HTTP request to the /autocomplete endpoint of the NASA Common Metadata Repository API."
        "Input: A search query string."
        "Returns: A list of possible datasets that might include information about the search term."
    ),
    return_direct=True,
    args_schema=CMRAutocompleteEndpointParameters,
    # infer_schema=False,
    response_format="content",
)
@CircuitBreaker(failure_threshold=5, recovery_timeout=60).protect
async def query_cmr_autocomplete_endpoint(query: str) -> list[AutocompleteEntry] | None:
    """
    Sends an HTTP request to the /autocomplete endpoint of the NASA Common Metadata Repository API and returns the response.

    Args:
      query: Search term to use

    Returns:
      A list of possible datasets that might include information about the search term
    """
    cleaned_query: str = replace_double_newline(query)
    response = await get_request(
        f"{Configuration.base_endpoint}{CMR_ENDPOINTS.AUTOCOMPLETE.value}.json",
        parameters={"q": cleaned_query},
    )
    if response is not None:
        search_response: SearchResponse = SearchResponse(**response)
        autocomplete_entries: list[AutocompleteEntry] = [
            AutocompleteEntry(**entry) for entry in search_response.feed.entry
        ]
        return autocomplete_entries


class CMREndpointParameters(BaseModel):
    keyword: str


@tool(
    name_or_callable="query_cmr_collections_endpoint",
    description=(
        "Use this tool when you want to send an HTTP request to the /collections endpoint of the NASA Common Metadata Repository API."
        "Input: A search query string."
        "Returns: A list of possible datasets that might include information about the search term."
    ),
    return_direct=True,
    args_schema=CMREndpointParameters,
    # infer_schema=False,
    response_format="content",
)
@CircuitBreaker(failure_threshold=5, recovery_timeout=60).protect
async def query_cmr_collections_endpoint(keyword: str):
    """
    Sends an HTTP request to the /collections endpoint of the NASA Common Metadata Repository API and returns the response.

    Args:
      keyword: Search term to use

    Returns:
      A list of possible datasets that might include information about the search term
    """
    cleaned_keyword: str = replace_double_newline(keyword)
    response = await get_request(
        url=f"{Configuration.base_endpoint}{CMR_ENDPOINTS.COLLECTIONS.value}.json",
        parameters={"keyword": cleaned_keyword},
    )
    if response is not None:
        search_response: SearchResponse = SearchResponse(**response)
        collection_entries: list[CollectionEntry] = [
            CollectionEntry(**entry) for entry in search_response.feed.entry
        ]
        return collection_entries


@tool(
    name_or_callable="query_cmr_granules_endpoint",
    description=(
        "Use this tool when you want to send an HTTP request to the /granules endpoint of the NASA Common Metadata Repository API."
        "Input: A search query string."
        "Returns: A list of possible datasets that might include information about the search term."
    ),
    return_direct=True,
    args_schema=CMREndpointParameters,
    # infer_schema=False,
    response_format="content",
)
@CircuitBreaker(failure_threshold=5, recovery_timeout=60).protect
async def query_cmr_granules_endpoint(keyword: str):
    """
    Sends an HTTP request to the /granules endpoint of the NASA Common Metadata Repository API and returns the response.

    Args:
      keyword: Search term to use

    Returns:
      A list of possible datasets that might include information about the search term
    """
    cleaned_keyword: str = replace_double_newline(keyword)
    response = await get_request(
        url=f"{Configuration.base_endpoint}{CMR_ENDPOINTS.GRANULES.value}.json",
        parameters={"keyword": cleaned_keyword},
    )
    if response is not None:
        search_response: SearchResponse = SearchResponse(**response)
        return search_response
