import asyncio
import json
from dataclasses import asdict, dataclass, field, fields
from enum import Enum
from typing import Any

import aiohttp
from aiohttp.client_exceptions import InvalidUrlClientError
import requests

from config import Configuration


class CMR_ENDPOINTS(Enum):
    AUTOCOMPLETE = "autocomplete"
    COLLECTIONS = "collections"
    GRANULES = "granules"


# NOTE: Using "dataclass" instead of Pydantic here to avoid additional overhead.


# TODO: Look into if typeddict would be better (or if this amount of structure is even necessary?) because they're more performant than dataclass at runtime... and not all properties are included from the actual responses.
@dataclass()
class AutocompleteEntry:
    score: float
    type: str
    value: str
    fields: str


@dataclass(init=False)
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


@dataclass
class FeedItem:
    updated: str | None = field(default=None)
    id: str | None = field(default=None)
    title: str | None = field(default=None)
    entry: list[dict[str, Any]] = field(default_factory=list[dict[str, Any]])


@dataclass
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


# TODO: Consider removing later, but is useful now for helping understand CMR API
@dataclass
class CMRQueryParameters:
    page_size: int = field(default=10)  # Number of results per page
    page_num: int = field(default=1)  # The page number to return
    offset: int = field(
        default=0
    )  # As an alternative to page_num, a 0-based offset of individual results may be specified.
    scroll: bool = field(
        default=False
    )  # A boolean flag (true/false) that allows all results to be retrieved efficiently. page_size is supported with scroll while page_num and offset are not. If scroll is true then the first call of a scroll session sets the page size; page_size is ignored on subsequent calls
    sort_key: str | None = field(
        default=None
    )  # Indicates one or more fields to sort on
    pretty: bool = field(default=False)  # Return formatted results if set to true
    token: str | None = field(
        default=None
    )  # Specifies a user token from EDL or Launchpad for use as authentication. Using the standard Authorization header is the prefered way to supply a token. This parameter may be deprecated in the future
    echo_compatible: bool = field(
        default=False
    )  # When set to true results will be returned in an ECHO compatible format. This mostly removes fields and features specific to the CMR such as revision id, granule counts and facets in collection results. Metadata format style results will also use ECHO style names for concept ids such as echo_granule_id and echo_dataset_id.


class APIManager:
    @staticmethod
    async def get_request(url: str, params=None) -> Any:
        try:
            async with (
                aiohttp.ClientSession() as session,
                session.get(url, params=params) as response,
            ):
                response.raise_for_status()
                return await response.json()
        except InvalidUrlClientError as e:
            print(f"APIManager.async_get_request() - InvalidUrlClientError: {e}")
        except Exception as e:
            print(f"APIManager.async_get_request() - Exception: {e}")

    @staticmethod
    async def query_cmr(endpoint: CMR_ENDPOINTS, params=None, **kwargs):
        _base_url = Configuration.base_endpoint
        _url = f"{_base_url}{endpoint.value}.json"
        _response = await APIManager.get_request(_url, params=params)
        if _response is not None:
            _return_value: Any = _response
            _return_value = APIManager._get_search_entry_list(_response)
            return _return_value

    @staticmethod
    def _get_search_entry_list(
        search_response: SearchResponse,
    ) -> list[Any]:
        _search_response: SearchResponse = SearchResponse(**search_response)
        _search_feed: FeedItem = _search_response.feed
        return _search_feed.get(
            "entry", []
        )  # TODO: Figure out the type safety stuff here. (Again... consider if this amount of structure is necessary...?)

    @staticmethod
    async def query_collections_endpoint(params=None, **kwargs) -> list[dict[str, Any]]:
        # NOTE: This function seems redundant and probably not necessary.
        _base_url = Configuration.base_endpoint
        _url: str = f"{_base_url}{CMR_ENDPOINTS.COLLECTIONS.value}.json"
        _response = await APIManager.get_request(_url, params=params)
        _feed_entry_list = APIManager._get_search_entry_list(_response)
        for _feed_entry in _feed_entry_list:
            _feed_entry_class: CollectionEntry = CollectionEntry(
                **_feed_entry
            )  # TODO: Do we really need to convert the data into this class? Seems too restrictive.
        return _feed_entry_list
