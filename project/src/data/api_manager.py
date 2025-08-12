from dataclasses import dataclass, field, fields
from typing import Any

from config import Configuration
from lib.http_functions import get_request
from src.ENUMS import CMR_ENDPOINTS

# NOTE: I think this was a bit overengineered. In the beginning it was tough to understand the structure of the CMR API.


# NOTE: Using "dataclass" instead of Pydantic here to avoid additional overhead.


# TODO: Look into if typeddict would be better (or if this amount of structure is even necessary?) because they're more performant than dataclass at runtime... and not all properties are included from the actual responses.
class AutocompleteEntry:
    score: float
    type: str
    value: str
    fields: str


class CollectionEntry:
    processing_level_id: str
    boxes: list
    time_start: str
    entry_id: str
    short_name: str
    data_center: str
    title: str
    summary: str
    coordinate_system: str
    id: str
    score: int
    original_format: str
    links: list[dict[str, str]]
    extra_data: dict[str, Any] = field(
        default_factory=dict[str, Any], init=False
    )  # Stores unexpected kwargs

    def __init__(self, **kwargs):
        _fields = {f.name for f in fields(self) if f.name != "extra_data"}
        for name in _fields:
            setattr(self, name, kwargs.pop(name))
        self.extra_data = kwargs


class FeedItem:
    updated: str | None = field(default=None)
    id: str | None = field(default=None)
    title: str | None = field(default=None)
    entry: list[dict[str, Any]] = field(default_factory=list[dict[str, Any]])


class SearchResponse:
    feed: FeedItem


# TODO: Consider removing later, but is useful now for helping understand CMR API
@dataclass
class CMRSearchParameters:
    entry_title: str | None = field(default=None)
    entry_id: str | None = field(default=None)
    data_center: str | None = field(default=None)
    project: str | None = field(default=None)
    consortium: str | None = field(default=None)
    platform: str | None = field(default=None)
    instrument: str | None = field(default=None)
    sensor: str | None = field(default=None)
    browsable: str | None = field(default=None)
    keyword: str | None = field(default=None)
    provider: str | None = field(default=None)
    short_name: str | None = field(default=None)
    tag_parameters: str | None = field(default=None)
    service_parameters: str | None = field(default=None)
    author: str | None = field(default=None)
    standard_product: str | None = field(default=None)


class APIManager:
    @staticmethod
    async def query_cmr(
        endpoint: CMR_ENDPOINTS | str, params: dict[str, Any] = {}, **kwargs
    ):
        params: dict[str, Any] = params
        if params.get("page_size") is None:
            params = {
                **params,
                "page_size": 10,
            }  # TODO: Fix this. It's really badly written and just done to brute force the LLM to work.
        base_url = Configuration.base_endpoint
        url = f"{base_url}{endpoint.value}.json"  # TODO: Fix error here.
        response = await get_request(url, parameters=params)
        if response is not None:
            return_value: Any = response
            return_value = APIManager._get_search_entry_list(response)
            return return_value

    @staticmethod
    def _get_search_entry_list(
        search_response: SearchResponse,
    ) -> list[Any]:
        search_response: SearchResponse = SearchResponse(**search_response)
        search_feed: FeedItem = search_response.feed
        return search_feed.get(
            "entry", []
        )  # TODO: Figure out the type safety stuff here. (Again... consider if this amount of structure is necessary...?)

    @staticmethod
    async def query_collections_endpoint(
        parameters=None, **kwargs
    ) -> list[dict[str, Any]]:
        # NOTE: This function seems redundant and probably not necessary.
        base_url = Configuration.base_endpoint
        url: str = f"{base_url}{CMR_ENDPOINTS.COLLECTIONS.value}.json"
        response = await get_request(url, parameters=params)
        feed_entry_list = APIManager._get_search_entry_list(response)
        for feed_entry in feed_entry_list:
            feed_entry_class: CollectionEntry = CollectionEntry(
                **feed_entry
            )  # TODO: Do we really need to convert the data into this class? Seems too restrictive.
        return feed_entry_list
